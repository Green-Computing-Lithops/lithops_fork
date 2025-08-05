# Ejecutar Simulación de Costes con Dockerfile Oficial de Lithops

Esta guía te explica cómo usar el [Dockerfile oficial de Lithops](https://github.com/lithops-cloud/lithops/blob/master/runtime/aws_lambda/Dockerfile) para crear un runtime personalizado que incluya tu simulación de costes.

## 🎯 **Objetivo**

Crear un runtime personalizado de AWS Lambda que:
- ✅ Use el Dockerfile oficial de Lithops
- ✅ Incluya tu código de simulación de costes
- ✅ Permita ejecutar workloads con estimación previa
- ✅ Sea deployable y reutilizable

## 📂 **Estructura de archivos necesarios**

```
proyecto/
├── Dockerfile.lithops-costes     # Dockerfile personalizado
├── lithops_config.yaml          # Configuración de Lithops
├── main_german_container.py     # Tu función adaptada para container
├── simulacion_costes.py         # Módulo de simulación
├── requirements.txt             # Dependencias extra
└── deploy_runtime.sh            # Script de despliegue
```

## 🐳 **1. Dockerfile personalizado**

Basado en el [Dockerfile oficial](https://github.com/lithops-cloud/lithops/blob/master/runtime/aws_lambda/Dockerfile):

```dockerfile
# Dockerfile.lithops-costes
# Basado en: https://github.com/lithops-cloud/lithops/blob/master/runtime/aws_lambda/Dockerfile

# Python 3.10 (versión recomendada)
FROM python:3.10-slim-buster

RUN apt-get update \
    # Install aws-lambda-cpp build dependencies
    && apt-get install -y \
      g++ \
      make \
      cmake \
      unzip \
    # cleanup package lists
    && rm -rf /var/lib/apt/lists/* \
    && apt-cache search linux-headers-generic

ARG FUNCTION_DIR="/function"

# Copy function code
RUN mkdir -p ${FUNCTION_DIR}

# Update pip - DEPENDENCIAS OFICIALES DE LITHOPS
RUN pip install --upgrade --ignore-installed pip wheel six setuptools \
    && pip install --upgrade --no-cache-dir --ignore-installed \
        awslambdaric \
        boto3 \
        redis \
        httplib2 \
        requests \
        numpy \
        scipy \
        pandas \
        pika \
        kafka-python \
        cloudpickle \
        ps-mem \
        tblib \
        psutil

# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Add Lithops (esto se hace automáticamente por Lithops CLI)
COPY lithops_lambda.zip ${FUNCTION_DIR}
RUN unzip lithops_lambda.zip \
    && rm lithops_lambda.zip \
    && mkdir handler \
    && touch handler/__init__.py \
    && mv entry_point.py handler/

# 🆕 AÑADIR NUESTROS MÓDULOS DE SIMULACIÓN
COPY simulacion_costes.py ${FUNCTION_DIR}/
COPY main_german_container.py ${FUNCTION_DIR}/

# 🆕 DEPENDENCIAS ADICIONALES (si las necesitas)
COPY requirements.txt ${FUNCTION_DIR}/
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "handler.entry_point.lambda_handler" ]
```

## ⚙️ **2. Configuración de Lithops**

```yaml
# lithops_config.yaml
lithops:
    backend: aws_lambda
    storage: aws_s3

aws:
    access_key_id: YOUR_ACCESS_KEY_ID
    secret_access_key: YOUR_SECRET_ACCESS_KEY
    region: us-east-1

aws_lambda:
    execution_role: arn:aws:iam::YOUR_ACCOUNT:role/lithops-execution-role
    runtime: lithops-costes-runtime:latest
    runtime_memory: 256
    runtime_timeout: 300

aws_s3:
    bucket: lithops-us-east-1-45dk
```

## 🐍 **3. Tu función adaptada para container**

```python
# main_german_container.py
import lithops
from lithops.storage import Storage
from simulacion_costes import calcular_coste_aws_lambda, mostrar_simulacion_costes
import time
from datetime import datetime

def funcion_german_con_simulacion(x):
    """
    Tu función original con capacidad de simulación incluida
    """
    storage = Storage()
    try:
        bucket_name = "lithops-us-east-1-45dk"
        
        test_key = f"test-execution/test-file-{x}.txt"
        test_data = f"Hello from AWS Lambda task {x}"
        storage.put_object(bucket_name, test_key, test_data)
        print(f"Created test file in S3: {bucket_name}/{test_key}")
        
        keys = storage.list_keys(bucket_name, prefix="test-execution/")
        print(f"Found keys in {bucket_name}: {keys}")
        
        result = storage.get_object(bucket_name, test_key)
        print(f"Read back from S3: {result}")
        
    except Exception as e:
        print(f"AWS S3 operation failed: {e}")
        import traceback
        traceback.print_exc()
    
    return x + 1

def ejecutar_con_simulacion():
    """
    Función principal que incluye simulación de costes
    """
    # Datos de entrada
    datos = [1, 2, 3]
    
    # 🧮 SIMULACIÓN DE COSTES
    print("🧮 Realizando simulación de costes...")
    simulacion = calcular_coste_aws_lambda(
        num_invocaciones=len(datos),
        memoria_mb=256,
        duracion_estimada_ms=2000
    )
    
    mostrar_simulacion_costes(simulacion)
    
    # Crear executor
    executor = lithops.FunctionExecutor()
    
    # ⏰ Medir tiempo de ejecución
    inicio = time.time()
    
    # Ejecutar funciones
    futures = executor.map(funcion_german_con_simulacion, datos)
    resultados = executor.get_result(futures)
    
    fin = time.time()
    duracion_real = (fin - inicio) * 1000  # en ms
    
    print(f"\n✅ EJECUCIÓN COMPLETADA")
    print(f"📊 Resultados: {resultados}")
    print(f"⏱️  Duración real: {duracion_real:.2f} ms")
    
    # 🔄 Recalcular con duración real
    print("\n🔄 Costes con duración real:")
    simulacion_real = calcular_coste_aws_lambda(
        num_invocaciones=len(datos),
        memoria_mb=256,
        duracion_estimada_ms=int(duracion_real / len(datos))
    )
    
    print(f"   Estimado: ${simulacion['total']['coste_total_usd']}")
    print(f"   Real: ${simulacion_real['total']['coste_total_usd']}")
    
    return resultados

if __name__ == "__main__":
    ejecutar_con_simulacion()
```

## 📦 **4. Requirements adicionales**

```txt
# requirements.txt
# Aquí puedes añadir dependencias extra que no están en el Dockerfile base
# Por ejemplo:
# matplotlib>=3.5.0
# scikit-learn>=1.0.0
# opencv-python-headless>=4.5.0
```

## 🚀 **5. Script de despliegue**

```bash
#!/bin/bash
# deploy_runtime.sh

echo "🐳 Construyendo runtime personalizado con simulación de costes..."

# 1. Construir el runtime
lithops runtime build -f Dockerfile.lithops-costes -b aws_lambda lithops-costes-runtime:latest

# 2. Desplegar el runtime
lithops runtime deploy lithops-costes-runtime:latest -b aws_lambda

# 3. Listar runtimes disponibles
echo "📋 Runtimes disponibles:"
lithops runtime list -b aws_lambda

echo "✅ Runtime desplegado. Ahora puedes ejecutar:"
echo "   python main_german_container.py"
```

## 🛠️ **6. Pasos para ejecutar**

### **Paso 1: Preparar archivos**

```bash
# Crear directorio del proyecto
mkdir lithops-costes-runtime
cd lithops-costes-runtime

# Copiar los archivos que hemos creado
# - Dockerfile.lithops-costes
# - lithops_config.yaml  
# - main_german_container.py
# - simulacion_costes.py
# - requirements.txt
# - deploy_runtime.sh
```

### **Paso 2: Configurar credenciales AWS**

```bash
# Opción 1: AWS CLI
aws configure

# Opción 2: Variables de entorno
export AWS_ACCESS_KEY_ID="tu_access_key"
export AWS_SECRET_ACCESS_KEY="tu_secret_key"
export AWS_DEFAULT_REGION="us-east-1"
```

### **Paso 3: Instalar Lithops**

```bash
pip install lithops[aws]
```

### **Paso 4: Construir y desplegar**

```bash
# Dar permisos al script
chmod +x deploy_runtime.sh

# Ejecutar despliegue
./deploy_runtime.sh
```

### **Paso 5: Ejecutar con simulación**

```bash
# Ejecutar tu función con simulación integrada
python main_german_container.py
```

## 🎯 **Ventajas de este enfoque**

1. **📦 Runtime reutilizable**: Una vez construido, puedes usarlo múltiples veces
2. **🧮 Simulación integrada**: Costes calculados automáticamente
3. **⚡ Optimizado**: Basado en el Dockerfile oficial de Lithops
4. **🔧 Personalizable**: Puedes añadir las dependencias que necesites
5. **📊 Monitoreo**: Compara costes estimados vs reales

## 🔍 **Ejemplo de salida esperada**

```
🧮 Realizando simulación de costes...

============================================================
         SIMULACIÓN DE COSTES AWS LAMBDA + S3
============================================================

📊 CONFIGURACIÓN:
   • Invocaciones: 3
   • Memoria: 256 MB
   • Duración estimada: 2000 ms
   • Región: us-east-1

🔧 AWS LAMBDA:
   • Requests totales: 3
   • Requests free tier: 3
   • Requests facturables: 0
   • Coste Lambda total: $0.0

💾 AWS S3:
   • Coste S3 total: $0.001004

💰 COSTE TOTAL ESTIMADO:
   • USD: $0.001004
   • EUR: €0.000924 (aprox.)

✅ Coste muy bajo - menos de $0.01
============================================================

✅ EJECUCIÓN COMPLETADA
📊 Resultados: [2, 3, 4]
⏱️  Duración real: 1500.50 ms

🔄 Costes con duración real:
   Estimado: $0.001004
   Real: $0.001003
```

## 🚨 **Troubleshooting**

### **Error: Docker no encontrado**
```bash
# Instalar Docker
# macOS: brew install docker
# Ubuntu: sudo apt install docker.io
```

### **Error: Credenciales AWS**
```bash
# Verificar credenciales
aws sts get-caller-identity
```

### **Error: Permisos ECR**
```bash
# Tu rol IAM necesita permisos para ECR
# Añadir política: AmazonEC2ContainerRegistryFullAccess
```

## 📚 **Referencias**

- [Dockerfile oficial de Lithops](https://github.com/lithops-cloud/lithops/blob/master/runtime/aws_lambda/Dockerfile)
- [Documentación AWS Lambda Container Images](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html)
- [Lithops Runtime Documentation](https://lithops-cloud.github.io/docs/)

---

💡 **Tip**: Este runtime personalizado te permite ejecutar cualquier workload con simulación de costes automática, ideal para producción!
