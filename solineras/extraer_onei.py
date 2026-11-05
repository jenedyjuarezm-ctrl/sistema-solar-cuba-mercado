"""
Extrae datos de los Anuarios ONEI (archivos Excel .xls) y los convierte a formato Parquet.
Este script lee los archivos crudos de data/raw/externas/onei/ y guarda
los datos limpios de 2020 a 2022 en data/clean/.
"""
import pandas as pd
from pathlib import Path

# Definir rutas absolutas para que funcione desde cualquier carpeta
BASE = Path(__file__).parent.parent
RAW_DIR = BASE / "data" / "raw" / "externas" / "onei"
OUT_DIR = BASE / "data" / "clean"

# Crear la carpeta de salida si no existe
OUT_DIR.mkdir(parents=True, exist_ok=True)


def extraer_generacion():
    """Lee 10.16_planta.xls y extrae la generación FV y total."""
    ruta = RAW_DIR / "10.16_planta.xls"
    if not ruta.exists():
        print(f"[WARN] No se encontró el archivo: {ruta.name}")
        return

    try:
        # Saltamos las primeras 8 filas que son títulos de la ONEI
        df = pd.read_excel(ruta, skiprows=8)
        
        # La primera columna siempre es el año, la renombramos
        df = df.rename(columns={df.columns[0]: "anio"})
        
        # Convertir a número y filtrar solo los años que nos interesan
        df["anio"] = pd.to_numeric(df["anio"], errors="coerce")
        df = df[df["anio"].isin([2020, 2021, 2022, 2023, 2024])]
        
        # Buscar las columnas por coincidencia de texto
        col_total = next((c for c in df.columns if "Total" in str(c)), None)
        col_fv = next((c for c in df.columns if "Eólica" in str(c) or "Fotov" in str(c)), None)
        
        if col_total and col_fv:
            df_clean = df[["anio", col_total, col_fv]].copy()
            # Renombrar con nombres limpios para el análisis
            df_clean.columns = ["anio", "gen_total_gwh", "gen_fv_gwh"]
            df_clean.to_parquet(OUT_DIR / "onei_generacion.parquet", index=False)
            print("OK Generación guardada en Parquet.")
        else:
            print("[ERROR] No se encontraron las columnas de generación en 10.16.")
            
    except Exception as e:
        print(f"[ERROR] Falló la extracción de generación: {e}")


def extraer_consumo():
    """Lee 10.19_consumo.xls y extrae consumo total y población."""
    ruta = RAW_DIR / "10.19_consumo.xls"
    if not ruta.exists():
        print(f"[WARN] No se encontró el archivo: {ruta.name}")
        return

    try:
        # Saltamos 7 filas de títulos
        df = pd.read_excel(ruta, skiprows=7)
        df = df.rename(columns={df.columns[0]: "anio"})
        
        df["anio"] = pd.to_numeric(df["anio"], errors="coerce")
        df = df[df["anio"].isin([2020, 2021, 2022, 2023, 2024])]
        
        col_total = next((c for c in df.columns if "Total" in str(c)), None)
        col_pob = next((c for c in df.columns if "Población" in str(c)), None)
        col_perd = next((c for c in df.columns if "Pérdidas" in str(c)), None)
        
        if col_total and col_pob and col_perd:
            df_clean = df[["anio", col_total, col_pob, col_perd]].copy()
            df_clean.columns = ["anio", "consumo_total_gwh", "consumo_poblacion_gwh", "perdidas_gwh"]
            df_clean.to_parquet(OUT_DIR / "onei_consumo.parquet", index=False)
            print("OK Consumo guardado en Parquet.")
        else:
            print("[ERROR] No se encontraron las columnas de consumo en 10.19.")
            
    except Exception as e:
        print(f"[ERROR] Falló la extracción de consumo: {e}")


def extraer_potencia():
    """Lee 10.18_potencia.xls y extrae la potencia FV."""
    ruta = RAW_DIR / "10.18_potencia.xls"
    if not ruta.exists():
        print(f"[WARN] No se encontró el archivo: {ruta.name}")
        return

    try:
        # Este archivo es más complejo, leemos desde la fila 8
        df = pd.read_excel(ruta, skiprows=8)
        
        # La columna de años a veces se llama "AÑOS" o está en la primera posición
        if "AÑOS" in df.columns:
            df = df.rename(columns={"AÑOS": "anio"})
        else:
            df = df.rename(columns={df.columns[0]: "anio"})
            
        df["anio"] = pd.to_numeric(df["anio"], errors="coerce")
        df = df[df["anio"].isin([2020, 2021, 2022, 2023, 2024])]
        
        # En este Excel, la columna de FV suele estar a la derecha con el texto "Parques eólicos y fotovoltaicos"
        col_fv = next((c for c in df.columns if "Parques" in str(c) or "fotov" in str(c).lower()), None)
        
        if col_fv:
            df_clean = df[["anio", col_fv]].copy()
            df_clean.columns = ["anio", "potencia_fv_mw"]
            df_clean.to_parquet(OUT_DIR / "onei_potencia.parquet", index=False)
            print("OK Potencia guardada en Parquet.")
        else:
            print("[WARN] No se encontró la columna de Parques FV en 10.18. (Revisar estructura manualmente).")
            
    except Exception as e:
        print(f"[ERROR] Falló la extracción de potencia: {e}")


def extraer_todo():
    """Ejecuta todas las funciones de extracción en orden."""
    print("=== INICIANDO EXTRACCIÓN DE DATOS ONEI ===")
    print(f"Buscando Excel en: {RAW_DIR}")
    
    extraer_generacion()
    extraer_consumo()
    extraer_potencia()
    
    print("=== EXTRACCIÓN FINALIZADA ===")
    print(f"Archivos limpios listos en: {OUT_DIR}")


if __name__ == "__main__":
    extraer_todo()
