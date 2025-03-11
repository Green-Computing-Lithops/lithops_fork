"""
Simple Lithops example using the map_reduce method.

In this example the map_reduce() method will launch one
map function for each entry in 'iterdata', and then it will
wait locally for the reduce result.
"""
import pprint
import lithops
import time

iterdata = [1, 2, 3, 4, 5]

def my_map_function(x):
    print(f"Processing input: {x}")
    print(f"MAP FUNCITOPM ")
    time.sleep(x * 2)
    return x + 7


def my_map_function_costly(x):
    print(f"Processing input: {x}")
    print(f"MAP FUNCTION ")
    
    # CPU-intensive operations to consume energy
    result = x

    # Calculate prime numbers (very CPU intensive)
    for i in range(1, 50 ** x): # 500000 ** x --> abortamos mision 5050505050
        # Check if i is prime using trial division
        if i > 1:
            for j in range(2, int(i**0.5) + 1): #optimiza la division --> 1/2 
                if i % j == 0:
                    break
            else:
                # This is a prime number, do some work with it
                result = (result + i) % 10000000
    
    return result


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
    fexec.map_reduce(my_map_function, iterdata, my_reduce_function)
    print(fexec.get_result())
 

    print("Async call SLEEP function")
    fexec = lithops.FunctionExecutor()
    future = fexec.call_async(my_map_function, 3)
    result = fexec.get_result(fs=[future]) # leng --> return list of parameters 
    # pprint.pprint(future.stats)


    # Print only the three specific metrics
    print("SLEEP function metrics:")
    print(f"CPU User Time: {future.stats.get('worker_func_cpu_user_time', 'N/A')}")
    print(f"CPU Usage Average: {future.stats.get('worker_func_avg_cpu_usage', 'N/A')}")
    print(f"Energy Consumption: {future.stats.get('worker_func_energy_consumption', 'N/A')}")

    print("\nAsync call COSTLY function")
    fexec = lithops.FunctionExecutor()
    future = fexec.call_async(my_map_function_costly, 3)
    result = fexec.get_result(fs=[future]) # leng --> return list of parameters 
    # pprint.pprint(future.stats)
    
    # Print only the three specific metrics
    print("COSTLY function metrics:")
    print(f"CPU User Time: {future.stats.get('worker_func_cpu_user_time', 'N/A')}")
    print(f"CPU Usage Average: {future.stats.get('worker_func_avg_cpu_usage', 'N/A')}")
    print(f"Energy Consumption: {future.stats.get('worker_func_energy_consumption', 'N/A')}")



"""

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