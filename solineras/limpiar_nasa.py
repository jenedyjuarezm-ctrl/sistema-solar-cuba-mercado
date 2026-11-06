"""
Limpia el archivo CSV de NASA POWER.
"""
import pandas as pd
from pathlib import Path

BASE = Path(__file__).parent.parent
RAW_FILE = BASE / "data" / "raw" / "externas" / "nasa_power.csv"
OUT_DIR = BASE / "data" / "clean"

def limpiar_nasa():
    if not RAW_FILE.exists(): return
    # Saltamos las 10 líneas de texto iniciales
    df = pd.read_csv(RAW_FILE, skiprows=10)
    df = df[df['YEAR'].between(2020, 2024)]

    # Formato largo (meses en filas)
    df_largo = pd.melt(df, id_vars=['PARAMETER', 'YEAR'], 
        value_vars=['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'],
        var_name='mes', value_name='valor')

    # Separar variables
    irr = df_largo[df_largo['PARAMETER'] == 'ALLSKY_SFC_SW_DWN'][['YEAR', 'mes', 'valor']].copy()
    irr.columns = ['anio', 'mes', 'irradiancia_kwh_m2']
    temp = df_largo[df_largo['PARAMETER'] == 'T2M'][['YEAR', 'mes', 'valor']].copy()
    temp.columns = ['anio', 'mes', 'temperatura_c']
    hum = df_largo[df_largo['PARAMETER'] == 'RH2M'][['YEAR', 'mes', 'valor']].copy()
    hum.columns = ['anio', 'mes', 'humedad_pct']

    # Unir
    df_nasa = irr.merge(temp, on=['anio', 'mes']).merge(hum, on=['anio', 'mes'])
    df_nasa.to_parquet(OUT_DIR / "nasa_power_limpio.parquet", index=False)
    print("OK NASA POWER guardado.")

if __name__ == "__main__":
    limpiar_nasa()
