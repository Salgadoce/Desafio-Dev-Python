from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime


url = 'https://www.appaweb.appa.pr.gov.br/appaweb/pesquisa.aspx?WCI=relLineUpRetroativo'

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')
#Separar a tabela de interesse, ESPERADOS
table = soup.find_all('table')[5]

titles = table.find_all('th')

table_titles = [title.text for title in titles]

ini = table_titles.index(" Programação")
fim = table_titles.index(" Cal. Saída")

limpo = [item.strip() for item in table_titles[ini:fim+1]]

column_data = table.find_all('tr')
dados_comuns_salvos = []
dados_processados = []

for row in column_data[2:]:
    
    row_data = row.find_all('td')
    individual_row_data = [data.text for data in row_data]
    
    cleaned_row = individual_row_data[1:]
    #Detectar e corrigir linhas que estão aninhadas
    if len(cleaned_row) > 12:
        dados_processados.append(cleaned_row)
        dados_comuns_salvos = cleaned_row[:8]
    elif len(cleaned_row) > 0 and dados_comuns_salvos:
        linha_completa_nova = dados_comuns_salvos + cleaned_row
        dados_processados.append(linha_completa_nova)
    
df = pd.DataFrame(dados_processados, columns=limpo)


data_hoje = datetime.date.today()
caminho = rf'C:\Users\julio\OneDrive\Área de Trabalho\lineup\dados brutos\paranagua_dados{data_hoje}.csv'
df.to_csv(caminho, index=False, sep=';', encoding='utf-8-sig')

print("salvo com sucesso em:", caminho)



#df.to_csv(r'C:\Users\julio\OneDrive\Área de Trabalho\Nova pasta (2)\dados.csv')



