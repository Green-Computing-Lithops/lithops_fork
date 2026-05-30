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
import logging
import subprocess
import threading
from collections import defaultdict
from .energymonitor_json_utils import store_energy_data_json, update_function_name

logger = logging.getLogger(__name__)

# Simplified BPF program that focuses on CPU cycles and process tracking

BPF_PROGRAM_PURE_EBPF = """
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>
#include <linux/perf_event.h>

// Define a structure to store ONLY eBPF-based energy data
struct energy_data_t {
    u32 pid;
    u64 cpu_cycles;
    u64 instructions;      // Add CPU instructions counter
    u64 cache_misses;      // Add cache miss counter
    u64 timestamp;
};

// Create BPF maps to store energy data
BPF_HASH(energy_data, u32, struct energy_data_t);
BPF_PERF_OUTPUT(energy_events);

// Function to be called on context switch
int on_context_switch(struct pt_regs *ctx, struct task_struct *prev, struct task_struct *next)
{
    u32 pid = prev->pid;
    
    // Skip kernel threads
    if (pid == 0)
        return 0;
    
    // Get current timestamp
    u64 ts = bpf_ktime_get_ns();
    
    // Read CPU performance counters (NO RAPL)
    u64 cpu_cycles = 0;
    u64 instructions = 0;
    u64 cache_misses = 0;
    
    // Read performance counters using BPF perf event helpers
    bpf_perf_event_read(ctx, &cpu_cycles);
    // Note: Additional counters would need proper perf event setup
    
    // Create energy data structure (NO RAPL FIELDS)
    struct energy_data_t data = {};
    data.pid = pid;
    data.cpu_cycles = cpu_cycles;
    data.instructions = instructions;
    data.cache_misses = cache_misses;
    data.timestamp = ts;
    
    // Store energy data in map
    energy_data.update(&pid, &data);
    
    // Send energy data to user space
    energy_events.perf_submit(ctx, &data, sizeof(data));
    
    return 0;
}
"""


class PureEBPFEnergyMonitor:
    """
    Pure eBPF-based energy monitor that uses ONLY CPU cycles and performance counters
    for energy estimation. NO RAPL dependency.
    """
    def __init__(self, process_id):
        self.process_id = process_id
        self.bpf = None
        self.thread = None
        self.running = False
        self.energy_data = defaultdict(lambda: {
            'cpu_cycles': 0,
            'instructions': 0,
            'cache_misses': 0,
            'timestamps': []
        })
        self.start_time = None
        self.end_time = None
        self.function_name = None
        
        # Energy conversion constants (configurable)
        self.JOULES_PER_CYCLE = 2e-11      # 20 picojoules per cycle
        self.CACHE_MISS_PENALTY = 5e-12    # 5 picojoules per cache miss
        self.INSTRUCTION_EFFICIENCY = 0.8   # Instructions vs cycles efficiency
        
        print(f"\n==== PURE EBPF ENERGY MONITOR INITIALIZED FOR PROCESS {process_id} ====")
        
    def _process_energy_event(self, cpu, data, size):
        """Process energy events from BPF (NO RAPL)."""
        event = self.bpf["energy_events"].event(data)
        pid = event.pid
        
        # Store ONLY eBPF-based data (NO RAPL)
        self.energy_data[pid]['cpu_cycles'] += event.cpu_cycles
        self.energy_data[pid]['instructions'] += event.instructions
        self.energy_data[pid]['cache_misses'] += event.cache_misses
        self.energy_data[pid]['timestamps'].append(event.timestamp)
        
    def get_energy_data(self):
        """Get energy data calculated PURELY from eBPF performance counters."""
        print("\n==== GETTING PURE EBPF ENERGY DATA ====")
        
        duration = self.end_time - self.start_time if self.end_time and self.start_time else 0
        print(f"Duration: {duration:.2f} seconds")
        
        # Get performance counter data
        process_data = self.energy_data.get(self.process_id, {
            'cpu_cycles': 0,
            'instructions': 0,
            'cache_misses': 0,
            'timestamps': []
        })
        
        cpu_cycles = process_data['cpu_cycles']
        instructions = process_data['instructions']
        cache_misses = process_data['cache_misses']
        
        # PURE eBPF ENERGY CALCULATIONS (NO RAPL)
        
        # Method 1: Basic CPU cycles to energy
        energy_from_cycles = cpu_cycles * self.JOULES_PER_CYCLE
        
        # Method 2: Enhanced calculation with cache misses
        cache_miss_energy = cache_misses * self.CACHE_MISS_PENALTY
        
        # Method 3: Instruction-based efficiency adjustment
        if cpu_cycles > 0:
            ipc = instructions / cpu_cycles  # Instructions per cycle
            efficiency_factor = min(ipc * self.INSTRUCTION_EFFICIENCY, 1.0)
        else:
            efficiency_factor = 1.0
            
        # Total energy calculation
        total_energy = energy_from_cycles + cache_miss_energy
        adjusted_energy = total_energy * efficiency_factor
        
        # Estimate package vs cores distribution (since we don't have RAPL)
        # Assume cores consume 70% of total energy, package overhead is 30%
        cores_energy = adjusted_energy * 0.7
        pkg_energy = adjusted_energy  # Total package energy
        core_percentage = 0.7  # Fixed ratio without RAPL
        
        # Create result dictionary (NO RAPL VALUES)
        result = {
            'energy': {
                'pkg': pkg_energy,
                'cores': cores_energy,
                'core_percentage': core_percentage,
                'cpu_cycles': cpu_cycles,
                'instructions': instructions,
                'cache_misses': cache_misses,
                'energy_from_cycles': energy_from_cycles,
                'cache_miss_energy': cache_miss_energy,
                'efficiency_factor': efficiency_factor,
                'total_adjusted_energy': adjusted_energy
            },
            'duration': duration,
            'source': 'pure_ebpf'  # Changed source identifier
        }
        
        print(f"✅ Pure eBPF energy calculation:")
        print(f"  CPU Cycles: {cpu_cycles:,}")
        print(f"  Instructions: {instructions:,}")
        print(f"  Cache Misses: {cache_misses:,}")
        print(f"  Energy from cycles: {energy_from_cycles:.6f} J")
        print(f"  Cache miss penalty: {cache_miss_energy:.6f} J")
        print(f"  Efficiency factor: {efficiency_factor:.3f}")
        print(f"  Total adjusted energy: {adjusted_energy:.6f} J")
        print(f"  Package energy: {pkg_energy:.6f} J")
        print(f"  Cores energy: {cores_energy:.6f} J")
        
        return result
