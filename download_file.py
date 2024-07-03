from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time

# Configurações do Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

prefs = {"download.default_directory": "/download/pep"}  # Ajuste o caminho do diretório de download
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Acessar o link
driver.get("https://portaldatransparencia.gov.br/download-de-dados/pep")

# Esperar até que o primeiro dropdown esteja presente e selecioná-lo
try:
    select1_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "links-anos"))
    )
    select1 = Select(select1_element)
    print(select1)
    select1.select_by_index(0)
except Exception as e:
    print(f"Erro ao selecionar o primeiro dropdown: {e}")

# Esperar até que o segundo dropdown esteja presente e selecioná-lo
try:
    select2_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "links-meses"))
    )
    select2 = Select(select2_element)
    print(select2)
    select2.select_by_index(0)
except Exception as e:
    print(f"Erro ao selecionar o segundo dropdown: {e}")

# Esperar até que o botão de download esteja presente e clicar nele
try:
    download_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "btn"))
    )
    download_button.click()
except Exception as e:
    print(f"Erro ao clicar no botão de download: {e}")

# Aguardar o download
time.sleep(10)  # Ajuste o tempo conforme necessário

driver.quit()
