#!/usr/bin/env python3
"""
Función alemana adaptada para ejecutar en container runtime personalizado
con simulación de costes integrada
"""
import lithops
from lithops.storage import Storage
import time
from datetime import datetime
import os
import sys

# Añadir el directorio actual al path para importar simulacion_costes
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from simulacion_costes import calcular_coste_aws_lambda, mostrar_simulacion_costes
except ImportError:
    # Fallback si no está disponible el módulo
    print("⚠️ Módulo de simulación no disponible, ejecutando sin simulación")
    def calcular_coste_aws_lambda(*args, **kwargs):
        return {'total': {'coste_total_usd': 0.0}}
    def mostrar_simulacion_costes(resultado):
        print("Simulación de costes no disponible")


def funcion_german_con_simulacion(x):
    """
    Tu función original con capacidad de simulación incluida
    Optimizada para container runtime
    """
    storage = Storage()
    try:
        # Use the same bucket as configured in lithops
        bucket_name = "lithops-us-east-1-45dk"
        
        # Create a test object
        test_key = f"test-execution/test-file-{x}.txt"
        test_data = f"Hello from AWS Lambda container task {x}"
        storage.put_object(bucket_name, test_key, test_data)
        print(f"✅ Created test file in S3: {bucket_name}/{test_key}")
        
        # List objects in the test directory
        keys = storage.list_keys(bucket_name, prefix="test-execution/")
        print(f"📋 Found {len(keys)} keys in {bucket_name}")
        
        # Read back the test object
        result = storage.get_object(bucket_name, test_key)
        print(f"📖 Read back from S3: {result}")
        
    except Exception as e:
        print(f"❌ AWS S3 operation failed: {e}")
        import traceback
        traceback.print_exc()
    
    return x + 1


def ejecutar_con_simulacion_local():
    """
    Función para ejecutar localmente (antes del despliegue)
    """
    print("🏠 EJECUCIÓN LOCAL - SIMULACIÓN DE COSTES")
    print("=" * 50)
    
    # Datos de entrada
    datos = [1, 2, 3]
    
    # 🧮 SIMULACIÓN DE COSTES
    print("🧮 Realizando simulación de costes...")
    simulacion = calcular_coste_aws_lambda(
        num_invocaciones=len(datos),
        memoria_mb=256,
        duracion_estimada_ms=2000,
        region='us-east-1'
    )
    
    mostrar_simulacion_costes(simulacion)
    
    # Confirmación del usuario
    respuesta = input("¿Continuar con el despliegue en AWS Lambda? (s/n): ").lower().strip()
    
    if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
        print("❌ Despliegue cancelado por el usuario.")
        return None
    
    return simulacion


def ejecutar_en_aws_lambda():
    """
    Función principal que se ejecuta en AWS Lambda
    """
    print("☁️ EJECUCIÓN EN AWS LAMBDA")
    print("=" * 30)
    
    # Datos de entrada
    datos = [1, 2, 3]
    
    try:
        # Crear executor (usará el runtime configurado en lithops_config.yaml)
        # No especificamos runtime aquí - se toma de la configuración
        executor = lithops.FunctionExecutor()
        
        # ⏰ Medir tiempo de ejecución
        inicio = time.time()
        inicio_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"⏰ Inicio: {inicio_timestamp}")
        
        # Ejecutar funciones
        print(f"🚀 Ejecutando {len(datos)} invocaciones...")
        futures = executor.map(funcion_german_con_simulacion, datos)
        resultados = executor.get_result(futures)
        
        fin = time.time()
        fin_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duracion_real = (fin - inicio) * 1000  # en ms
        duracion_promedio = duracion_real / len(datos)
        
        print(f"\n✅ EJECUCIÓN COMPLETADA")
        print(f"⏰ Fin: {fin_timestamp}")
        print(f"📊 Resultados: {resultados}")
        print(f"⏱️  Duración total: {duracion_real:.2f} ms")
        print(f"⏱️  Duración promedio por función: {duracion_promedio:.2f} ms")
        
        # 🔄 Recalcular con duración real
        print("\n🔄 Recalculando costes con duración real...")
        simulacion_real = calcular_coste_aws_lambda(
            num_invocaciones=len(datos),
            memoria_mb=256,
            duracion_estimada_ms=int(duracion_promedio),
            region='us-east-1'
        )
        
        print(f"\n📊 COMPARACIÓN FINAL:")
        print(f"   • Duración estimada: 2000 ms/función")
        print(f"   • Duración real: {duracion_promedio:.0f} ms/función")
        print(f"   • Coste real estimado: ${simulacion_real['total']['coste_total_usd']}")
        
        if duracion_promedio < 2000:
            ahorro = ((2000 - duracion_promedio) / 2000) * 100
            print(f"   • 🎉 Función {ahorro:.1f}% más rápida de lo estimado!")
        else:
            exceso = ((duracion_promedio - 2000) / 2000) * 100
            print(f"   • ⚠️ Función {exceso:.1f}% más lenta de lo estimado")
        
        return resultados
        
    except Exception as e:
        print(f"❌ Error ejecutando en AWS Lambda: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """
    Función principal que maneja tanto simulación local como ejecución en AWS
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Ejecutar función con simulación de costes')
    parser.add_argument('--mode', choices=['local', 'aws'], default='local',
                        help='Modo de ejecución: local (simulación) o aws (real)')
    parser.add_argument('--config', '-c', default='lithops_config.yaml',
                        help='Archivo de configuración de Lithops')
    
    args = parser.parse_args()
    
    if args.mode == 'local':
        # Ejecutar simulación local
        simulacion = ejecutar_con_simulacion_local()
        if simulacion:
            print("\n💡 Para ejecutar en AWS Lambda, usa:")
            print(f"   python {__file__} --mode aws")
            
    elif args.mode == 'aws':
        # Ejecutar en AWS Lambda
        if os.path.exists(args.config):
            os.environ['LITHOPS_CONFIG_FILE'] = args.config
        
        resultados = ejecutar_en_aws_lambda()
        if resultados:
            print(f"\n🏆 Proceso completado exitosamente: {resultados}")


if __name__ == "__main__":
    # Si se ejecuta sin argumentos, hacer simulación local por defecto
    if len(sys.argv) == 1:
        print("🧮 Ejecutando simulación local por defecto...")
        print("💡 Para ver opciones: python main_german_container.py --help\n")
        
        simulacion = ejecutar_con_simulacion_local()
        if simulacion:
            print("\n💡 Para ejecutar en AWS Lambda, usa:")
            print(f"   python {__file__} --mode aws")
    else:
        main()
