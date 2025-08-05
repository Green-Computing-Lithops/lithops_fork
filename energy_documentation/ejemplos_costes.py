#!/usr/bin/env python3
"""
Ejemplo de uso del simulador de costes para diferentes tipos de workloads
========================================================================

Este script demuestra cómo integrar la simulación de costes en diferentes
tipos de aplicaciones que usan Lithops con AWS Lambda.
"""

import sys
import os
import time
import json
from datetime import datetime

# Añadir el directorio padre al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_german import calcular_coste_aws_lambda, mostrar_simulacion_costes


def ejemplo_procesamiento_imagenes():
    """
    Ejemplo: Procesamiento de imágenes en batch
    """
    print("🖼️  EJEMPLO: PROCESAMIENTO DE IMÁGENES")
    print("=" * 40)
    
    # Parámetros del workload
    num_imagenes = 500
    memoria_necesaria = 512  # MB - necesaria para procesamiento de imágenes
    tiempo_por_imagen = 8000  # ms - redimensionar, aplicar filtros, etc.
    
    print(f"📝 Escenario:")
    print(f"   • Procesar {num_imagenes} imágenes")
    print(f"   • Redimensionar y aplicar filtros")
    print(f"   • Subir resultados a S3")
    
    # Simular costes
    simulacion = calcular_coste_aws_lambda(
        num_invocaciones=num_imagenes,
        memoria_mb=memoria_necesaria,
        duracion_estimada_ms=tiempo_por_imagen
    )
    
    mostrar_simulacion_costes(simulacion)
    
    # Comparar con diferentes configuraciones
    print("\n🔄 OPTIMIZACIÓN: Comparando configuraciones...")
    
    configuraciones = [
        {'memoria': 256, 'tiempo': 15000, 'descripcion': 'Memoria baja'},
        {'memoria': 512, 'tiempo': 8000, 'descripcion': 'Memoria media (recomendada)'},
        {'memoria': 1024, 'tiempo': 5000, 'descripcion': 'Memoria alta'},
    ]
    
    print("\n📊 Comparación de configuraciones:")
    for config in configuraciones:
        sim = calcular_coste_aws_lambda(
            num_invocaciones=num_imagenes,
            memoria_mb=config['memoria'],
            duracion_estimada_ms=config['tiempo']
        )
        print(f"   • {config['descripcion']:20s}: ${sim['total']['coste_total_usd']:8.6f}")


def ejemplo_analisis_datos():
    """
    Ejemplo: Análisis de datos en paralelo
    """
    print("\n📊 EJEMPLO: ANÁLISIS DE DATOS")
    print("=" * 30)
    
    # Parámetros del workload
    archivos_csv = 1000
    memoria_analisis = 256  # MB
    tiempo_por_archivo = 3000  # ms
    
    print(f"📝 Escenario:")
    print(f"   • Analizar {archivos_csv} archivos CSV")
    print(f"   • Calcular estadísticas descriptivas")
    print(f"   • Generar informes en JSON")
    
    # Simular costes
    simulacion = calcular_coste_aws_lambda(
        num_invocaciones=archivos_csv,
        memoria_mb=memoria_analisis,
        duracion_estimada_ms=tiempo_por_archivo
    )
    
    mostrar_simulacion_costes(simulacion)
    
    # Análisis de escalabilidad
    print("\n📈 ANÁLISIS DE ESCALABILIDAD:")
    escalas = [100, 500, 1000, 5000, 10000]
    
    for escala in escalas:
        sim = calcular_coste_aws_lambda(
            num_invocaciones=escala,
            memoria_mb=memoria_analisis,
            duracion_estimada_ms=tiempo_por_archivo
        )
        print(f"   • {escala:5d} archivos: ${sim['total']['coste_total_usd']:8.6f}")


def ejemplo_machine_learning():
    """
    Ejemplo: Entrenamiento distribuido de ML
    """
    print("\n🤖 EJEMPLO: MACHINE LEARNING")
    print("=" * 30)
    
    # Parámetros del workload
    num_workers = 50
    memoria_ml = 1024  # MB - necesaria para modelos ML
    tiempo_entrenamiento = 45000  # ms - 45 segundos por worker
    
    print(f"📝 Escenario:")
    print(f"   • Entrenamiento distribuido con {num_workers} workers")
    print(f"   • Procesamiento de features")
    print(f"   • Entrenamiento de modelo")
    print(f"   • Validación cruzada")
    
    # Simular costes
    simulacion = calcular_coste_aws_lambda(
        num_invocaciones=num_workers,
        memoria_mb=memoria_ml,
        duracion_estimada_ms=tiempo_entrenamiento
    )
    
    mostrar_simulacion_costes(simulacion)
    
    # Análisis coste-beneficio
    print("\n💡 ANÁLISIS COSTE-BENEFICIO:")
    print("   🔸 Alternativa 1: Más workers, menos tiempo")
    sim1 = calcular_coste_aws_lambda(100, 512, 25000)
    print(f"      100 workers, 512MB, 25s: ${sim1['total']['coste_total_usd']:8.6f}")
    
    print("   🔸 Alternativa 2: Menos workers, más tiempo")
    sim2 = calcular_coste_aws_lambda(25, 2048, 60000)
    print(f"      25 workers, 2GB, 60s: ${sim2['total']['coste_total_usd']:8.6f}")


