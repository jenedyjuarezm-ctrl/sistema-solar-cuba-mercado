"""Codifica y analiza respuestas abiertas de entrevistas."""
import json
from pathlib import Path
import pandas as pd

DATA = Path("data")
RAW = DATA / "raw"
OUT = DATA / "analisis"
OUT.mkdir(parents=True, exist_ok=True)

CODIGOS = {
    "falta_repuestos": ["repuesto", "pieza", "escasez"],
    "clima_adverso": ["huracan", "lluvia", "nublado", "tormenta"],
    "almacenamiento": ["bateria", "almacenamiento", "no alcanza"],
    "mantenimiento": ["mantenimiento", "limpieza", "revision", "averia"],
    "costo": ["caro", "costo", "precio"],
    "conocimiento_tecnico": ["no se", "no entiendo", "capacitacion"],
    "red_electrica": ["apagon", "red", "conexion"],
    "satisfaccion_positiva": ["bien", "excelente", "bueno", "contento"],
}


def codificar(texto: str) -> list:
    if not isinstance(texto, str):
        return []
    t = texto.lower()
    return [c for c, palabras in CODIGOS.items() if any(p in t for p in palabras)]


def leer_jsonl(path: Path) -> list:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def analizar():
    registros = []
    for tipo, archivo in [
        ("solinera", "entrevistas_solineras.jsonl"),
        ("centro", "entrevistas_centros.jsonl"),
        ("residente", "entrevistas_residentes.jsonl"),
    ]:
        for doc in leer_jsonl(RAW / archivo):
            sid = doc.get("id_solinera") or doc.get("id_centro") or doc.get("id_residente")
            for seccion, contenido in doc.items():
                if isinstance(contenido, dict):
                    for campo, valor in contenido.items():
                        if isinstance(valor, str) and len(valor) > 3:
                            for c in codificar(valor):
                                registros.append({
                                    "id_entidad": sid,
                                    "tipo_entidad": tipo,
                                    "seccion": seccion,
                                    "campo": campo,
                                    "texto": valor,
                                    "codigo": c,
                                })

    df = pd.DataFrame(registros)
    if df.empty:
        print("[WARN] No hay textos codificables.")
        return
    df.to_parquet(DATA / "clean" / "cualitativo_codificado.parquet", index=False)
    freq = df["codigo"].value_counts()
    freq.to_csv(OUT / "cualitativo_frecuencia_global.csv")
    por_tipo = df.groupby(["tipo_entidad", "codigo"]).size().unstack(fill_value=0)
    por_tipo.to_csv(OUT / "cualitativo_por_tipo.csv")

    print(f"OK Cualitativo: {len(df)} citas codificadas, {df['codigo'].nunique()} temas.")
    print(f"   Top 3: {freq.head(3).to_dict()}")


if __name__ == "__main__":
    analizar()
