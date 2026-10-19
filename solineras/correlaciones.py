"""Correlaciones de Spearman entre variables numéricas."""
from pathlib import Path
import pandas as pd
from scipy.stats import spearmanr

DATA = Path("data")
CLEAN = DATA / "clean"
OUT = DATA / "analisis"
OUT.mkdir(parents=True, exist_ok=True)


def generar_correlaciones():
    f = CLEAN / "encuestas_consolidadas.parquet"
    if not f.exists():
        print("[WARN] No existe encuestas_consolidadas.parquet")
        return
    df = pd.read_parquet(f)

    cols = [
        "potencia_pico_kwp", "num_paneles", "capacidad_baterias_kwh",
        "consumo_total_anual_kwh", "pr_promedio", "satisfaccion",
        "kwh_por_kwp", "antiguedad_anios", "ratio_bateria_panel",
    ]
    cols = [c for c in cols if c in df.columns and df[c].notna().sum() >= 5]
    if len(cols) < 2:
        print("[WARN] Muy pocas columnas numéricas.")
        return

    sub = df[cols].dropna(thresh=len(cols) // 2)
    if len(sub) < 5:
        print("[WARN] Muy pocos datos completos.")
        return

    corr = sub.corr(method="spearman").round(3)
    corr.to_csv(OUT / "correlaciones_spearman.csv")

    pares = []
    for i, a in enumerate(cols):
        for b in cols[i + 1:]:
            s2 = df[[a, b]].dropna()
            if len(s2) >= 5:
                r, p = spearmanr(s2[a], s2[b])
                pares.append({
                    "var_a": a, "var_b": b,
                    "rho": round(r, 3), "p": round(p, 4),
                    "n": len(s2), "significativo": p < 0.05,
                })
    pd.DataFrame(pares).sort_values("rho", key=abs, ascending=False)\
        .to_csv(OUT / "correlaciones_pares.csv", index=False)

    print(f"OK Correlaciones sobre {len(sub)} registros completos.")


if __name__ == "__main__":
    generar_correlaciones()
