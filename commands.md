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