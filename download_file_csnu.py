from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os
import time

# Configurações do Selenium
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.page_load_strategy = 'eager'

download_dir = os.getenv("DOWNLOAD_DIR", "/tmp")  # Diretório de download
prefs = {"download.default_directory": download_dir}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

time.sleep(3.5)

# Acessar o link
driver.get("https://www.un.org/securitycouncil/content/un-sc-consolidated-list")
print(download_dir)

try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.documentlinks.uw-link-btn'))
    )

    # Encontrar todos os links pelo seletor CSS
    links = driver.find_elements(By.CSS_SELECTOR, 'a.documentlinks.uw-link-btn')

    # Filtrar o link desejado com base no texto do link
    xml_link = None
    for link in links:
        if link.text.strip().lower() == 'xml':
            xml_link = link
            break

    # Verificar se o link foi encontrado
    if xml_link:
        xml_url = xml_link.get_attribute('href')
        print(f"URL do XML: {xml_url}")

        # Fazer o download do arquivo XML
        response = requests.get(xml_url, verify=False)
        if response.status_code == 200:
            xml_path = os.path.join(download_dir, 'consolidated.xml')
            with open(xml_path, 'wb') as file:
                file.write(response.content)
            print(f"XML baixado com sucesso: {xml_path}")
        else:
            print(f"Falha ao baixar o XML. Status code: {response.status_code}")
    else:
        print("Link para o XML não encontrado.")
except Exception as e:
    print(f"Erro ao clicar no botão de download: {e}")
    print(driver.page_source)

# Aguardar o download
time.sleep(5)  # Ajuste o tempo conforme necessário

driver.quit()
