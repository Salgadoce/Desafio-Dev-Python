from playwright.sync_api import sync_playwright
import datetime
import os

def extract_santos_data(directory_path: str) -> str:
    """
    Navega até o site do Porto de Santos, baixa a planilha de navios esperados
    e a salva no diretório especificado.

    Args:
        directory_path: O caminho da pasta onde o arquivo CSV será salvo.

    Returns:
        O caminho completo do arquivo salvo.
    """
    print("Iniciando extração de Santos...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.portodesantos.com.br/informacoes-operacionais/operacoes-portuarias/navegacao-e-movimento-de-navios/navios-esperados-carga/")
        
        btn = page.locator('//button[contains(., "Exportar para planilha")]')
        btn.wait_for(state="visible", timeout=30000)
        
        with page.expect_download() as download_info:
            btn.click()
        download = download_info.value
        
        data_hoje = datetime.date.today()
        
        suggested_filename = download.suggested_filename
        file_name = f"santos_{data_hoje}_{suggested_filename}"
        
        save_path = os.path.join(directory_path, file_name)
        download.save_as(save_path)
        browser.close()
        
        return save_path

if __name__ == '__main__':
    
    temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    file_path = extract_santos_data(temp_dir)
    print(f"Teste de extração de Santos concluído. Arquivo salvo em: {file_path}")