"""Compara los grupos usando Kruskal-Wallis."""
import json
from pathlib import Path
import pandas as pd
from scipy import stats

DATA = Path(__file__).parent.parent / "data"
CLEAN = DATA / "clean"
OUT = DATA / "analisis"
OUT.mkdir(parents=True, exist_ok=True)

VARS = ["potencia_pico_kwp", "capacidad_baterias_kwh", "satisfaccion"]

def comparar_grupos():
    f = CLEAN / "encuestas_consolidadas.parquet"
    if not f.exists(): return
    df = pd.read_parquet(f)

    resultados = []
    for var in VARS:
        if var not in df.columns: continue
        
        # Agrupar ignorando nulos
        grupos = [g[var].dropna().values for name, g in df.groupby("tipo_entidad") if len(g[var].dropna()) > 2]
        
        if len(grupos) >= 2:
            h, p = stats.kruskal(*grupos)
            resultados.append({
                "variable": var,
                "kruskal_H": round(h, 3),
                "p_valor": round(p, 4),
                "significativo": bool(p < 0.05)
            })

    with open(OUT / "comparativo_grupos.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
        
    print("✅ OK Análisis comparativo guardado en data/analisis/")

if __name__ == "__main__":
    comparar_grupos()
