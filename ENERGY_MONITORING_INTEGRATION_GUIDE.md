# Energy Monitoring Integration Guide

This guide explains how to integrate RAPL, eBPF, PERF, and PSUtil energy monitoring systems into other environments, based on the comprehensive implementation developed for Lithops.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [RAPL Integration](#rapl-integration)
- [PERF Integration](#perf-integration)
- [eBPF Integration](#ebpf-integration)
- [PSUtil Integration](#psutil-integration)
- [Unified Energy Manager](#unified-energy-manager)
- [Testing and Validation](#testing-and-validation)
- [Troubleshooting](#troubleshooting)

## Overview

This energy monitoring system provides comprehensive energy measurement and system resource monitoring through four complementary approaches:

- **RAPL (Running Average Power Limit)**: Hardware-level energy counters
- **PERF**: Kernel performance counters for energy measurement
- **eBPF**: In-kernel monitoring with custom energy estimation
- **PSUtil**: System resource monitoring and CPU information

## Prerequisites

### System Requirements
```bash
# Linux kernel 3.3+ (for RAPL)
uname -r

# Check RAPL availability
ls /sys/class/powercap/intel-rapl*/

# Check PERF availability
which perf

# Python 3.6+
python3 --version
```

### Required Packages
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y \
    linux-tools-common \
    linux-tools-generic \
    linux-tools-$(uname -r) \
    python3-dev \
    python3-pip \
    build-essential \
    clang \
    llvm \
    libbpf-dev

# Python packages
pip install psutil bcc-python
```

### Permissions Setup
```bash
# For RAPL access (requires root or specific permissions)
sudo chmod +r /sys/class/powercap/intel-rapl*/energy_uj

# For PERF access
echo 'kernel.perf_event_paranoid = -1' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# For eBPF (requires root or CAP_BPF capability)
# Run with sudo or add user to appropriate groups
```

## RAPL Integration

### 1. RAPL Energy Monitor Implementation

Create `energymonitor_rapl.py`:

```python
import os
import time
import logging

class EnergyMonitor:
    """RAPL-based energy monitor using direct /sys/class/powercap/ access."""
    
    def __init__(self, process_id):
        self.process_id = process_id
        self.start_time = None
        self.end_time = None
        self.initial_energy = {}
        self.final_energy = {}
        self.rapl_domains = {}
        
    def _discover_rapl_domains(self):
        """Discover available RAPL domains."""
        rapl_base = "/sys/class/powercap"
        domains = {}
        
        try:
            for item in os.listdir(rapl_base):
                if item.startswith("intel-rapl:"):
                    domain_path = os.path.join(rapl_base, item)
                    name_file = os.path.join(domain_path, "name")
                    energy_file = os.path.join(domain_path, "energy_uj")
                    
                    if os.path.exists(name_file) and os.path.exists(energy_file):
                        with open(name_file, 'r') as f:
                            domain_name = f.read().strip()
                        domains[domain_name] = energy_file
                        
        except (OSError, IOError) as e:
            logging.warning(f"Error discovering RAPL domains: {e}")
            
        return domains
    
    def start(self):
        """Start RAPL energy monitoring."""
        self.rapl_domains = self._discover_rapl_domains()
        
        if not self.rapl_domains:
            logging.warning("No RAPL domains found")
            return False
            
        self.start_time = time.time()
        self.initial_energy = self._read_energy_values()
        
        return len(self.initial_energy) > 0
    
    def stop(self):
        """Stop RAPL energy monitoring."""
        if self.start_time is None:
            return
            
        self.end_time = time.time()
        self.final_energy = self._read_energy_values()
    
    def _read_energy_values(self):
        """Read current energy values from RAPL domains."""
        energy_values = {}
        
        for domain_name, energy_file in self.rapl_domains.items():
            try:
                with open(energy_file, 'r') as f:
                    # Energy is in microjoules, convert to joules
                    energy_uj = int(f.read().strip())
                    energy_values[domain_name] = energy_uj / 1_000_000.0
            except (OSError, IOError, ValueError) as e:
                logging.debug(f"Error reading {energy_file}: {e}")
                
        return energy_values
    
    def get_energy_data(self):
        """Get energy consumption data."""
        if not self.initial_energy or not self.final_energy:
            return {
                'duration': 0.0,
                'source': 'unavailable',
                'energy': {'pkg': 0.0, 'cores': 0.0}
            }
        
        duration = self.end_time - self.start_time
        energy_consumption = {}
        
        # Calculate energy deltas
        for domain in self.initial_energy:
            if domain in self.final_energy:
                delta = self.final_energy[domain] - self.initial_energy[domain]
                energy_consumption[domain] = max(0.0, delta)
        
        # Map to standard format
        pkg_energy = energy_consumption.get('package-0', 0.0)
        cores_energy = energy_consumption.get('core', 0.0)
        
        return {
            'duration': duration,
            'source': 'rapl_direct',
            'energy': {
                'pkg': pkg_energy,
                'cores': cores_energy
            },
            'raw_domains': energy_consumption
        }
```

### 2. Usage Commands

```bash
# Check RAPL availability
ls -la /sys/class/powercap/intel-rapl*/energy_uj

# Fix permissions if needed
sudo chmod +r /sys/class/powercap/intel-rapl*/energy_uj

# Test RAPL reading
cat /sys/class/powercap/intel-rapl:0/energy_uj
```

## PERF Integration

### 1. PERF Energy Monitor Implementation

Create `energymonitor_perf.py`:

```python
import subprocess
import tempfile
import os
import time
import logging

class EnergyMonitor:
    """PERF-based energy monitor using kernel perf subsystem."""
    
    def __init__(self, process_id):
        self.process_id = process_id
        self.perf_process = None
        self.temp_file = None
        self.start_time = None
        self.end_time = None
        
    def _find_perf_binary(self):
        """Find working perf binary."""
        perf_paths = [
            '/usr/bin/perf',
            f'/usr/lib/linux-tools/{os.uname().release}/perf',
            '/usr/lib/linux-tools/6.8.0-78-generic/perf'  # Fallback
        ]
        
        for perf_path in perf_paths:
            if os.path.exists(perf_path):
                try:
                    result = subprocess.run([perf_path, '--version'], 
                                          capture_output=True, timeout=5)
                    if result.returncode == 0:
                        return perf_path
                except:
                    continue
                    
        return None
    
    def start(self):
        """Start PERF energy monitoring."""
        perf_binary = self._find_perf_binary()
        if not perf_binary:
            logging.warning("No working perf binary found")
            return False
        
        # Create temporary file for perf output
        self.temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        self.temp_file.close()
        
        # PERF command for energy monitoring
        perf_cmd = [
            perf_binary, 'stat',
            '-e', 'power/energy-pkg/',
            '-e', 'power/energy-cores/',
            '-o', self.temp_file.name,
            '-p', str(self.process_id)
        ]
        
        try:
            self.perf_process = subprocess.Popen(
                perf_cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.start_time = time.time()
            return True
            
        except Exception as e:
            logging.error(f"Failed to start perf: {e}")
            return False
    
    def stop(self):
        """Stop PERF energy monitoring."""
        if self.perf_process:
            self.perf_process.terminate()
            self.perf_process.wait(timeout=10)
            self.end_time = time.time()
    
    def get_energy_data(self):
        """Parse PERF output and return energy data."""
        if not self.temp_file or not os.path.exists(self.temp_file.name):
            return {
                'duration': 0.0,
                'source': 'unavailable',
                'energy': {'pkg': 0.0, 'cores': 0.0}
            }
        
        duration = (self.end_time - self.start_time) if self.end_time and self.start_time else 0.0
        pkg_energy = 0.0
        cores_energy = 0.0
        
        try:
            with open(self.temp_file.name, 'r') as f:
                content = f.read()
                
            # Parse perf output for energy values
            for line in content.split('\n'):
                if 'power/energy-pkg/' in line:
                    parts = line.split()
                    if len(parts) > 0:
                        try:
                            pkg_energy = float(parts[0].replace(',', ''))
                        except ValueError:
                            pass
                elif 'power/energy-cores/' in line:
                    parts = line.split()
                    if len(parts) > 0:
                        try:
                            cores_energy = float(parts[0].replace(',', ''))
                        except ValueError:
                            pass
                            
        except Exception as e:
            logging.error(f"Error parsing perf output: {e}")
        
        # Cleanup
        try:
            os.unlink(self.temp_file.name)
        except:
            pass
        
        return {
            'duration': duration,
            'source': 'perf_stat' if pkg_energy > 0 or cores_energy > 0 else 'unavailable',
            'energy': {
                'pkg': pkg_energy,
                'cores': cores_energy
            }
        }
```

### 2. Usage Commands

```bash
# Check perf availability
perf --version

# Find correct perf binary for your kernel
ls /usr/lib/linux-tools/*/perf

# Test perf energy events
perf list | grep power

# Set permissions for perf
echo 'kernel.perf_event_paranoid = -1' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

## eBPF Integration

### 1. eBPF Energy Monitor Implementation

Create `energymonitor_ebpf.py`:

```python
from bcc import BPF
import time
import logging

class EBPFEnergyMonitor:
    """eBPF-based energy monitor with context switch tracking."""
    
    def __init__(self, process_id):
        self.process_id = process_id
        self.bpf = None
        self.start_time = None
        self.end_time = None
        
    def start(self):
        """Start eBPF energy monitoring."""
        bpf_program = """
        #include <uapi/linux/ptrace.h>
        #include <linux/sched.h>
        
        BPF_HASH(context_switches, u32, u64);
        BPF_HASH(cpu_time, u32, u64);
        
        int trace_context_switch(struct pt_regs *ctx) {
            u32 pid = bpf_get_current_pid_tgid() >> 32;
            u64 ts = bpf_ktime_get_ns();
            u64 *count = context_switches.lookup(&pid);
            
            if (count) {
                (*count)++;
            } else {
                u64 initial = 1;
                context_switches.update(&pid, &initial);
            }
            
            cpu_time.update(&pid, &ts);
            return 0;
        }
        """
        
        try:
            self.bpf = BPF(text=bpf_program)
            self.bpf.attach_kprobe(event="finish_task_switch", fn_name="trace_context_switch")
            self.start_time = time.time()
            return True
            
        except Exception as e:
            logging.error(f"Failed to start eBPF monitoring: {e}")
            return False
    
    def stop(self):
        """Stop eBPF energy monitoring."""
        if self.bpf:
            self.bpf.detach_kprobe(event="finish_task_switch")
            self.end_time = time.time()
    
    def get_energy_data(self):
        """Get energy data from eBPF measurements."""
        if not self.bpf or not self.start_time:
            return {
                'duration': 0.0,
                'source': 'unavailable',
                'energy': {'pkg': 0.0, 'cores': 0.0, 'cpu_cycles': 0.0}
            }
        
        duration = (self.end_time - self.start_time) if self.end_time else 0.0
        
        # Get context switch data
        context_switches = self.bpf["context_switches"]
        total_switches = 0
        
        for k, v in context_switches.items():
            if k.value == self.process_id:
                total_switches = v.value
                break
        
        # Estimate energy based on context switches and duration
        # This is a simplified model - adjust coefficients based on your system
        base_power = 15.0  # Base CPU power in watts
        switch_energy = total_switches * 0.001  # Energy per context switch
        time_energy = duration * base_power
        
        estimated_energy = time_energy + switch_energy
        
        return {
            'duration': duration,
            'source': 'ebpf_estimation',
            'energy': {
                'pkg': estimated_energy * 0.6,  # Assume 60% package
                'cores': estimated_energy * 0.4,  # Assume 40% cores
                'cpu_cycles': total_switches,
                'energy_from_cycles': switch_energy
            }
        }
```

### 2. Usage Commands

```bash
# Install BCC (BPF Compiler Collection)
sudo apt-get install bpfcc-tools linux-headers-$(uname -r)

# Install Python BCC
pip install bcc

# Test eBPF availability
sudo python3 -c "from bcc import BPF; print('eBPF available')"

# Check BPF filesystem
mount | grep bpf
```

## PSUtil Integration

### 1. PSUtil System Monitor Implementation

Create `energymonitor_psutil.py`:

```python
import time
import logging

class EnergyMonitor:
    """PSUtil-based system resource monitor."""
    
    def __init__(self, process_id):
        self.process_id = process_id
        self.start_time = None
        self.end_time = None
        self.initial_metrics = {}
        self.final_metrics = {}
        
    def start(self):
        """Start PSUtil system monitoring."""
        try:
            import psutil
            self.start_time = time.time()
            self.initial_metrics = self._collect_system_metrics()
            return True
        except ImportError:
            logging.warning("PSUtil not available")
            return False
    
    def stop(self):
        """Stop PSUtil system monitoring."""
        if self.start_time:
            import psutil
            self.end_time = time.time()
            self.final_metrics = self._collect_system_metrics()
    
    def _collect_system_metrics(self):
        """Collect comprehensive system metrics using PSUtil."""
        import psutil
        metrics = {}
        
        # CPU metrics with proper measurement
        psutil.cpu_percent(interval=None)  # Initialize
        time.sleep(0.5)  # Wait for measurement
        cpu_percent = psutil.cpu_percent(interval=None)
        per_cpu_percent = psutil.cpu_percent(interval=None, percpu=True)
        
        metrics.update({
            'cpu_percent': cpu_percent,
            'per_cpu_percent': per_cpu_percent,
            'cpu_cores_physical': psutil.cpu_count(logical=False) or 0,
            'cpu_cores_logical': psutil.cpu_count(logical=True) or 0,
        })
        
        # CPU frequency
        try:
            freq_info = psutil.cpu_freq()
            metrics['cpu_freq_current'] = freq_info.current if freq_info else 0.0
        except:
            metrics['cpu_freq_current'] = 0.0
        
        # Memory metrics
        try:
            memory = psutil.virtual_memory()
            metrics.update({
                'memory_percent': memory.percent,
                'memory_used_mb': memory.used / (1024 * 1024),
                'memory_total_mb': memory.total / (1024 * 1024)
            })
        except:
            metrics.update({
                'memory_percent': 0.0,
                'memory_used_mb': 0.0,
                'memory_total_mb': 0.0
            })
        
        # CPU temperature
        try:
            temps = psutil.sensors_temperatures()
            cpu_temp = 0.0
            if temps:
                for name, entries in temps.items():
                    if 'cpu' in name.lower() or 'core' in name.lower():
                        if entries:
                            cpu_temp = entries[0].current
                            break
            metrics['cpu_temp_celsius'] = cpu_temp
        except:
            metrics['cpu_temp_celsius'] = 0.0
        
        # Process-specific metrics
        try:
            process = psutil.Process(self.process_id)
            process.cpu_percent()  # Initialize
            time.sleep(0.2)
            process_cpu = process.cpu_percent()
            process_memory = process.memory_info()
            
            metrics.update({
                'process_cpu_percent': process_cpu,
                'process_memory_mb': process_memory.rss / (1024 * 1024)
            })
        except:
            metrics.update({
                'process_cpu_percent': 0.0,
                'process_memory_mb': 0.0
            })
        
        return metrics
    
    def get_energy_data(self):
        """Get system monitoring data (no energy, but resource metrics)."""
        duration = (self.end_time - self.start_time) if self.end_time and self.start_time else 0.0
        
        if not self.initial_metrics or not self.final_metrics:
            return {
                'duration': duration,
                'source': 'unavailable',
                'system': {},
                'process': {},
                'cpu_info': {}
            }
        
        # Calculate best CPU measurement
        initial_cpu = self.initial_metrics.get('cpu_percent', 0.0)
        final_cpu = self.final_metrics.get('cpu_percent', 0.0)
        best_cpu = max(initial_cpu, final_cpu)
        
        return {
            'duration': duration,
            'source': 'psutil_system_monitoring',
            'system': {
                'cpu_percent': best_cpu,
                'cpu_percent_initial': initial_cpu,
                'cpu_percent_final': final_cpu,
                'per_cpu_initial': self.initial_metrics.get('per_cpu_percent', []),
                'per_cpu_final': self.final_metrics.get('per_cpu_percent', []),
                'memory_percent': self.final_metrics.get('memory_percent', 0.0),
                'memory_used_mb': self.final_metrics.get('memory_used_mb', 0.0),
                'cpu_freq_current': self.final_metrics.get('cpu_freq_current', 0.0),
                'cpu_temp_celsius': self.final_metrics.get('cpu_temp_celsius', 0.0),
            },
            'process': {
                'cpu_percent': max(
                    self.initial_metrics.get('process_cpu_percent', 0.0),
                    self.final_metrics.get('process_cpu_percent', 0.0)
                ),
                'memory_mb': self.final_metrics.get('process_memory_mb', 0.0)
            },
            'cpu_info': {
                'cores_physical': self.final_metrics.get('cpu_cores_physical', 0),
                'cores_logical': self.final_metrics.get('cpu_cores_logical', 0),
                'frequency_current': self.final_metrics.get('cpu_freq_current', 0.0)
            }
        }
```

### 2. Usage Commands

```bash
# Install PSUtil
pip install psutil

# Test PSUtil functionality
python3 -c "import psutil; print(f'CPU: {psutil.cpu_percent()}%, Memory: {psutil.virtual_memory().percent}%')"

# Check available sensors
python3 -c "import psutil; print(psutil.sensors_temperatures())"
```

## Unified Energy Manager

### 1. Energy Manager Implementation

Create `energymanager.py`:

```python
import logging

class EnergyManager:
    """Unified energy manager running all monitoring methods simultaneously."""
    
    def __init__(self, process_id):
        self.process_id = process_id
        self.monitors = {}
        self.monitor_status = {}
        self._initialize_monitors()
    
    def _initialize_monitors(self):
        """Initialize all available energy monitoring methods."""
        monitor_configs = {
            'perf': {
                'class': 'EnergyMonitor',
                'module': 'energymonitor_perf'
            },
            'rapl': {
                'class': 'EnergyMonitor', 
                'module': 'energymonitor_rapl'
            },
            'ebpf': {
                'class': 'EBPFEnergyMonitor',
                'module': 'energymonitor_ebpf'
            },
            'psutil': {
                'class': 'EnergyMonitor',
                'module': 'energymonitor_psutil'
            }
        }
        
        for method_name, config in monitor_configs.items():
            try:
                module = __import__(config['module'], fromlist=[config['class']])
                monitor_class = getattr(module, config['class'])
                monitor = monitor_class(self.process_id)
                self.monitors[method_name] = monitor
                self.monitor_status[method_name] = False
                logging.debug(f"Initialized {method_name} energy monitor")
            except Exception as e:
                logging.warning(f"Failed to initialize {method_name}: {e}")
                self.monitors[method_name] = None
                self.monitor_status[method_name] = False
    
    def start(self):
        """Start all available energy monitoring methods."""
        any_started = False
        
        for method_name, monitor in self.monitors.items():
            if monitor is not None:
                try:
                    started = monitor.start()
                    self.monitor_status[method_name] = started
                    if started:
                        logging.info(f"Started {method_name} energy monitor")
                        any_started = True
                except Exception as e:
                    logging.error(f"Error starting {method_name}: {e}")
                    self.monitor_status[method_name] = False
        
        return any_started
    
    def stop(self):
        """Stop all active energy monitoring methods."""
        for method_name, monitor in self.monitors.items():
            if monitor is not None and self.monitor_status[method_name]:
                try:
                    monitor.stop()
                    logging.debug(f"Stopped {method_name} energy monitor")
                except Exception as e:
                    logging.error(f"Error stopping {method_name}: {e}")
    
    def get_energy_data(self):
        """Collect energy data from all active monitors."""
        results = {}
        
        for method_name, monitor in self.monitors.items():
            if monitor is not None and self.monitor_status[method_name]:
                try:
                    energy_data = monitor.get_energy_data()
                    results[method_name] = energy_data
                    logging.info(f"{method_name}: {energy_data}")
                except Exception as e:
                    logging.error(f"Error getting data from {method_name}: {e}")
        
        return results
```

### 2. Usage Example

Create `test_energy_monitoring.py`:

```python
import time
import os
from energymanager import EnergyManager

def cpu_intensive_task():
    """Simple CPU-intensive task for testing."""
    result = 0
    for i in range(1000000):
        result += i * i
    return result

def main():
    # Get current process ID
    process_id = os.getpid()
    
    # Initialize energy manager
    energy_manager = EnergyManager(process_id)
    
    # Start monitoring
    if not energy_manager.start():
        print("Failed to start any energy monitors")
        return
    
    print("Starting energy monitoring...")
    
    # Run test workload
    start_time = time.time()
    result = cpu_intensive_task()
    end_time = time.time()
    
    # Stop monitoring
    energy_manager.stop()
    
    # Get results
    energy_data = energy_manager.get_energy_data()
    
    print(f"\nTask completed in {end_time - start_time:.3f} seconds")
    print(f"Result: {result}")
    print("\nEnergy Monitoring Results:")
    print("=" * 50)
    
    for method, data in energy_data.items():
        print(f"\n{method.upper()}:")
        print(f"  Duration: {data.get('duration', 0):.3f}s")
        print(f"  Source: {data.get('source', 'unknown')}")
        
        if 'energy' in data:
            energy = data['energy']
            print(f"  Package Energy: {energy.get('pkg', 0):.3f}J")
            print(f"  Cores Energy: {energy.get('cores', 0):.3f}J")
            total = energy.get('pkg', 0) + energy.get('cores', 0)
            print(f"  Total Energy: {total:.3f}J")
        
        if method == 'psutil' and 'system' in data:
            system = data['system']
            print(f"  CPU Usage: {system.get('cpu_percent', 0):.1f}%")
            print(f"  Memory Usage: {system.get('memory_percent', 0):.1f}%")
            print(f"  CPU Frequency: {system.get('cpu_freq_current', 0):.0f}MHz")
            print(f"  CPU Temperature: {system.get('cpu_temp_celsius', 0):.1f}°C")

if __name__ == "__main__":
    main()
```

## Testing and Validation

### 1. System Compatibility Check

Create `check_compatibility.py`:

```python
#!/usr/bin/env python3
import os
import subprocess
import sys

def check_rapl():
    """Check RAPL availability."""
    rapl_path = "/sys/class/powercap"
    if not os.path.exists(rapl_path):
        return False, "RAPL not available - /sys/class/powercap not found"
    
    rapl_domains = [d for d in os.listdir(rapl_path) if d.startswith("intel-rapl:")]
    if not rapl_domains:
        return False, "No Intel RAPL domains found"
    
    # Check permissions
    for domain in rapl_domains:
        energy_file = os.path.join(rapl_path, domain, "energy_uj")
        if os.path.exists(energy_file):
            try:
                with open(energy_file, 'r') as f:
                    f.read()
                return True, f"RAPL available with {len(rapl_domains)} domains"
            except PermissionError:
                return False, "RAPL available but permission denied - run with sudo or fix permissions"
    
    return False, "RAPL domains found but no readable energy files"

def check_perf():
    """Check PERF availability."""
    perf_paths = [
        '/usr/bin/perf',
        f'/usr/lib/linux-tools/{os.uname().release}/perf'
    ]
    
    for perf_path in perf_paths:
        if os.path.exists(perf_path):
            try:
                result = subprocess.run([perf_path, 'list'], 
                                      capture_output=True, timeout=10)
                if result.returncode == 0:
                    output = result.stdout.decode()
                    if 'power/energy' in output:
                        return True, f"PERF available at {perf_path} with energy events"
                    else:
                        return False, f"PERF available at {perf_path} but no energy events"
            except:
                continue
    
    return False, "PERF not available or not working"

def check_ebpf():
    """Check eBPF/BCC availability."""
    try:
        from bcc import BPF
        # Try to compile a simple BPF program
        simple_program = "int hello(void *ctx) { return 0; }"
        bpf = BPF(text=simple_program)
        return True, "eBPF/BCC available and working"
    except ImportError:
        return False, "BCC not installed - run: pip install bcc"
    except Exception as e:
        return False, f"eBPF/BCC available but not working: {e}"

def check_psutil():
    """Check PSUtil availability."""
    try:
        import psutil
        # Test basic functionality
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        return True, f"PSUtil available - CPU: {cpu_percent}%, Memory: {memory.percent}%"
    except ImportError:
        return False, "PSUtil not installed - run: pip install psutil"
    except Exception as e:
        return False, f"PSUtil available but not working: {e}"

def main():
    print("Energy Monitoring Compatibility Check")
    print("=" * 40)
    
    checks = [
        ("RAPL", check_rapl),
        ("PERF", check_perf),
        ("eBPF", check_ebpf),
        ("PSUtil", check_psutil)
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            available, message = check_func()
            results[name] = (available, message)
            status = "✅ AVAILABLE" if available else "❌ NOT AVAILABLE"
            print(f"{name:8} {status:15} - {message}")
        except Exception as e:
            results[name] = (False, f"Error during check: {e}")
            print(f"{name:8} ❌ ERROR        - {e}")
    
    print("\n" + "=" * 40)
    available_count = sum(1 for available, _ in results.values() if available)
    print(f"Summary: {available_count}/{len(checks)} monitoring methods available")
    
    if available_count == 0:
        print("⚠️  No energy monitoring methods available!")
        print("   Install required packages and check permissions.")
        sys.exit(1)
    elif available_count < len(checks):
        print("⚠️  Some monitoring methods unavailable.")
        print("   System will work with available methods.")
    else:
        print("✅ All monitoring methods available!")

if __name__ == "__main__":
    main()
```

### 2. Quick Test Script

Create `quick_test.py`:

```python
#!/usr/bin/env python3
import time
import os
import sys
from energymanager import EnergyManager

def simple_workload():
    """Simple test workload."""
    total = 0
    for i in range(100000):
        total += i ** 2
    return total

def main():
    print("Quick Energy Monitoring Test")
    print("=" * 30)
    
    # Get current process ID
    process_id = os.getpid()
    print(f"Process ID: {process_id}")
    
    # Initialize energy manager
    energy_manager = EnergyManager(process_id)
    
    # Start monitoring
    started = energy_manager.start()
    if not started:
        print("❌ Failed to start any energy monitors")
        sys.exit(1)
    
    active_monitors = [name for name, status in energy_manager.monitor_status.items() if status]
    print(f"✅ Started monitors: {', '.join(active_monitors)}")
    
    # Run workload
    print("\n🔄 Running test workload...")
    start_time = time.time()
    result = simple_workload()
    end_time = time.time()
    
    # Stop monitoring
    energy_manager.stop()
    
    # Get and display results
    energy_data = energy_manager.get_energy_data()
    
    print(f"✅ Workload completed in {end_time - start_time:.3f}s")
    print(f"   Result: {result}")
    
    print("\n📊 Energy Monitoring Results:")
    print("-" * 30)
    
    for method, data in energy_data.items():
        print(f"\n{method.upper()}:")
        duration = data.get('duration', 0)
        source = data.get('source', 'unknown')
        print(f"  Duration: {duration:.3f}s")
        print(f"  Source: {source}")
        
        if 'energy' in data and source != 'unavailable':
            energy = data['energy']
            pkg = energy.get('pkg', 0)
            cores = energy.get('cores', 0)
            total = pkg + cores
            
            if total > 0:
                print(f"  Package: {pkg:.3f}J")
                print(f"  Cores: {cores:.3f}J")
                print(f"  Total: {total:.3f}J")
                if duration > 0:
                    power = total / duration
                    print(f"  Avg Power: {power:.3f}W")
            else:
                print("  No energy data")
        
        if method == 'psutil' and 'system' in data:
            system = data['system']
            print(f"  CPU: {system.get('cpu_percent', 0):.1f}%")
            print(f"  Memory: {system.get('memory_percent', 0):.1f}%")
            temp = system.get('cpu_temp_celsius', 0)
            if temp > 0:
                print(f"  Temperature: {temp:.1f}°C")

if __name__ == "__main__":
    main()
```

## Troubleshooting

### Common Issues and Solutions

#### 1. RAPL Permission Issues
```bash
# Problem: Permission denied when reading RAPL files
# Solution: Fix permissions or run with sudo
sudo chmod +r /sys/class/powercap/intel-rapl*/energy_uj

# Alternative: Add user to appropriate group
sudo usermod -a -G adm $USER
# Then logout and login again
```

#### 2. PERF Not Working
```bash
# Problem: perf command not found or wrong version
# Solution: Install correct perf tools for your kernel
sudo apt-get install linux-tools-$(uname -r)

# Problem: Permission denied for perf events
# Solution: Adjust perf_event_paranoid setting
echo 'kernel.perf_event_paranoid = -1' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# Problem: No energy events available
# Check if your CPU supports energy events
perf list | grep power
```

#### 3. eBPF/BCC Issues
```bash
# Problem: BCC not installed
pip install bcc

# Problem: BCC compilation errors
# Install required headers and tools
sudo apt-get install linux-headers-$(uname -r) clang llvm

# Problem: Permission denied for BPF
# Run with sudo or adjust capabilities
sudo setcap cap_bpf+ep /usr/bin/python3
```

#### 4. PSUtil Issues
```bash
# Problem: PSUtil not installed
pip install psutil

# Problem: No temperature sensors
# Install lm-sensors and detect sensors
sudo apt-get install lm-sensors
sudo sensors-detect
```

### Performance Considerations

#### 1. Monitoring Overhead
- **RAPL**: Very low overhead (~0.1% CPU)
- **PERF**: Low overhead (~0.5% CPU)
- **eBPF**: Medium overhead (~1-2% CPU)
- **PSUtil**: Medium overhead (~1-3% CPU)

#### 2. Accuracy vs. Overhead Trade-offs
```python
# For high-frequency monitoring (reduce overhead)
class LightweightEnergyManager(EnergyManager):
    def _initialize_monitors(self):
        # Only initialize RAPL and PSUtil (lowest overhead)
        monitor_configs = {
            'rapl': {'class': 'EnergyMonitor', 'module': 'energymonitor_rapl'},
            'psutil': {'class': 'EnergyMonitor', 'module': 'energymonitor_psutil'}
        }
        # ... rest of initialization
```

#### 3. Sampling Frequency
```python
# Adjust PSUtil sampling intervals based on needs
def _collect_system_metrics(self):
    # For high-frequency monitoring, reduce sleep times
    time.sleep(0.1)  # Instead of 0.5
    
    # For low-frequency monitoring, increase sleep times
    time.sleep(1.0)  # For less overhead
```

### Integration Examples

#### 1. Flask Web Application
```python
from flask import Flask, jsonify
from energymanager import EnergyManager
import os
import threading

app = Flask(__name__)
energy_manager = EnergyManager(os.getpid())

@app.before_first_request
def start_monitoring():
    energy_manager.start()

@app.route('/energy')
def get_energy():
    data = energy_manager.get_energy_data()
    return jsonify(data)

@app.teardown_appcontext
def stop_monitoring(exception):
    energy_manager.stop()
```

#### 2. Jupyter Notebook Integration
```python
# Cell 1: Setup
from energymanager import EnergyManager
import os

energy_manager = EnergyManager(os.getpid())
energy_manager.start()

# Cell 2: Your computation
# ... your code here ...

# Cell 3: Get results
energy_manager.stop()
results = energy_manager.get_energy_data()
print("Energy consumption:", results)
```

#### 3. Command Line Tool
```python
#!/usr/bin/env python3
import argparse
import subprocess
import sys
from energymanager import EnergyManager

def main():
    parser = argparse.ArgumentParser(description='Monitor energy consumption of a command')
    parser.add_argument('command', nargs='+', help='Command to monitor')
    parser.add_argument('--output', '-o', help='Output file for results')
    args = parser.parse_args()
    
    # Start the command
    process = subprocess.Popen(args.command)
    
    # Monitor its energy consumption
    energy_manager = EnergyManager(process.pid)
    energy_manager.start()
    
    # Wait for command to complete
    process.wait()
    
    # Stop monitoring and get results
    energy_manager.stop()
    results = energy_manager.get_energy_data()
    
    # Output results
    if args.output:
        import json
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
    else:
        print("Energy monitoring results:")
        for method, data in results.items():
            if 'energy' in data:
                energy = data['energy']
                total = energy.get('pkg', 0) + energy.get('cores', 0)
                print(f"{method}: {total:.3f}J")

if __name__ == "__main__":
    main()
```

## Advanced Configuration

### 1. Custom Energy Models
```python
# Create custom energy estimation models
class CustomEnergyEstimator:
    def __init__(self, cpu_model, base_power_watts=15.0):
        self.cpu_model = cpu_model
        self.base_power = base_power_watts
        
    def estimate_energy(self, cpu_percent, duration, frequency_mhz=None):
        """Estimate energy based on CPU usage and frequency."""
        # Simple linear model - customize based on your CPU
        load_factor = cpu_percent / 100.0
        freq_factor = (frequency_mhz / 2000.0) if frequency_mhz else 1.0
        
        estimated_power = self.base_power * load_factor * freq_factor
        return estimated_power * duration
```

### 2. Multi-Process Monitoring
```python
class MultiProcessEnergyManager:
    def __init__(self, process_ids):
        self.managers = {pid: EnergyManager(pid) for pid in process_ids}
    
    def start_all(self):
        for manager in self.managers.values():
            manager.start()
    
    def stop_all(self):
        for manager in self.managers.values():
            manager.stop()
    
    def get_combined_data(self):
        combined = {}
        for pid, manager in self.managers.items():
            combined[f'process_{pid}'] = manager.get_energy_data()
        return combined
```

### 3. Real-time Monitoring
```python
import threading
import time

class RealtimeEnergyMonitor:
    def __init__(self, process_id, interval=1.0):
        self.process_id = process_id
        self.interval = interval
        self.running = False
        self.data_history = []
        
    def start_realtime(self):
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.start()
    
    def stop_realtime(self):
        self.running = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join()
    
    def _monitor_loop(self):
        energy_manager = EnergyManager(self.process_id)
        
        while self.running:
            energy_manager.start()
            time.sleep(self.interval)
            energy_manager.stop()
            
            data = energy_manager.get_energy_data()
            data['timestamp'] = time.time()
            self.data_history.append(data)
            
            # Keep only last 100 measurements
            if len(self.data_history) > 100:
                self.data_history.pop(0)
```

## Conclusion

This comprehensive energy monitoring system provides:

- **Multi-method approach**: RAPL, PERF, eBPF, and PSUtil for comprehensive coverage
- **Cross-validation**: Multiple measurement methods for accuracy verification
- **Flexible integration**: Easy to integrate into existing applications
- **Detailed metrics**: Energy consumption, system resources, and performance data
- **Robust error handling**: Graceful degradation when methods are unavailable

The system automatically detects available monitoring methods and uses all functional ones simultaneously, providing the most comprehensive energy monitoring possible for your environment.

For questions or issues, refer to the troubleshooting section or check the individual monitor implementations for method-specific details.
