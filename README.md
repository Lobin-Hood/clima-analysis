# Análisis de Datos Climáticos

## 📋 Descripción del Proyecto

Este proyecto realiza un análisis estadístico de datos meteorológicos históricos para identificar tendencias en temperatura y precipitaciones a nivel global desde 1880 hasta la actualidad.

## 👥 Integrantes del Equipo

- **Hugo (P1):** Líder y Organizador - Estructura del proyecto y coordinación
- **Paco (P2):** Desarrollador Técnico - Lógica algorítmica y scripts de análisis
- **Luis (P3):** Revisor y QA - Documentación, revisión por pares e integración

## 🎯 Objetivo General

Analizar un conjunto de datos climáticos para generar **indicadores estadísticos básicos** que permitan:
- Entender las tendencias de temperatura global a lo largo del tiempo
- Identificar patrones de cambio climático
- Visualizar la evolución de la anomalía de temperatura

### Indicadores Calculados

1. **Temperatura Promedio (Anomalía):** Promedio de desviación respecto a la línea base
2. **Temperatura Máxima:** Anomalía más alta registrada
3. **Temperatura Mínima:** Anomalía más baja registrada
4. **Desviación Estándar:** Variabilidad de los datos
5. **Promedio por Década:** Tendencia por período de 10 años

## 📂 Estructura del Proyecto
clima-analysis/
├── datos/                          # Archivos CSV con datos climáticos
│   └── temperatura_global.csv      # Datos climáticos de temperatura
│
├── scripts/                        # Scripts de análisis (Python/R)
│   └── analisis_datos.py           # Script principal de análisis
│
├── resultados/                     # Gráficos y resultados generados
│   ├── evolucion_temperatura.png   # Gráfico principal
│   ├── indicadores_climaticos.csv  # Indicadores en formato tabla
│   └── promedio_decadas.csv        # Promedios por década
│
├── README.md                       # Este archivo
└── .gitignore                      # Archivo para excluir elementos de Git

## 📊 Dataset Utilizado

**Fuente:** Global Temperature Dataset (GISTEMP)  
**URL:** https://datahub.io/core/global-temp  
**Licencia:** CC0 (Dominio Público)

### Características del dataset:
- **Cobertura temporal:** 1880 - 2024 (más de 140 años)
- **Registros:** Datos mensuales
- **Formato:** CSV
- **Tamaño:** ~2000 registros

### Interpretación de Datos:
- **Anomalía:** Desviación respecto a una temperatura "normal" (línea base: 1951-1980)
- **Valores positivos:** Meses más cálidos que la línea base
- **Valores negativos:** Meses más fríos que la línea base

## 🚀 Instrucciones de Ejecución

### Requisitos previos:
- Python 3.8+
- Librerías: pandas, matplotlib, numpy