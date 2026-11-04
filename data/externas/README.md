# Fuentes Externas (Datos Secundarios)

Esta carpeta contiene los datos descargados de organismos internacionales y fuentes oficiales, utilizados para triangular y validar la información recolectada en el campo.

## 📊 Inventario de Archivos

### 1. `nasa_power.csv`
*   **Fuente:** NASA POWER (Prediction Of Worldwide Energy Resources).
*   **Descripción:** Datos meteorológicos satelitales mensuales para La Habana (Latitud 23.13, Longitud -82.38).
*   **Período:** Enero 2020 - Diciembre 2024.
*   **Variables incluidas:**
    *   `ALLSKY_SFC_SW_DWN`: Irradiancia solar (kWh/m²/día).
    *   `T2M`: Temperatura ambiente a 2 metros (°C).
    *   `RH2M`: Humedad relativa (%).
*   **Uso en el proyecto:** Calcular el Performance Ratio (PR) de los paneles, justificar pérdidas de eficiencia por calor extremo y contextualizar las condiciones climáticas del país.

### 2. `onei_anuario.csv`
*   **Fuente:** Oficina Nacional de Estadística e Información (ONEI) - Anuario Estadístico de Cuba.
*   **Descripción:** Datos macroeconómicos del sector energético nacional.
*   **Período:** 2020 - 2024 (Extraído de los Anuarios 2021 al 2024).
*   **Variables incluidas:**
    *   Generación bruta de electricidad (Total y Renovable).
    *   Potencia instalada en plantas eléctricas (MW).
    *   Consumo de energía eléctrica (GWh).
*   **Uso en el proyecto:** Análisis de series temporales, cálculo de la matriz energética y pronóstico de la generación renovable.

### 3. `revolico_scraping.csv`
*   **Fuente:** Revolico.com (Mercado informal cubano).
*   **Descripción:** Datos extraídos mediante *Web Scraping* (script `solineras/scraping_revolico.py`).
*   **Variables incluidas:** Títulos de anuncios, precios de paneles, inversores y baterías.
*   **Uso en el proyecto:** Análisis económico del costo real de los equipos en el mercado informal y estimación del retorno de inversión (ROI).

## ⚠️ Nota Metodológica
Los archivos `.csv` en esta carpeta son la **materia prima secundaria**. No se analizan directamente. El script `solineras/extraer_onei.py` y los notebooks de Jupyter se encargan de limpiar y procesar esta información para convertirla en archivos `.parquet` optimizados.
