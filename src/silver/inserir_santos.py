import pandas as pd
from sqlalchemy import create_engine, text
import unicodedata
import os
import traceback

def normalize_text(text_data):
    if pd.isnull(text_data): return None
    text_data = str(text_data)
    nfkd_form = unicodedata.normalize('NFKD', text_data)
    return nfkd_form.encode('ASCII', 'ignore').decode('utf-8')

def parse_flexible_date(date_string):
    if pd.isnull(date_string) or date_string in ['nan', '']: return pd.NaT
    for fmt in ('%d/%m/%Y %H:%M:%S', '%d/%m/%Y'):
        try: return pd.to_datetime(date_string, format=fmt)
        except ValueError: pass
    return pd.NaT

def insert_santos_data(csv_file_path: str, db_connection_str: str):
    """
    Lê o arquivo CSV de Santos, limpa os dados e usa uma tabela de staging
    para inserir/atualizar na tabela navios_santos.
    """
    print(f"Iniciando inserção para Santos a partir de {os.path.basename(csv_file_path)}...")
    table_name = "navios_santos"
    staging_table_name = "navios_santos_staging"

    try:
        df = pd.read_csv(csv_file_path, delimiter=';', header=1, on_bad_lines='skip', index_col=False, encoding='latin1')
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo CSV de Santos: {e}")
        raise

    col_names = ['navio', 'bandeira', 'com_cal', 'nav', 'chegada', 'carimbo', 'agencia', 'operacao', 'mercadoria', 'peso', 'viagem', 'duv', 'p', 'terminal', 'imo']
    if len(df.columns) != len(col_names):
        print(f"Erro: O número de colunas no CSV de Santos ({len(df.columns)}) não corresponde ao esperado ({len(col_names)}).")
        return

    df.columns = col_names
    com_cal_split = df['com_cal'].astype(str).str.split('\n', n=1, expand=True)
    df['com'] = pd.to_numeric(com_cal_split[0], errors='coerce')
    df['cal'] = pd.to_numeric(com_cal_split[1], errors='coerce') if com_cal_split.shape[1] > 1 else None
    df['chegada'] = df['chegada'].astype(str).str.strip().apply(parse_flexible_date)
    df['peso'] = pd.to_numeric(df['peso'].astype(str).str.replace('\n', '', regex=False), errors='coerce')
    df['duv'] = pd.to_numeric(df['duv'], errors='coerce')
    df['imo'] = pd.to_numeric(df['imo'], errors='coerce')
    
    text_cols = ['navio', 'bandeira', 'nav', 'carimbo', 'agencia', 'operacao', 'mercadoria', 'viagem', 'p', 'terminal']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.replace('\n', '/', regex=False).apply(normalize_text)

    final_columns = ['navio', 'bandeira', 'com', 'cal', 'nav', 'chegada', 'carimbo', 'agencia', 'operacao', 'mercadoria', 'peso', 'viagem', 'duv', 'p', 'terminal', 'imo']
    df_final = df.reindex(columns=final_columns)
    df_final.dropna(subset=['navio', 'viagem'], inplace=True)
    df_final.drop_duplicates(subset=['navio', 'viagem'], keep='first', inplace=True)
    print(f"{len(df_final)} linhas válidas e únicas para inserir/atualizar em Santos.")

    engine = create_engine(db_connection_str)
    
    try:
        with engine.connect() as connection:
            with connection.begin() as transaction:
                df_final.to_sql(staging_table_name, con=connection, if_exists='replace', index=False)
                
                update_sql = text(f"""
                    UPDATE {table_name} t JOIN {staging_table_name} s ON t.navio = s.navio AND t.viagem = s.viagem
                    SET t.bandeira=s.bandeira, t.com=s.com, t.cal=s.cal, t.nav=s.nav, t.chegada=s.chegada, t.carimbo=s.carimbo,
                        t.agencia=s.agencia, t.operacao=s.operacao, t.mercadoria=s.mercadoria, t.peso=s.peso, t.duv=s.duv,
                        t.p=s.p, t.terminal=s.terminal, t.imo=s.imo;
                """)
                result_update = connection.execute(update_sql)
                
                insert_sql = text(f"""
                    INSERT INTO {table_name} (navio, bandeira, com, cal, nav, chegada, carimbo, agencia, operacao, mercadoria, peso, viagem, duv, p, terminal, imo)
                    SELECT s.navio, s.bandeira, s.com, s.cal, s.nav, s.chegada, s.carimbo, s.agencia, s.operacao, s.mercadoria, s.peso, s.viagem, s.duv, s.p, s.terminal, s.imo
                    FROM {staging_table_name} s LEFT JOIN {table_name} t ON s.navio = t.navio AND s.viagem = t.viagem
                    WHERE t.id IS NULL;
                """)
                result_insert = connection.execute(insert_sql)
                
                connection.execute(text(f"DROP TABLE {staging_table_name}"))
                print(f"Resumo Santos -> Inseridos: {result_insert.rowcount}, Atualizados: {result_update.rowcount}")
    except Exception as e:
        print(f"\nOcorreu um erro durante a operação de merge/update de Santos.")
        traceback.print_exc()
        raise