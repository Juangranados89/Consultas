#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import time
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURACIÓN ---
URL         = "https://app2.mintrabajo.gov.co/CentrosEntrenamiento/consulta_ext.aspx"
INPUT_FILE  = "cedulas.txt"
OUTPUT_FILE = "resultados.csv"

# --- OPCIONES DE CHROME HEADLESS ---
options = Options()
options.headless = True

# Usar un directorio único en /tmp para el perfil de Chrome
user_data_dir = tempfile.mkdtemp(prefix="chrome-data-")
options.add_argument(f"--user-data-dir={user_data_dir}")

# Flags necesarias en contenedores sin privilegios
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-setuid-sandbox")

# Arranca el driver
driver = webdriver.Chrome(options=options)
wait   = WebDriverWait(driver, 10)

# Lee las cédulas
with open(INPUT_FILE, encoding="utf-8") as f:
    cedulas = [line.strip() for line in f if line.strip()]

resultados = []

for cc in cedulas:
    driver.get(URL)

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

    # 4) Espera breve
    time.sleep(1)

    try:
        tabla = wait.until(EC.presence_of_element_located(
            (By.ID, "ctl00_ContentPlaceHolder1_gdvCertificados")
        ))
        filas  = tabla.find_elements(By.CSS_SELECTOR, "tbody > tr")[1:]
        try:
            nombre = driver.find_element(
                By.ID, "ctl00_ContentPlaceHolder1_lblNombre"
            ).text
        except:
            nombre = ""
        cursos = [f.find_elements(By.TAG_NAME, "td")[1].text for f in filas]
        resultados.append({
            "cedula": cc,
            "nombre": nombre,
            "cursos": "; ".join(cursos)
        })
    except:
        resultados.append({
            "cedula": cc,
            "nombre": "",
            "cursos": "Sin resultados"
        })

driver.quit()

# Guarda el CSV final
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as out:
    writer = csv.DictWriter(out, fieldnames=["cedula", "nombre", "cursos"])
    writer.writeheader()
    writer.writerows(resultados)

print(f"✅ {len(resultados)} registros volcados en '{OUTPUT_FILE}'.")
