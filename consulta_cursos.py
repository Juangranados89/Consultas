import csv, time, tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# …

# --- CONFIGURACIÓN DE CHROME HEADLESS ---
options = Options()
options.headless = True

# Apunta a un directorio de perfil único
user_data_dir = tempfile.mkdtemp(prefix="chrome-user-data-")
options.add_argument(f"--user-data-dir={user_data_dir}")

# Opciones necesarias en entornos “sin privilegios” como Render
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")          # si fuese necesario
options.add_argument("--disable-setuid-sandbox")

# Ahora arranca el driver
driver = webdriver.Chrome(options=options)
wait   = WebDriverWait(driver, 10)
