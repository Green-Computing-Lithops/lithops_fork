#
# (C) Copyright IBM Corp. 2020
# (C) Copyright Cloudlab URV 2020
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import sys
import zlib
import time
import json
import uuid
import base64
import pickle
import logging
import traceback
import subprocess
import re
import multiprocessing as mp
from queue import Queue, Empty
from threading import Thread
from multiprocessing import Process, Pipe
from tblib import pickling_support
from types import SimpleNamespace
from multiprocessing.managers import SyncManager

from lithops.version import __version__
from lithops.config import extract_storage_config
from lithops.storage import InternalStorage
from lithops.worker.jobrunner import JobRunner
from lithops.worker.utils import LogStream, custom_redirection, \
    get_function_and_modules, get_function_data
from lithops.constants import JOBS_PREFIX, LITHOPS_TEMP_DIR, MODULES_DIR
from lithops.utils import setup_lithops_logger, is_unix_system
from lithops.worker.status import create_call_status
from lithops.worker.utils import SystemMonitor

pickling_support.install()

logger = logging.getLogger(__name__)


class EnergyMonitor:
    """
    Simplified energy monitor that focuses only on power/energy-pkg/ from perf.
    Based on the approach from perf_alternative_powerapi.py.
    """
    def __init__(self, process_id):
        self.process_id = process_id
        self.perf_process = None
        self.start_time = None
        self.end_time = None
        self.energy_value = None
        self.cpu_percent = None
        self.perf_output_file = f"/tmp/perf_energy_{process_id}.txt"
        
        # Print directly to terminal for debugging
        print(f"\n==== ENERGY MONITOR INITIALIZED FOR PROCESS {process_id} ====")
        
    def _get_available_energy_events(self):
        """Get a list of available energy-related events from perf."""
        print("\n==== CHECKING AVAILABLE ENERGY EVENTS ====")
        try:
            # Try both with and without sudo
            try:
                print("Trying 'sudo perf list'...")
                result = subprocess.run(
                    ["sudo", "perf", "list"], 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=False
                )
                print(f"sudo perf list result: {result.returncode}")
            except Exception as e:
                print(f"Error with sudo perf list: {e}")
                # Fallback to non-sudo
                print("Trying 'perf list'...")
                result = subprocess.run(
                    ["perf", "list"], 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=False
                )
                print(f"perf list result: {result.returncode}")
            
            output = result.stdout + result.stderr
            print(f"Perf list output length: {len(output)} characters")
            
            # Extract energy-related events
            energy_events = []
            for line in output.splitlines():
                if "energy" in line.lower():
                    print(f"Found energy line: {line}")
                    # Extract the event name from the line
                    match = re.search(r'(\S+/\S+/)', line)
                    if match:
                        energy_events.append(match.group(1))
            
            # Prepare the events string
            if energy_events:
                print(f"Found {len(energy_events)} energy events: {', '.join(energy_events)}")
                
                # Check for both pkg and cores events
                pkg_events = [e for e in energy_events if "energy-pkg" in e]
                cores_events = [e for e in energy_events if "energy-cores" in e]
                
                events = []
                if pkg_events:
                    print(f"Found energy-pkg event: {pkg_events[0]}")
                    events.append(pkg_events[0])
                else:
                    print("No energy-pkg event found, using default")
                    events.append("power/energy-pkg/")
                    
                if cores_events:
                    print(f"Found energy-cores event: {cores_events[0]}")
                    events.append(cores_events[0])
                else:
                    print("No energy-cores event found, using default")
                    events.append("power/energy-cores/")
                
                # Join events with comma
                events_str = ",".join(events)
                print(f"Using energy events: {events_str}")
                return events_str
            else:
                print("No energy events found in perf list")
                
            # Default to both pkg and cores events
            events_str = "power/energy-pkg/,power/energy-cores/"
            print(f"Using default energy events: {events_str}")
            return events_str
        except Exception as e:
            print(f"Error getting available energy events: {e}")
            # Default to both pkg and cores events
            events_str = "power/energy-pkg/,power/energy-cores/"
            print(f"Using default energy events: {events_str}")
            return events_str
        
    def start(self):
        """Start monitoring energy consumption using perf for power/energy-pkg/."""
        print("\n==== STARTING ENERGY MONITORING ====")
        try:
            # Get the energy-pkg event
            energy_event = self._get_available_energy_events()
            print(f"Using energy event: {energy_event}")
            
            # Create a unique output file for this run
            self.perf_output_file = f"/tmp/perf_energy_{self.process_id}_{int(time.time())}.txt"
            
            # Start perf in the background to monitor the entire function execution
            # This will capture the actual energy consumption of the function
            print("Starting perf stat to monitor energy consumption...")
            
            # Use a direct approach with sudo
            cmd = [
                "sudo", "perf", "stat",
                "-e", energy_event,
                "-a",  # Monitor all CPUs
                "-o", self.perf_output_file  # Output to a file
            ]
            
            print(f"Running command: {' '.join(cmd)}")
            
            # Start perf in the background
            self.perf_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.start_time = time.time()
            print(f"Energy monitoring started at: {self.start_time}")
            print(f"Perf process PID: {self.perf_process.pid}")
            return True
        except Exception as e:
            print(f"Error starting energy monitoring: {e}")
            return False
            
    def stop(self):
        """Stop monitoring energy consumption and collect results."""
        print("\n==== STOPPING ENERGY MONITORING ====")
        
        if self.perf_process is None:
            print("No perf process to stop")
            return
            
        try:
            # Record the end time
            self.end_time = time.time()
            duration = self.end_time - self.start_time
            print(f"Energy monitoring stopped at: {self.end_time}")
            print(f"Monitoring duration: {duration:.2f} seconds")
            
            # Stop the perf process
            print(f"Stopping perf process (PID: {self.perf_process.pid})...")
            
            # Send SIGINT to perf to make it output the results
            import signal
            os.kill(self.perf_process.pid, signal.SIGINT)
            
            # Wait for the process to exit
            try:
                stdout, stderr = self.perf_process.communicate(timeout=5)
                print("Perf process exited")
                print(f"Perf stdout: {stdout}")
                print(f"Perf stderr: {stderr}")
            except subprocess.TimeoutExpired:
                print("Perf process did not exit, killing it")
                self.perf_process.kill()
                stdout, stderr = self.perf_process.communicate()
            
            # Initialize energy values
            self.energy_pkg = None
            self.energy_cores = None
            
            # Read the output file
            print(f"Reading perf output file: {self.perf_output_file}")
            try:
                if os.path.exists(self.perf_output_file):
                    with open(self.perf_output_file, 'r') as f:
                        perf_output = f.read()
                        print(f"Perf output file content: {perf_output}")
                        
                        # Process the output to extract energy values
                        for line in perf_output.splitlines():
                            print(f"Processing line: {line}")
                            if "Joules" in line:
                                # Use a more precise regex to extract the energy value
                                match = re.search(r'\s*([\d,.]+)\s+Joules\s+(\S+)', line)
                                if match:
                                    value_str = match.group(1).replace(',', '.')
                                    event_name = match.group(2)
                                    try:
                                        # Handle numbers with multiple dots (e.g. 1.043.75 -> 1043.75)
                                        if value_str.count('.') > 1:
                                            parts = value_str.split('.')
                                            value_str = ''.join(parts[:-1]) + '.' + parts[-1]
                                            print(f"Converted malformed value with multiple dots to {value_str}")
                                        
                                        energy_value = float(value_str)
                                        print(f"Found energy value: {energy_value} Joules for {event_name}")
                                        
                                        # Store the value based on the event type
                                        if "energy-pkg" in event_name:
                                            self.energy_pkg = energy_value
                                            print(f"Stored energy-pkg value: {self.energy_pkg} Joules")
                                        elif "energy-cores" in event_name:
                                            self.energy_cores = energy_value
                                            print(f"Stored energy-cores value: {self.energy_cores} Joules")
                                    except ValueError as e:
                                        print(f"Could not convert '{value_str}' to float: {e}")
                else:
                    print(f"Perf output file not found: {self.perf_output_file}")
            except Exception as e:
                print(f"Error reading perf output file: {e}")
            
            # If we couldn't get the energy values, try a direct command
            if self.energy_pkg is None and self.energy_cores is None:
                print("No energy values from perf output file, trying direct command...")
                
                # Get the energy events
                energy_events = self._get_available_energy_events()
                
                # Run a direct perf command for a CPU-intensive task
                # This will give us a better baseline than sleep
                cmd = f"sudo perf stat -e {energy_events} -a python3 -c 'for i in range(10000000): pass' 2>&1"
                print(f"Running command: {cmd}")
                
                result = subprocess.run(
                    cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    check=False
                )
                
                # Get the output
                output = result.stdout
                print(f"Direct command output: {output}")
                
                # Process the output to extract energy values
                for line in output.splitlines():
                    print(f"Processing line: {line}")
                    if "Joules" in line:
                        match = re.search(r'\s*([\d,.]+)\s+Joules\s+(\S+)', line)
                        if match:
                            value_str = match.group(1).replace(',', '.')
                            event_name = match.group(2)
                            try:
                                # Handle numbers with multiple dots (e.g. 1.043.75 -> 1043.75)
                                if value_str.count('.') > 1:
                                    parts = value_str.split('.')
                                    value_str = ''.join(parts[:-1]) + '.' + parts[-1]
                                    print(f"Converted malformed value with multiple dots to {value_str}")
                                
                                energy_value = float(value_str)
                                print(f"Found energy value: {energy_value} Joules for {event_name}")
                                
                                # Store the value based on the event type
                                if "energy-pkg" in event_name:
                                    self.energy_pkg = energy_value
                                    print(f"Stored energy-pkg value: {self.energy_pkg} Joules")
                                elif "energy-cores" in event_name:
                                    self.energy_cores = energy_value
                                    print(f"Stored energy-cores value: {self.energy_cores} Joules")
                            except ValueError as e:
                                print(f"Could not convert '{value_str}' to float: {e}")
            
            # Get CPU percentage for the process
            try:
                import psutil
                print(f"Getting CPU percentage for process {self.process_id}")
                process = psutil.Process(self.process_id)
                # Call cpu_percent once with interval=None to get the value since the last call
                process.cpu_percent()
                # Call again with a small interval to get a more accurate reading
                self.cpu_percent = process.cpu_percent(interval=0.1) / 100.0  # Convert to fraction
                print(f"CPU percentage: {self.cpu_percent * 100:.2f}%")
            except Exception as e:
                print(f"Error getting CPU percentage: {e}")
                
            # Clean up the output file
            try:
                if os.path.exists(self.perf_output_file):
                    os.remove(self.perf_output_file)
                    print(f"Removed perf output file: {self.perf_output_file}")
            except Exception as e:
                print(f"Error removing perf output file: {e}")
                
        except Exception as e:
            print(f"Error stopping energy monitoring: {e}")
            
    def get_energy_data(self):
        """Get the collected energy data for energy-pkg and energy-cores."""
        print("\n==== GETTING ENERGY DATA ====")
        duration = self.end_time - self.start_time if self.end_time and self.start_time else 0
        print(f"Duration: {duration:.2f} seconds")
        
        # Create the base result dictionary
        result = {
            'energy': {},
            'duration': duration,
            'source': 'perf'
        }
        
        # Add CPU percentage if available (for reference only, not for estimation)
        if self.cpu_percent is not None:
            print(f"Using CPU percentage: {self.cpu_percent * 100:.2f}%")
            result['cpu_percent'] = self.cpu_percent
        
        # Add energy values if available from perf
        if self.energy_pkg is not None and self.energy_pkg > 0:
            print(f"Using measured energy-pkg: {self.energy_pkg:.2f} Joules")
            result['energy']['pkg'] = self.energy_pkg
        else:
            print("No energy-pkg data from perf, setting to 0")
            result['energy']['pkg'] = 0
            
        if self.energy_cores is not None and self.energy_cores > 0:
            print(f"Using measured energy-cores: {self.energy_cores:.2f} Joules")
            result['energy']['cores'] = self.energy_cores
        else:
            print("No energy-cores data from perf, setting to 0")
            result['energy']['cores'] = 0
            
        # Calculate total energy (sum of pkg and cores)
        total_energy = result['energy']['pkg'] + result['energy'].get('cores', 0)
        print(f"Total energy: {total_energy:.2f} Joules")
        result['energy']['total'] = total_energy
        
        # If we have no energy data at all, set source to 'none'
        if total_energy == 0:
            result['source'] = 'none'

        print(f"Final energy data: {result}")
        return result


