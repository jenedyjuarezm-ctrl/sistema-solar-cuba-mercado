"""
Scraper de Revolico usando Selenium para evadir bloqueos.
Extrae datos y los clasifica según las variables de nuestro formulario.
"""
import time
import random
import re
import pandas as pd
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Rutas de salida
BASE = Path(__file__).parent.parent
OUT_DIR = BASE / "data" / "raw" / "externas"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Configurar el navegador Chrome para que no parezca un bot
opciones = Options()
opciones.add_argument("--headless") # Se ejecuta en segundo plano
opciones.add_argument("--no-sandbox")
opciones.add_argument("--disable-dev-shm-usage")
opciones.add_argument("--window-size=1920,1080")
# User-Agent real de Chrome
opciones.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

def iniciar_driver():
    servicio = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=servicio, options=opciones)
    return driver

def extraer_datos(driver, url_busqueda):
    print(f"Buscando en: {url_busqueda}")
    driver.get(url_busqueda)
    
    # Esperar a que cargue la página de forma aleatoria (simula un humano)
    time.sleep(random.uniform(4, 7))
    
    anuncios = []
    
    # Buscar los contenedores de anuncios en la página
    # NOTA: Revolico cambia sus clases a veces. Si falla, inspecciona la web y cambia 'container' por la clase actual.
    items = driver.find_elements(By.XPATH, "//div[contains(@class, 'container')]")
    
    if not items:
        print("  [!] No se encontraron anuncios. Posible bloqueo o cambio de diseño.")
        return anuncios

    for item in items:
        try:
            titulo = item.find_element(By.TAG_NAME, "h2").text.strip()
            try:
                precio = item.find_element(By.XPATH, ".//span[contains(@class, 'price')]").text.strip()
            except:
                precio = "Sin precio"

            # --- CLASIFICACIÓN BASADA EN TUS VARIABLES ---
            # 1. Detectar Potencia (ej. 500W, 5kw)
            potencia = re.search(r'(\d+)\s*[wW]\b|(\d+[.,]\d+)\s*[kK][wW]\b', titulo)
            potencia_w = potencia.group(0) if potencia else None
            
            # 2. Detectar Batería (ej. 48v, 100ah, kwh)
            bateria = re.search(r'(\d+)\s*[vV]\b|(\d+)\s*[aA][hH]\b|(\d+[.,]\d+)\s*[kK][wW][hH]\b', titulo)
            bateria_dato = bateria.group(0) if bateria else None
            
            # 3. Detectar Tecnología
            tecnologia = "Litio" if re.search(r'litio|lifepo4', titulo, re.IGNORECASE) else None
            
            # 4. Categoría
            categoria = "Otro"
            if re.search(r'panel|solar|placa', titulo, re.IGNORECASE): categoria = "Panel"
            elif re.search(r'inversor|inverter', titulo, re.IGNORECASE): categoria = "Inversor"
            elif re.search(r'bateria|litio', titulo, re.IGNORECASE): categoria = "Batería"
            elif re.search(r'ecoflow|bluetti|estacion|power station', titulo, re.IGNORECASE): categoria = "Estación de energía"

            anuncios.append({
                "Titulo": titulo,
                "Precio": precio,
                "Categoria": categoria,
                "Potencia_Detectada": potencia_w,
                "Bateria_Detectada": bateria_dato,
                "Tecnologia": tecnologia,
                "Fecha_Scraping": time.strftime("%Y-%m-%d")
            })
        except Exception as e:
            continue

    return anuncios

def main():
    driver = iniciar_driver()
    todos_los_datos = []
    
    # Palabras clave basadas en los formularios
    busquedas = [
        "panel solar", 
        "inversor hibrido", 
        "bateria litio", 
        "power station"
    ]
    
    for termino in busquedas:
        url = f"https://www.revolico.com/search?q={termino.replace(' ', '+')}"
        datos = extraer_datos(driver, url)
        todos_los_datos.extend(datos)
        time.sleep(random.uniform(5, 10)) # Pausa entre búsquedas para no ser detectado
        
    driver.quit()
    
    if todos_los_datos:
        df = pd.DataFrame(todos_los_datos)
        # Eliminar duplicados por título
        df = df.drop_duplicates(subset=["Titulo"])
        df.to_csv(OUT_DIR / "revolico_scraping.csv", index=False, encoding="utf-8-sig")
        print(f"✅ Scraping finalizado. {len(df)} anuncios guardados en {OUT_DIR}/revolico_scraping.csv")
    else:
        print("❌ No se pudo extraer ningún dato.")

if __name__ == "__main__":
    main()
