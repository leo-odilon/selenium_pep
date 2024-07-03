from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
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

# Selecionar os valores nos dropdowns
select1 = Select(driver.find_element(By.ID, "links-anos"))
select1.select_by_index(0)

select2 = Select(driver.find_element(By.ID, "links-meses"))
select2.select_by_index(0)

# Clicar no botão para baixar o arquivo
download_button = driver.find_element(By.ID, "btn")
download_button.click()

# Aguardar o download
time.sleep(10)  # Ajuste o tempo conforme necessário

driver.quit()
