"""Genera reporte PDF por solinera."""
import argparse
import json
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
)

BASE = Path(__file__).parent.parent
DATA = BASE / "data"
REPORTES = BASE / "reportes"
TMP = BASE / "tmp_graficos"
REPORTES.mkdir(exist_ok=True)
TMP.mkdir(exist_ok=True)


def grafico_series(hist: pd.DataFrame, id_solinera: str) -> Path:
    hist["timestamp"] = pd.to_datetime(hist["timestamp"], utc=True, errors="coerce")
    hist = hist.dropna(subset=["timestamp"]).set_index("timestamp")
    serie = hist.resample("D")[["produccion_kwh", "consumo_kwh"]].sum()
    fig, ax = plt.subplots(figsize=(9, 3.5))
    ax.plot(serie.index, serie["produccion_kwh"], label="Produccion", color="#f4a900")
    ax.plot(serie.index, serie["consumo_kwh"], label="Consumo", color="#2a6f97")
    ax.set_title(f"Produccion vs Consumo diario - {id_solinera}")
    ax.set_ylabel("kWh")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    ruta = TMP / f"series_{id_solinera}.png"
    fig.savefig(ruta, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return ruta


def build_pdf(id_solinera: str, salida: Path):
    enc_path = DATA / "clean" / "encuestas_consolidadas.parquet"
    hist_path = DATA / "clean" / "historico_validado.parquet"
    met_path = DATA / "analisis" / "metricas_solinera.json"

    if not enc_path.exists():
        print(f"[ERROR] Falta {enc_path}. Ejecuta consolidar.py primero.")
        return False

    enc = pd.read_parquet(enc_path)
    fila = enc[enc["id"] == id_solinera]
    if fila.empty:
        print(f"[ERROR] Solinera {id_solinera} no encontrada.")
        return False
    e = fila.iloc[0]

    hist = pd.DataFrame()
    if hist_path.exists():
        hist = pd.read_parquet(hist_path)
        hist = hist[hist["id_solinera"] == id_solinera].copy()

    metricas = {}
    if met_path.exists():
        metricas = json.loads(met_path.read_text(encoding="utf-8")).get(id_solinera, {})

    estilos = getSampleStyleSheet()
    titulo = ParagraphStyle("t", parent=estilos["Title"], fontSize=18, textColor=colors.HexColor("#1f3864"))
    subt = ParagraphStyle("s", parent=estilos["Heading2"], textColor=colors.HexColor("#2a6f97"))
    normal = estilos["Normal"]

    doc = SimpleDocTemplate(str(salida), pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    flow = []

    flow.append(Paragraph(f"Reporte - Solinera {id_solinera}", titulo))
    flow.append(Spacer(1, 0.3*cm))
    flow.append(Paragraph(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}", normal))
    flow.append(Spacer(1, 1*cm))

    info = [
        ["Nombre", str(e.get("nombre", "-"))],
        ["Ubicacion", str(e.get("ubicacion", "-"))],
        ["Anio puesta en marcha", str(e.get("anio_puesta_marcha", "-"))],
        ["Tipo instalacion", str(e.get("tipo_instalacion", "-"))],
        ["Potencia pico (kWp)", str(e.get("potencia_pico_kwp", "-"))],
        ["Capacidad baterias (kWh)", str(e.get("capacidad_baterias_kwh", "-"))],
    ]
    tabla = Table(info, colWidths=[5*cm, 10*cm])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#dce6f1")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))
    flow.append(Paragraph("1. Informacion general", subt))
    flow.append(tabla)
    flow.append(Spacer(1, 0.5*cm))

    flow.append(Paragraph("2. Indicadores clave", subt))
    kpis = [
        ["Produccion total (kWh)", f"{metricas.get('produccion_total_kwh', 0):,.1f}"],
        ["Consumo total (kWh)", f"{metricas.get('consumo_total_kwh', 0):,.1f}"],
        ["Balance (kWh)", f"{metricas.get('balance_kwh', 0):,.1f}"],
        ["Autosuficiencia (%)", f"{metricas.get('autosuficiencia_pct', 0):.2f}"],
    ]
    tabla_kpi = Table(kpis, colWidths=[7*cm, 7*cm])
    tabla_kpi.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#fff2cc")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
    ]))
    flow.append(tabla_kpi)

    if not hist.empty:
        flow.append(PageBreak())
        flow.append(Paragraph("3. Series temporales", subt))
        try:
            img = grafico_series(hist, id_solinera)
            flow.append(Image(str(img), width=16*cm))
        except Exception as ex:
            flow.append(Paragraph(f"No se pudo generar grafico: {ex}", normal))

    flow.append(Spacer(1, 1*cm))
    flow.append(Paragraph("Reporte generado automaticamente. Datos con fines academicos.",
                          ParagraphStyle("f", parent=normal, fontSize=8, textColor=colors.grey)))

    doc.build(flow)
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solinera", required=True)
    args = parser.parse_args()

    salida = REPORTES / f"reporte_{args.solinera}_{datetime.now().strftime('%Y%m%d')}.pdf"
    ok = build_pdf(args.solinera, salida)
    if ok:
        print(f"OK Reporte: {salida}")


if __name__ == "__main__":
    main()
