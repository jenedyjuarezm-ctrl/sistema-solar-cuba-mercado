# Datos Oficiales de la ONEI (Oficina Nacional de Estadística e Información)

Esta carpeta está destinada a contener los archivos Excel originales descargados del *Anuario Estadístico de Cuba: Minería y Energía*.

## ⚠️ Nota sobre los archivos:
Los archivos `.xls` y `.xlsx` **NO se suben a este repositorio** por las siguientes razones:
1. Son archivos binarios que no se pueden visualizar correctamente en la web de GitHub.
2. Contienen fórmulas y macros de Excel que Python no debe procesar directamente.

## ¿Cómo se procesan estos datos?
En lugar de analizar el Excel, el proyecto utiliza un pipeline ETL (Extracción, Transformación y Carga):
1. El script `solineras/extraer_onei.py` lee localmente los Excel, filtra los años (2020-2024), limpia las cabeceras y los convierte a formato `.parquet`.
2. El resultado se guarda en `data/clean/onei_generacion.parquet` y `data/clean/onei_consumo.parquet`.
3. Los notebooks y el Dashboard trabajan únicamente con los archivos limpios en Parquet.

## ¿Cómo replicar la descarga?
Si necesitas descargar los datos originales, puedes hacerlo desde el sitio web oficial de la ONEI:
*   Buscar: "Anuario Estadístico de Cuba [Año] - Capítulo 10: Minería y Energía".
*   Descargar los cuadros: 10.13, 10.14, 10.15, 10.16, 10.18 y 10.19.
*   Renombrarlos como se indica en el script de extracción y colocarlos en esta carpeta antes de ejecutar `extraer_onei.py`.
