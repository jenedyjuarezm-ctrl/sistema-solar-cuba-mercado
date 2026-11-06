"""Ejecuta todo el pipeline (Limpieza + Análisis + Reporte) en orden."""
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).parent

PASOS = [
    # FASE 1: Limpieza y Procesamiento
    ("1/8 Extraer ONEI",         [sys.executable, str(BASE / "extraer_onei.py")]),
    ("2/8 Limpiar NASA",         [sys.executable, str(BASE / "limpiar_nasa.py")]),
    ("3/8 Consolidar",           [sys.executable, str(BASE / "consolidar.py")]),
    
    # FASE 2: Análisis Estadístico y Visual
    ("4/8 Análisis Descriptivo", [sys.executable, str(BASE / "analisis_descriptivo.py")]),
    ("5/8 Análisis Comparativo", [sys.executable, str(BASE / "analisis_comparativo.py")]),
    ("6/8 Análisis Cualitativo", [sys.executable, str(BASE / "analisis_cualitativo.py")]),
    ("7/8 Correlaciones",        [sys.executable, str(BASE / "correlaciones.py")]),
    
    # FASE 3: Reporte Final
    ("8/8 Reporte Ejecutivo",    [sys.executable, str(BASE / "reporte.py")]),
]

def main():
    print("==============================================")
    print("🚀 INICIANDO PIPELINE COMPLETO DEL PROYECTO")
    print("==============================================")
    
    for nombre, cmd in PASOS:
        print(f"\n>>> Ejecutando: {nombre} <<<")
        try:
            # check=True detiene el proceso si el script devuelve un error
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            print(f"\n❌ ERROR en el paso: {nombre}.")
            print("Revisa el mensaje de error de arriba para solucionarlo.")
            return 1
            
    print("\n==============================================")
    print("✅ PIPELINE FINALIZADO CON ÉXITO")
    print("==============================================")
    return 0

if __name__ == "__main__":
    sys.exit(main())
