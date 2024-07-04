from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

# Configurações do Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-blink-features=AutomationControlled")

download_dir = os.getenv("DOWNLOAD_DIR", "/tmp")  # Diretório de download
prefs = {"download.default_directory": download_dir}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Acessar o link
driver.get("https://portaldatransparencia.gov.br/download-de-dados/pep")
print(download_dir)

try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'btn'))
    )

    # Espera até que o botão esteja visível e clicável
    download_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'btn'))
    )
    print(download_button.get_attribute('outerHTML'))

    # Clica no botão de download
    download_button.click()
except Exception as e:
    print(f"Erro ao clicar no botão de download: {e}")
    print(driver.page_source)

# Aguardar o download
time.sleep(20)  # Ajuste o tempo conforme necessário

driver.quit()
