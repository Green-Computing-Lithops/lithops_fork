# 🎯 CONFIGURACIÓN DEL RUNTIME: Archivo vs Código

## ✅ **FORMA RECOMENDADA: Archivo de configuración**

### **1. En `lithops_config.yaml`:**
```yaml
lithops:
    backend: aws_lambda
    storage: aws_s3

aws_lambda:
    # ✅ Runtime especificado en configuración
    runtime: lithops-costes-runtime:latest
    runtime_memory: 256
    runtime_timeout: 300
    execution_role: arn:aws:iam::YOUR_ACCOUNT_ID:role/lithops-execution-role
    region: us-east-1

aws_s3:
    bucket: lithops-us-east-1-45dk
    region: us-east-1
```

### **2. En tu código Python:**
```python
import lithops

# ✅ No especifica runtime - usa el de la configuración
executor = lithops.FunctionExecutor()

# Tu función ejecuta automáticamente con lithops-costes-runtime:latest
futures = executor.map(funcion_german, [1, 2, 3])
results = executor.get_result(futures)
```

## 🔄 **COMPARACIÓN: Archivo vs Código**

### **📁 OPCIÓN 1: En archivo de configuración (RECOMENDADO)**

**Ventajas:**
- ✅ **Separación clara** entre configuración y código
- ✅ **Fácil cambio** sin tocar código
- ✅ **Diferentes entornos** (dev, staging, prod)
- ✅ **Mejor práctica** para producción
- ✅ **Configuración centralizada**

**lithops_config.yaml:**
```yaml
aws_lambda:
    runtime: lithops-costes-runtime:latest  # ← Especificado aquí
    runtime_memory: 256
```

**Código Python:**
```python
# Limpio y simple
executor = lithops.FunctionExecutor()
```

### **💻 OPCIÓN 2: En código Python (menos recomendado)**

**Ventajas:**
- ✅ **Control granular** por función
- ✅ **Runtime dinámico** según lógica

**Desventajas:**
- ❌ **Código menos limpio**
- ❌ **Difícil de mantener**
- ❌ **Hardcodeado** en el código

```python
# Menos recomendado
executor = lithops.FunctionExecutor(
    runtime='lithops-costes-runtime:latest',
    runtime_memory=256
)
```

## 🔧 **CONFIGURACIONES AVANZADAS**

### **🌍 Diferentes entornos:**

**desarrollo.yaml:**
```yaml
aws_lambda:
    runtime: lithops-costes-runtime:dev
    runtime_memory: 128
    runtime_timeout: 180
```

**produccion.yaml:**
```yaml
aws_lambda:
    runtime: lithops-costes-runtime:latest
    runtime_memory: 512
    runtime_timeout: 900
```

**Uso:**
```python
# Especificar archivo de configuración
import os
os.environ['LITHOPS_CONFIG_FILE'] = 'produccion.yaml'

executor = lithops.FunctionExecutor()  # Usa produccion.yaml
```

### **🎛️ Override selectivo:**

```python
# Usa configuración por defecto, pero override memoria
executor = lithops.FunctionExecutor(runtime_memory=512)

# Usa configuración por defecto, pero override runtime
executor = lithops.FunctionExecutor(runtime='otro-runtime:v2')
```

## 📊 **TU CONFIGURACIÓN ACTUAL**

Con la configuración actualizada:

**lithops_config.yaml:**
```yaml
aws_lambda:
    runtime: lithops-costes-runtime:latest  # ← Runtime personalizado
    runtime_memory: 256                     # ← 256MB de memoria  
    runtime_timeout: 300                    # ← 5 minutos timeout
```

**main_german_container.py:**
```python
# ✅ Código simplificado - usa configuración del archivo
executor = lithops.FunctionExecutor()
```

## 🔄 **Flujo de ejecución actualizado:**

```
1. 📁 Lithops lee lithops_config.yaml
   └── runtime: lithops-costes-runtime:latest
   
2. 🐍 Tu código crea FunctionExecutor()
   └── Sin especificar runtime
   
3. 🔄 Lithops usa automáticamente:
   └── lithops-costes-runtime:latest (del archivo)
   
4. ☁️ AWS Lambda ejecuta tu container personalizado
   └── Con simulación de costes incluida
```

## 💡 **VENTAJAS de tu nueva configuración:**

### **✅ Código más limpio:**
**Antes:**
```python
executor = lithops.FunctionExecutor(
    runtime='lithops-costes-runtime:latest',
    runtime_memory=256
)
```

**Ahora:**
```python
executor = lithops.FunctionExecutor()  # ¡Mucho más limpio!
```

### **✅ Flexibilidad:**
```bash
# Cambiar runtime sin tocar código
# Solo editar lithops_config.yaml:
runtime: lithops-costes-runtime:v2
```

### **✅ Diferentes entornos:**
```bash
# Desarrollo
LITHOPS_CONFIG_FILE=dev_config.yaml python main_german_container.py

# Producción  
LITHOPS_CONFIG_FILE=prod_config.yaml python main_german_container.py
```

## 🎯 **TESTING de tu configuración:**

### **Verificar que usa el runtime correcto:**
```python
import lithops

# Crear executor
executor = lithops.FunctionExecutor()

# Ver qué runtime está usando
print(f"Runtime en uso: {executor.config['aws_lambda']['runtime']}")
print(f"Memoria: {executor.config['aws_lambda']['runtime_memory']}MB")
```

### **Probar simulación:**
```bash
# Tu código actualizado - usa configuración del archivo
python main_german_container.py --mode local
```

## 🏆 **RESULTADO FINAL:**

- ✅ **Runtime configurado** en `lithops_config.yaml`
- ✅ **Código Python limpio** sin hardcodear runtime
- ✅ **Fácil mantenimiento** y cambios
- ✅ **Mejor práctica** para proyectos serios
- ✅ **Simulación de costes** automática

¡Tu configuración ahora sigue las mejores prácticas! 🚀
