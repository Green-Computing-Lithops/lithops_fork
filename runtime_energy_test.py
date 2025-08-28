 
import lithops
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'energy_documentation'))
from standarized_measurement_functions import sleep_function, prime_function

def print_corrected_energy_summary(future, function_name):
    """Print energy summary in a simple table format."""
    
    print(f"\n{'='*60}")
    print(f"🔋 ENERGY SUMMARY FOR: {function_name.upper()}")
    print(f"{'='*60}")
    
    # Basic execution info
    duration = future.stats.get('worker_func_energy_duration', 0.0)
    cpu_usage = future.stats.get('worker_func_avg_cpu_usage', 0.0)
    energy_method = future.stats.get('worker_func_energy_method_used', 'unknown')
    
    print(f"⏱️  Execution Duration: {duration:.3f} seconds")
    print(f"🖥️  Average CPU Usage: {cpu_usage:.2f}%")
    print(f"🔧 Energy Method Used: {energy_method}")
    
    # PERF metrics
    perf_energy_pkg = future.stats.get('worker_func_perf_energy_pkg', 0.0)
    perf_energy_cores = future.stats.get('worker_func_perf_energy_cores', 0.0)
    perf_energy_total = future.stats.get('worker_func_perf_energy_total', 0.0)
    perf_source = future.stats.get('worker_func_perf_source', 'unavailable')
    perf_available = future.stats.get('worker_func_perf_available', False)
    
    # RAPL metrics
    rapl_energy_pkg = future.stats.get('worker_func_rapl_energy_pkg', 0.0)
    rapl_energy_cores = future.stats.get('worker_func_rapl_energy_cores', 0.0)
    rapl_energy_total = future.stats.get('worker_func_rapl_energy_total', 0.0)
    rapl_source = future.stats.get('worker_func_rapl_source', 'unavailable')
    rapl_available = future.stats.get('worker_func_rapl_available', False)
    
    # eBPF metrics
    ebpf_energy_pkg = future.stats.get('worker_func_ebpf_energy_pkg', 0.0)
    ebpf_energy_cores = future.stats.get('worker_func_ebpf_energy_cores', 0.0)
    ebpf_energy_total = future.stats.get('worker_func_ebpf_energy_total', 0.0)
    ebpf_cpu_cycles = future.stats.get('worker_func_ebpf_cpu_cycles', 0.0)
    ebpf_energy_from_cycles = future.stats.get('worker_func_ebpf_energy_from_cycles', 0.0)
    ebpf_source = future.stats.get('worker_func_ebpf_source', 'unavailable')
    ebpf_available = future.stats.get('worker_func_ebpf_available', False)
    
    # PSUtil metrics - using correct field names from energy manager
    psutil_cpu_usage = future.stats.get('worker_func_avg_cpu_usage', 0.0)
    psutil_memory_usage = future.stats.get('worker_func_psutil_memory_used_mb', 0.0)  # Corrected field name
    psutil_cpu_freq = future.stats.get('worker_func_psutil_cpu_freq_current', 0.0)  # Corrected field name
    psutil_cpu_temp = future.stats.get('worker_func_psutil_cpu_temp_celsius', 0.0)  # Corrected field name
    psutil_cpu_cores_physical = future.stats.get('worker_func_psutil_cpu_cores_physical', 0)  # Corrected field name
    psutil_cpu_cores_logical = future.stats.get('worker_func_psutil_cpu_cores_logical', 0)  # Added logical cores
    psutil_available = True  # PSUtil is always available

    # Print all metrics in a simple table format
    print(f"\n📊 ALL ENERGY METRICS TABLE:")
    print(f"{'Metric Name':<40} {'Value':<20}")
    print(f"{'-'*60}")
    
    # PERF metrics
    print(f"{'worker_func_perf_energy_pkg':<40} {perf_energy_pkg:<20.3f}")
    print(f"{'worker_func_perf_energy_cores':<40} {perf_energy_cores:<20.3f}")
    print(f"{'worker_func_perf_energy_total':<40} {perf_energy_total:<20.3f}")
    print(f"{'worker_func_perf_source':<40} {perf_source:<20}")
    print(f"{'worker_func_perf_available':<40} {perf_available:<20}")
    print(f"{'-'*60}")   
    
    # RAPL metrics
    print(f"{'worker_func_rapl_energy_pkg':<40} {rapl_energy_pkg:<20.3f}")
    print(f"{'worker_func_rapl_energy_cores':<40} {rapl_energy_cores:<20.3f}")
    print(f"{'worker_func_rapl_energy_total':<40} {rapl_energy_total:<20.3f}")
    print(f"{'worker_func_rapl_source':<40} {rapl_source:<20}")
    print(f"{'worker_func_rapl_available':<40} {rapl_available:<20}")
    print(f"{'-'*60}")
    
    # eBPF metrics
    print(f"{'worker_func_ebpf_energy_pkg':<40} {ebpf_energy_pkg:<20.3f}")
    print(f"{'worker_func_ebpf_energy_cores':<40} {ebpf_energy_cores:<20.3f}")
    print(f"{'worker_func_ebpf_energy_total':<40} {ebpf_energy_total:<20.3f}")
    print(f"{'worker_func_ebpf_cpu_cycles':<40} {ebpf_cpu_cycles:<20.0f}")
    print(f"{'worker_func_ebpf_energy_from_cycles':<40} {ebpf_energy_from_cycles:<20.3f}")
    print(f"{'worker_func_ebpf_source':<40} {ebpf_source:<20}")
    print(f"{'worker_func_ebpf_available':<40} {ebpf_available:<20}")
    print(f"{'-'*60}")
    
    # PSUtil metrics
    print(f"{'worker_func_avg_cpu_usage':<40} {psutil_cpu_usage:<20.2f}")
    print(f"{'worker_func_psutil_cpu_percent':<40} {future.stats.get('worker_func_psutil_cpu_percent', 0.0):<20.2f}")
    print(f"{'worker_func_psutil_process_cpu_percent':<40} {future.stats.get('worker_func_psutil_process_cpu_percent', 0.0):<20.2f}")
    
    # Per-CPU percentage arrays - individual CPU core usage
    per_cpu_initial = future.stats.get('worker_func_psutil_per_cpu_initial', [])
    per_cpu_final = future.stats.get('worker_func_psutil_per_cpu_final', [])
    per_cpu_average = future.stats.get('worker_func_psutil_per_cpu_average', [])
    
    print(f"{'worker_func_psutil_per_cpu_initial':<40} {str(per_cpu_initial):<20}")
    print(f"{'worker_func_psutil_per_cpu_final':<40} {str(per_cpu_final):<20}")
    print(f"{'worker_func_psutil_per_cpu_average':<40} {str(per_cpu_average):<20}")
    
    # Additional detailed CPU metrics
    cpu_percent_initial = future.stats.get('worker_func_psutil_cpu_percent_initial', 0.0)
    cpu_percent_final = future.stats.get('worker_func_psutil_cpu_percent_final', 0.0)
    cpu_percent_avg_initial = future.stats.get('worker_func_psutil_cpu_percent_avg_initial', 0.0)
    cpu_percent_avg_final = future.stats.get('worker_func_psutil_cpu_percent_avg_final', 0.0)
    cpu_percent_max_initial = future.stats.get('worker_func_psutil_cpu_percent_max_initial', 0.0)
    cpu_percent_max_final = future.stats.get('worker_func_psutil_cpu_percent_max_final', 0.0)
    
    print(f"{'worker_func_psutil_cpu_percent_initial':<40} {cpu_percent_initial:<20.2f}")
    print(f"{'worker_func_psutil_cpu_percent_final':<40} {cpu_percent_final:<20.2f}")
    print(f"{'worker_func_psutil_cpu_percent_avg_initial':<40} {cpu_percent_avg_initial:<20.2f}")
    print(f"{'worker_func_psutil_cpu_percent_avg_final':<40} {cpu_percent_avg_final:<20.2f}")
    print(f"{'worker_func_psutil_cpu_percent_max_initial':<40} {cpu_percent_max_initial:<20.2f}")
    print(f"{'worker_func_psutil_cpu_percent_max_final':<40} {cpu_percent_max_final:<20.2f}")
    
    print(f"{'worker_func_psutil_memory_used_mb':<40} {psutil_memory_usage:<20.2f}")
    print(f"{'worker_func_psutil_cpu_freq_current':<40} {psutil_cpu_freq:<20.0f}")
    print(f"{'worker_func_psutil_cpu_temp_celsius':<40} {psutil_cpu_temp:<20.1f}")
    print(f"{'worker_func_psutil_cpu_cores_physical':<40} {psutil_cpu_cores_physical:<20}")
    print(f"{'worker_func_psutil_cpu_cores_logical':<40} {psutil_cpu_cores_logical:<20}")
    print(f"{'worker_func_psutil_available':<40} {psutil_available:<20}")
    print(f"{'-'*60}")
    

def main():
 
    
    # Test 1: Sleep Function
    print("\n📋 Testing Sleep Function...")
    fexec = lithops.FunctionExecutor()
    sleep_future = fexec.call_async(sleep_function, 2)
    sleep_result = fexec.get_result(fs=[sleep_future])
    print(f"✅ Sleep function result: {sleep_result}")
    
    print_corrected_energy_summary(sleep_future, "sleep_function")
    
    # Test 2: Prime Function
    print("\n📋 Testing Prime Function...")
    fexec = lithops.FunctionExecutor()
    prime_future = fexec.call_async(prime_function, 2)
    prime_result = fexec.get_result(fs=[prime_future])
    print(f"✅ Prime function result: {prime_result}")
    
    print_corrected_energy_summary(prime_future, "prime_function")
    
 

if __name__ == "__main__":
    main()
