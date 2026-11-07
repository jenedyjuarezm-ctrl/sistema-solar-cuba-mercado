# 📉 Análisis de Datos: Transición Solar en Cuba (2020-2026)

**Autor:** [Tu Nombre]
**Materia:** Ciencia de Datos (Primer Proyecto)

##  Resumen del Proyecto
Este repositorio contiene el pipeline de datos (ETL), los análisis estadísticos, los cuadernos de Jupyter y el Dashboard interactivo desarrollados para investigar la crisis energética en Cuba y la respuesta ciudadana mediante paneles solares. El estudio triangula datos oficiales de la ONEI, datos climáticos de la NASA, registros OSINT y 32 entrevistas primarias validadas.

##  Resultados Principales
*   **Paradoja de la Eficiencia:** La potencia FV instalada creció un 18.7% (2020-2022), pero la generación real cayó un 7.4%.
*   **Brecha de Transparencia:** El 90% de los centros estatales negaron datos, en contraste con la apertura del sector privado y residencial.
*   **Motivación Ciudadana:** El 100% de los 32 residentes encuestados afirmó que su motivación no fue el ahorro, sino la **supervivencia** ante los apagones.

👉 **[Haz clic aquí para leer el Informe Técnico Final en PDF](docs/Informe_Tecnico_Final_Cuba_Solar_2026.pdf)**

## 📊 Visualizaciones Clave
![Gráfica 1: Crisis ONEI](docs/img/grafica_1_onei.png)
![Gráfica 2: Potencia por Sector](docs/img/grafica_2_potencia.png)
![Gráfica 4: Motivaciones](docs/img/grafica_4_motivaciones.png)

## ⚙️ Estructura del Repositorio
*   `data/`: Datos crudos (JSONL) y resultados limpios (CSV).
*   `solineras/`: Código fuente en Python (Scripts ETL y Dashboard).
*   `notebooks/`: Cuadernos de Jupyter con el análisis exploratorio.
*   `evidencias/`: Fotos de etiquetas de equipos (validación de datos).
*   `docs/`: Informe final en PDF, documentación y gráficas.

## 🚀 Cómo ejecutar el pipeline
1. Instalar dependencias: `pip install -r requirements.txt`
2. Ejecutar el pipeline ETL y de análisis: `python solineras/run_all.py`
3. Abrir el Dashboard interactivo: `streamlit run solineras/dashboard.py`
