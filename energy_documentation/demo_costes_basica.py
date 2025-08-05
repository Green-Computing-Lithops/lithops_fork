#!/usr/bin/env python3
"""
Simulación directa de costes para tu función básica
==================================================
"""

def calcular_coste_aws_lambda(num_invocaciones, memoria_mb=128, duracion_estimada_ms=1000, region='us-east-1'):
    """
    Calcula el coste estimado de ejecutar funciones Lambda en AWS
    """
    
    # Pricing de AWS Lambda (us-east-1) - Julio 2025
    coste_por_request = 0.20 / 1_000_000  # $0.20 por millón de requests
    coste_por_gb_segundo = 0.0000166667   # $0.0000166667 por GB-segundo
    
    # Free tier: 1M requests gratuitos y 400,000 GB-segundos por mes
    free_requests = 1_000_000
    free_gb_seconds = 400_000
    
    # Convertir memoria a GB
    memoria_gb = memoria_mb / 1024
    
    # Calcular duración en segundos
    duracion_segundos = duracion_estimada_ms / 1000
    
    # Calcular GB-segundos totales
    gb_segundos_totales = num_invocaciones * memoria_gb * duracion_segundos
    
    # Calcular requests billables (después del free tier)
    requests_billables = max(0, num_invocaciones - free_requests)
    
    # Calcular GB-segundos billables (después del free tier)
    gb_segundos_billables = max(0, gb_segundos_totales - free_gb_seconds)
    
    # Calcular costes
    coste_requests = requests_billables * coste_por_request
    coste_compute = gb_segundos_billables * coste_por_gb_segundo
    coste_total = coste_requests + coste_compute
    
    # Estimar coste de S3 (storage y operaciones)
    s3_put_requests = num_invocaciones  # 1 PUT por invocación
    s3_get_requests = num_invocaciones * 2  # 1 GET para list_keys + 1 GET para get_object
    
    coste_s3_puts = (s3_put_requests / 1000) * 0.0005
    coste_s3_gets = (s3_get_requests / 1000) * 0.0004
    coste_s3_storage = 0.001  # Estimado para archivos muy pequeños (<1MB total)
    coste_s3_total = coste_s3_puts + coste_s3_gets + coste_s3_storage
    
    coste_total_con_s3 = coste_total + coste_s3_total
    
    resultado = {
        'configuracion': {
            'invocaciones': num_invocaciones,
            'memoria_mb': memoria_mb,
            'duracion_estimada_ms': duracion_estimada_ms,
            'region': region
        },
        'lambda': {
            'requests_totales': num_invocaciones,
            'requests_free_tier': min(num_invocaciones, free_requests),
            'requests_billables': requests_billables,
            'gb_segundos_totales': round(gb_segundos_totales, 6),
            'gb_segundos_free_tier': min(gb_segundos_totales, free_gb_seconds),
            'gb_segundos_billables': round(gb_segundos_billables, 6),
            'coste_requests_usd': round(coste_requests, 6),
            'coste_compute_usd': round(coste_compute, 6),
            'coste_lambda_total_usd': round(coste_total, 6)
        },
        's3': {
            'put_requests': s3_put_requests,
            'get_requests': s3_get_requests,
            'coste_puts_usd': round(coste_s3_puts, 6),
            'coste_gets_usd': round(coste_s3_gets, 6),
            'coste_storage_usd': round(coste_s3_storage, 6),
            'coste_s3_total_usd': round(coste_s3_total, 6)
        },
        'total': {
            'coste_total_usd': round(coste_total_con_s3, 6),
            'coste_total_eur': round(coste_total_con_s3 * 0.92, 6)  # Conversión aproximada USD->EUR
        }
    }
    
    return resultado


def mostrar_simulacion_costes(resultado):
    """
    Muestra de forma legible la simulación de costes
    """
    print("\n" + "="*60)
    print("         SIMULACIÓN DE COSTES AWS LAMBDA + S3")
    print("="*60)
    
    config = resultado['configuracion']
    print(f"\n📊 CONFIGURACIÓN:")
    print(f"   • Invocaciones: {config['invocaciones']:,}")
    print(f"   • Memoria: {config['memoria_mb']} MB")
    print(f"   • Duración estimada: {config['duracion_estimada_ms']} ms")
    print(f"   • Región: {config['region']}")
    
    lambda_info = resultado['lambda']
    print(f"\n🔧 AWS LAMBDA:")
    print(f"   • Requests totales: {lambda_info['requests_totales']:,}")
    print(f"   • Requests free tier: {lambda_info['requests_free_tier']:,}")
    print(f"   • Requests facturables: {lambda_info['requests_billables']:,}")
    print(f"   • GB-segundos totales: {lambda_info['gb_segundos_totales']}")
    print(f"   • GB-segundos free tier: {lambda_info['gb_segundos_free_tier']}")
    print(f"   • GB-segundos facturables: {lambda_info['gb_segundos_billables']}")
    print(f"   • Coste requests: ${lambda_info['coste_requests_usd']}")
    print(f"   • Coste compute: ${lambda_info['coste_compute_usd']}")
    print(f"   • Coste Lambda total: ${lambda_info['coste_lambda_total_usd']}")
    
    s3_info = resultado['s3']
    print(f"\n💾 AWS S3:")
    print(f"   • PUT requests: {s3_info['put_requests']:,}")
    print(f"   • GET requests: {s3_info['get_requests']:,}")
    print(f"   • Coste PUTs: ${s3_info['coste_puts_usd']}")
    print(f"   • Coste GETs: ${s3_info['coste_gets_usd']}")
    print(f"   • Coste storage: ${s3_info['coste_storage_usd']}")
    print(f"   • Coste S3 total: ${s3_info['coste_s3_total_usd']}")
    
    total = resultado['total']
    print(f"\n💰 COSTE TOTAL ESTIMADO:")
    print(f"   • USD: ${total['coste_total_usd']}")
    print(f"   • EUR: €{total['coste_total_eur']} (aprox.)")
    
    if total['coste_total_usd'] == 0:
        print(f"\n✅ ¡Excelente! Tu ejecución está dentro del free tier de AWS!")
    elif total['coste_total_usd'] < 0.01:
        print(f"\n✅ Coste muy bajo - menos de $0.01")
    elif total['coste_total_usd'] < 1.00:
        print(f"\n⚠️  Coste moderado - menos de $1.00")
    else:
        print(f"\n⚠️  Coste significativo - más de $1.00")
    
    print("="*60 + "\n")


