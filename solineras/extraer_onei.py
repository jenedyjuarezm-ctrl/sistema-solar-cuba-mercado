"""
Extrae datos de los Anuarios ONEI (Excel) basándose en la posición exacta
de las columnas para evitar errores de celdas combinadas.
"""
import pandas as pd
from pathlib import Path

BASE = Path(__file__).parent.parent
RAW_DIR = BASE / "data" / "raw" / "externas" / "onei"
OUT_DIR = BASE / "data" / "clean"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def extraer_generacion():
    ruta = RAW_DIR / "10.16_planta.xls"
    if not ruta.exists(): return
    # Saltamos 10 filas (títulos combinados) y leemos todo
    df = pd.read_excel(ruta, skiprows=10, header=None)
    
    # En este Excel, el año está en la col A (0), Total en la B (1), Eólica en la K (10)
    # Filtramos las filas que tengan un año válido
    df = df[[0, 1, 10]]
    df.columns = ["anio", "gen_total_gwh", "gen_fv_gwh"]
    df["anio"] = pd.to_numeric(df["anio"], errors="coerce")
    df = df.dropna(subset=["anio"])
    df = df[df["anio"].isin([2020, 2021, 2022])]
    
    if not df.empty:
        df.to_parquet(OUT_DIR / "onei_generacion.parquet", index=False)
        print("✅ OK Generación guardada.")

def extraer_consumo():
    ruta = RAW_DIR / "10.19_consumo.xls"
    if not ruta.exists(): return
    df = pd.read_excel(ruta, skiprows=7, header=None)
    
    # Año en A (0), Total en B (1), Población en K (10), Pérdidas en L (11)
    df = df[[0, 1, 10, 11]]
    df.columns = ["anio", "consumo_total_gwh", "consumo_poblacion_gwh", "perdidas_gwh"]
    df["anio"] = pd.to_numeric(df["anio"], errors="coerce")
    df = df.dropna(subset=["anio"])
    df = df[df["anio"].isin([2020, 2021, 2022])]
    
    if not df.empty:
        df.to_parquet(OUT_DIR / "onei_consumo.parquet", index=False)
        print("✅ OK Consumo guardado.")

def extraer_potencia():
    ruta = RAW_DIR / "10.18_potencia.xls"
    if not ruta.exists(): return
    # La tabla de potencia está a la derecha del todo. Leemos desde la columna V (índice 21)
    df = pd.read_excel(ruta, skiprows=10, header=None, usecols=[21, 22, 29])
    
    # Año en V (0), Total en W (1), Parques FV en AD (8)
    df.columns = ["anio", "potencia_total_mw", "potencia_fv_mw"]
    df["anio"] = pd.to_numeric(df["anio"], errors="coerce")
    df = df.dropna(subset=["anio"])
    df = df[df["anio"].isin([2020, 2021, 2022])]
    
    if not df.empty:
        # Nos quedamos solo con el año y la FV
        df_final = df[["anio", "potencia_fv_mw"]]
        df_final.to_parquet(OUT_DIR / "onei_potencia.parquet", index=False)
        print("✅ OK Potencia guardada.")

def extraer_todo():
    print("=== EXTRAYENDO ONEI ===")
    extraer_generacion()
    extraer_consumo()
    extraer_potencia()

if __name__ == "__main__":
    extraer_todo()
