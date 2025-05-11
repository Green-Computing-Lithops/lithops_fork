
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# DISTRIBUCION DE LAS TAREAS TFG: 
* discord: https://discord.gg/y5Qe5dHt


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

# 
german: muy importante ejecutar y recopilar no el que 
# plotmap

manri sufi 
varios nodos de distribucion y han cargado los nodos --> experimentos y no funcionan 
# Tareas pendientes
grafo funcionalidad --> diagrama de flujo --> chatgpt / draw.io



# Manri 07/03/2023: 
valores base y heuristica --> estimacion de energia --> links german 
TDP= procesador 65w
porcentaje de uso de cada aplicacion --> primer aproach 

version naive : consultar basicamente 

scrapping a una api -> consumo energia base 
hardcoding --> cambiar por necesario 


# STEPS to follow: 
1. Obtener la energia
    - version basica con tdp --> funcionando 
    - perf: te falta como guardar la informacion 
    - PowerApi: intentamos hasta las 9 --> sino pedimos ayuda
    - Ver como funciona Powerapi y ver alternativas

2. Predictor de carga 


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Debbugger
## solved: 
 .vscode/launch.json

 {
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python no justMyCode",
      "type": "debugpy",
      "request": "launch",
      "purpose": ["debug-test"],
      "program": "${file}",
      "console": "integratedTerminal",
      "justMyCode": false
    }
  ]
}

ctrl + , --> justMyCode --> unselect all 


# run your own model without 
/home/bigrobbin/Desktop/git/lithops_fork/venv/bin/python flexecutor-main/examples/energy_comparison.py

# elementos de la reunion 
comando minio --> contenedor docker object storage != file storage --> almacenamiento object storage 
minio --> subir informacion ahi ( importante para replicar en el futuro --> object storage / no lithops storage --> S3 )
lithops --> bucket localhost / almacenamiento minio --> credenciales docker --> Map a storage ahi 


 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# minio
docker run -d --name minio-server -p 9000:9000 -p 9001:9001 -v /home/bigrobbin/Desktop/git/lithops_fork/test-bucket:/data/test-bucket -e "MINIO_ROOT_USER=minioadmin" -e "MINIO_ROOT_PASSWORD=minioadmin" quay.io/minio/minio server /data --console-address ":9001"


sudo docker run -d --name minio-server -p 9000:9000 -p 9001:9001 -v /home/bigrobbin/Desktop/git/lithops_fork/test-bucket:/data/test-bucket -e "MINIO_ROOT_USER=minioadmin" -e "MINIO_ROOT_PASSWORD=minioadmin" quay.io/minio/minio server /data --console-address ":9001"

sudo docker run -d -p 9000:9000 -p 9001:9001 --name minio quay.io/minio/minio server /data --console-address ":9001"


sudo docker run -d --name minio-server -p 9000:9000 -p 9001:9001 -e "MINIO_ROOT_USER=minioadmin" -e "MINIO_ROOT_PASSWORD=minioadmin" quay.io/minio/minio server /data --console-address ":9001"

# servidor web --> 9001 / api rest 9000 : forwarding de dos puertos --> puerto sw vs api rest  

curl -O https://dl.min.io/client/mc/release/linux-amd64/mc

(venv) bigrobbin@bigrobbin:~/Desktop/git/lithops_fork$ chmod +x mc
(venv) bigrobbin@bigrobbin:~/Desktop/git/lithops_fork$ ./mc alias set myminio http://localhost:9000 minioadmin minioadmin
mc: Configuration written to `/home/bigrobbin/.mc/config.json`. Please update your access credentials.
mc: Successfully created `/home/bigrobbin/.mc/share`.
mc: Initialized share uploads `/home/bigrobbin/.mc/share/uploads.json` file.
mc: Initialized share downloads `/home/bigrobbin/.mc/share/downloads.json` file.
Added `myminio` successfully.
(venv) bigrobbin@bigrobbin:~/Desktop/git/lithops_fork$ ./mc mb myminio/test-bucket

 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# paralelismo

Now I understand how the profiling data is stored. The get_my_exec_path() function returns the path where the flexorchestrator script is located, which is set by the @flexorchestrator() decorator. This path is used as the base path for storing the profiling data.

