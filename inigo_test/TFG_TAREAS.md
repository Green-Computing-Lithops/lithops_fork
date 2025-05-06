








# DISTRIBUCION DE LAS TAREAS TFG: 

## SEMANA 1 (07/02/2025): Viaje a tarragona
1. Instalar lithops y entender el funcionamiento
2. Presentacion de la idea Green computing
3. Diseno del modelo inicial

## SEMANA 2 (28/02/2025): 
1. Introducir valor aleatorio medicion de energia 
2. Dentro del handler, ver jobs alternativos

## SEMANA 3 (7/03/2025): 
1. Explorar alternativas de medicion de energia 
2. Valorar 

## SEMANA 4 (14/03/2025):

### ENERGIA:
1. Alternatively, you could use a different approach for measuring energy consumption that doesn't require sudo, such as using the RAPL interface directly through sysfs.
2. functions --> entornos que se pueda ejecutar perf o no + rapl
    - Esquema de procesadores : conocer procesador & ver si se puede ejecutar perf
    - Condicional para establecer metodo de calculo lithops directamente
        * De momento hacemos comparativa de todos los metodos: TDP / RAPL / PERF
3. Testear con algunos ejemplos de aplicaciones lithops: 
    - https://github.com/lithops-cloud/applications/blob/master/montecarlo/pi_estimation/pi_estimation.ipynb
    - https://github.com/lithops-cloud/applications/blob/master/mandelbrot/example_mandelbrot.ipynb




## SEMANA 5 (21/03/2025): 

### PARALELISMO: 
1. medir que paralelismo se ejecuta con menos energia 
    - kpi : optimizacion kpi estimator --> optimizar para energia en local 

2. Extraccion de multiples datos para ver que paralelismo da menos consumo energetico 
    - plot graph ( x niveles paralelismo y energy consumption)

3. Diseno y analisis de los datos de energia para diferentes niveles de paralelismo --> crear problema optimizable 
- x paralelismo:  map_instances 
- y energia:  ver que paralelismo menos energia da 

4. Obtener datos (evitar dependencia de entorno de ejecucion):  
    * pi estimation
    * airbnb 
    * paralel mandelbrot 
    * stock prediction


### ELEMENTOS A INTEGRAR 
- perf: media vs suma 
- detectar rapl con lithops
- Separar codigo energia del handler 
 

### DATABASE TDP: (agg energia Crear base de datos : Firebase + Scraper + N8N diario --> calculos directas ) 
* fuentes de datos de tdp maquinas de computacion mas comunes
* maquina EC2: uso cpu +  funcion --> maquinas de instancias virtuales : 
* Github: Extraer procesadores  
* Postgres: generar base de datos 
    - Generar API:
    - Valores null 
    -  


### LISTA DE IDEAS: 
1. Diferencia energia de lithops vs nativo  1 processor--> plot  
2. guardar la energia: decir en que maquina es mas eficiente ejecutar metabolomica 



## SEMANA 6 (28/03/2025):  fiesta major => Manri se complica 



## SEMANA 7: viernes 4 no reunion 



# reunion: 
virtualizaciones sobre maquinas --> caso de que tiene no tienes acceso a rapl
* no RAPL

baremetal: rapl --> nadie mas ejecutando el servidor 
* worker vs funcion: 
worker: unidad logica que te permite ejecurar una funcion dentro 

worker puede pasar que todas las funciones se estan ejecutando 
4 maquinas virtuales --> 4 worker --> 100 funciones --> cada una de las 25 funciones 
TDP --> energia de todo el host / no de la funcion completa 
* formula computo total y dividir por numero de funciones que tiene el worker 
* consumo energia funcion de pipeline --> 
* practica valores agregados --> llamada de workers paralelos --


PASO POSTERIOR:
optimizar por pipelines 
por detras: algoritmo de normalizacion de datos comparativa ejecuciones pasadas 

comparar : algoritmo de normalizacion en base de lo que ha pasado anterior 


