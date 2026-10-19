"""Compara solineras vs centros vs residentes con tests no paramétricos."""
import json
from pathlib import Path
import pandas as pd
from scipy import stats

DATA = Path("data")
CLEAN = DATA / "clean"
OUT = DATA / "analisis"
OUT.mkdir(parents=True, exist_ok=True)

VARS = [
    "potencia_pico_kwp", "consumo_total_anual_kwh", "pr_promedio",
    "satisfaccion", "kwh_por_kwp", "antiguedad_anios", "ratio_bateria_panel",
]


def comparar_grupos():
    f = CLEAN / "encuestas_consolidadas.parquet"
    if not f.exists():
        print("[WARN] No existe encuestas_consolidadas.parquet")
        return
    df = pd.read_parquet(f)
    if df.empty or df["tipo_entidad"].nunique() < 2:
        print("[WARN] Se necesitan al menos 2 tipos de entidad.")
        return

    resultados = []
    for var in VARS:
        if var not in df.columns:
            continue
        grupos = [g[var].dropna().values for _, g in df.groupby("tipo_entidad")]
        grupos = [g for g in grupos if len(g) > 0]
        if len(grupos) < 2:
            continue

        if all(len(g) >= 3 for g in grupos):
            h, p_kw = stats.kruskal(*grupos)
        else:
            h, p_kw = float("nan"), float("nan")

        pares = []
        tipos = list(df["tipo_entidad"].unique())
        for i in range(len(tipos)):
            for j in range(i + 1, len(tipos)):
                a = df[df["tipo_entidad"] == tipos[i]][var].dropna()
                b = df[df["tipo_entidad"] == tipos[j]][var].dropna()
                if len(a) >= 3 and len(b) >= 3:
                    u, p = stats.mannwhitneyu(a, b, alternative="two-sided")
                    pares.append({
                        "par": f"{tipos[i]} vs {tipos[j]}",
                        "p": round(p, 4),
                        "significativo": p < 0.05,
                    })

        resultados.append({
            "variable": var,
            "kruskal_H": round(h, 3) if h == h else None,
            "kruskal_p": round(p_kw, 4) if p_kw == p_kw else None,
            "significativo_0.05": (p_kw < 0.05) if p_kw == p_kw else None,
            "medianas": {
                t: round(float(g[var].median()), 3)
                for t, g in df.groupby("tipo_entidad")
                if var in g and g[var].notna().any()
            },
            "pares": pares,
        })

    with open(OUT / "comparativo_grupos.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)

    print(f"OK Comparativo: {len(resultados)} variables testeadas.")
    for r in resultados:
        sig = "SIG" if r["significativo_0.05"] else "---"
        print(f"  {r['variable']:<25} p={r['kruskal_p']} [{sig}]")


if __name__ == "__main__":
    comparar_grupos()
