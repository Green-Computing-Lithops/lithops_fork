## 🔄 FLUJO COMPLETO: Dónde y cuándo se usa el Dockerfile

```
📂 Tu máquina local
├── Dockerfile.lithops-costes     ← Aquí defines el runtime
├── simulacion_costes.py          ← Tu código personalizado
├── main_german_container.py      ← Tu función principal
└── lithops_config.yaml           ← Configuración

     │
     │ 1️⃣ lithops runtime build
     ▼
     
🐳 Docker Build Process
├── FROM python:3.10-slim-buster   ← Base image
├── RUN apt-get install...         ← System dependencies  
├── RUN pip install awslambdaric   ← AWS Lambda runtime
├── RUN pip install boto3...       ← Lithops dependencies
├── COPY lithops_lambda.zip        ← Handler de Lithops (auto-generado)
├── COPY simulacion_costes.py      ← Tu código personalizado
└── ENTRYPOINT awslambdaric        ← Punto de entrada

     │
     │ 2️⃣ docker push to ECR
     ▼
     
☁️ Amazon ECR (Container Registry)
└── lithops-costes-runtime:latest  ← Tu imagen almacenada

     │
     │ 3️⃣ lithops runtime deploy
     ▼
     
⚡ AWS Lambda Function
├── Function Name: lithops-worker-xxx
├── Runtime: Container Image
├── Image URI: xxx.dkr.ecr.us-east-1.amazonaws.com/lithops-costes-runtime:latest
├── Memory: 256 MB
├── Timeout: 300 seconds
└── Handler: handler.entry_point.lambda_handler

     │
     │ 4️⃣ executor.map(funcion, datos)
     ▼
     
🏃‍♂️ Ejecución en AWS Lambda
┌─────────────────────────────────────┐
│ Container Instance:                 │
│                                     │
│ /function/                          │
│ ├── handler/                        │
│ │   └── entry_point.py              │ ← Entry point de Lithops
│ ├── lithops/                        │ ← Código de Lithops  
│ ├── simulacion_costes.py            │ ← Tu módulo
│ ├── main_german_container.py        │ ← Tu función
│ └── ...todas las dependencias       │
│                                     │
│ Proceso:                            │
│ 1. AWS invoca entry_point.py        │
│ 2. Lithops carga tu función         │
│ 3. Ejecuta funcion_german()         │
│ 4. Usa simulacion_costes.py         │
│ 5. Devuelve resultados              │
└─────────────────────────────────────┘

     │
     │ 5️⃣ Resultados
     ▼
     
📊 Tu aplicación recibe:
├── Resultados: [2, 3, 4]
├── Logs de ejecución
├── Métricas de duración
└── Datos para comparar con simulación
```

## 🎯 **Puntos clave de uso:**

### **Durante BUILD (lithops runtime build):**
```bash
lithops runtime build -f Dockerfile.lithops-costes -b aws_lambda lithops-costes-runtime:latest
```

1. **Lithops lee** tu `Dockerfile.lithops-costes`
2. **Crea automáticamente** `lithops_lambda.zip` (contiene entry_point.py)
3. **Ejecuta** `docker build` usando tu Dockerfile
4. **Las líneas COPY** copian tus archivos al container
5. **El resultado** es una imagen Docker en ECR

### **Durante DEPLOY (lithops runtime deploy):**
```bash
lithops runtime deploy lithops-costes-runtime:latest -b aws_lambda
```

1. **Crea función Lambda** apuntando a tu imagen en ECR
2. **Configura** la función con memoria, timeout, etc.
3. **El ENTRYPOINT** se convierte en el comando que AWS ejecutará

### **Durante EJECUCIÓN (executor.map):**
```python
executor = lithops.FunctionExecutor(runtime='lithops-costes-runtime:latest')
futures = executor.map(funcion_german, [1, 2, 3])
```

1. **AWS Lambda** descarga tu imagen
2. **Inicia container** con `ENTRYPOINT ["/usr/local/bin/python", "-m", "awslambdaric"]`
3. **awslambdaric** llama a `handler.entry_point.lambda_handler`
4. **Lithops handler** carga y ejecuta tu función
5. **Tu función** puede importar `simulacion_costes.py`

## 🔍 **Diferencias con el Dockerfile oficial:**

### **Dockerfile oficial de Lithops:**
```dockerfile
# Solo dependencias estándar
COPY lithops_lambda.zip ${FUNCTION_DIR}
# Sin archivos personalizados
```

### **Nuestro Dockerfile personalizado:**
```dockerfile
# Mismas dependencias estándar
COPY lithops_lambda.zip ${FUNCTION_DIR}
# + TUS archivos personalizados
COPY simulacion_costes.py ${FUNCTION_DIR}/
COPY main_german_container.py ${FUNCTION_DIR}/
```

## 🎯 **Ventajas de este enfoque:**

1. **✅ 100% compatible** con Lithops (misma base)
2. **✅ Reutilizable** - construyes una vez, usas múltiples veces  
3. **✅ Optimizado** - todas las dependencias pre-instaladas
4. **✅ Personalizable** - puedes añadir lo que necesites
5. **✅ Transparente** - Lithops maneja todo automáticamente

## 💡 **En resumen:**

El Dockerfile se usa en **3 momentos clave:**

1. **🔨 BUILD**: Para crear la imagen con tus personalizaciones
2. **🚀 DEPLOY**: Para crear la función Lambda que usa esa imagen  
3. **⚡ RUN**: Para ejecutar tu código dentro del container en AWS

¡Es exactamente como el oficial de Lithops, pero con tus archivos añadidos! 🎉
