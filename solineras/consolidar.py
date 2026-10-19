"""Une solineras + centros + residentes en un dataset maestro."""
import json
from pathlib import Path
import pandas as pd

DATA = Path("data")
RAW = DATA / "raw"
CLEAN = DATA / "clean"
CLEAN.mkdir(parents=True, exist_ok=True)


def _leer_jsonl(path: Path) -> list:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def _aplanar(doc: dict, tipo: str) -> dict:
    a = doc.get("seccion_a", {}) or {}
    b = doc.get("seccion_b", {}) or {}
    d = doc.get("seccion_d", {}) or {}
    e = doc.get("seccion_e", {}) or {}
    f_ = doc.get("seccion_f", {}) or {}
    g = doc.get("seccion_g", {}) or {}
    return {
        "id": doc.get("id_solinera") or doc.get("id_centro") or doc.get("id_residente"),
        "tipo_entidad": tipo,
        "fecha_encuesta": doc.get("fecha_encuesta"),
        "nombre": a.get("nombre"),
        "ubicacion": a.get("ubicacion"),
        "anio_puesta_marcha": a.get("anio_puesta_marcha") or a.get("anio_instalacion"),
        "tipo_instalacion": a.get("tipo_instalacion"),
        "area_total_m2": a.get("area_total_m2"),
        "num_paneles": b.get("num_paneles"),
        "potencia_pico_kwp": b.get("potencia_pico_kwp") or b.get("potencia_instalada_w"),
        "tecnologia_paneles": b.get("tecnologia_paneles"),
        "num_inversores": b.get("num_inversores"),
        "capacidad_baterias_kwh": b.get("capacidad_baterias_kwh"),
        "tipo_baterias": b.get("tipo_baterias"),
        "seguimiento_solar": b.get("seguimiento_solar"),
        "conexion_red": b.get("conexion_red"),
        "consumo_total_anual_kwh": d.get("consumo_total_anual_kwh") or d.get("consumo_mensual_kwh"),
        "consumo_promedio_diario_kwh": d.get("consumo_promedio_diario_kwh"),
        "venta_excedentes": d.get("venta_excedentes"),
        "pr_promedio": e.get("pr_promedio"),
        "fallas_ultimo_anio": e.get("fallas_ultimo_anio"),
        "satisfaccion": f_.get("satisfaccion") or g.get("satisfaccion"),
        "reduce_co2": f_.get("reduce_co2"),
        "num_desafios": len(f_.get("desafios") or []),
    }


def consolidar() -> pd.DataFrame:
    filas = []
    for tipo, archivo in [
        ("solinera", "entrevistas_solineras.jsonl"),
        ("centro", "entrevistas_centros.jsonl"),
        ("residente", "entrevistas_residentes.jsonl"),
    ]:
        for doc in _leer_jsonl(RAW / archivo):
            filas.append(_aplanar(doc, tipo))

    df = pd.DataFrame(filas)
    if df.empty:
        print("[WARN] No hay encuestas para consolidar.")
        return df

    df["kwh_por_kwp"] = df["consumo_total_anual_kwh"] / df["potencia_pico_kwp"]
    df["antiguedad_anios"] = 2026 - df["anio_puesta_marcha"]
    df["ratio_bateria_panel"] = df["capacidad_baterias_kwh"] / df["potencia_pico_kwp"]

    df.to_parquet(CLEAN / "encuestas_consolidadas.parquet", index=False)
    print(f"OK Dataset maestro: {len(df)} registros")
    if "tipo_entidad" in df.columns:
        print(f"   Distribucion: {df['tipo_entidad'].value_counts().to_dict()}")
    return df


if __name__ == "__main__":
    consolidar()
