.PHONY: help install pipeline dashboard lint test clean

help:
	@echo "Comandos:"
	@echo "  make install    Instalar dependencias"
	@echo "  make pipeline   Ejecutar pipeline completo"
	@echo "  make dashboard  Lanzar dashboard"
	@echo "  make test       Verificar entorno"
	@echo "  make clean      Limpiar temporales"

install:
	pip install -r requirements.txt

pipeline:
	python solineras/run_all.py

dashboard:
	streamlit run solineras/dashboard.py

test:
	python test_entorno.py

clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .pytest_cache .coverage
	rm -rf tmp_graficos/
	rm -rf build/ dist/ *.egg-info/
