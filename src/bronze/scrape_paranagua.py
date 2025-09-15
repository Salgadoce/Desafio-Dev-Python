import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import os

def scrape_paranagua_data(directory_path: str) -> str:
    """
    Faz o scrape da tabela de navios do site da APPA e salva como um arquivo Excel.

    Args:
        directory_path: O caminho da pasta onde o arquivo .xlsx será salvo.

    Returns:
        O caminho completo do arquivo salvo.
    """
    print("Iniciando extração de Paranaguá...")
    url = 'https://www.appaweb.appa.pr.gov.br/appaweb/pesquisa.aspx?WCI=relLineUpRetroativo'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    table = soup.find_all('table')[5]
    titles = table.find_all('th')
    table_titles = [title.text for title in titles]
    
    ini = table_titles.index(" Programação")
    fim = table_titles.index(" Cal. Saída")
    limpo = [item.strip() for item in table_titles[ini:fim+1]]
    
    column_data = table.find_all('tr')
    dados_processados = []
    dados_comuns_salvos = []
    
    for row in column_data[2:]:
        row_data = row.find_all('td')
        individual_row_data = [data.text for data in row_data]
        cleaned_row = individual_row_data[1:]
        
        if len(cleaned_row) > 12:
            dados_processados.append(cleaned_row)
            dados_comuns_salvos = cleaned_row[:8]
        elif len(cleaned_row) > 0 and dados_comuns_salvos:
            linha_completa_nova = dados_comuns_salvos + cleaned_row
            dados_processados.append(linha_completa_nova)
            
    df = pd.DataFrame(dados_processados, columns=limpo)
    
    data_hoje = datetime.date.today()
    file_name = f'paranagua_dados_{data_hoje}.xlsx'
    save_path = os.path.join(directory_path, file_name)
    
    df.to_excel(save_path, index=False)
    
    return save_path


if __name__ == '__main__':
    temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    file_path = scrape_paranagua_data(temp_dir)
    print(f"Teste de extração de Paranaguá concluído. Arquivo salvo em: {file_path}")