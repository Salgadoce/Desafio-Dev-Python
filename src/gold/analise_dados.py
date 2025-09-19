import pandas as pd
from sqlalchemy import create_engine, text

def run_query(query: str, engine, params: dict = None):
    """
    Executa uma query SQL e retorna o resultado como um DataFrame do Pandas.
    """
    try:
        return pd.read_sql(text(query), engine.connect(), params=params)
    except Exception as e:
        if "doesn't exist" in str(e):
            print(f"ERRO: A tabela de agregados não foi encontrada.")
            print("Por favor, execute o pipeline principal (main.py) primeiro.")
            return pd.DataFrame()
        else:
            print(f"Ocorreu um erro na query: {e}")
            return pd.DataFrame()


def analysis_viagens_por_porto(engine):
    print("--- 1. Total de Viagens Registradas por Porto ---")
    query = "SELECT porto, COUNT(*) AS total_viagens FROM agregado_mercadoria_sentido GROUP BY porto ORDER BY total_viagens DESC;"
    df = run_query(query, engine)
    if not df.empty: print(df.to_string(index=False))
    print("\n" + "="*50 + "\n")

def analysis_operacoes_por_sentido(engine):
    print("--- 2. Distribuição de Operações por Sentido (Importação/Exportação) ---")
    query = "SELECT porto, sentido, COUNT(*) AS total_operacoes FROM agregado_mercadoria_sentido GROUP BY porto, sentido ORDER BY porto, sentido;"
    df = run_query(query, engine)
    if not df.empty: print(df.to_string(index=False))
    print("\n" + "="*50 + "\n")

def analysis_top_mercadorias(engine, top_n=10):
    print(f"--- 3. Top {top_n} Mercadorias Mais Movimentadas (por n° de viagens) ---")
    query = "SELECT mercadoria, COUNT(*) AS total_viagens FROM agregado_mercadoria_sentido GROUP BY mercadoria ORDER BY total_viagens DESC LIMIT :limit;"
    df = run_query(query, engine, params={'limit': top_n})
    if not df.empty: print(df.to_string(index=False))
    print("\n" + "="*50 + "\n")

def analysis_viagens_por_mes(engine):
    print("--- 4. Atividade Mensal (Viagens por Ano/Mês) ---")
    query = "SELECT YEAR(data_viagem) AS ano, MONTH(data_viagem) AS mes, COUNT(*) AS total_viagens FROM agregado_mercadoria_sentido GROUP BY ano, mes ORDER BY ano, mes;"
    df = run_query(query, engine)
    if not df.empty: print(df.to_string(index=False))
    print("\n" + "="*50 + "\n")

def analysis_proximas_viagens(engine, limit=5):
    print(f"--- 5. Próximas {limit} Viagens Agendadas ---")
    query = "SELECT data_viagem, porto, embarcacao, mercadoria, sentido FROM agregado_mercadoria_sentido WHERE data_viagem >= CURDATE() ORDER BY data_viagem ASC LIMIT :limit;"
    df = run_query(query, engine, params={'limit': limit})
    if not df.empty:
        print(df.to_string(index=False))
    else:
        print("Nenhuma viagem futura encontrada nos dados.")
    print("\n" + "="*50 + "\n")

def run_analysis(db_connection_str: str):
    """
    Função principal que orquestra a execução das análises.
    """
    print("\n" + "#"*60)
    print("INICIANDO SCRIPT DE ANÁLISE DE DADOS PORTUÁRIOS ")
    print("#"*60 + "\n")
    
    try:
        engine = create_engine(db_connection_str)
        
        analysis_viagens_por_porto(engine)
        analysis_operacoes_por_sentido(engine)
        analysis_top_mercadorias(engine, top_n=10)
        analysis_viagens_por_mes(engine)
        analysis_proximas_viagens(engine, limit=5)
        
    except Exception as e:
        print(f"Ocorreu um erro ao conectar ao banco de dados para análise: {e}")
        raise


if __name__ == "__main__":
    DB_CONNECTION_STR_TEST = 'mysql+pymysql://root:mysqldb@localhost/lineup'
    run_analysis(DB_CONNECTION_STR_TEST)