def simular_funcion_basica():
    """
    Simula exactamente tu función básica de main_german.py
    """
    print("🎯 SIMULACIÓN DE TU FUNCIÓN BÁSICA")
    print("=" * 35)
    print("Función: funcion_german(x)")
    print("Operaciones:")
    print("  • Crear Storage()")
    print("  • PUT object en S3")
    print("  • LIST keys en S3")  
    print("  • GET object de S3")
    print("  • Return x + 1")
    print("Datos: [1, 2, 3] (3 invocaciones)\n")
    
    # Configuración actual de tu función
    num_invocaciones = 3  # [1, 2, 3]
    memoria_mb = 128  # Default de Lambda
    duracion_estimada_ms = 2000  # Estimación realista con operaciones S3
    
    resultado = calcular_coste_aws_lambda(
        num_invocaciones=num_invocaciones,
        memoria_mb=memoria_mb,
        duracion_estimada_ms=duracion_estimada_ms
    )
    
    mostrar_simulacion_costes(resultado)
    
    return resultado


def comparar_escalas():
    """
    Compara costes para diferentes escalas de datos
    """
    print("📈 COMPARACIÓN POR ESCALAS")
    print("=" * 30)
    
    escalas = [
        {'datos': [1, 2, 3], 'descripcion': 'Tu función actual'},
        {'datos': list(range(1, 11)), 'descripcion': '10 elementos'},
        {'datos': list(range(1, 101)), 'descripcion': '100 elementos'},
        {'datos': list(range(1, 1001)), 'descripcion': '1,000 elementos'},
        {'datos': list(range(1, 10001)), 'descripcion': '10,000 elementos'}
    ]
    
    print("Coste por escala:")
    print("-" * 40)
    
    for escala in escalas:
        num_invocaciones = len(escala['datos'])
        resultado = calcular_coste_aws_lambda(
            num_invocaciones=num_invocaciones,
            memoria_mb=128,
            duracion_estimada_ms=2000
        )
        
        coste = resultado['total']['coste_total_usd']
        print(f"   {escala['descripcion']:20s}: ${coste:8.6f}")


def comparar_optimizaciones():
    """
    Compara diferentes optimizaciones posibles
    """
    print("\n🚀 OPTIMIZACIONES POSIBLES")
    print("=" * 30)
    
    optimizaciones = [
        {
            'nombre': 'Actual (sin optimizar)',
            'memoria': 128,
            'duracion': 2000,
            'descripcion': 'Tu configuración actual'
        },
        {
            'nombre': 'Código optimizado',
            'memoria': 128,
            'duracion': 1000,
            'descripcion': 'Mismo hardware, código más eficiente'
        },
        {
            'nombre': 'Más memoria',
            'memoria': 256,
            'duracion': 1500,
            'descripcion': 'Más memoria para mayor velocidad'
        },
        {
            'nombre': 'Mucha más memoria',
            'memoria': 512,
            'duracion': 1000,
            'descripcion': 'Memoria alta para máxima velocidad'
        }
    ]
    
    print("Comparación de optimizaciones (3 invocaciones):")
    print("-" * 50)
    
    for opt in optimizaciones:
        resultado = calcular_coste_aws_lambda(
            num_invocaciones=3,
            memoria_mb=opt['memoria'],
            duracion_estimada_ms=opt['duracion']
        )
        
        coste = resultado['total']['coste_total_usd']
        print(f"   {opt['nombre']:20s}: ${coste:8.6f} - {opt['descripcion']}")


if __name__ == "__main__":
    # Simular tu función básica
    resultado_basico = simular_funcion_basica()
    
    # Mostrar comparaciones
    comparar_escalas()
    comparar_optimizaciones()
    
    # Análisis final
    print("\n🎯 ANÁLISIS PARA TU FUNCIÓN:")
    print("=" * 30)
    if resultado_basico['total']['coste_total_usd'] == 0:
        print("✅ Tu función actual está completamente dentro del FREE TIER")
        print("   Puedes ejecutarla miles de veces sin coste")
    else:
        print(f"💰 Coste actual: ${resultado_basico['total']['coste_total_usd']}")
    
    print("\n💡 RECOMENDACIONES:")
    print("   1. Para desarrollo/testing: ✅ Perfecto, coste mínimo")
    print("   2. Para producción: Considera optimizar duración")
    print("   3. Para escalabilidad: Monitorea cuando superes 1000+ invocaciones")
