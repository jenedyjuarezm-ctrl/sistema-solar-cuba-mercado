"""Carga, valida y consolida encuestas y series históricas."""
import json
from pathlib import Path

import pandas as pd
from jsonschema import validate, ValidationError

BASE = Path(__file__).parent.parent
DATA = BASE / "data"
SCHEMAS = Path(__file__).parent / "schemas"

SCHEMAS_DICT = {
    "solinera": SCHEMAS / "schema_solinera.json",
    "centro": SCHEMAS / "schema_centro.json",
    "residente": SCHEMAS / "schema_residente.json",
    "historico": SCHEMAS / "schema_historico.json",
}


def _cargar_schema(tipo: str) -> dict:
    path = SCHEMAS_DICT.get(tipo)
    if not path or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def validar(doc: dict, tipo: str) -> tuple[bool, str | None]:
    schema = _cargar_schema(tipo)
    if not schema:
        return True, None
    try:
        validate(instance=doc, schema=schema)
        return True, None
    except ValidationError as e:
        return False, e.message


def cargar_jsonl(path: Path, tipo: str) -> tuple[list[dict], list[dict]]:
    validos, errores = [], []
    if not path.exists():
        return validos, errores
    with open(path, encoding="utf-8") as f:
        for i, linea in enumerate(f, start=1):
            linea = linea.strip()
            if not linea:
                continue
            try:
                doc = json.loads(linea)
            except json.JSONDecodeError as e:
                errores.append({"linea": i, "error": f"JSON inválido: {e}"})
                continue
            ok, msg = validar(doc, tipo)
            if ok:
                validos.append(doc)
            else:
                errores.append({"linea": i, "error": msg})
    return validos, errores


def cargar_todo() -> dict:
    resultado = {}
    for tipo, archivo in [
        ("solinera", "entrevistas_solineras.jsonl"),
        ("centro", "entrevistas_centros.jsonl"),
        ("residente", "entrevistas_residentes.jsonl"),
        ("historico", "historico_series.jsonl"),
    ]:
        path = DATA / "raw" / archivo
        validos, errores = cargar_jsonl(path, tipo)
        resultado[tipo] = {"validos": validos, "errores": errores}
        print(f"{tipo:<12} validos={len(validos):>3} errores={len(errores):>3}")
    return resultado


def guardar_errores(resultado: dict):
    out = DATA / "auditoria" / "errores_validacion.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        for tipo, info in resultado.items():
            for err in info["errores"]:
                f.write(json.dumps({"tipo": tipo, **err}, ensure_ascii=False) + "\n")
    print(f"Errores guardados en {out}")


if __name__ == "__main__":
    print("=== Ingesta ===")
    resultado = cargar_todo()
    guardar_errores(resultado)
