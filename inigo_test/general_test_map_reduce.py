"""
Simple Lithops example using the map_reduce method.

In this example the map_reduce() method will launch one
map function for each entry in 'iterdata', and then it will
wait locally for the reduce result.

RUN WITH SUDO:

sudo env "PATH=$PATH" /home/bigrobbin/Desktop/TFG/lithops/venv/bin/python3 inigo_test/map_reduce.py

sudo env "PATH=$PATH" /home/bigrobbin/Desktop/TFG/lithops/venv/bin/python3 inigo_test/map_reduce.py


previous
cd inigo_test/

"""
import pprint
import lithops
from standarized_measurement_functions import sleep_function, prime_function

# iterdata = [1, 2, 3, 4, 5]

iterdata = [2]


def my_reduce_function(results):
    total = 0
    for map_result in results:
        total = total + map_result
    return total

def print_stats(future):

    print(f"CPU User Time: {future.stats.get('worker_func_cpu_user_time', 'N/A')}")
    print(f"CPU Usage Average: {future.stats.get('worker_func_avg_cpu_usage', 'N/A')}")
    print(f"Energy Consumption: {future.stats.get('worker_func_energy_consumption', 'N/A')}")
    
    # PERF: added new 
    # print(f"Energy Efficiency: {future.stats.get('worker_func_energy_efficiency', 'N/A')}")
    print(f"Perf CPU Percentage: {future.stats.get('worker_func_energy_cpu_percent', 'N/A')}")

    print(f"Perf Energy: {future.stats.get('worker_func_perf_energy', 'N/A')}")
    print(f"Perf Energy pkg: {future.stats.get('worker_func_perf_energy_pkg', 'N/A')}")
    print(f"Perf Energy cores: {future.stats.get('worker_func_perf_energy_cores', 'N/A')}")
 



if __name__ == "__main__":
 

    # creates an instance of Lithops’ FunctionExecutor --> localhost & manage 
    fexec = lithops.FunctionExecutor() 

    #  executor distributes the my_map_function across the items in iterdata
    # The my_reduce_function is set to combine the results of the map phase.
    fexec.map_reduce(sleep_function, iterdata, my_reduce_function)
    print(fexec.get_result())
 

    print("Async call SLEEP function")
    fexec = lithops.FunctionExecutor()
    future = fexec.call_async(sleep_function, iterdata[0])
    result = fexec.get_result(fs=[future]) # leng --> return list of parameters 
    # pprint.pprint(future.stats)


    # Print only the three specific metrics
    print("\n\nSLEEP function metrics:")
    print_stats(future)

    print("\n\nAsync call COSTLY function")
    fexec = lithops.FunctionExecutor()
    future = fexec.call_async(prime_function, iterdata[0])
    max_prime_method1 = future.result()                     # needed to wait 
    max_prime_method2 = fexec.get_result(fs=[future])       # needed to wait 
    print(f"Method 1 - future.result(): {max_prime_method1}")
    print(f"Method 2 - fexec.get_result(): {max_prime_method2}")
    print(f"Both methods return the same max prime number: {max_prime_method1 == max_prime_method2}")

    # Print only the three specific metrics
    print("\n\nCOSTLY function metrics:")
    print_stats(future)





"""
Basics results :
initial results: 

SLEEP function metrics:
CPU User Time: 12162.92
CPU Usage Average: 2.414285714285714
Energy Consumption: 29364.764



COSTLY function metrics:
CPU User Time: 12163.19
CPU Usage Average: 6.464285714285714 // suma en vez de caluclo 1600% --> 
Energy Consumption: 78626.33535714286

 







POWERAPI EXTRA: 
https://blog.theodo.com/2020/09/power-api-deep-dive/
https://www.sciencedirect.com/science/article/pii/S1389128624002032





AUX COMMANDS: 
sqlite3 /home/bigrobbin/Desktop/TFG/lithops/energy_consumption.db "SELECT * FROM energy_consumption"
sqlite3 /home/bigrobbin/Desktop/TFG/lithops/energy_consumption.db "SELECT AVG(energy_pkg) FROM energy_consumption"
sqlite3 /home/bigrobbin/Desktop/TFG/lithops/energy_consumption.db "drop table energy_consumption"




-- Get energy consumption by function name
SELECT function_name, AVG(energy_pkg) as avg_energy
FROM energy_consumption
GROUP BY function_name
ORDER BY avg_energy DESC;

-- Get CPU usage patterns for specific functions
SELECT e.function_name, c.cpu_id, AVG(c.cpu_percent) as avg_cpu
FROM energy_consumption e
JOIN cpu_usage c ON e.job_key = c.job_key AND e.call_id = c.call_id
GROUP BY e.function_name, c.cpu_id
ORDER BY e.function_name, c.cpu_id;





sqlite3 /home/bigrobbin/Desktop/TFG/lithops/energy_consumption.db <<EOF
.headers on
.mode column
SELECT * FROM energy_consumption;
EOF




MAP FUNCTION PRIME
MAX PRIME 6249989 

 Performance counter stats for 'system wide':

          1.373,00 Joules power/energy-pkg/                                                     
          1.265,14 Joules power/energy-cores/                                                   

      16,553457859 seconds time elapsed

(venv) bigrobbin@bigrobbin:~/Desktop/TFG/lithops$ cd /home/bigrobbin/Desktop/TFG/lithops && sudo perf stat -e power/energy-pkg/,power/energy-cores/ -a python3 -c "import time; import sys; sys.path.append('/home/bigrobbin/Desktop/TFG/lithops/inigo_test'); from standarized_measurement_functions import sleep_function; sleep_function(4)"
Processing input: 4
MAP FUNCTION SLEEP

 Performance counter stats for 'system wide':

             83,87 Joules power/energy-pkg/                                                     
             30,29 Joules power/energy-cores/                                                   

       8,012292576 seconds time elapsed











"""
