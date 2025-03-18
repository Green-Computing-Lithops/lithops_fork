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
    print(f"Total Energy: {future.stats.get('worker_func_energy_cpu_percent', 'N/A')}")
    print(f"Total Energy: {future.stats.get('worker_func_total_energy', 'N/A')}") # perf default


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

-- funciona  calculo base: 
* lithops vs local --> energia cambia --> 


-- perf : 
storage de los valores --> al finalizar el proceso 
calculo general 

timeout --> parar el cpu 


Average vs suma: calculo 
- empiezan a coincidir valores perf  --> 


/* RAPL low level : german no necesario */

GERMAN: 
functions --> entornos que se pueda ejecutar perf o no 
- que detecte directamentes --> si existe directamente 
- que lo haga lithosp no tu en terminal --> extraer RAPL --> method: TDP / RAPL / PERF
+ agg energia : 

fuentes de datos de tdp maquinas de computacion mas comunes --> 
uso cpu + maquina EC2 --> funcion --> maquinas de instancias virtuales : 


Crear base de datos : Firebase + Scraper + N8N diario --> calculos directas 

guardar la energia:

-- decir en que maquina es mas eficiente ejecutar metabolomica 


MAP de lithops --> energia total por todas las funciones 
 --> una applicacion de lithos 

medir que paralelismo se ejecuta con menos energia 
--> kpi : optimizacion kpi estimator --> optimizar para energia en local 
--> Codigo de ejemplo : 

ver que paralelismo da menos consumo energetico 
* plot graph ( x niveles paralelismo / y energy consumption)

MANRI:

https://github.com/lithops-cloud/applications/blob/master/montecarlo/pi_estimation/pi_estimation.ipynb
https://github.com/lithops-cloud/applications/blob/master/mandelbrot/example_mandelbrot.ipynb



perf: media vs suma 
detectar rapl o no 
analisis energia graph plot --> paralelismos ( x niveles paralelismo / y energy consumption)
--> analisis energetico --> 


base de datos CPU: 
https://www.cpu-world.com/CPUs/Xeon/Intel-Xeon%208275CL.html
https://www.cpu-world.com/CPUs/SoC.html


POWERAPI EXTRA: 

https://blog.theodo.com/2020/09/power-api-deep-dive/

https://www.sciencedirect.com/science/article/pii/S1389128624002032





AWS services migrando a AMD: 
https://d1.awsstatic.com/events/Summits/nycsummit2023/PRT208-S_AMD_CostOptimizedScaling_E1_20230712_HCEdited.pdf



ya han hablado de crear un dataset: 
https://www.apiscene.io/sustainability/building-an-aws-ec2-carbon-emissions-dataset/

On modern Intel CPUs, we have access to RAPL, Running Average Power Limit, an interface that gives access to a set of counters, giving energy and power consumption information. Using Turbostat, a tool by Intel, we can get the CPU TDP (Thermal Design Power). According to Intel, it refers to the power consumption under the maximum theoretical load. So it’s supposed to be the maximum sustainable power consumption for the CPU. This is especially useful because, on AWS, we use custom-made CPUs, which means that even if we can get the CPU model using a simple LS CPU comment on the terminal, we will never find any public information about this CPU model online. But most importantly, the tool gives us access to the CPU’s power consumption and the machine’s memory.
* Turbostat, a tool by Intel, we can get the CPU TDP (Thermal Design Power).

El tio sigue con el dataset: 
https://medium.com/teads-engineering/building-an-aws-ec2-carbon-emissions-dataset-3f0fd76c98ac

ha montado una base de datoas: 
https://doc.api.boavizta.org/getting_started/cpu_component/
https://docs.google.com/spreadsheets/d/1DqYgQnEDLQVQm5acMAhLgHLD8xXCG9BIrk-_Nv6jF3k/edit?gid=224728652#gid=224728652
estimator: 

https://medium.com/@benjamin.davy



You need to identify make and model of as much of the hardware as you can. Things that consume electricity such as the CPU, chipset/motherboard, and the power supply unit (or its equivalent). I presume you are talking about EC2. If you log into a Linux EC2, try the command "lshw." It will list hardware info. Also, search for "linux list hardward" for more commands. Then the manufacturer of each subcomponent should have datasheets that detail the power requirements of its products



https://sustainability.aboutamazon.com/products-services/aws-cloud



antiguo pero bueno: https://medium.com/teads-engineering/evaluating-the-carbon-footprint-of-a-software-platform-hosted-in-the-cloud-e716e14e060c






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



Alternatively, you could use a different approach for measuring energy consumption that doesn't require sudo, such as using the RAPL interface directly through sysfs.
















sqlite3 /home/bigrobbin/Desktop/TFG/lithops/energy_consumption.db <<EOF
.headers on
.mode column
SELECT * FROM energy_consumption;
EOF


"""
