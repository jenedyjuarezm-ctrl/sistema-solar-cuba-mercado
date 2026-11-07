# Pregunta principal
"¿Cómo ha evolucionado la transición energética fotovoltaica en Cuba (2020-2026), y de qué manera la crisis del sistema eléctrico estatal ha impulsado la adopción de sistemas solares autónomos (residenciales y privados) como una estrategia de resiliencia ciudadana?"

# Preguntas de Investigación 
Este proyecto de ciencia de datos se estructuró en torno a 5 preguntas centrales, diseñadas para ser respondidas mediante la triangulación de datos oficiales (ONEI), satelitales (NASA) y de campo (32 residencias y 64 registros web).

## 1. ¿Cómo ha evolucionado la generación fotovoltaica en Cuba y cuál es su peso en la matriz energética (2020-2022)?
*   **Respuesta corta:** La generación FV se mantuvo resiliente en torno a los 240 GW·h, pero representa apenas el 1.5% de la matriz total, la cual cayó un 17.5%.
*   **Fuente/Análisis:** Cuadros 10.16 y 10.15 de la ONEI.

## 2. ¿Existe una brecha entre la potencia instalada y la energía realmente generada (Paradoja de la Eficiencia)?
*   **Respuesta corta:** Sí, es el hallazgo principal. La potencia FV instalada creció un 18.7% (221.5 a 263 MW), pero la generación real cayó un 7.4% (260.8 a 241.5 GW·h). Esto evidencia problemas de mantenimiento o degradación por clima.
*   **Fuente/Análisis:** Cruce de los cuadros 10.18 y 10.16 de la ONEI.

## 3. ¿Cómo se comparan los usuarios del sector privado (locales) con los del sector residencial en inversión y satisfacción?
*   **Respuesta corta:** Los locales privados invierten en sistemas de mayor potencia (mediana de 4.5 kWp) en comparación con las residencias (2.0 kWp). El sector privado busca continuidad de negocio, mientras el residencial busca supervivencia.
*   **Fuente/Análisis:** Entrevistas primarias (JSONL de residentes) y datos web (OSINT).

## 4. ¿Cuáles son los principales desafíos y motivaciones de los usuarios de energía solar en Cuba?
*   **Respuesta corta:** El 100% de los residentes afirmó que su motivación principal no fue el ahorro económico, sino la **supervivencia** ante los apagones. El principal desafío es la falta de repuestos y baterías de litio.
*   **Fuente/Análisis:** Análisis cualitativo de la Sección E de las entrevistas.

## 5. ¿Cómo influyen las condiciones climáticas en el rendimiento de los paneles según la zona?
*   **Respuesta corta:** Cuba tiene una irradiancia excelente (hasta 6.7 kWh/m²), pero las temperaturas extremas de 30°C en verano y la humedad superior al 80% reducen la eficiencia de los paneles y aceleran su degradación.
*   **Fuente/Análisis:** Datos satelitales mensuales de NASA POWER cruzados con los datos de generación.
