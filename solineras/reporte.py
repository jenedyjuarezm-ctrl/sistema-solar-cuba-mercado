"""
Genera un reporte ejecutivo rápido por consola basado en el dataset consolidado.
No genera PDFs para evitar fallos por falta de gráficos temporales.
"""
from pathlib import Path
import pandas as pd

DATA = Path(__file__).parent.parent / "data"
CLEAN = DATA / "clean"

def generar_reporte():
    f = CLEAN / "encuestas_consolidadas.parquet"
    if not f.exists():
        print("⚠️ No existe el archivo consolidado. Ejecuta consolidar.py primero.")
        return

    df = pd.read_parquet(f)
    
    print("\n" + "="*50)
    print("📊 REPORTE EJECUTIVO - TRANSICIÓN SOLAR EN CUBA")
    print("="*50)
    
    # 1. Resumen por tipo de entidad
    print("\n--- 1. CANTIDAD DE ENTIDADES ANALIZADAS ---")
    conteo = df["tipo_entidad"].value_counts()
    for tipo, cantidad in conteo.items():
        print(f"  - {tipo.title()}: {cantidad} registros")

    # 2. KPIs de Residentes (Datos primarios)
    print("\n--- 2. INDICADORES CLAVE (RESIDENTES) ---")
    df_res = df[df["tipo_entidad"] == "residente"]
    if not df_res.empty:
        pot_media = df_res["potencia_pico_kwp"].median()
        bat_media = df_res["capacidad_baterias_kwh"].median()
        print(f"  - Potencia Mediana Instalada: {pot_media:.2f} kWp")
        print(f"  - Batería Mediana: {bat_media:.2f} kWh")
    else:
        print("  No hay datos de residentes.")

    # 3. KPIs de la ONEI (Macro)
    print("\n--- 3. CONTEXTO MACRO (ONEI 2020-2022) ---")
    onei_path = CLEAN / "onei_generacion.parquet"
    if onei_path.exists():
        onei = pd.read_parquet(onei_path)
        caida = onei["gen_total_gwh"].iloc[-1] - onei["gen_total_gwh"].iloc[0]
        print(f"  - Variación de Generación Total (2020-2022): {caida:,.0f} GW·h")
    else:
        print("  No hay datos de la ONEI.")

    # 4. Correlaciones Clima (NASA)
    print("\n--- 4. CORRELACIONES CLIMÁTICAS ---")
    corr_path = DATA / "analisis" / "correlaciones_clima.csv"
    if corr_path.exists():
        corr = pd.read_csv(corr_path)
        for _, row in corr.iterrows():
            print(f"  - {row['variable_climatica']}: rho = {row['rho']} (p={row['p_valor']})")
    else:
        print("  No se han generado las correlaciones aún.")

    print("\n" + "="*50)
    print("✅ Reporte finalizado.")

if __name__ == "__main__":
    generar_reporte()
