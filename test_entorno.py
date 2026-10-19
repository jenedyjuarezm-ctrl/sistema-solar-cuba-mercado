"""Verifica que todas las librerías del proyecto estén instaladas."""
import sys

print(f"Python: {sys.version}")
print("-" * 40)

paquetes = [
    "pandas", "numpy", "matplotlib", "scipy",
    "seaborn", "pyarrow", "sklearn", "jsonschema",
]

opcionales = ["streamlit", "plotly", "reportlab", "jupyter"]

ok = 0
fallos = []

for p in paquetes:
    try:
        mod = __import__(p)
        v = getattr(mod, "__version__", "?")
        print(f"[OK]      {p}: {v}")
        ok += 1
    except ImportError:
        print(f"[FALTA]   {p}")
        fallos.append(p)

print("\nOpcionales:")
for p in opcionales:
    try:
        mod = __import__(p)
        v = getattr(mod, "__version__", "?")
        print(f"[OK]      {p}: {v}")
    except ImportError:
        print(f"[NO INST] {p} (opcional)")

print("-" * 40)
print(f"Core instalados: {ok}/{len(paquetes)}")

if fallos:
    print(f"\nFaltan: {fallos}")
    print(f"Ejecuta: pip install {' '.join(fallos)}")
    sys.exit(1)
else:
    print("\nTodo listo.")
