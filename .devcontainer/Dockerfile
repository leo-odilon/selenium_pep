# Use a imagem base oficial do Python para ARM
FROM python:3.9-slim

# Instalação de dependências
RUN apt-get update \
    && apt-get install -y wget gnupg curl unzip

# Instalação do Chromium para ARM64
RUN apt-get update \
    && apt-get install -y chromium git

# Instalação do ChromeDriver para ARM
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$(wget -q -O - https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip

# Defina a variável de ambiente para o ChromeDriver
ENV PATH="/usr/local/bin:${PATH}"

# Instala outras dependências Python necessárias
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
