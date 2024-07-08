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
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-blink-features=AutomationControlled")

download_dir = os.getenv("DOWNLOAD_DIR", "/tmp")  # Diretório de download
prefs = {"download.default_directory": download_dir}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Acessar o link
driver.get("https://www.un.org/securitycouncil/content/un-sc-consolidated-list")
print(download_dir)

try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'documentlinks'))
    )

    # Encontrar o link para o XML
    xml_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, 'Xml'))
    )
    print(xml_link.get_attribute('outerHTML'))

    # Clicar no link do XML para iniciar o download
    xml_link.click()
except Exception as e:
    print(f"Erro ao clicar no botão de download: {e}")
    print(driver.page_source)

# Aguardar o download
time.sleep(20)  # Ajuste o tempo conforme necessário

driver.quit()