def ejemplo_api_serverless():
    """
    Ejemplo: API serverless con picos de tráfico
    """
    print("\n🌐 EJEMPLO: API SERVERLESS")
    print("=" * 25)
    
    print(f"📝 Escenario:")
    print(f"   • API REST serverless")
    print(f"   • Diferentes patrones de tráfico")
    print(f"   • Operaciones CRUD en base de datos")
    
    # Diferentes patrones de tráfico mensual
    patrones = {
        'Tráfico bajo': {'requests_dia': 1000, 'memoria': 128, 'tiempo': 500},
        'Tráfico medio': {'requests_dia': 10000, 'memoria': 256, 'tiempo': 800},
        'Tráfico alto': {'requests_dia': 100000, 'memoria': 512, 'tiempo': 1200},
        'Viral/Pico': {'requests_dia': 1000000, 'memoria': 512, 'tiempo': 1200}
    }
    
    print(f"\n📊 COSTE MENSUAL POR PATRÓN DE TRÁFICO:")
    
    for nombre, config in patrones.items():
        requests_mes = config['requests_dia'] * 30
        sim = calcular_coste_aws_lambda(
            num_invocaciones=requests_mes,
            memoria_mb=config['memoria'],
            duracion_estimada_ms=config['tiempo']
        )
        print(f"   • {nombre:12s}: ${sim['total']['coste_total_usd']:8.2f}/mes "
              f"({requests_mes:7,} requests/mes)")


def generar_informe_costes(workload_name, simulacion, archivo_salida=None):
    """
    Genera un informe detallado en formato JSON
    """
    informe = {
        'timestamp': datetime.now().isoformat(),
        'workload': workload_name,
        'simulacion': simulacion,
        'recomendaciones': []
    }
    
    # Añadir recomendaciones basadas en el análisis
    coste_total = simulacion['total']['coste_total_usd']
    
    if coste_total == 0:
        informe['recomendaciones'].append("✅ Workload completamente dentro del free tier")
    elif coste_total < 0.01:
        informe['recomendaciones'].append("✅ Coste muy bajo - excelente para desarrollo")
    elif coste_total < 1.00:
        informe['recomendaciones'].append("⚠️ Coste moderado - monitorear en producción")
    else:
        informe['recomendaciones'].append("🔴 Coste alto - considerar optimizaciones")
    
    # Recomendaciones específicas
    lambda_info = simulacion['lambda']
    if lambda_info['gb_segundos_billables'] > 0:
        informe['recomendaciones'].append("💡 Optimizar duración o reducir memoria para reducir costes")
    
    if lambda_info['requests_billables'] > 100000:
        informe['recomendaciones'].append("💡 Considerar arquitectura híbrida para workloads muy grandes")
    
    if archivo_salida:
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(informe, f, indent=2, ensure_ascii=False)
        print(f"📄 Informe guardado en: {archivo_salida}")
    
    return informe


def main():
    """
    Función principal que ejecuta todos los ejemplos
    """
    print("🧮 EJEMPLOS DE SIMULACIÓN DE COSTES AWS LAMBDA")
    print("=" * 50)
    print("Este script muestra diferentes escenarios de uso y sus costes estimados.\n")
    
    # Ejecutar ejemplos
    ejemplo_procesamiento_imagenes()
    ejemplo_analisis_datos()
    ejemplo_machine_learning()
    ejemplo_api_serverless()
    
    # Resumen final
    print("\n" + "="*60)
    print("                    RESUMEN FINAL")
    print("="*60)
    print("📋 Puntos clave para optimización de costes:")
    print("   1. ⚡ Optimizar duración es más efectivo que reducir memoria")
    print("   2. 🎯 Aprovechar el free tier para desarrollo y testing")
    print("   3. 📊 Monitorear costes reales vs estimados")
    print("   4. 🔄 Considerar trade-offs memoria vs duración")
    print("   5. 📈 Planificar escalabilidad desde el inicio")
    print("\n🔗 Herramientas recomendadas:")
    print("   • AWS Cost Explorer para monitoreo")
    print("   • AWS Budgets para alertas")
    print("   • CloudWatch para métricas detalladas")
    print("="*60)


if __name__ == "__main__":
    main()
