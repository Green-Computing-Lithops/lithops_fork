import lithops
from lithops.storage import Storage ## abstraccion de lithops para interactuar con el subyacente : interfaz comun independiente al storage

 

def funcion_german ( x ): 
    storage = Storage()
    print(storage.list_keys("lithops-test")) #
    return x + 1



executor= lithops.FunctionExecutor(log_level='debug' )

ft = executor.map(funcion_german, [1,2,3])

#  mv venv .venv # no flag activado 
# code /home/bigrobbin/.lithops/config
# path de config 
# anadir usuario al c group de docker 

print(executor.get_result(ft))


'''
(venv) bigrobbin@bigrobbin:~/Desktop/TFG$ sudo groupadd docker
groupadd: group 'docker' already exists
(venv) bigrobbin@bigrobbin:~/Desktop/TFG$ sudo usermod -aG docker $USER
(venv) bigrobbin@bigrobbin:~/Desktop/TFG$ newgrp docker
bigrobbin@bigrobbin:~/Desktop/TFG$ docker run  hello-world

german: 
usuario no permisos sobre docker --> bigrrobin 

diferentes entornos con configuraciones 
imagen --> definir el container con una imagen especifica


runtime: docker.io/lithopscloud/ibmcf-python-v312 # imagen publica en docker: 
* permisos especiales por default --> usuario normal no tiene permisos 
* anadir usuario al grupo de docker 
(venv) bigrobbin@bigrobbin:~/Desktop/TFG$ docker ps
permission denied while trying to connect to the Docker daemon socket at 


unix:///var/run/docker.sock: Get "http://%2Fvar%2Frun%2Fdocker.sock/v1.45/containers/json": dial unix /var/run/docker.sock: connect: permission denied

framework programacion 
por debajo container 
no podias correr containers de locker 

hello world de docker --> 
primero a gestionar c group de docker 
https://stackoverflow.com/questions/48957195/how-to-fix-docker-permission-denied



 docker ps -a

 
(venv) bigrobbin@bigrobbin:~/Desktop/TFG$ docker rm minio
Error response from daemon: No such container: minio
(venv) bigrobbin@bigrobbin:~/Desktop/TFG$ docker rm /minio-server













"""
Simple Lithops example using the map method.
In this example the map() method will launch one
map function for each entry in 'iterdata'. Finally
it will print the results for each invocation with
fexec.get_result()
"""
import lithops
import time


def my_map_function(id, x):
    print(f"I'm activation number {id}")
    time.sleep(5)
    return x + 7


if __name__ == "__main__":
    iterdata = [1, 2, 3, 4]
    fexec = lithops.FunctionExecutor()
    fexec.map(my_map_function, range(2))
    fexec.map(my_map_function, range(6))
    print(fexec.get_result())


    
time sleep_pro 
forzar cpu loggaritmo --> replantear funcion 
chunck --> dividir en 2 
que la funcion que haga 
1000 ciclos
2 500 ciclos 
4 250 ciclos 

weak scaling 
automatizar sobre ese codigo --> cambiar para que sea 
consumo de energia segun paralelismo 
minio y runtimes 
automatizas + plot 

POC

word count 
1 lee 
2 archivo la mitad 

# GERMAN: 
error docker --> clasico permisos
lithops logs poll

docker ps -a
* no puedes usar sudo pq en las maquinas virtuales y funciones no permite
* eliminar imagenes no necesarios: docker rm /minio-server


# web interface / rest api 

'''