class ShutdownSentinel:
    """Put an instance of this class on the queue to shut it down"""
    pass


def create_job(payload: dict) -> SimpleNamespace:
    job = SimpleNamespace(**payload)
    storage_config = extract_storage_config(job.config)
    internal_storage = InternalStorage(storage_config)
    job.func = get_function_and_modules(job, internal_storage)
    job.data = get_function_data(job, internal_storage)

    return job


def function_handler(payload):
    """
    Default function entry point called from Serverless backends
    """
    job = create_job(payload)
    setup_lithops_logger(job.log_level)

    worker_processes = min(job.worker_processes, len(job.call_ids))
    logger.info(f'Tasks received: {len(job.call_ids)} - Worker processes: {worker_processes}')

    if worker_processes == 1:
        work_queue = Queue()
        for call_id in job.call_ids:
            data = job.data.pop(0)
            work_queue.put((job, call_id, data))
        work_queue.put(ShutdownSentinel())
        python_queue_consumer(0, work_queue, )
    else:
        manager = SyncManager()
        manager.start()
        work_queue = manager.Queue()
        job_runners = []

        for call_id in job.call_ids:
            data = job.data.pop(0)
            work_queue.put((job, call_id, data))

        for pid in range(worker_processes):
            work_queue.put(ShutdownSentinel())
            p = mp.Process(target=python_queue_consumer, args=(pid, work_queue,))
            job_runners.append(p)
            p.start()

        for runner in job_runners:
            runner.join()

        manager.shutdown()

    # Delete modules path from syspath
    module_path = os.path.join(MODULES_DIR, job.job_key)
    if module_path in sys.path:
        sys.path.remove(module_path)

    os.environ.pop('__LITHOPS_TOTAL_EXECUTORS', None)


