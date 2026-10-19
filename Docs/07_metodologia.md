## Metodologia 
 
 # Enfoque general 
 Investigacion **mixta** (cuantitativa + caulitativa) con 
 alcance descriptivo - exploratorio


## Fases

1. **Recolección**
   - Entrevistas estructuradas (formularios HTML) ( plantillas)
   - Descarga de anuarios ONEI.
   - Consulta APIs (NASA POWER, IRENA).
   - Scraping controlado (Revolico).

2. **Validación**
   - JSON Schema por tipo de documento.
   - Umbral mínimo: 30 muestras por fuente.

3. **Consolidación**
   - Aplanado a formato tabular.
   - Variables derivadas.
   - Guardado en Parquet.

4. **Análisis**
   - Descriptivo (medianas, IQR, outliers).
   - Comparativo (Kruskal-Wallis, Mann-Whitney).
   - Correlacional (Spearman).
   - Cualitativo (codificación temática).
   - Predictivo (regresión lineal).
   - Bootstrap para IC de medianas.

5. **Visualización**
   - Notebooks Jupyter por análisis.
   - Dashboard Streamlit.
   - Reportes PDF por solinera.

6. **Storytelling**
   - Narrativa en 5 actos.
   - Tablas con título con verbo.

## Control de calidad

- JSON Schema por tipo de documento.
- Auditoría automática de cobertura.
- Tests con `test_entorno.py`.

## Reproducibilidad

python solineras/run_all.py



# Métodos Cuantitativos

| Método | Uso |
| :--- | :--- |
| Media, mediana, moda | Tendencias centrales |
| Desviación estándar | Dispersión de datos |
| Series temporales | Evolución anual |
| Correlación | Relación entre variables |

# Métodos Cualitativos

| Método | Uso |
| :--- | :--- |
| Entrevistas estructuradas | Formularios diseñados para técnicos y personal |
| Análisis temáticos | Patrones en respuestas |
| Triangulación | Validar hallazgos |

# Herramientas

| Herramienta | Uso |
| :--- | :--- |
| Python (pandas, matplotlib, seaborn) | Análisis de datos y visualización |
| Jupyter | Análisis interactivo |
| Git/GitHub | Control de versiones |
| OpenCode | Asistencia con IA |
| CSV | Datos tabulares |



Limitaciones previstas 
- Acceso limitado a datos oficiales 
- Posible desactualización de cifras
- Recursos computacionales limitados
- Tiempo acotado por el semestre 
