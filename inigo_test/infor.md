# commands: 
sudo apt-get install linux-tools-common linux-tools-generic linux-tools-`uname -r`
sudo python3 inigo_test/perf_alternative_powerapi.py


I see the issue now! The error is coming from the perf command not recognizing the energy-ram event, even though it does recognize energy-pkg and energy-cores. Let me fix the script to use only the available energy counters on your system.