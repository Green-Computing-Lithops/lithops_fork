# 🚀 INSTRUCCIONES COMPLETAS: Ejecutar con Dockerfile Oficial de Lithops

## 📁 **Archivos creados para ti:**

```
energy_documentation/
├── Dockerfile.lithops-costes      # Dockerfile personalizado basado en el oficial
├── lithops_config.yaml           # Configuración de Lithops
├── main_german_container.py      # Tu función adaptada para container
├── simulacion_costes.py          # Módulo de simulación (funciona ✅)
├── deploy_runtime.sh             # Script automático de despliegue
├── GUIA_DOCKERFILE_LITHOPS.md    # Documentación completa
└── INSTRUCCIONES_EJECUTAR.md     # Este archivo
```

## 🎯 **¿Qué hemos logrado?**

✅ **Dockerfile personalizado** basado en el oficial de Lithops
✅ **Simulación de costes** completamente funcional 
✅ **Script automatizado** para construir y desplegar
✅ **Función adaptada** para ejecutar en container runtime
✅ **Configuración lista** para AWS Lambda

## 🔥 **OPCIÓN 1: Simulación rápida (SIN AWS)**

Si solo quieres ver la simulación de costes:

```bash
# Probar simulación directamente
python simulacion_costes.py
```

**Resultado esperado:**
```
🧪 Test del módulo de simulación de costes
📊 CONFIGURACIÓN: 3 invocaciones, 256 MB, 2000 ms
💰 COSTE TOTAL ESTIMADO: $0.001004 USD
✅ Coste muy bajo - menos de $0.01
```

## 🌟 **OPCIÓN 2: Despliegue completo en AWS**

Para usar el Dockerfile oficial de Lithops y desplegar en AWS:

### **Prerrequisitos:**
1. ✅ Docker instalado
2. ✅ AWS CLI configurado
3. ✅ Lithops instalado: `pip install lithops[aws]`
4. ✅ Credenciales AWS configuradas

### **Paso 1: Configurar credenciales**
```bash
# Configurar AWS CLI
aws configure

# O usar variables de entorno
export AWS_ACCESS_KEY_ID="tu_access_key"
export AWS_SECRET_ACCESS_KEY="tu_secret_key"
export AWS_DEFAULT_REGION="us-east-1"
```

### **Paso 2: Actualizar configuración**
Edita `lithops_config.yaml`:
```yaml
aws_lambda:
    execution_role: arn:aws:iam::TU_ACCOUNT_ID:role/lithops-execution-role
aws_s3:
    bucket: tu-bucket-s3
```

### **Paso 3: Desplegar automáticamente**
```bash
# Ejecutar script de despliegue
./deploy_runtime.sh
```

Este script:
- 🔨 Construye el runtime usando el Dockerfile oficial
- 🚀 Lo despliega en AWS Lambda
- 📋 Lista todos los runtimes disponibles
- ✅ Verifica que todo esté listo

### **Paso 4: Ejecutar con simulación**
```bash
# Simulación local (sin coste)
python main_german_container.py

# Ejecución real en AWS
python main_german_container.py --mode aws
```

## 🎯 **Ejemplo de flujo completo:**

```bash
# 1. Verificar simulación local
python simulacion_costes.py

# 2. Configurar AWS (si no está hecho)
aws configure

# 3. Actualizar lithops_config.yaml con tus valores

# 4. Desplegar runtime personalizado
./deploy_runtime.sh

# 5. Ejecutar con simulación completa
python main_german_container.py --mode aws
```

## 📊 **Salida esperada del despliegue:**

```
🐳 CONSTRUYENDO RUNTIME PERSONALIZADO CON SIMULACIÓN DE COSTES
=============================================================

🔑 Verificando credenciales AWS...
✅ Credenciales AWS verificadas

🔨 Paso 1: Construyendo runtime personalizado...
✅ Runtime construido exitosamente

🚀 Paso 2: Desplegando runtime en AWS Lambda...
✅ Runtime desplegado exitosamente

📋 Paso 3: Runtimes disponibles en tu cuenta:
   - lithops-costes-runtime:latest

🎉 DESPLIEGUE COMPLETADO
========================

✅ Tu runtime 'lithops-costes-runtime:latest' está listo para usar
```

## 🧮 **Características del runtime personalizado:**

1. **Basado en Dockerfile oficial**: Usa exactamente la misma base que recomienda Lithops
2. **Simulación integrada**: Calcula costes antes y después de la ejecución
3. **Optimizado**: Incluye todas las dependencias oficiales de Lithops
4. **Reutilizable**: Una vez desplegado, puedes usarlo múltiples veces
5. **Monitoreo**: Compara duración estimada vs real

## 🔍 **Ejemplo de ejecución con simulación:**

```
🧮 Realizando simulación de costes...

📊 CONFIGURACIÓN:
   • Invocaciones: 3
   • Memoria: 256 MB
   • Duración estimada: 2000 ms

💰 COSTE TOTAL ESTIMADO: $0.001004 USD

☁️ EJECUCIÓN EN AWS LAMBDA
⏰ Inicio: 2025-01-17 15:30:00
🚀 Ejecutando 3 invocaciones...
✅ EJECUCIÓN COMPLETADA
📊 Resultados: [2, 3, 4]
⏱️ Duración real promedio: 1800 ms

🔄 Recalculando costes con duración real...
📊 COMPARACIÓN FINAL:
   • Duración estimada: 2000 ms/función
   • Duración real: 1800 ms/función
   • 🎉 Función 10% más rápida de lo estimado!
```

## 🚨 **Troubleshooting:**

### **Error: "Docker not found"**
```bash
# macOS
brew install docker

# Ubuntu
sudo apt install docker.io
```

### **Error: "AWS credentials not configured"**
```bash
# Verificar credenciales
aws sts get-caller-identity

# Si falla, configurar
aws configure
```

### **Error: "Lithops not found"**
```bash
pip install lithops[aws]
```

### **Error: "Runtime build failed"**
- Verificar que Docker esté corriendo
- Verificar permisos ECR en tu cuenta AWS

## 💡 **Consejos:**

1. **Desarrollo**: Usa primero `python simulacion_costes.py` para probar
2. **Testing**: Usa `python main_german_container.py` para simulación local
3. **Producción**: Usa `python main_german_container.py --mode aws` para ejecución real
4. **Limpieza**: Elimina el runtime cuando no lo necesites: `lithops runtime delete lithops-costes-runtime:latest -b aws_lambda`

## 🏆 **Resultado final:**

Tendrás un runtime de AWS Lambda completamente funcional que:
- ✅ Usa el Dockerfile oficial de Lithops
- ✅ Incluye simulación automática de costes
- ✅ Es reutilizable y optimizado
- ✅ Te permite comparar estimaciones vs realidad
- ✅ Te ayuda a optimizar costes desde el primer día

¡Perfecto para producción y desarrollo! 🚀
