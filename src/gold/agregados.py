import pandas as pd
from sqlalchemy import create_engine

def run_aggregation(db_connection_str: str):
    """
    Lê os dados das tabelas de Paranaguá e Santos, unifica, padroniza e
    cria a tabela agregada final.
    """
    print("Iniciando a criação/atualização da tabela de agregados...")
    engine = create_engine(db_connection_str)
    
    tabela_paranagua = 'navios_paranagua'
    tabela_santos = 'navios_santos'
    tabela_destino = 'agregado_mercadoria_sentido'
    
    query_pna = f"SELECT embarcacao, mercadoria, sentido, eta FROM {tabela_paranagua}"
    query_santos = f"SELECT navio, mercadoria, operacao, chegada FROM {tabela_santos}"

    try:
        df_pna = pd.read_sql(query_pna, engine)
        df_santos = pd.read_sql(query_santos, engine)

        # --- Padronização e Expansão ---
        df_pna['porto'] = 'Paranaguá'
        df_pna.rename(columns={'eta': 'data_viagem'}, inplace=True)
        pna_sentido_map = {'imp': ['Importação'], 'exp': ['Exportação'], 'imp/exp': ['Importação', 'Exportação']}
        df_pna['sentido'] = df_pna['sentido'].str.lower().map(pna_sentido_map)
        df_pna.dropna(subset=['sentido'], inplace=True)
        df_pna = df_pna.explode('sentido')

        df_santos['porto'] = 'Santos'
        df_santos.rename(columns={'operacao': 'sentido', 'navio': 'embarcacao', 'chegada': 'data_viagem'}, inplace=True)
        santos_sentido_map = {'desc': ['Importação'], 'emb': ['Exportação'], 'emb/desc': ['Importação', 'Exportação']}
        df_santos['sentido'] = df_santos['sentido'].str.lower().map(santos_sentido_map)
        df_santos.dropna(subset=['sentido'], inplace=True)
        df_santos = df_santos.explode('sentido')

        # --- Unificação ---
        colunas_finais = ['porto', 'embarcacao', 'mercadoria', 'sentido', 'data_viagem']
        df_agregado = pd.concat([df_pna[colunas_finais], df_santos[colunas_finais]], ignore_index=True)
        df_agregado.dropna(subset=['mercadoria', 'embarcacao', 'data_viagem'], inplace=True)
        
        # --- Carga ---
        print(f"Total de {len(df_agregado)} viagens individuais para inserir na tabela agregada.")
        df_agregado.to_sql(tabela_destino, con=engine, if_exists='replace', index=False)
        
    except Exception as e:
        print("\nOcorreu um erro durante a criação da tabela de agregados.")
        raise