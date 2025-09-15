import pandas as pd
from sqlalchemy import create_engine, text
from decimal import Decimal
import traceback
import os

def clean_data_paranagua(row):
    # (A função de clean_data permanece a mesma, apenas renomeada para clareza)
    cleaned = {}
    cleaned['programacao'] = int(row['Programação']) if pd.notna(row['Programação']) else None
    cleaned['imo'] = int(row['IMO']) if pd.notna(row['IMO']) else None
    
    def to_decimal(value, precision='0.01'):
        if pd.isna(value): return None
        cleaned_value_str = str(value).replace('.', '').replace(',', '.')
        return Decimal(cleaned_value_str).quantize(Decimal(precision))

    cleaned['loa'] = to_decimal(row['LOA'])
    cleaned['dwt'] = to_decimal(row['DWT'])
    cleaned['calado_chegada'] = to_decimal(row['Cal. Cheg.'])
    cleaned['calado_saida'] = to_decimal(row['Cal. Saída'])
    cleaned['eta'] = pd.to_datetime(row['ETA'], format='%d/%m/%Y %H:%M', errors='coerce')
    if pd.isna(cleaned['eta']): cleaned['eta'] = None

    cleaned['berco'] = str(row['Berço']) if pd.notna(row['Berço']) else None
    cleaned['duv'] = str(row['DUV']) if pd.notna(row['DUV']) else None
    cleaned['embarcacao'] = str(row['Embarcação']) if pd.notna(row['Embarcação']) else None
    cleaned['sentido'] = str(row['Sentido']) if pd.notna(row['Sentido']) else None
    cleaned['agencia'] = str(row['Agência']) if pd.notna(row['Agência']) else None
    cleaned['operador'] = str(row['Operador']) if pd.notna(row['Operador']) else None
    cleaned['mercadoria'] = str(row['Mercadoria']) if pd.notna(row['Mercadoria']) else ''
    cleaned['janela_operacional'] = str(row['Janela Operacional']) if pd.notna(row['Janela Operacional']) else None
    cleaned['prancha_t_dia'] = str(row['Prancha (t/dia)']) if pd.notna(row['Prancha (t/dia)']) else None
    cleaned['previsto'] = str(row['Previsto']) if pd.notna(row['Previsto']) else None
    
    return cleaned

def insert_paranagua_data(excel_file_path: str, db_connection_str: str):
    """
    Lê o arquivo Excel de Paranaguá, limpa os dados e insere/atualiza
    na tabela navios_paranagua.
    """
    print(f"Iniciando inserção para Paranaguá a partir de {os.path.basename(excel_file_path)}...")
    table_name = 'navios_paranagua'
    
    try:
        df = pd.read_excel(excel_file_path, sheet_name='Sheet1')
        print(f"{len(df)} linhas encontradas no Excel de Paranaguá.")

        engine = create_engine(db_connection_str)

        stmt_upsert = text(f"""
            INSERT INTO {table_name} (
                programacao, duv, berco, embarcacao, imo, loa, dwt, sentido, 
                agencia, operador, mercadoria, eta, janela_operacional, 
                prancha_t_dia, previsto, calado_chegada, calado_saida
            ) VALUES (
                :programacao, :duv, :berco, :embarcacao, :imo, :loa, :dwt, :sentido, 
                :agencia, :operador, :mercadoria, :eta, :janela_operacional, 
                :prancha_t_dia, :previsto, :calado_chegada, :calado_saida
            )
            ON DUPLICATE KEY UPDATE
                duv = VALUES(duv), berco = VALUES(berco), embarcacao = VALUES(embarcacao),
                imo = VALUES(imo), loa = VALUES(loa), dwt = VALUES(dwt), sentido = VALUES(sentido),
                agencia = VALUES(agencia), operador = VALUES(operador), eta = VALUES(eta),
                janela_operacional = VALUES(janela_operacional), prancha_t_dia = VALUES(prancha_t_dia),
                previsto = VALUES(previsto), calado_chegada = VALUES(calado_chegada),
                calado_saida = VALUES(calado_saida)
        """)

        with engine.begin() as connection:
            total_inserido = 0
            total_atualizado = 0
            for index, row in df.iterrows():
                try:
                    data_to_process = clean_data_paranagua(row)
                    if data_to_process['programacao'] is None: continue
                    result = connection.execute(stmt_upsert, data_to_process)
                    if result.rowcount == 1: total_inserido += 1
                    elif result.rowcount == 2: total_atualizado += 1
                except Exception as row_error:
                    print(f" -> ERRO na linha {index + 2} de Paranaguá: {row_error}")
            print(f"Resumo Paranaguá -> Inseridos: {total_inserido}, Atualizados: {total_atualizado}")
            
    except FileNotFoundError:
        print(f"ERRO: O arquivo '{excel_file_path}' não foi encontrado.")
        raise
    except Exception as e:
        print(f"\nOcorreu um erro durante a inserção de Paranaguá.")
        traceback.print_exc()
        raise