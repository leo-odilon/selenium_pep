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
        # Clicar no link do XML para abrir a página
        xml_link.click()

        # Aguardar a página carregar
        time.sleep(20)  # Ajuste o tempo conforme necessário

        # Criar um arquivo em branco no diretório de destino
        xml_path = os.path.join(download_dir, 'csnu.xml')
        open(xml_path, 'w').close()

        # Obter o conteúdo visível na página
        page_content = driver.execute_script("return document.body.innerText")

        # Salvar o conteúdo em um arquivo XML
        with open(xml_path, 'w', encoding='utf-8') as file:
            file.write(page_content)
        print(f"XML salvo com sucesso: {xml_path}")
    else:
        print("Link para o XML não encontrado.")
except Exception as e:
    print(f"Erro ao clicar no botão de download: {e}")
    print(driver.page_source)

# Aguardar o download
time.sleep(5)  # Ajuste o tempo conforme necessário

driver.quit()
