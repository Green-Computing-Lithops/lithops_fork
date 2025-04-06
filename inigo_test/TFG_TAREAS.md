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