In the main.py file, the @flexorchestrator(bucket="test-bucket") decorator is used, which sets the base path to the directory where main.py is located, which is flexecutor-main/examples/video.

So the profiling data should be stored in:
flexecutor-main/examples/video/profiling/video/stage0.json
flexecutor-main/examples/video/profiling/video/stage1.json
flexecutor-main/examples/video/profiling/video/stage2.json
flexecutor-main/examples/video/profiling/video/stage3.json



# elements to solve the error 
        //     "(cpu 1, mem, worker 2)": { 
        //     "(cpu 4, mem, worker 4)": {
        //     "(cpu 8, mem, worker 8)": {
        //     "(cpu 8, mem, worker 16)": { --> principalmete workers



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Structure of the project 

1. **Lithops** – my serverless compute framework.  
2. **MinIO** – S3-compatible object storage used as the communication bus between functions.  
3. **Flexecutor** – a Python wrapper around Lithops that aggregates execution metadata (logs, perf stats, outputs) into a single report.

 


 





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# LITHOPS 
# install lithops backend: 

docker pull lithopscloud/ibmcf-python-v312


net stop LxssManager
net start LxssManager
wsl --update

## Entorno virtual

### configuracion entorno virtual
python -m venv venv
python3 -m venv venv


venv\Scripts\activate // for mac
venv\Scripts\Activate.ps1 // for windows
source venv/bin/activate 
source .venv/bin/activate 
source lithops-venv/bin/activate 


### to finish the sesion: 
deactivate

### comprobacion elementos de entorno virtual
python --version
pip list
pip install -r requirements.txt // not allways necessary
pip install setup.py

### install lithops: 
<!-- pip install lithops -->

### Install the Package in Editable Mode
venv/bin/python -m pip install -e . 
pip install -e .

### una vez instalado el v env 
pip install -e ".[all]" --break-system-packages
pip install -e ".[all]" 


# lithops yaml
https://github.com/lithops-cloud/lithops/blob/master/config/config_template.yaml

# where configuration lithops is : 
export LITHOPS_CONFIG_FILE=/home/bigrobbin/Desktop/TFG/lithops_fork/lithops_config   #/path/to/your/config

# LITHOPS_CONFIG_FILE system environment variable:
export LITHOPS_CONFIG_FILE='/home/bigrobbin/Desktop/TFG/lithops_fork/lithops_config'
unset LITHOPS_CONFIG_FILE

echo $LITHOPS_CONFIG_FILE
ls ~/.lithops/config ./.lithops_config /etc/lithops/config


nano ~/.lithops/config

# command:  
python -c "import lithops; print(lithops.__file__)"


# inside the venv 
pip install --force-reinstall lithops



# see where lithops is 
C:\Users\Usuario\Desktop\lithops\lithops\__init__.py
pip uninstall lithops -y
rmdir /s /q C:\Users\Usuario\Desktop\lithops\lithops

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# DOCKER
## Install wsl
https://docs.microsoft.com/es-es/windows/wsl/install-win10

## install docker
https://docs.docker.com/docker-for-windows/install/

* verify docker is installed
* verify the path to docker is in the environment variables


## instalar docker imagen de lithops
docker pull lithopscloud/ibmcf-python-v312
docker images
docker run -it lithopscloud/ibmcf-python-v312 python --version

 


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Problemas: 
## no module pika installed as well as all requierements and libraries
* only when i intall lithops in local and execute the examples in the virtual machine it works 
* seems that the file should be installed in the venv python but also in the system
* in the folder: C:\Users\Usuario\AppData\Local\Temp\lithops-root there where errors bc the both enviroments are using the same folder 


```bash
$env:LITHOPS_DEBUG = "True"
lithops hello
```
 

## to run the examples:

* have complete and funtional commits in your local git repository
* create a new branch
* push the branch to the remote repository
* create a new cloud function
* push the cloud function to the remote repository
* create a new job
* push the job to the remote repository
* run the job
* validate before update 


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# elements to execution enviroments 
lithops logs poll

# test in local: 
https://github.com/lithops-cloud/lithops/blob/master/docs/source/compute_config/localhost.md 
lithops hello -b localhost -s localhost

# see the logs : 
lithops logs poll



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 

 


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~