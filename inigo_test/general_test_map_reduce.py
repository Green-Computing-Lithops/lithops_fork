"""
Simple Lithops example using the map_reduce method.

In this example the map_reduce() method will launch one
map function for each entry in 'iterdata', and then it will
wait locally for the reduce result.

RUN WITH SUDO:

sudo env "PATH=$PATH" /home/bigrobbin/Desktop/TFG/lithops/venv/bin/python3 inigo_test/map_reduce.py

sudo env "PATH=$PATH" /home/bigrobbin/Desktop/TFG/venv/bin/python3 lithops_fork/inigo_test/general_test_map_reduce.py

previous
cd inigo_test/

"""
import pprint
import lithops
from standarized_measurement_functions import sleep_function, prime_function

# iterdata = [1, 2, 3, 4, 5]

iterdata = [4]


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
Comparacion de resultados: 6249989



-- TEST 1
SLEEP function metrics:
CPU User Time: 1737.66
CPU Usage Average: 2.810714285714286
Energy Consumption: 4884.065785714286
Perf CPU Percentage: 0.0
Perf Energy: {'pkg': 80.97, 'cores': 29.26, 'total': 110.23}
Perf Energy pkg: 80.97
Perf Energy cores: 29.26


COSTLY function metrics:
CPU User Time: 1757.64
CPU Usage Average: 4.142857142857143
Energy Consumption: 7281.651428571429
Perf CPU Percentage: 0.0
Perf Energy: {'pkg': 887.55, 'cores': 781.07, 'total': 1668.62}
Perf Energy pkg: 887.55
Perf Energy cores: 781.07

-- TEST 2
SLEEP function metrics:
CPU User Time: 1797.43
CPU Usage Average: 4.103571428571429
Energy Consumption: 7375.882392857143
Perf CPU Percentage: 0.0
Perf Energy: {'pkg': 89.28, 'cores': 38.43, 'total': 127.71000000000001}
Perf Energy pkg: 89.28
Perf Energy cores: 38.43

COSTLY function metrics:
CPU User Time: 1821.18
CPU Usage Average: 5.075
Energy Consumption: 9242.488500000001
Perf CPU Percentage: 0.0
Perf Energy: {'pkg': 1248.04, 'cores': 1136.52, 'total': 2384.56}
Perf Energy pkg: 1248.04
Perf Energy cores: 1136.52


-- TEST 3
SLEEP function metrics:
CPU User Time: 1869.18
CPU Usage Average: 4.2
Energy Consumption: 7850.5560000000005
Perf CPU Percentage: 0.0
Perf Energy: {'pkg': 76.69, 'cores': 26.08, 'total': 102.77}
Perf Energy pkg: 76.69
Perf Energy cores: 26.08

COSTLY function metrics:
CPU User Time: 1891.89
CPU Usage Average: 4.867857142857142
Energy Consumption: 9209.450249999998
Perf CPU Percentage: 0.0
Perf Energy: {'pkg': 1229.86, 'cores': 1118.91, 'total': 2348.77}
Perf Energy pkg: 1229.86
Perf Energy cores: 1118.91


after refactoring: 
-- TEST 1
SLEEP function metrics:
CPU User Time: 3731.99
CPU Usage Average: 4.271428571428571
Energy Consumption: 15940.928714285714
Perf CPU Percentage: 0.0
Perf Energy: {'pkg': 80.42, 'cores': 29.64, 'total': 110.06}
Perf Energy pkg: 80.42
Perf Energy cores: 29.64

COSTLY function metrics:
CPU User Time: 3756.44
CPU Usage Average: 5.210714285714286
Energy Consumption: 19573.735571428573
Perf CPU Percentage: 0.0
Perf Energy: {'pkg': 1281.83, 'cores': 1169.28, 'total': 2451.1099999999997}
Perf Energy pkg: 1281.83
Perf Energy cores: 1169.28

-- TEST 2
SLEEP function metrics:
CPU User Time: 3808.64
CPU Usage Average: 4.7749999999999995
Energy Consumption: 18186.255999999998
Perf CPU Percentage: 0.0
Perf Energy: {'pkg': 142.31, 'cores': 91.08, 'total': 233.39}
Perf Energy pkg: 142.31
Perf Energy cores: 91.08

COSTLY function metrics:
CPU User Time: 3830.74
CPU Usage Average: 4.621428571428572
Energy Consumption: 17703.491285714288
Perf CPU Percentage: 0.0
Perf Energy: {'pkg': 1234.27, 'cores': 1119.24, 'total': 2353.51}
Perf Energy pkg: 1234.27
Perf Energy cores: 1119.24

-- TEST 3


SLEEP function metrics:
CPU User Time: 3913.89
CPU Usage Average: 4.867857142857143
Energy Consumption: 19052.257392857144
Perf CPU Percentage: 0.0
Perf Energy: {'pkg': 149.81, 'cores': 93.71, 'total': 243.51999999999998}
Perf Energy pkg: 149.81
Perf Energy cores: 93.71

COSTLY function metrics:
CPU User Time: 3935.84
CPU Usage Average: 4.6571428571428575
Energy Consumption: 18329.769142857145
Perf CPU Percentage: 0.0
Perf Energy: {'pkg': 1207.99, 'cores': 1096.28, 'total': 2304.27}
Perf Energy pkg: 1207.99
Perf Energy cores: 1096.28
"""