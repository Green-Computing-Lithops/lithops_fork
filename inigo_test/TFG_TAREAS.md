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

