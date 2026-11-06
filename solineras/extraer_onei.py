import pandas as pd
from pathlib import Path

BASE = Path(__file__).parent.parent
RAW_DIR = BASE / "data" / "raw" / "externas" / "onei"
OUT_DIR = BASE / "data" / "clean"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def extraer_generacion():
    ruta = RAW_DIR / "10.16_planta.xls"
    if not ruta.exists():
        print(f"[WARN] No existe {ruta.name}")
        return
    try:
        # En el 10.16, los datos reales empiezan en la fila 9 (índice 8)
        df = pd.read_excel(ruta, skiprows=8)
        
        # La primera columna es el año
        df = df.rename(columns={df.columns[0]: "anio"})
        
        # En este Excel, la columna 1 (Total) y la columna 9 (Eólica y Fotov) son las que queremos
        # Usamos iloc para tomar por posición y evitar errores de nombres
        df_clean = df.iloc[:, [0, 1, 9]].copy()
        df_clean.columns = ["anio", "gen_total_gwh", "gen_fv_gwh"]
        
        # Limpiar años (quitar nulos y dejar 2020, 2021, 2022)
        df_clean["anio"] = pd.to_numeric(df_clean["anio"], errors="coerce")
        df_clean = df_clean[df_clean["anio"].isin([2020, 2021, 2022])]
        
        df_clean.to_parquet(OUT_DIR / "onei_generacion.parquet", index=False)
        print("OK Generación guardada en Parquet.")
    except Exception as e:
        print(f"[ERROR] Falló generación: {e}")

def extraer_consumo():
    ruta = RAW_DIR / "10.19_consumo.xls"
    if not ruta.exists():
        print(f"[WARN] No existe {ruta.name}")
        return
    try:
        # En el 10.19, los datos reales empiezan en la fila 8 (índice 7)
        df = pd.read_excel(ruta, skiprows=7)
        
        df = df.rename(columns={df.columns[0]: "anio"})
        
        # Columna 1 (Total), Columna 10 (Población), Columna 11 (Pérdidas)
        df_clean = df.iloc[:, [0, 1, 10, 11]].copy()
        df_clean.columns = ["anio", "consumo_total_gwh", "consumo_poblacion_gwh", "perdidas_gwh"]
        
        df_clean["anio"] = pd.to_numeric(df_clean["anio"], errors="coerce")
        df_clean = df_clean[df_clean["anio"].isin([2020, 2021, 2022])]
        
        df_clean.to_parquet(OUT_DIR / "onei_consumo.parquet", index=False)
        print("OK Consumo guardado en Parquet.")
    except Exception as e:
        print(f"[ERROR] Falló consumo: {e}")

def extraer_todo():
    print("=== INICIANDO EXTRACCIÓN DE DATOS ONEI ===")
    extraer_generacion()
    extraer_consumo()
    print("=== EXTRACCIÓN FINALIZADA ===")

if __name__ == "__main__":
    extraer_todo()
