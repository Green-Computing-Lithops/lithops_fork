install lithops backend: 

docker pull lithopscloud/ibmcf-python-v312


net stop LxssManager
net start LxssManager
wsl --update

# Entorno virtual

## configuracion entorno virtual
python -m venv venv
python3 -m venv venv


venv\Scripts\activate // for mac
venv\Scripts\Activate.ps1 // for windows
source venv/bin/activate 

## comprobacion elementos de entorno virtual
python --version
pip list
pip install -r requirements.txt // not allways necessary

## install lithops: 
pip install lithops


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



pip install .
pip install joblib 



# Comprobar lithops 




# Problemas: 
## no module pika installed as well as all requierements and libraries
* only when i intall lithops in local and execute the examples in the virtual machine it works 
* seems that the file should be installed in the venv python but also in the system
* in the folder: C:\Users\Usuario\AppData\Local\Temp\lithops-root there where errors bc the both enviroments are using the same folder 


```bash
$env:LITHOPS_DEBUG = "True"
lithops hello
```
 

# to run the examples:

* have complete and funtional commits in your local git repository
* create a new branch
* push the branch to the remote repository
* create a new cloud function
* push the cloud function to the remote repository
* create a new job
* push the job to the remote repository
* run the job
* validate before update 



# elements to execution enviroments 
lithops logs poll


# test in local: 
https://github.com/lithops-cloud/lithops/blob/master/docs/source/compute_config/localhost.md 
lithops hello -b localhost -s localhost

# see the logs : 
lithops logs poll



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# New approack 
* Install the Package in Editable Mode
pip install -e .

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~











!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# to finish the sesion: 
deactivate


# Tareas pendientes
grafo funcionalidad --> diagrama de flujo --> chatgpt / draw.io



# command:  
python -c "import lithops; print(lithops.__file__)"


# inside the venv 
pip install --force-reinstall lithops



# see where lithops is 
C:\Users\Usuario\Desktop\lithops\lithops\__init__.py
pip uninstall lithops -y
rmdir /s /q C:\Users\Usuario\Desktop\lithops\lithops


# install all libraries : 
pip install lithops[all]
 

# computer optimization: 
minirobbin@minirobbin:~$ sudo systemctl restart logid
minirobbin@minirobbin:~$ sudo nano /etc/logid.cfg

## Main repository
https://github.com/PixlOne/logiops

### Guide
https://medium.com/@jeromedecinco/configuring-logiops-for-logitech-mx-master-3s-on-rhel-based-systems-d3971101c324

### example
https://github.com/menuRivera/logiops/blob/master/logid.cfg


main explanations : https://github.com/Datawithinigo/lithops_fork.git
https://thinktank.ottomator.ai/t/videos-to-get-started/2388/5


# run modifications: 
pip install -e . 






# linux : 

https://cambiatealinux.com/instalar-google-drive-en-ubuntu



# instal hcp
sudo bash ./smartwatts_install.sh

# usamos mongo como base de datos 
sudo docker run -d --name mongo_source -p 27017:27017 mongo

https://blog.ptidej.net/using-powerapi-to-measure-the-energy-consumption-of-your-device/

# REFERENCIA PRINCIPAL: 
https://powerapi.org/reference/sensors/hwpc-sensor/#usage
https://powerapi.org/reference/sensors/hwpc-sensor/

However, 

generaciones 2 a 10
tu 10 = ice lake : 
*  Intel Core Tiger Lake =  11
*  Alder Lake = 12
*  Raptor Lake = 13, 14
c7i 
c7e
c6
c5 (mas consumo / menos rendimiento) + %cpu * tiempo * TDP


docker ps -a | grep mongo_destination

perf --> api : 
semana end to end --> version inicial 
manri mentalidad aerea : cambiar rapido cuando no funciona / iterar rapido 







1. Check what's using port 27017:
sudo lsof -i :27017
2. Check all running Docker containers:
docker ps -a


commands to extract mongo infromation: 
sudo lsof -i :27017

docker ps -a

docker rm <container_id>

docker run -d --name mongo_destination -p 27017:27017 mongo

docker exec -it mongo_destination bash


docker exec -it mongo_destination bash

pwd
data/db
ls -la  --> avoid hidden 

find /data -type d | sort

# informations: 
The directories you see are standard MongoDB storage structures:

/data/db - This is the main data directory
/data/db/.mongodb/mongosh - Contains MongoDB shell settings and history
/data/db/diagnostic.data - Stores diagnostic information
/data/db/journal - Contains write-ahead logs for durability


connect mongo shell: 
mongosh
show dbs


use testdb
db.test.insertOne({name: "Test Document", value: 42})
show dbs
db.test.find()



# InfluxDB
sudo docker run \
 --name influxdb2 \
 --publish 8086:8086 \
 --mount type=volume,source=influxdb2-data,target=/var/lib/influxdb2 \
 --mount type=volume,source=influxdb2-config,target=/etc/influxdb2 \
 --env DOCKER_INFLUXDB_INIT_MODE=setup \
 --env DOCKER_INFLUXDB_INIT_USERNAME=ADMIN_USERNAME \
 --env DOCKER_INFLUXDB_INIT_PASSWORD=ADMIN_PASSWORD \
 --env DOCKER_INFLUXDB_INIT_ORG=org_test \
 --env DOCKER_INFLUXDB_INIT_BUCKET=power_consumption \
 influxdb:2

Initializing with environment 
variables for username (ADMIN_USERNAME),
password (ADMIN_PASSWORD),  
organization (org_test), 
and bucket (power_consumption)

name:
lithops 
token: 



# grafana: 

sudo docker run -d -p 3000:3000 grafana/grafana

admin
admin
pss: admin

hostname -I

ip + puerto  local 
https://192.168.1.43:8086



# Manri 07/03/2023: 
valores base y heuristica --> estimacion de energia --> links german 
TDP= procesador 65w
porcentaje de uso de cada aplicacion --> primer aproach 

version naive : consultar basicamente 

scrapping a una api -> consumo energia base 
hardcoding --> cambiar por necesario 


# seo 
# en la carpeta /build/logiops : 
sudo systemctl enable --now logid

sudo systemctl restart logid



keyword research 
intencionalidad 
- transacionales (comprar)
- informacionales 

## Tansacionales
crear articulo vs ir para comprar 
categoria / subcategoria / producto
- menos busquedas 
- suelen tener anuncios 


## Informacionales 
supinador 
se trabajan desde blog / contenido de valor 
mucho mas volumen de busqueda 
no tienen tantos ads  ->  no anuncions pq no convierten 

## Mixtas 
invertir en criptomonedas 
informacional: criptomonedas
transacional: comprar criptomonedas 

como saber como es una palabra --> vas a google y ves los anuncios como son 
si son transacionales o informacionales --> si hay o no 

google quiere ensenar al usuario lo que quiere encontrar 


Customer 






























