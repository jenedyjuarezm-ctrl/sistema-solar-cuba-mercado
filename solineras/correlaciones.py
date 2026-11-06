"""Calcula correlaciones entre el clima y la energía."""
from pathlib import Path
import pandas as pd
from scipy.stats import spearmanr

DATA = Path(__file__).parent.parent / "data"
CLEAN = DATA / "clean"
OUT = DATA / "analisis"
OUT.mkdir(parents=True, exist_ok=True)

def generar_correlaciones():
    onei = pd.read_parquet(CLEAN / "onei_generacion.parquet")
    nasa = pd.read_parquet(CLEAN / "nasa_power_limpio.parquet")

    # Agrupar NASA por año
    nasa_anual = nasa.groupby('anio').mean(numeric_only=True).reset_index()
    df = onei.merge(nasa_anual, on='anio')

    # Correlacionar la generación con las variables climáticas
    pares = []
    for var in ["irradiancia_kwh_m2", "temperatura_c", "humedad_pct"]:
        if var in df.columns:
            r, p = spearmanr(df["gen_fv_gwh"], df[var])
            pares.append({"variable_climatica": var, "rho": round(r, 3), "p_valor": round(p, 4)})

    pd.DataFrame(pares).to_csv(OUT / "correlaciones_clima.csv", index=False)
    print("✅ OK Correlaciones guardadas en data/analisis/")

if __name__ == "__main__":
    generar_correlaciones()
