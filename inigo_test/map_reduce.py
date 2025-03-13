"""
Simple Lithops example using the map_reduce method.

In this example the map_reduce() method will launch one
map function for each entry in 'iterdata', and then it will
wait locally for the reduce result.

RUN WITH SUDO:

sudo env "PATH=$PATH" /home/bigrobbin/Desktop/TFG/lithops/venv/bin/python3 inigo_test/map_reduce.py

sudo env "PATH=$PATH" /home/bigrobbin/Desktop/TFG/lithops/venv/bin/python3 inigo_test/map_reduce.py



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


if __name__ == "__main__":
 

    # creates an instance of Lithops’ FunctionExecutor --> localhost & manage 
    fexec = lithops.FunctionExecutor() 

    #  executor distributes the my_map_function across the items in iterdata
    # The my_reduce_function is set to combine the results of the map phase.
    fexec.map_reduce(sleep_function, iterdata, my_reduce_function)
    print(fexec.get_result())
 

    print("Async call SLEEP function")
    fexec = lithops.FunctionExecutor()
    future = fexec.call_async(sleep_function, 3)
    result = fexec.get_result(fs=[future]) # leng --> return list of parameters 
    # pprint.pprint(future.stats)


    # Print only the three specific metrics
    print("SLEEP function metrics:")
    print(f"CPU User Time: {future.stats.get('worker_func_cpu_user_time', 'N/A')}")
    print(f"CPU Usage Average: {future.stats.get('worker_func_avg_cpu_usage', 'N/A')}")
    print(f"Energy Consumption: {future.stats.get('worker_func_energy_consumption', 'N/A')}")

    print("\nAsync call COSTLY function")
    fexec = lithops.FunctionExecutor()
    future = fexec.call_async(prime_function, 3)
    print(f"Prime function result: {future.result()}") #max prime 6249989
    result = fexec.get_result(fs=[future]) # leng --> return list of parameters 
    # pprint.pprint(future.stats)
    # added new 
    # print(f"Energy Efficiency: {future.stats.get('worker_func_energy_efficiency', 'N/A')}")
    print(f"Total Energy: {future.stats.get('worker_func_total_energy', 'N/A')}")

    # Print only the three specific metrics
    print("COSTLY function metrics:")
    print(f"CPU User Time: {future.stats.get('worker_func_cpu_user_time', 'N/A')}")
    print(f"CPU Usage Average: {future.stats.get('worker_func_avg_cpu_usage', 'N/A')}")
    print(f"Energy Consumption: {future.stats.get('worker_func_energy_consumption', 'N/A')}")
    
    # added new 
    # print(f"Energy Efficiency: {future.stats.get('worker_func_energy_efficiency', 'N/A')}")
    print(f"Total Energy: {future.stats.get('worker_func_energy_cpu_percent', 'N/A')}")



"""
Basics results :
initial results: 

SLEEP function metrics:
CPU User Time: 12162.92
CPU Usage Average: 2.414285714285714
Energy Consumption: 29364.764



COSTLY function metrics:
CPU User Time: 12163.19
CPU Usage Average: 6.464285714285714
Energy Consumption: 78626.33535714286


"""