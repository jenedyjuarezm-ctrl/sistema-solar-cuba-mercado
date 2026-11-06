"""Codifica y analiza los textos de las entrevistas a residentes basándose en el Formulario."""
import json
from pathlib import Path
import pandas as pd

DATA = Path(__file__).parent.parent / "data"
RAW = DATA / "raw"
OUT = DATA / "analisis"
OUT.mkdir(parents=True, exist_ok=True)

def leer_jsonl(p):
    if not p.exists(): return []
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]

def analizar():
    registros = []
    # Procesamos el JSONL de residentes (Seccion E del formulario)
    for doc in leer_jsonl(RAW / "entrevistas_residentes.jsonl"):
        sid = doc.get("id_residente")
        
        # Pregunta 15 del formulario: Motivación
        motivaciones = doc.get("seccion_e", {}).get("motivacion", [])
        for m in motivaciones:
            registros.append({"id_entidad": sid, "tipo": "Motivación", "valor": m.replace("_", " ").title()})
        
        # Pregunta de Desafíos del formulario
        desafios = doc.get("seccion_e", {}).get("dificultades", [])
        for d in desafios:
            registros.append({"id_entidad": sid, "tipo": "Desafío", "valor": d.replace("_", " ").title()})

    df = pd.DataFrame(registros)
    
    if not df.empty:
        # Guardar las frecuencias en CSV
        resumen_mot = df[df["tipo"] == "Motivación"]["valor"].value_counts()
        resumen_des = df[df["tipo"] == "Desafío"]["valor"].value_counts()
        
        resumen_mot.to_csv(OUT / "frecuencia_motivaciones.csv")
        resumen_des.to_csv(OUT / "frecuencia_desafios.csv")
        
        print("✅ OK Análisis cualitativo guardado en data/analisis/")
        print("\n--- TOP MOTIVACIONES ---")
        print(resumen_mot)
        print("\n--- TOP DESAFÍOS ---")
        print(resumen_des)
    else:
        print("No hay datos cualitativos para analizar.")

if __name__ == "__main__":
    analizar()
