"""
Une residentes (primarios) + solineras (web) + centros (web) en un dataset maestro.
"""
import json
from pathlib import Path
import pandas as pd

DATA = Path(__file__).parent.parent / "data"
RAW = DATA / "raw"
CLEAN = DATA / "clean"
CLEAN.mkdir(parents=True, exist_ok=True)

def _leer_jsonl(path: Path) -> list:
    if not path.exists(): return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]

def _aplanar(doc: dict, tipo: str) -> dict:
    a = doc.get("seccion_a", {}) or {}
    b = doc.get("seccion_b", {}) or {}
    c = doc.get("seccion_c", {}) or {}
    d = doc.get("seccion_d", {}) or {}
    e = doc.get("seccion_e", {}) or {}
    f_ = doc.get("seccion_f", {}) or {}
    g = doc.get("seccion_g", {}) or {}
    
    return {
        "id": doc.get("id_residente") or doc.get("id_centro") or doc.get("id_solinera"),
        "tipo_entidad": tipo,
        "fecha_encuesta": doc.get("fecha_encuesta"),
        "ubicacion": a.get("ubicacion"),
        "anio_puesta_marcha": a.get("anio_puesta_marcha") or a.get("anio_instalacion"),
        "num_paneles": b.get("num_paneles"),
        "potencia_pico_kwp": b.get("potencia_pico_kwp") or (b.get("potencia_instalada_w") / 1000 if b.get("potencia_instalada_w") else None),
        "capacidad_baterias_kwh": b.get("capacidad_baterias_kwh"),
        "tecnologia_paneles": b.get("tecnologia_paneles"),
        "consumo_total_anual_kwh": d.get("consumo_total_anual_kwh") or (d.get("consumo_mensual_kwh") * 12 if d.get("consumo_mensual_kwh") else None),
        "satisfaccion": e.get("satisfaccion") or f_.get("satisfaccion") or g.get("satisfaccion"),
        "costo_instalacion": f_.get("costo_instalacion"),
        "moneda_costo": f_.get("moneda_costo")
    }

def consolidar():
    filas = []
    # 1. Residentes (Primarios)
    for doc in _leer_jsonl(RAW / "entrevistas_residentes.jsonl"):
        filas.append(_aplanar(doc, "residente"))
    
    # 2. Centros (Primarios)
    for doc in _leer_jsonl(RAW / "entrevistas_centros.jsonl"):
        filas.append(_aplanar(doc, "centro"))
        
    # 3. Solineras Web (Secundarios)
    for doc in _leer_jsonl(RAW / "externas" / "solineras_web.jsonl"):
        filas.append(_aplanar(doc, "solinera_web"))
        
    # 4. Centros Web (Secundarios)
    for doc in _leer_jsonl(RAW / "externas" / "centros_web_habana.jsonl"):
        filas.append(_aplanar(doc, "centro_web"))

    df = pd.DataFrame(filas)
    if df.empty: return df

    # Calcular derivados de forma segura
    df["kwh_por_kwp"] = df["consumo_total_anual_kwh"] / df["potencia_pico_kwp"]
    df["antiguedad_anios"] = 2026 - df["anio_puesta_marcha"]
    df["ratio_bateria_panel"] = df["capacidad_baterias_kwh"] / df["potencia_pico_kwp"]

    df.to_parquet(CLEAN / "encuestas_consolidadas.parquet", index=False)
    print(f"OK Dataset maestro: {len(df)} registros.")
    print(df['tipo_entidad'].value_counts())
    return df

if __name__ == "__main__":
    consolidar()
