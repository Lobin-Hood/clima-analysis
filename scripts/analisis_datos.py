#!/usr/bin/env python3
"""
Script de Análisis de Datos Climáticos
========================================

Objetivo: Procesar datos meteorológicos históricos y generar indicadores 
básicos de temperatura y precipitaciones.

Autor: Paco (P2 - Desarrollador Técnico)
Proyecto: Análisis de Datos Climáticos

Descripción de funcionalidades:
- Importar archivo CSV con registros de temperatura
- Calcular indicadores estadísticos (promedio, máximo, mínimo)
- Generar gráficos de evolución temporal
- Guardar resultados en formato CSV y PNG
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# Definir rutas relativas (funcionan en Google Colab)
BASE_DIR = Path(__file__).parent.parent
DATOS_DIR = BASE_DIR / "datos"
RESULTADOS_DIR = BASE_DIR / "resultados"

def cargar_datos(ruta_archivo):
    """
    Cargar datos climáticos desde un archivo CSV.
    
    Args:
        ruta_archivo (str): Ruta al archivo CSV
        
    Returns:
        pd.DataFrame: DataFrame con los datos cargados
        
    Raises:
        FileNotFoundError: Si el archivo no existe
    """
    try:
        df = pd.read_csv(ruta_archivo)
        print(f"✅ Datos cargados exitosamente desde: {ruta_archivo}")
        print(f"   Dimensiones: {df.shape[0]} filas, {df.shape[1]} columnas")
        return df
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {ruta_archivo}")
        raise


def procesar_datos(df):
    """
    Procesar y limpiar los datos climáticos.
    
    Se convierte la columna 'Year' a formato datetime y se separan
    año y mes para análisis posterior. Se eliminan filas con valores NaN.
    
    Args:
        df (pd.DataFrame): DataFrame original
        
    Returns:
        pd.DataFrame: DataFrame procesado
    """
    # Convertir columna Date a datetime
    df['Date'] = pd.to_datetime(df['Year'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    
    # Filtrar por fuente GISTEMP y limpiar nulos en 'Mean'
    df_limpio = df[df['Source'] == 'GISTEMP'].copy()
    df_limpio = df_limpio.dropna(subset=['Mean'])

    print(f"✅ Datos procesados")
    print(f"   Filas después de limpiar: {len(df_limpio)} (eliminadas {len(df) - len(df_limpio)})")
    
    return df_limpio


def calcular_indicadores(df):
    """
    Calcular indicadores estadísticos básicos de temperatura.
    
    Calcula:
    - Temperatura promedio (anomalía promedio)
    - Temperatura máxima (anomalía máxima)
    - Temperatura mínima (anomalía mínima)
    - Promedio por década
    
    Args:
        df (pd.DataFrame): DataFrame con datos procesados
        
    Returns:
        dict: Diccionario con indicadores calculados
    """
    indicadores = {
        'temperatura_promedio': df['Mean'].mean(),
        'temperatura_maxima': df['Mean'].max(),
        'temperatura_minima': df['Mean'].min(),
        'desviacion_estandar': df['Mean'].std(),
        'fecha_temperatura_maxima': df.loc[df['Mean'].idxmax(), 'Date'],
        'fecha_temperatura_minima': df.loc[df['Mean'].idxmin(), 'Date'],
    }
    
    # Calcular promedio por década
    df['Decada'] = (df['Year'] // 10) * 10
    promedio_decadas = df.groupby('Decada')['Mean'].mean()
    
    print(f"\n📊 INDICADORES CALCULADOS:")
    print(f"   Temperatura promedio: {indicadores['temperatura_promedio']:.4f}°C")
    print(f"   Temperatura máxima: {indicadores['temperatura_maxima']:.4f}°C ({indicadores['fecha_temperatura_maxima'].strftime('%Y-%m-%d')})")
    print(f"   Temperatura mínima: {indicadores['temperatura_minima']:.4f}°C ({indicadores['fecha_temperatura_minima'].strftime('%Y-%m-%d')})")
    print(f"   Desviación estándar: {indicadores['desviacion_estandar']:.4f}°C")
    
    print(f"\n📈 PROMEDIO POR DÉCADA:")
    for decada, valor in promedio_decadas.items():
        print(f"   {int(decada)}s: {valor:.4f}°C")
    
    return indicadores, promedio_decadas


def generar_grafico_temperatura(df, ruta_salida):
    """
    Generar gráfico de evolución de temperatura en el tiempo.
    
    Crea un gráfico de línea mostrando la anomalía de temperatura mensual
    a lo largo del tiempo, con tendencia superpuesta (suavizado).
    
    Args:
        df (pd.DataFrame): DataFrame con datos procesados
        ruta_salida (str): Ruta donde guardar el gráfico PNG
    """
    plt.figure(figsize=(14, 6))
    
    # Gráfico principal: temperatura mensual
    plt.plot(df['Date'], df['Mean'], 
             linewidth=0.8, alpha=0.6, label='Anomalía mensual')
    
    # Línea de tendencia (promedio móvil de 12 meses = 1 año)
    df_sorted = df.sort_values('Date')
    promedio_movil = df_sorted['Mean'].rolling(window=12).mean()
    plt.plot(df_sorted['Date'], promedio_movil, 
             linewidth=2.5, color='red', label='Tendencia (promedio anual)', alpha=0.8)
    
    # Línea de referencia en 0
    plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    
    # Etiquetas y titulo
    plt.xlabel('Año', fontsize=12, fontweight='bold')
    plt.ylabel('Anomalía de Temperatura (°C)', fontsize=12, fontweight='bold')
    plt.title('Evolución de la Anomalía de Temperatura Global (1880-2024)', 
              fontsize=14, fontweight='bold', pad=20)
    
    plt.legend(loc='upper left', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Guardar figura
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico guardado en: {ruta_salida}")
    plt.close()


def guardar_resultados(indicadores, promedio_decadas, ruta_salida_csv):
    """
    Guardar indicadores en archivo CSV para referencia futura.
    
    Args:
        indicadores (dict): Diccionario con indicadores calculados
        promedio_decadas (pd.Series): Series con promedio por década
        ruta_salida_csv (str): Ruta donde guardar el CSV
    """
    # Crear DataFrame con los indicadores
    resultados_df = pd.DataFrame({
        'Indicador': list(indicadores.keys()),
        'Valor': list(indicadores.values())
    })
    
    # Guardar a CSV
    resultados_df.to_csv(ruta_salida_csv, index=False, encoding='utf-8')
    print(f"✅ Resultados guardados en: {ruta_salida_csv}")
    
    # Guardar promedios por década
    promedio_decadas_df = pd.DataFrame({
        'Decada': promedio_decadas.index.astype(int),
        'Promedio_Anomalia_°C': promedio_decadas.values
    })
    
    ruta_decadas = RESULTADOS_DIR / "promedio_decadas.csv"
    promedio_decadas_df.to_csv(ruta_decadas, index=False, encoding='utf-8')
    print(f"✅ Promedios por década guardados en: {ruta_decadas}")


def main():
    """
    Función principal que ejecuta el flujo completo del análisis.
    """
    print("=" * 70)
    print("ANÁLISIS DE DATOS CLIMÁTICOS - TEMPERATURA GLOBAL")
    print("=" * 70)
    
    try:
        # 1. Cargar datos
        ruta_datos = DATOS_DIR / "temperatura_global.csv"
        df = cargar_datos(str(ruta_datos))
        
        # 2. Procesar datos
        df_procesado = procesar_datos(df)
        
        # 3. Calcular indicadores
        indicadores, promedio_decadas = calcular_indicadores(df_procesado)
        
        # 4. Generar gráfico
        ruta_grafico = RESULTADOS_DIR / "evolucion_temperatura.png"
        generar_grafico_temperatura(df_procesado, str(ruta_grafico))
        
        # 5. Guardar resultados
        ruta_csv_resultados = RESULTADOS_DIR / "indicadores_climaticos.csv"
        guardar_resultados(indicadores, promedio_decadas, str(ruta_csv_resultados))
        
        print("\n" + "=" * 70)
        print("✅ ANÁLISIS COMPLETADO EXITOSAMENTE")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error durante el análisis: {str(e)}")
        raise


if __name__ == "__main__":
    main()