# MANRI : 
1. Minio: plataforma de objet storage de codigo abierto --> docker --> hacer pruebas 
    * ejecutar deployment de minio en local con docker --> chagpt en un unico comando 
    * flexecutor --> ejecutar 
2. flexecutor: plataforma jolteon --> adaptar / plataforma estructurada donde queda mas facil llevar a cabo operaciones 
    - profiling: pi_montecarlo --> directiva que permite lanzar pipeline de ejecucion con diferentes configuraciones 
    - output guarda ejecucion de tiempo de ejecucion : 
    - Trainign que permite tomar estos profiling --> entrenar modelos predictivos que nos pueden recomendar las mejora de los tiempos futuros --> predicting 
    - Accesso manri : finales de verano / algun bug --> ajustes --> preguntar 

3. Predicting: que ejecucion tiene el menor coste, introducir la menor parte de la energia 
* deployment de minio --> lanzar en local los casos de uso 
- link con todos los datos para poder lanzar los pipelines 

mini: ejemplos -- dag_execurion 
dag_profiling.py : importante --> lo mas encapsulada posible stages de computacione y ejecutan todas un mismo codigo 


con flexecutor: tener el ciclo cerrado que sea end to end 
* sintaxis de 
despues de ejecucion de profiling --> tiempo y ejecuciones 
* cuando tengamos eso vemos como optimizar --> tener ahi la energia 
* discriminador para cual optimizar cada approach ? 
flexecutor: TDP / rapl --> cuando escriba las diferentes metricas escriba tambien las metricas de energia 
flexecutor: ofrecer de manera clara smart provisioning que lithops no ofrece
lithops ofrece las capacidades , pero sin la nocion de optimizacion 
libreria
* aportar las directrivas de optimizacion
* optimizar los resultados de optimizacion 
cuando ejecutamos --> nos explica como funciona cada uno para 

iteraciones que cada una hace diferencte --> explicar jolteon 
tiempo / energia / 
def optimize(self): --> optimiza el pipeline con todos los predict que tiene y coge las opciones que mas te favorece 


punto clave esta semans 
dag_profiling : 
hito bastante guay y hacer la optimizacion real -> cloud -> cargas interesantes -> opciones reales 


# conexion para hacer el end to end 
en funcion de los resultados que existen 
* todos los papers de jolteon los optimicemos por energia --> ml / nl / video 
* listos para lanzar 

TFG 
jolteon : 
reiterar sobre algo existente 

tfm: 
pensar despues para tener un valor nuevo --> las piensas cuando ya tienes un resultado 
con iterar con un algorimo nuevo --> tfm 

32 paginas : experiencia no copypaste 
no pages 
secciones con hablar con ciertos elementos 
tfg documento --> claro
super conciso --> primer nivel 12 paginas de maximo nivel --> 
estructura tfg resultadista --> anexo lo que sea 

minimo integracion flexecutor y caso optimizacion maximo 

preguntar jolteon : 

mas facil introducirse si esta poco explotado 
estas cargando con trabajo de manri y german --> no les hagas perder el tiempo 








 # prompt : 
 im creating a library using minion as a base, the library is in the path flexecutor-main, inside it i have 

 al ejecutar el profile tenemos un output de la energia 


 
 change the flexecutor-main/flexecutor/workflow/executor.py  --> profile funtion to storage the energy consumption and include in the json output keeping the format of 



 # Extensions : 
 Augment
 



















"""
general in 
Simple Lithops example using the map_reduce method.

In this example the map_reduce() method will launch one
map function for each entry in 'iterdata', and then it will
wait locally for the reduce result.

RUN WITH SUDO:

sudo env "PATH=$PATH" "PYTHONPATH=$PYTHONPATH" /home/bigrobbin/Desktop/TFG/venv/bin/python3 inigo_test/general_test_map_reduce.py


previous
cd inigo_test/

"""


codigo general 

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


Te falta ver pq el log se guarda aqui: 
cat /tmp/lithops-root/logs/12acd6-0-M000.log
 
