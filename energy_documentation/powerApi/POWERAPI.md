
# LINKS DE INTERES:
https://webtv.univ-lille.fr/video/11485/experimenting-software-defined-power-meters-with-powerapi
https://docs.openeuler.org/en/docs/22.03_LTS_SP4/docs/powerapi/development_using_powerapi.html
https://powerapi.org/getting_started/
https://powerapi.org/reference/cgroup/cgroup/
https://github.com/powerapi-ng/powerapi/tree/master
https://blog.ptidej.net/using-powerapi-to-measure-the-energy-consumption-of-your-device/


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


## install docker: 
sudo apt update
sudo apt install docker.io -y
sudo systemctl enable docker
sudo systemctl start docker

## install the docker elements: 
sudo bash ./smartwatts_install.sh
--> chose all docker options--> easier 

## put mondo to work: 
sudo docker run -d --name mongo_source -p 27017:27017 mongo

## install influxDB: 
Now that the sensors are writing to MongoDB to store sensor reports, the SmartWatts formula will read from those, and generate new reports to estimate the power consumption of the system. We will write these reports to InfluxDB.

```bash
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

```

http://localhost:8086
ADMIN_USERNAME
ADMIN_PASSWORD

generate all access api token --> grafana

## grafana: 
sudo docker run -d -p 3000:3000 grafana/grafana

### generic credentials: 
admin
admin

## hostname -I
hostname -I

ip + puerto  local 
http://192.168.1.168:8086

#### heather autentication 
Under Custom HTTP headers, add a new header with the key "Authorization"
"Token <my-token>" 


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



 

ELEMENTS: 
Check if RAPL is supported on your system:
```bash
sudo modprobe intel_rapl_common
ls /sys/class/powercap/intel-rapl
```


POWERAPI EXTRA: 
https://blog.theodo.com/2020/09/power-api-deep-dive/
https://www.sciencedirect.com/science/article/pii/S1389128624002032