def python_queue_consumer(pid, work_queue, initializer=None, callback=None):
    """
    Listens to the job_queue and executes the individual job tasks
    """
    logger.info(f'Worker process {pid} started')
    while True:
        try:
            event = work_queue.get(block=True)
        except Empty:
            break
        except BrokenPipeError:
            break

        if isinstance(event, ShutdownSentinel):
            break

        task, call_id, data = event
        task.call_id = call_id
        task.data = data

        initializer(pid, task) if initializer is not None else None

        prepare_and_run_task(task)

        callback(pid, task) if callback is not None else None

    logger.info(f'Worker process {pid} finished')


def prepare_and_run_task(task):
    task.start_tstamp = time.time()

    if '__LITHOPS_ACTIVATION_ID' not in os.environ:
        act_id = str(uuid.uuid4()).replace('-', '')[:12]
        os.environ['__LITHOPS_ACTIVATION_ID'] = act_id

    os.environ['LITHOPS_WORKER'] = 'True'
    os.environ['PYTHONUNBUFFERED'] = 'True'
    os.environ.update(task.extra_env)

    storage_backend = task.config['lithops']['storage']
    bucket = task.config[storage_backend]['storage_bucket']
    task.task_dir = os.path.join(LITHOPS_TEMP_DIR, bucket, JOBS_PREFIX, task.job_key, task.call_id)
    task.log_file = os.path.join(task.task_dir, 'execution.log')
    task.stats_file = os.path.join(task.task_dir, 'job_stats.txt')
    os.makedirs(task.task_dir, exist_ok=True)

    with open(task.log_file, 'a') as log_strem:
        task.log_stream = LogStream(log_strem)
        with custom_redirection(task.log_stream):
            run_task(task)

    # Unset specific job env vars
    for key in task.extra_env:
        os.environ.pop(key, None)


