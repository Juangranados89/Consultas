# Dockerfile
FROM python:3.9-slim

# 1. Instala dependencias del SO necesarias
RUN apt-get update && apt-get install -y \
    wget unzip xvfb libxi6 libgconf-2-4 \
  && rm -rf /var/lib/apt/lists/*

# 2. Instala Chrome
RUN wget -qO /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
  && dpkg -i /tmp/chrome.deb || apt-get -fy install \
  && rm /tmp/chrome.deb

# 3. Descarga la misma versión de Chromedriver
RUN CHROME_VER=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+') \
  && wget -qO /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/${CHROME_VER}/chromedriver_linux64.zip" \
  && unzip /tmp/chromedriver.zip -d /usr/local/bin \
  && chmod +x /usr/local/bin/chromedriver \
  && rm /tmp/chromedriver.zip

# 4. Copia tu app
WORKDIR /app
COPY . .

# 5. Instala dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# 6. Comando por defecto (se usará en el Cron Job)
CMD ["python", "consulta_cursos.py"]
