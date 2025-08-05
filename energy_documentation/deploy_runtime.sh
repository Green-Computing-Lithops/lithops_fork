#!/bin/bash
# deploy_runtime.sh
# Script para construir y desplegar runtime personalizado con simulación de costes

set -e  # Salir si hay algún error

echo "🐳 CONSTRUYENDO RUNTIME PERSONALIZADO CON SIMULACIÓN DE COSTES"
echo "============================================================="

# Verificar que Docker esté instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor instálalo primero:"
    echo "   - macOS: brew install docker"
    echo "   - Ubuntu: sudo apt install docker.io"
    exit 1
fi

# Verificar que Lithops esté instalado
if ! command -v lithops &> /dev/null; then
    echo "❌ Lithops no está instalado. Instalando..."
    pip install lithops[aws]
fi

# Verificar credenciales AWS
echo "🔑 Verificando credenciales AWS..."
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ Credenciales AWS no configuradas. Configúralas con:"
    echo "   aws configure"
    echo "   O establece las variables de entorno AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY"
    exit 1
fi

echo "✅ Credenciales AWS verificadas"

# 1. Construir el runtime
echo ""
echo "🔨 Paso 1: Construyendo runtime personalizado..."
echo "Archivo: Dockerfile.lithops-costes"
echo "Runtime: lithops-costes-runtime:latest"

if [ ! -f "Dockerfile.lithops-costes" ]; then
    echo "❌ No se encuentra Dockerfile.lithops-costes en el directorio actual"
    exit 1
fi

if [ ! -f "simulacion_costes.py" ]; then
    echo "❌ No se encuentra simulacion_costes.py en el directorio actual"
    exit 1
fi

if [ ! -f "main_german_container.py" ]; then
    echo "❌ No se encuentra main_german_container.py en el directorio actual"
    exit 1
fi

# Construir el runtime
lithops runtime build -f Dockerfile.lithops-costes -b aws_lambda lithops-costes-runtime:latest

if [ $? -eq 0 ]; then
    echo "✅ Runtime construido exitosamente"
else
    echo "❌ Error construyendo el runtime"
    exit 1
fi

# 2. Desplegar el runtime
echo ""
echo "🚀 Paso 2: Desplegando runtime en AWS Lambda..."

lithops runtime deploy lithops-costes-runtime:latest -b aws_lambda -m 256 -t 300

if [ $? -eq 0 ]; then
    echo "✅ Runtime desplegado exitosamente"
else
    echo "❌ Error desplegando el runtime"
    exit 1
fi

# 3. Listar runtimes disponibles
echo ""
echo "📋 Paso 3: Runtimes disponibles en tu cuenta:"
lithops runtime list -b aws_lambda

# 4. Verificar configuración
echo ""
echo "⚙️ Paso 4: Verificando configuración..."

if [ -f "lithops_config.yaml" ]; then
    echo "✅ Archivo de configuración encontrado: lithops_config.yaml"
    echo "💡 Recuerda actualizar:"
    echo "   - execution_role: con tu ARN de rol IAM"
    echo "   - bucket: con tu bucket de S3"
else
    echo "⚠️ No se encuentra lithops_config.yaml"
    echo "   Usa el archivo de ejemplo proporcionado"
fi

# 5. Instrucciones finales
echo ""
echo "🎉 DESPLIEGUE COMPLETADO"
echo "======================"
echo ""
echo "✅ Tu runtime 'lithops-costes-runtime:latest' está listo para usar"
echo ""
echo "🧪 Para probar localmente (simulación):"
echo "   python main_german_container.py"
echo ""
echo "☁️ Para ejecutar en AWS Lambda:"
echo "   python main_german_container.py --mode aws"
echo ""
echo "🔧 Para ver opciones:"
echo "   python main_german_container.py --help"
echo ""
echo "📊 Para eliminar el runtime cuando ya no lo necesites:"
echo "   lithops runtime delete lithops-costes-runtime:latest -b aws_lambda"
echo ""
echo "💡 El runtime incluye:"
echo "   ✓ Simulación automática de costes"
echo "   ✓ Comparación estimado vs real"
echo "   ✓ Todas las dependencias de Lithops"
echo "   ✓ Tu función optimizada para containers"

echo ""
echo "🎯 ¡Todo listo! Disfruta de tu simulador de costes en AWS Lambda!"
