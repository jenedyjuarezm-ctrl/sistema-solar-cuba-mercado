"""Verifica que cada fuente tenga al menos 30 muestras."""
import json
from pathlib import Path
import pandas as pd

DATA = Path("data")
AUDITORIA = DATA / "auditoria"
AUDITORIA.mkdir(parents=True, exist_ok=True)

MINIMO = 30

FUENTES = {
    "entrevista_solineras": DATA / "raw" / "entrevistas_solineras.jsonl",
    "entrevista_centros": DATA / "raw" / "entrevistas_centros.jsonl",
    "entrevista_residentes": DATA / "raw" / "entrevistas_residentes.jsonl",
    "historico_series": DATA / "raw" / "historico_series.jsonl",
    "onei_anuario": DATA / "raw" / "externas" / "onei_anuario.csv",
    "nasa_power": DATA / "raw" / "externas" / "nasa_power.csv",
    "irena_cuba": DATA / "raw" / "externas" / "irena_cuba.csv",
    "revolico_precios": DATA / "raw" / "externas" / "revolico_precios.csv",
}


def contar_registros(path: Path) -> int:
    if not path.exists():
        return 0
    if path.suffix == ".jsonl":
        with open(path, encoding="utf-8") as f:
            return sum(1 for line in f if line.strip())
    if path.suffix == ".csv":
        try:
            return len(pd.read_csv(path))
        except Exception:
            return 0
    return 0


def auditar() -> dict:
    resultado = {"minimo_requerido": MINIMO, "fuentes": {}}
    for nombre, path in FUENTES.items():
        n = contar_registros(path)
        resultado["fuentes"][nombre] = {
            "path": str(path),
            "n": n,
            "cumple": n >= MINIMO,
            "faltan": max(0, MINIMO - n),
        }
    with open(AUDITORIA / "cobertura_fuentes.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)

    print("\n=== AUDITORÍA DE FUENTES ===")
    print(f"{'Fuente':<28} {'n':>6} {'>=30':>5} {'Faltan':>8}")
    print("-" * 50)
    for nombre, info in resultado["fuentes"].items():
        ok = "OK" if info["cumple"] else "--"
        print(f"{nombre:<28} {info['n']:>6} {ok:>5} {info['faltan']:>8}")
    return resultado


if __name__ == "__main__":
    auditar()
