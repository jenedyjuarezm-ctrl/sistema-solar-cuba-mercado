"""Genera estadísticas descriptivas de los residentes."""
import json
from pathlib import Path
import pandas as pd
import numpy as np

DATA = Path(__file__).parent.parent / "data"
CLEAN = DATA / "clean"
OUT = DATA / "analisis"
OUT.mkdir(parents=True, exist_ok=True)

def generar_descriptivo():
    f = CLEAN / "encuestas_consolidadas.parquet"
    if not f.exists():
        print("[WARN] No existe encuestas_consolidadas.parquet")
        return
    df = pd.read_parquet(f)
    df_res = df[df["tipo_entidad"] == "residente"]

    num_cols = ["potencia_pico_kwp", "num_paneles", "capacidad_baterias_kwh", "satisfaccion"]
    num_cols = [c for c in num_cols if c in df_res.columns]

    desc = df_res[num_cols].describe().T
    desc["mediana"] = df_res[num_cols].median()
    desc["iqr"] = df_res[num_cols].quantile(0.75) - df_res[num_cols].quantile(0.25)
    desc.round(3).to_csv(OUT / "descriptivo_residentes.csv")

    # Distribución por tecnología (El fenómeno de las estaciones portátiles)
    if "tecnologia_paneles" in df_res.columns:
        tech = df_res["tecnologia_paneles"].value_counts()
        tech.to_csv(OUT / "tecnologia_residentes.csv")

    print("✅ OK Análisis descriptivo de residentes guardado en data/analisis/")

if __name__ == "__main__":
    generar_descriptivo()
