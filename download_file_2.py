from playwright.sync_api import sync_playwright
import os
import shutil
import time

download_dir = os.getenv("DOWNLOAD_DIR", "/tmp")  # Diretório de download

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(
        accept_downloads=True,
        viewport={'width': 1280, 'height': 1024}
    )
    
    page = context.new_page()

    # Acessar o link
    page.goto("https://portaldatransparencia.gov.br/download-de-dados/pep")
    print(download_dir)

    try:
        # Espera até que o botão esteja visível e clicável
        page.wait_for_selector('#btn', state='visible', timeout=20000)
        download_button = page.query_selector('#btn')
        print(download_button.inner_html())

        # Clica no botão de download
        with page.expect_download() as download_info:
            download_button.click()
        download = download_info.value

        # Salva o arquivo no diretório desejado
        download_path = download.path()
        shutil.move(download_path, os.path.join(download_dir, download.suggested_filename))

    except Exception as e:
        print(f"Erro ao clicar no botão de download: {e}")
        print(page.content())

    # Aguardar o download
    time.sleep(20)  # Ajuste o tempo conforme necessário

    browser.close()

with sync_playwright() as playwright:
    run(playwright)