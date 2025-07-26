#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# --- CONFIGURACIÓN ---
URL         = "https://app2.mintrabajo.gov.co/CentrosEntrenamiento/consulta_ext.aspx"
INPUT_FILE  = "cedulas.txt"
OUTPUT_FILE = "resultados.csv"

# --- OPCIONES DE CHROME HEADLESS ---
options = Options()
options.add_argument("--headless=new")

# Flags necesarias para entornos de despliegue como Render o Docker
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-setuid-sandbox")

# Arranca el driver
driver = webdriver.Chrome(options=options)
wait   = WebDriverWait(driver, 10) # Aumentar el tiempo si la página es lenta

# Lee las cédulas del archivo de entrada
try:
    with open(INPUT_FILE, encoding="utf-8") as f:
        cedulas = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"❌ Error: No se encontró el archivo de entrada '{INPUT_FILE}'.")
    cedulas = []

resultados = []

# Carga la URL una sola vez antes de empezar el bucle
if cedulas:
    driver.get(URL)

for cc in cedulas:
    print(f"Consultando cédula: {cc}...")
    try:
        # 1) Seleccionar tipo de documento
        sel = Select(wait.until(EC.element_to_be_clickable(
            (By.ID, "ctl00_ContentPlaceHolder1_cboTipoDocumento")
        )))
        sel.select_by_visible_text("CÉDULA DE CIUDADANÍA")

        # 2) Ingresar cédula
        campo = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtNumeroDocumento")
        campo.clear()
        campo.send_keys(cc)

        # 3) Clic en Consultar
        driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btnConsultar").click()

        # 4) Esperar y extraer resultados
        tabla = wait.until(EC.presence_of_element_located(
            (By.ID, "ctl00_ContentPlaceHolder1_gdvCertificados")
        ))
        
        # Extraer nombre (con manejo de error por si no aparece)
        try:
            nombre = driver.find_element(
                By.ID, "ctl00_ContentPlaceHolder1_lblNombre"
            ).text
        except Exception:
            nombre = "No encontrado"
            
        # Extraer cursos de la tabla
        filas  = tabla.find_elements(By.CSS_SELECTOR, "tbody > tr")[1:] # Omitir la fila de cabecera
        cursos = [f.find_elements(By.TAG_NAME, "td")[1].text for f in filas]
        
        resultados.append({
            "cedula": cc,
            "nombre": nombre,
            "cursos": "; ".join(cursos) if cursos else "Certificados no encontrados"
        })

    except TimeoutException:
        # Esto ocurre cuando la tabla de resultados no aparece después del tiempo de espera
        print(f"  -> Cédula {cc} sin resultados.")
        resultados.append({
            "cedula": cc,
            "nombre": "",
            "cursos": "Sin resultados"
        })
    except Exception as e:
        # Captura cualquier otro error inesperado durante el proceso
        print(f"  -> Ocurrió un error inesperado con la cédula {cc}: {e}")
        resultados.append({
            "cedula": cc,
            "nombre": "Error",
            "cursos": str(e)
        })

# Cierra el navegador y libera los recursos
driver.quit()

# Guarda el archivo CSV final
if resultados:
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=["cedula", "nombre", "cursos"])
        writer.writeheader()
        writer.writerows(resultados)
    print(f"\n✅ Proceso finalizado. {len(resultados)} registros guardados en '{OUTPUT_FILE}'.")
else:
    print("\n⚠️ No se procesó ningún registro.")
