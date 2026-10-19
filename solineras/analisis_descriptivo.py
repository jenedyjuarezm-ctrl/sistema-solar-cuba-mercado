"""Estadísticas descriptivas por tipo de entidad y provincia."""
import json
from pathlib import Path
import pandas as pd

DATA = Path("data")
CLEAN = DATA / "clean"
OUT = DATA / "analisis"
OUT.mkdir(parents=True, exist_ok=True)


def generar_descriptivo():
    f = CLEAN / "encuestas_consolidadas.parquet"
    if not f.exists():
        print("[WARN] No existe encuestas_consolidadas.parquet")
        return
    df = pd.read_parquet(f)
    if df.empty:
        print("[WARN] Dataset vacío.")
        return

    num_cols = [
        "potencia_pico_kwp", "num_paneles", "capacidad_baterias_kwh",
        "consumo_total_anual_kwh", "pr_promedio", "satisfaccion",
        "kwh_por_kwp", "antiguedad_anios", "ratio_bateria_panel",
    ]
    num_cols = [c for c in num_cols if c in df.columns]

    desc = df[num_cols].describe().T
    desc["mediana"] = df[num_cols].median()
    desc["iqr"] = df[num_cols].quantile(0.75) - df[num_cols].quantile(0.25)
    desc["nulos_pct"] = df[num_cols].isna().mean() * 100
    desc.round(3).to_csv(OUT / "descriptivo_global.csv")

    for tipo, g in df.groupby("tipo_entidad"):
        g[num_cols].describe().T.round(3).to_csv(OUT / f"descriptivo_{tipo}.csv")

    if "ubicacion" in df.columns:
        df["provincia"] = df["ubicacion"].astype(str).str.strip()
        por_prov = df.groupby("provincia").agg(
            n=("id", "count"),
            potencia_total_kwp=("potencia_pico_kwp", "sum"),
            potencia_media_kwp=("potencia_pico_kwp", "mean"),
            pr_medio=("pr_promedio", "mean"),
        ).round(2).sort_values("potencia_total_kwp", ascending=False)
        por_prov.to_csv(OUT / "por_provincia.csv")

    outliers = {}
    for c in num_cols:
        q1, q3 = df[c].quantile([0.25, 0.75])
        iqr = q3 - q1
        li, ls = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        outliers[c] = df[(df[c] < li) | (df[c] > ls)]["id"].tolist()
    with open(OUT / "outliers.json", "w", encoding="utf-8") as f:
        json.dump(outliers, f, indent=2, ensure_ascii=False)

    print(f"OK Descriptivo en {OUT}/")


if __name__ == "__main__":
    generar_descriptivo()
