# /projeto_portos/main.py

import os
import datetime
import sys

# Adiciona o diretório 'src' ao path do Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Importa as funções de cada etapa do pipeline
from src.modelo_database import setup_database # <-- ADICIONADO
from bronze.extractor_santos import extract_santos_data
from bronze.scrape_paranagua import scrape_paranagua_data
from silver.inserir_paranagua import insert_paranagua_data
from silver.inserir_santos import insert_santos_data
from gold.agregados import run_aggregation

# --- CONFIGURAÇÃO CENTRALIZADA ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BRONZE_DATA_PATH = os.path.join(BASE_DIR, 'data', 'bronze')
os.makedirs(BRONZE_DATA_PATH, exist_ok=True)

# Configurações de Banco de Dados separadas para mais clareza
DB_URL_BASE = "mysql+pymysql://root:mysqldb@localhost"
DB_NAME = "lineup"
DB_CONNECTION_STR = f"{DB_URL_BASE}/{DB_NAME}"
# ------------------------------------

def run_pipeline():

    print("INICIANDO PIPELINE DE DADOS DOS PORTOS")
    print(f"Data de execução: {datetime.date.today()}")
    try:
       
        setup_database(DB_URL_BASE, DB_NAME)

        print("Etapa Bronze: Iniciando Extração")
        
        santos_raw_file = extract_santos_data(BRONZE_DATA_PATH)
        print(f"Dados de Santos salvos em: {os.path.basename(santos_raw_file)}")

        paranagua_raw_file = scrape_paranagua_data(BRONZE_DATA_PATH)
        print(f"Dados de Paranaguá salvos em: {os.path.basename(paranagua_raw_file)}\n")

        
        print("--- Etapa Silver: Iniciando Limpeza e Inserção ---")
        
        insert_paranagua_data(paranagua_raw_file, DB_CONNECTION_STR)
        print(f"Dados de Paranaguá inseridos/atualizados na tabela 'navios_paranagua'.\n")

        insert_santos_data(santos_raw_file, DB_CONNECTION_STR)
        print(f"Dados de Santos inseridos/atualizados na tabela 'navios_santos'.\n")
        
        
        print("--- Etapa Gold: Iniciando Agregação ---")
        
        run_aggregation(DB_CONNECTION_STR)
        print("Tabela de agregados criada/atualizada com sucesso.\n")

        
        print("PIPELINE CONCLUÍDO COM SUCESSO!")
       

    except Exception as e:
        
        print(f"ERRO CRÍTICO NO PIPELINE: {e}")
       
        
if __name__ == "__main__":
    run_pipeline()