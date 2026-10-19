# Variables

## Identificación

| Variable | Tipo | Unidad |
|---|---|---|
| id_solinera | string | — |
| ubicacion | string | — |
| anio_puesta_marcha | int | año |
| tipo_instalacion | categórica | — |

## Técnicas

| Variable | Tipo | Unidad |
|---|---|---|
| num_paneles | int | — |
| potencia_pico_kwp | float | kWp |
| tecnologia_paneles | categórica | — |
| num_inversores | int | — |
| capacidad_baterias_kwh | float | kWh |
| tipo_baterias | categórica | — |
| seguimiento_solar | categórica | — |
| conexion_red | categórica | — |
| voltaje_operacion_v | float | V |

## Producción y consumo

| Variable | Tipo | Unidad |
|---|---|---|
| produccion_mensual_kwh | float | kWh |
| horas_sol_pico | float | h |
| perdidas_estimadas_kwh | float | kWh |
| consumo_total_anual_kwh | float | kWh |
| consumo_promedio_diario_kwh | float | kWh |
| energia_inyectada_anual_kwh | float | kWh |

## Derivadas

| Variable | Fórmula |
|---|---|
| kwh_por_kwp | consumo_total_anual / potencia_pico |
| antiguedad_anios | 2026 − anio_puesta_marcha |
| ratio_bateria_panel | capacidad_baterias / potencia_pico |
| pr_estimado | produccion_real / (potencia_pico × horas_sol_pico) |
