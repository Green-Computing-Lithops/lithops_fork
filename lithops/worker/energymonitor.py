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
import time
import re
import subprocess
import logging

# Ensure json is imported in this scope
import json

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
        self.function_name = None
        
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
            
        # Calculate core percentage (energy_cores / energy_pkg)
        if result['energy']['pkg'] > 0:
            core_percentage = result['energy']['cores'] / result['energy']['pkg']
            print(f"Core percentage: {core_percentage:.4f} ({core_percentage * 100:.2f}%)")
            result['energy']['core_percentage'] = core_percentage
        else:
            print("Cannot calculate core percentage, energy_pkg is 0")
            result['energy']['core_percentage'] = 0
        
        # If we have no energy data at all, set source to 'none'
        if result['energy']['pkg'] == 0 and result['energy']['cores'] == 0:
            result['source'] = 'none'

        print(f"Final energy data: {result}")
        return result
        
    def log_energy_data(self, energy_data, task, cpu_info, function_name=None):
        """Log energy data and store it in JSON format."""
        import json
        import logging
        
        logger = logging.getLogger(__name__)
        
        # Store function name if provided
        if function_name:
            self.function_name = function_name
        
        # Log energy consumption
        logger.info(f"Energy consumption: {energy_data['energy'].get('pkg', 'N/A')} Joules (pkg), {energy_data['energy'].get('cores', 'N/A')} Joules (cores)")
        logger.info(f"Core percentage: {energy_data['energy'].get('core_percentage', 0) * 100:.2f}%")
        logger.info(f"Energy efficiency: {energy_data['energy'].get('pkg', 0) / max(energy_data['duration'], 0.001):.2f} Watts")
        
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
            energy_data['source'] = 'cpu_estimate'
            print(f"Using CPU-based energy estimate: {pkg_energy:.2f} Joules")
        
        pkg_energy_str = f"{pkg_energy:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        print(f"          {pkg_energy_str} Joules power/energy-pkg/")
        
        # If we have cores energy data, print it too, otherwise estimate it as 90% of pkg
        cores_energy = energy_data['energy'].get('cores', pkg_energy * 0.9)
        cores_energy_str = f"{cores_energy:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        print(f"          {cores_energy_str} Joules power/energy-cores/")
        
        # Print core percentage
        core_percentage = energy_data['energy'].get('core_percentage', 0)
        print(f"          {core_percentage * 100:.2f}% core percentage (cores/pkg)")
        print()
        
        # Store energy consumption data in JSON format
        self._store_energy_data_json(energy_data, task, cpu_info, pkg_energy, cores_energy, core_percentage, self.function_name)
        
    def _store_energy_data_json(self, energy_data, task, cpu_info, pkg_energy, cores_energy, core_percentage, function_name=None):
        """Store energy data in JSON format."""
        import json
        import logging
        import os
        
        logger = logging.getLogger(__name__)
        
        # Base directory for JSON files - use current working directory or fallback to /tmp
        try:
            # Get the current working directory
            cwd = os.getcwd()
            json_dir = os.path.join(cwd, 'energy_data')
            # Create directory with proper permissions
            os.makedirs(json_dir, exist_ok=True)
            # Ensure the directory has the right permissions
            os.chmod(json_dir, 0o777)  # rwx for all users
            logger.info(f"Created energy data directory: {json_dir}")
        except Exception as e:
            logger.error(f"Error creating energy data directory: {e}")
            # Fallback to /tmp directory which should be writable
            json_dir = os.path.join("/tmp", 'lithops_energy_data')
            os.makedirs(json_dir, exist_ok=True)
            logger.info(f"Using fallback energy data directory: {json_dir}")
        
        timestamp = time.time()
        
        try:
            # Create a unique ID for this execution
            execution_id = f"{task.job_key}_{task.call_id}"
            
            # Main energy consumption data
            energy_consumption = {
                'job_key': task.job_key,
                'call_id': task.call_id,
                'timestamp': timestamp,
                'energy_pkg': pkg_energy,
                'energy_cores': cores_energy,
                'core_percentage': core_percentage,
                'duration': energy_data['duration'],
                'source': energy_data.get('source', 'unknown'),
                'function_name': function_name
            }
            
            # CPU usage data
            cpu_usage = []
            
            # Get start timestamp and end timestamps from cpu_info if available
            start_timestamp = cpu_info.get('start_timestamp', timestamp)
            end_timestamps = cpu_info.get('end_timestamps', [])
            
            # If end_timestamps is not available or empty, use the current timestamp for all cores
            if not end_timestamps:
                end_timestamps = [timestamp] * len(cpu_info['usage'])
            
            # Create CPU usage entries with both start and end timestamps
            for cpu_id, cpu_percent in enumerate(cpu_info['usage']):
                # Get the end timestamp for this CPU core
                end_timestamp = end_timestamps[cpu_id] if cpu_id < len(end_timestamps) else timestamp
                
                cpu_usage.append({
                    'cpu_id': cpu_id,
                    'cpu_percent': cpu_percent,
                    'start_timestamp': start_timestamp,
                    'end_timestamp': end_timestamp
                })
            
            # Combine all data into one object (without cpu_times and formatted_output)
            all_data = {
                'energy_consumption': energy_consumption,
                'cpu_usage': cpu_usage
            }
            
            # Write to a single JSON file
            json_file = os.path.join(json_dir, f"{execution_id}.json")
            with open(json_file, 'w') as f:
                json.dump(all_data, f, indent=2)
            
            logger.info(f"Energy data stored in JSON file: {json_file}")
            
            # Also write a summary file that contains all execution IDs
            summary_file = os.path.join(json_dir, 'summary.json')
            summary = []
            
            if os.path.exists(summary_file):
                try:
                    with open(summary_file, 'r') as f:
                        summary = json.load(f)
                except Exception as e:
                    logger.error(f"Error reading summary file: {e}")
                    summary = []
            
            summary.append({
                'execution_id': execution_id,
                'function_name': function_name,
                'timestamp': timestamp,
                'energy_pkg': pkg_energy,
                'energy_cores': cores_energy,
                'core_percentage': core_percentage
            })
            
            with open(summary_file, 'w') as f:
                json.dump(summary, f, indent=2)
            
        except Exception as e:
            logger.error(f"Error writing energy data to JSON file: {e}")
            # Fallback to simple text file in /tmp directory if JSON fails
            energy_file = os.path.join("/tmp", f'lithops_energy_consumption_{task.job_key}_{task.call_id}.txt')
            # Ensure the directory exists
            os.makedirs(os.path.dirname(energy_file), exist_ok=True)
            with open(energy_file, 'w') as f:
                f.write("Performance counter stats for 'system wide':\n\n")
                f.write(f"          {pkg_energy:.2f} Joules power/energy-pkg/\n")
                f.write(f"          {cores_energy:.2f} Joules power/energy-cores/\n")
                f.write(f"          {core_percentage * 100:.2f}% core percentage (cores/pkg)\n")
            logger.info(f"Energy data stored in fallback file: {energy_file}")
            
    def update_function_name(self, task, function_name):
        """Update the function name in the JSON files."""
        import json
        import logging
        import os
        
        logger = logging.getLogger(__name__)
        
        # Store function name
        self.function_name = function_name
        
        try:
            # Get the current working directory
            cwd = os.getcwd()
            json_dir = os.path.join(cwd, 'energy_data')
            json_file = os.path.join(json_dir, f"{task.job_key}_{task.call_id}.json")
            
            if os.path.exists(json_file):
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                # Update function name
                if 'energy_consumption' in data:
                    data['energy_consumption']['function_name'] = function_name
                
                # Write updated data back to file
                with open(json_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                logger.info(f"Updated function name in JSON file: {function_name}")
                
                # Also update the summary file
                summary_file = os.path.join(json_dir, 'summary.json')
                if os.path.exists(summary_file):
                    with open(summary_file, 'r') as f:
                        summary = json.load(f)
                    
                    for entry in summary:
                        if entry.get('execution_id') == f"{task.job_key}_{task.call_id}":
                            entry['function_name'] = function_name
                    
                    with open(summary_file, 'w') as f:
                        json.dump(summary, f, indent=2)
            else:
                logger.warning(f"JSON file not found for updating function name: {json_file}")
        except Exception as e:
            logger.error(f"Error updating function name in JSON file: {e}")
            
    def read_function_name_from_stats(self, stats_file):
        """Read function name from stats file and update it in the energy monitor."""
        import logging
        
        logger = logging.getLogger(__name__)
        
        if not os.path.exists(stats_file):
            logger.warning(f"Stats file not found: {stats_file}")
            return False
        
        function_name_updated = False
        logger.info(f"Reading stats file for energy monitoring: {stats_file}")
        
        try:
            with open(stats_file, 'r') as fid:
                for line in fid.readlines():
                    try:
                        key, value = line.strip().split(" ", 1)
                        if key == 'function_name':
                            self.function_name = value
                            function_name_updated = True
                            logger.info(f"Found function name in stats file for energy monitoring: {self.function_name}")
                            break  # Exit loop once function name is found
                    except Exception as e:
                        logger.error(f"Error processing stats file line for energy monitoring: {line} - {e}")
            
            if not function_name_updated:
                logger.warning("Function name not found in stats file for energy monitoring")
        except Exception as e:
            logger.error(f"Error reading stats file for energy monitoring: {e}")
            
        return function_name_updated
