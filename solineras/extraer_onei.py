"""
Extrae datos de los Anuarios ONEI (Excel) y los convierte a Parquet.
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
    # Saltamos 8 filas de títulos
    df = pd.read_excel(ruta, skiprows=8)
    df = df.rename(columns={df.columns[0]: "anio"})
    df["anio"] = pd.to_numeric(df["anio"], errors="coerce")
    df = df[df["anio"].isin([2020, 2021, 2022])]
    
    # Buscar columnas de forma flexible
    col_total = next((c for c in df.columns if "Total" in str(c)), None)
    col_fv = next((c for c in df.columns if "Eólica" in str(c) or "Fotov" in str(c)), None)
    
    if col_total and col_fv:
        df_clean = df[["anio", col_total, col_fv]].copy()
        df_clean.columns = ["anio", "gen_total_gwh", "gen_fv_gwh"]
        df_clean.to_parquet(OUT_DIR / "onei_generacion.parquet", index=False)
        print("OK Generación guardada.")
    else:
        print("ERROR en columnas de 10.16")

def extraer_consumo():
    ruta = RAW_DIR / "10.19_consumo.xls"
    if not ruta.exists(): return
    df = pd.read_excel(ruta, skiprows=7)
    df = df.rename(columns={df.columns[0]: "anio"})
    df["anio"] = pd.to_numeric(df["anio"], errors="coerce")
    df = df[df["anio"].isin([2020, 2021, 2022])]
    
    col_total = next((c for c in df.columns if "Total" in str(c)), None)
    col_pob = next((c for c in df.columns if "Población" in str(c)), None)
    col_perd = next((c for c in df.columns if "Pérdidas" in str(c) or "Perdidas" in str(c)), None)
    
    if col_total and col_pob and col_perd:
        df_clean = df[["anio", col_total, col_pob, col_perd]].copy()
        df_clean.columns = ["anio", "consumo_total_gwh", "consumo_poblacion_gwh", "perdidas_gwh"]
        df_clean.to_parquet(OUT_DIR / "onei_consumo.parquet", index=False)
        print("OK Consumo guardado.")
    else:
        print("ERROR en columnas de 10.19")

def extraer_potencia():
    ruta = RAW_DIR / "10.18_potencia.xls"
    if not ruta.exists(): return
    # Este Excel tiene la tabla principal a la izquierda (A hasta J)
    df = pd.read_excel(ruta, skiprows=8, usecols="A:J")
    df = df.rename(columns={df.columns[0]: "anio"})
    df["anio"] = pd.to_numeric(df["anio"], errors="coerce")
    df = df[df["anio"].isin([2020, 2021, 2022])]
    
    col_fv = next((c for c in df.columns if "fotov" in str(c).lower() or "eólicos" in str(c).lower()), None)
    
    if col_fv:
        df_clean = df[["anio", col_fv]].copy()
        df_clean.columns = ["anio", "potencia_fv_mw"]
        df_clean.to_parquet(OUT_DIR / "onei_potencia.parquet", index=False)
        print("OK Potencia guardada.")
    else:
        print("ADVERTENCIA: No se encontró columna FV en 10.18 (pero el archivo está a salvo)")

if __name__ == "__main__":
    print("=== INICIANDO EXTRACCIÓN ONEI ===")
    extraer_generacion()
    extraer_consumo()
    extraer_potencia()
    print("=== FINALIZADO ===")