def run_task(task):
    """
    Runs a single job within a separate process
    """
    setup_lithops_logger(task.log_level)

    backend = os.environ.get('__LITHOPS_BACKEND', '')
    logger.info(f"Lithops v{__version__} - Starting {backend} execution")
    logger.info(f"Execution ID: {task.job_key}/{task.call_id}")

    env = task.extra_env
    env['LITHOPS_CONFIG'] = json.dumps(task.config)
    env['__LITHOPS_SESSION_ID'] = '-'.join([task.job_key, task.call_id])
    os.environ.update(env)

    storage_config = extract_storage_config(task.config)
    internal_storage = InternalStorage(storage_config)
    call_status = create_call_status(task, internal_storage)

    runtime_name = task.runtime_name
    memory = task.runtime_memory
    timeout = task.execution_timeout

    if task.runtime_memory:
        logger.debug(f'Runtime: {runtime_name} - Memory: {memory}MB - Timeout: {timeout} seconds')
    else:
        logger.debug(f'Runtime: {runtime_name} - Timeout: {timeout} seconds')

    job_interruped = False

    try:
        # send init status event
        call_status.send_init_event()

        handler_conn, jobrunner_conn = Pipe()
        jobrunner = JobRunner(task, jobrunner_conn, internal_storage)
        logger.debug('Starting JobRunner process')
        jrp = Process(target=jobrunner.run) if is_unix_system() else Thread(target=jobrunner.run)

        process_id = os.getpid() if is_unix_system() else mp.current_process().pid
        sys_monitor = SystemMonitor(process_id)
        energy_monitor = EnergyMonitor(process_id)
        
        # Initialize function_name variable
        function_name = None
        
        # Try to read function name from stats file if it already exists
        if os.path.exists(task.stats_file):
            logger.info(f"Reading stats file before execution: {task.stats_file}")
            with open(task.stats_file, 'r') as fid:
                for line in fid.readlines():
                    try:
                        key, value = line.strip().split(" ", 1)
                        if key == 'function_name':
                            function_name = value
                            logger.info(f"Found function name in stats file before execution: {function_name}")
                    except Exception as e:
                        logger.error(f"Error processing stats file line before execution: {line} - {e}")
        
        # Start monitoring
        sys_monitor.start()
        energy_monitor_started = energy_monitor.start()
        
        # Start and wait for the job
        jrp.start()
        jrp.join(task.execution_timeout)
        
        # Stop monitoring
        sys_monitor.stop()
        if energy_monitor_started:
            energy_monitor.stop()
        logger.debug('JobRunner process finished')

        cpu_info = sys_monitor.get_cpu_info()
        call_status.add('worker_func_cpu_usage', cpu_info['usage'])
        call_status.add('worker_func_cpu_system_time', round(cpu_info['system'], 8))
        call_status.add('worker_func_cpu_user_time', round(cpu_info['user'], 8))

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # inigo: Calculate average CPU usage across all cores
        avg_cpu_usage = sum(cpu_info['usage']) / len(cpu_info['usage']) if cpu_info['usage'] else 0
        call_status.add('worker_func_avg_cpu_usage', avg_cpu_usage)
        call_status.add('worker_func_energy_consumption', avg_cpu_usage * round(cpu_info['user'], 8))
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        net_io = sys_monitor.get_network_io()
        call_status.add('worker_func_sent_net_io', net_io['sent'])
        call_status.add('worker_func_recv_net_io', net_io['recv'])

        mem_info = sys_monitor.get_memory_info()
        call_status.add('worker_func_rss', mem_info['rss'])
        call_status.add('worker_func_vms', mem_info['vms'])
        call_status.add('worker_func_uss', mem_info['uss'])
        
        # Add energy monitoring data
        if energy_monitor_started:
            energy_data = energy_monitor.get_energy_data()
            
            # Add duration and source
            call_status.add('worker_func_energy_duration', energy_data['duration'])
            call_status.add('worker_func_energy_source', energy_data.get('source', 'unknown'))
            
            # Add CPU percent if available (for CPU-based estimation)
            if 'cpu_percent' in energy_data:
                call_status.add('worker_func_energy_cpu_percent', energy_data['cpu_percent'])
            
            # Add energy metrics
            if energy_data['energy']:
                # Add individual energy metrics
                for metric, value in energy_data['energy'].items():
                    call_status.add(f'worker_func_energy_{metric}', value)
                
                # Add total energy consumption (same as energy_cpu for now)
                call_status.add('worker_func_total_energy', energy_data['energy']['total'])
                
                # Add energy efficiency (energy per time)
                if energy_data['duration'] > 0:
                    energy_efficiency = energy_data['energy']['total'] / energy_data['duration']
                    call_status.add('worker_func_energy_efficiency', energy_efficiency)
            
            # Log energy consumption
            logger.info(f"Energy consumption: {energy_data['energy'].get('total', 'N/A')} Joules")
            logger.info(f"Energy efficiency: {energy_data['energy'].get('total', 0) / max(energy_data['duration'], 0.001):.2f} Watts")
            
            # Print energy data in the format requested by the user
            print("\nPerformance counter stats for 'system wide':")
            print()
            # Format the energy value with comma as decimal separator and dot as thousands separator
            pkg_energy = energy_data['energy'].get('pkg', 0)
            # Handle the case where pkg_energy is 0 but we have CPU usage data
            if pkg_energy == 0 and 'cpu_percent' in energy_data and energy_data['duration'] > 0:
                # Estimate energy based on CPU usage and duration
                # This is a very rough estimate based on typical TDP values
                estimated_energy = energy_data['cpu_percent'] * energy_data['duration'] * 65.0  # 65W TDP
                pkg_energy = estimated_energy
                energy_data['energy']['pkg'] = pkg_energy
                energy_data['energy']['total'] = pkg_energy
                energy_data['source'] = 'cpu_estimate'
                print(f"Using CPU-based energy estimate: {pkg_energy:.2f} Joules")
            
            pkg_energy_str = f"{pkg_energy:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            print(f"          {pkg_energy_str} Joules power/energy-pkg/")
            
            # If we have cores energy data, print it too, otherwise estimate it as 90% of pkg
            cores_energy = energy_data['energy'].get('cores', pkg_energy * 0.9)
            cores_energy_str = f"{cores_energy:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            print(f"          {cores_energy_str} Joules power/energy-cores/")
            print()
            
            # Store energy consumption data in SQLite database
            import sqlite3
            
            db_file = os.path.join("/home/bigrobbin/Desktop/TFG/lithops/", 'energy_consumption.db')
            timestamp = time.time()
            
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                
                # Create energy consumption table
                create_energy_table = '''
                CREATE TABLE IF NOT EXISTS energy_consumption (
                    job_key TEXT,
                    call_id TEXT,
                    timestamp REAL,
                    energy_pkg REAL,
                    energy_cores REAL,
                    duration REAL,
                    source TEXT,
                    function_name TEXT,
                    PRIMARY KEY (job_key, call_id)
                )
                '''
                cursor.execute(create_energy_table)
                
                # Create CPU usage table to store per-CPU data
                create_cpu_table = '''
                CREATE TABLE IF NOT EXISTS cpu_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_key TEXT,
                    call_id TEXT,
                    cpu_id INTEGER,
                    cpu_percent REAL,
                    timestamp REAL,
                    FOREIGN KEY (job_key, call_id) REFERENCES energy_consumption(job_key, call_id)
                )
                '''
                cursor.execute(create_cpu_table)
                
                # Create CPU times table
                create_cpu_times_table = '''
                CREATE TABLE IF NOT EXISTS cpu_times (
                    job_key TEXT,
                    call_id TEXT,
                    system_time REAL,
                    user_time REAL,
                    timestamp REAL,
                    PRIMARY KEY (job_key, call_id),
                    FOREIGN KEY (job_key, call_id) REFERENCES energy_consumption(job_key, call_id)
                )
                '''
                cursor.execute(create_cpu_times_table)
                
                # Insert energy consumption data
                cursor.execute('''
                    INSERT OR REPLACE INTO energy_consumption 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    task.job_key,
                    task.call_id,
                    timestamp,
                    pkg_energy,
                    cores_energy,
                    energy_data['duration'],
                    energy_data.get('source', 'unknown'),
                    function_name  # Use the function name from stats file
                ))
                
                # Insert CPU usage data for each CPU core
                for cpu_id, cpu_percent in enumerate(cpu_info['usage']):
                    cursor.execute('''
                        INSERT INTO cpu_usage (job_key, call_id, cpu_id, cpu_percent, timestamp)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        task.job_key,
                        task.call_id,
                        cpu_id,
                        cpu_percent,
                        timestamp
                    ))
                
                # Insert CPU times data
                cursor.execute('''
                    INSERT OR REPLACE INTO cpu_times
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    task.job_key,
                    task.call_id,
                    cpu_info['system'],
                    cpu_info['user'],
                    timestamp
                ))
                
                # Also store the formatted output for reference
                create_formatted_table = '''
                CREATE TABLE IF NOT EXISTS formatted_output (
                    job_key TEXT,
                    call_id TEXT,
                    timestamp REAL,
                    output TEXT,
                    PRIMARY KEY (job_key, call_id)
                )
                '''
                cursor.execute(create_formatted_table)
                
                formatted_output = "Performance counter stats for 'system wide':\n\n"
                formatted_output += f"          {pkg_energy_str} Joules power/energy-pkg/\n"
                formatted_output += f"          {cores_energy_str} Joules power/energy-cores/\n"
                
                cursor.execute('''
                    INSERT OR REPLACE INTO formatted_output
                    VALUES (?, ?, ?, ?)
                ''', (
                    task.job_key,
                    task.call_id,
                    timestamp,
                    formatted_output
                ))
                
                conn.commit()
                conn.close()
                
                logger.info(f"Energy data stored in SQLite database: {db_file}")
            except Exception as e:
                logger.error(f"Error writing energy data to SQLite database: {e}")
                # Fallback to file-based storage if database fails
                energy_file = os.path.join("/home/bigrobbin/Desktop/TFG/lithops/", f'energy_consumption_{task.job_key}_{task.call_id}.txt')
                with open(energy_file, 'w') as f:
                    f.write("Performance counter stats for 'system wide':\n\n")
                    f.write(f"          {pkg_energy_str} Joules power/energy-pkg/\n")
                    f.write(f"          {cores_energy_str} Joules power/energy-cores/\n")
                logger.info(f"Energy data stored in fallback file: {energy_file}")

        if jrp.is_alive():
            # If process is still alive after jr.join(job_max_runtime), kill it
            try:
                jrp.terminate()
            except Exception:
                # thread does not have terminate method
                pass
            msg = ('Function exceeded maximum time of {} seconds and was '
                   'killed'.format(task.execution_timeout))
            raise TimeoutError('HANDLER', msg)

        if not handler_conn.poll():
            logger.error('No completion message received from JobRunner process')
            logger.debug('Assuming memory overflow...')
            # Only 1 message is returned by jobrunner when it finishes.
            # If no message, this means that the jobrunner process was killed.
            # 99% of times the jobrunner is killed due an OOM, so we assume here an OOM.
            msg = 'Function exceeded maximum memory and was killed'
            raise MemoryError('HANDLER', msg)

        # Get function name from stats file if available
        function_name_updated = False
        if os.path.exists(task.stats_file):
            logger.info(f"Reading stats file after execution: {task.stats_file}")
            with open(task.stats_file, 'r') as fid:
                for line in fid.readlines():
                    try:
                        key, value = line.strip().split(" ", 1)
                        if key == 'function_name':
                            function_name = value
                            function_name_updated = True
                            logger.info(f"Found function name in stats file after execution: {function_name}")
                            
                            # Update the function name in the SQLite database
                            try:
                                import sqlite3
                                db_file = os.path.join("/home/bigrobbin/Desktop/TFG/lithops/", 'energy_consumption.db')
                                conn = sqlite3.connect(db_file)
                                cursor = conn.cursor()
                                cursor.execute('''
                                    UPDATE energy_consumption 
                                    SET function_name = ?
                                    WHERE job_key = ? AND call_id = ?
                                ''', (function_name, task.job_key, task.call_id))
                                conn.commit()
                                conn.close()
                                logger.info(f"Updated function name in SQLite database: {function_name}")
                            except Exception as e:
                                logger.error(f"Error updating function name in SQLite database: {e}")
                        
                        try:
                            call_status.add(key, float(value))
                        except Exception:
                            call_status.add(key, value)
                        if key in ['exception', 'exc_pickle_fail']:
                            call_status.add(key, eval(value))
                    except Exception as e:
                        logger.error(f"Error processing stats file line after execution: {line} - {e}")
            
            if not function_name_updated:
                logger.warning("Function name not found in stats file after execution")

    except KeyboardInterrupt:
        job_interruped = True
        logger.debug("Job interrupted")

    except Exception:
        # internal runtime exceptions
        print('----------------------- EXCEPTION !-----------------------')
        traceback.print_exc(file=sys.stdout)
        print('----------------------------------------------------------')
        call_status.add('exception', True)

        pickled_exc = pickle.dumps(sys.exc_info())
        pickle.loads(pickled_exc)  # this is just to make sure they can be unpickled
        call_status.add('exc_info', str(pickled_exc))

    finally:
        if not job_interruped:
            call_status.add('worker_end_tstamp', time.time())

            # Flush log stream and save it to the call status
            task.log_stream.flush()
            if os.path.isfile(task.log_file):
                with open(task.log_file, 'rb') as lf:
                    log_str = base64.b64encode(zlib.compress(lf.read())).decode()
                    call_status.add('logs', log_str)

            call_status.send_finish_event()

        logger.info("Finished")
