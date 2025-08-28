ssh iarriazu@cloudfunctions.urv.cat


ssh -N -L 44444:storage4-10Gbit:9001iarriazu@cloudfunctions.urv.cat

ssh -o IdentitiesOnly=yes -i ~/.ssh/id_rsa iarriazu@cloudfunctions.urv.cat

change the priv key permisions to solve permision : 
chmod 600 ~/.ssh/id_rsa

# ssh config: 
# Read more about SSH config files: https://linux.die.net/man/5/ssh_config
Host urv-server
    HostName cloudfunctions.urv.cat
    User iarriazu
    IdentityFile ~/.ssh/id_rsa

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# for running rapl: 
```bash
sudo -E env PATH="/home/minirobbin/Desktop/GreenComputing/flexecutor-main/venv310/bin:$PATH" /home/minirobbin/Desktop/GreenComputing/flexecutor-main/venv310/bin/python runtime_energy_test.py
```

### __nergy Efficiency Analysis__

- __Sleep Function__: Higher total energy (450.8J) due to longer duration (6.77s) but lower power (~66.6W average)
- __Prime Function__: Lower total energy (238.7J) with shorter duration (4.06s) but higher power (~58.7W average)
- __Core vs Package__: Cores consume ~1.7x more energy than package measurements, indicating high core utilization

### __Command for Future Use__

```bash
sudo -E env PATH="/home/minirobbin/Desktop/GreenComputing/flexecutor-main/venv310/bin:$PATH" /home/minirobbin/Desktop/GreenComputing/flexecutor-main/venv310/bin/python runtime_energy_test.py
```

### __Alternative Solutions for Production__

For regular use without sudo, consider:

```bash
# Fix permissions permanently
sudo chmod 644 /sys/class/powercap/intel-rapl*/energy_uj
sudo chmod 644 /sys/class/powercap/intel-rapl*/intel-rapl*/energy_uj
```

__RAPL energy monitoring is now fully functional and providing accurate hardware-level energy measurements!__ 🚀


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# perf values: 
sudo apt update && sudo apt install linux-tools-6.14.0-28-generic linux-cloud-tools-6.14.0-28-generic


# EBPF : 
grep -i ebpf /tmp/lithops-minirobbin/logs/54e1e0-0-A000.log

==== EBPF ENERGY MONITOR INITIALIZED FOR PROCESS 675393 ====
==== STARTING EBPF ENERGY MONITORING ====
2025-08-29 00:11:15,456 [WARNING] energymanager.py:98 -- Failed to start ebpf energy monitor


sudo -n echo "test" 2>/dev/null || echo "No sudo access"

recomended: 
sudo python3 runtime_energy_test.py


```bash
sudo -E venv310/bin/python runtime_energy_test.py
```
cd /home/minirobbin/Desktop/GreenComputing/lithops_fork && sudo -E PATH=$PATH:$(pwd)/venv310/bin $(pwd)/venv310/bin/python runtime_energy_test.py




sudo -E PATH=$PATH:$(pwd)/venv310/bin $(pwd)/venv310/bin/python runtime_energy_test.py
 

 cd /home/minirobbin/Desktop/GreenComputing/lithops_fork && sudo -E PATH=$PATH:$(pwd)/venv310/bin LITHOPS_CONFIG_FILE=/home/minirobbin/Desktop/GreenComputing/lithops_fork/localhost.yaml $(pwd)/venv310/bin/python runtime_energy_test.py


 # Energy working 
 cd /home/minirobbin/Desktop/GreenComputing/lithops_fork && sudo -E PATH=$PATH:$(pwd)/venv310/bin LITHOPS_CONFIG_FILE=/home/minirobbin/Desktop/GreenComputing/lithops_fork/localhost.yaml $(pwd)/venv310/bin/python runtime_energy_test.py




============================================================
🔋 ENERGY SUMMARY FOR: PRIME_FUNCTION
============================================================
⏱️  Execution Duration: 2.267 seconds
🖥️  Average CPU Usage: 57.98%
🔧 Energy Method Used: perf, rapl, ebpf, psutil

📊 ALL ENERGY METRICS TABLE:
Metric Name                              Value               
------------------------------------------------------------
worker_func_perf_energy_pkg              29.020              
worker_func_perf_energy_cores            24.810              
worker_func_perf_energy_total            53.830              
worker_func_perf_source                  perf                
worker_func_perf_available               1                   
------------------------------------------------------------
worker_func_rapl_energy_pkg              56.705              
worker_func_rapl_energy_cores            84.312              
worker_func_rapl_energy_total            141.017             
worker_func_rapl_source                  rapl_direct         
worker_func_rapl_available               1                   
------------------------------------------------------------
worker_func_ebpf_energy_pkg              17.360              
worker_func_ebpf_energy_cores            26.041              
worker_func_ebpf_energy_total            43.401              
worker_func_ebpf_cpu_cycles              978586127           
worker_func_ebpf_energy_from_cycles      43.401              
worker_func_ebpf_source                  ebpf                
worker_func_ebpf_available               1                   
------------------------------------------------------------
worker_func_avg_cpu_usage                57.98               
worker_func_psutil_cpu_percent           74.60               
worker_func_psutil_process_cpu_percent   94.90               
worker_func_psutil_per_cpu_initial       [40.2, 61.5, 54.6, 43.2, 41.5, 46.3, 64.7, 43.2]
worker_func_psutil_per_cpu_final         [40.1, 40.1, 38.4, 37.0, 74.6, 40.0, 37.2, 37.7]
worker_func_psutil_per_cpu_average       [40.150000000000006, 50.8, 46.5, 40.1, 58.05, 43.15, 50.95, 40.45]
worker_func_psutil_cpu_percent_initial   63.10               
worker_func_psutil_cpu_percent_final     33.20               
worker_func_psutil_cpu_percent_avg_initial 49.40               
worker_func_psutil_cpu_percent_avg_final 43.14               
worker_func_psutil_cpu_percent_max_initial 64.70               
worker_func_psutil_cpu_percent_max_final 74.60               
worker_func_psutil_memory_used_mb        19382.33            
worker_func_psutil_cpu_freq_current      2800                
worker_func_psutil_cpu_temp_celsius      63.0                
worker_func_psutil_cpu_cores_physical    4                   
worker_func_psutil_cpu_cores_logical     8                   
worker_func_psutil_available             1                   
--------------------------------------------



