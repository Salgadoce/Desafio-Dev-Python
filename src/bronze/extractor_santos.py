from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.portodesantos.com.br/informacoes-operacionais/operacoes-portuarias/navegacao-e-movimento-de-navios/navios-esperados-carga/")

    
    btn = page.locator('//button[contains(., "Exportar para planilha")]')
    btn.wait_for(state="visible", timeout=30000)

    
    with page.expect_download() as download_info:
        btn.click()
    download = download_info.value
    download.save_as("esperados.csv")

    browser.close()
