from sqlalchemy import create_engine, text

def setup_database(db_url_base: str, db_name: str):
    """
    Garante que o banco de dados e todas as tabelas necessárias existam.

    Args:
        db_url_base (str): A string de conexão sem o nome do banco de dados.
        db_name (str): O nome do banco de dados a ser criado/verificado.
    """
    print(f"--- Configurando Banco de Dados: '{db_name}' ---")
    
    
    try:
        engine_base = create_engine(db_url_base)
        with engine_base.connect() as connection:
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
            connection.commit()
        print(f"Banco de dados '{db_name}' verificado/criado com sucesso.")
    except Exception as e:
        print(f"Erro ao criar o banco de dados: {e}")
        raise

    
    sql_create_table_paranagua = """
    CREATE TABLE IF NOT EXISTS navios_paranagua (
        id INT AUTO_INCREMENT PRIMARY KEY,
        programacao BIGINT,
        duv VARCHAR(255),
        berco VARCHAR(255),
        embarcacao VARCHAR(255),
        imo BIGINT,
        loa DECIMAL(10, 2),
        dwt DECIMAL(10, 2),
        sentido VARCHAR(50),
        agencia VARCHAR(255),
        operador VARCHAR(255),
        mercadoria VARCHAR(255) NOT NULL DEFAULT '', 
        eta DATETIME,
        janela_operacional VARCHAR(255),
        prancha_t_dia VARCHAR(255),
        previsto VARCHAR(255),
        calado_chegada DECIMAL(5, 2),
        calado_saida DECIMAL(5, 2),
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        UNIQUE KEY uk_prog_merc (programacao, mercadoria)
    );
    """

    sql_create_table_santos = """
    CREATE TABLE IF NOT EXISTS navios_santos (
        id INT PRIMARY KEY AUTO_INCREMENT,
        navio VARCHAR(100),
        bandeira VARCHAR(50),
        com DECIMAL(10, 2),
        cal DECIMAL(10, 2),
        nav VARCHAR(20),
        chegada DATETIME,
        carimbo VARCHAR(50),
        agencia VARCHAR(150),
        operacao VARCHAR(50),
        mercadoria VARCHAR(100),
        peso INT,
        viagem VARCHAR(50),
        duv BIGINT,
        p VARCHAR(20),
        terminal VARCHAR(50),
        imo BIGINT,
        UNIQUE KEY uk_navio_viagem (navio, viagem),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    """

    sql_create_table_agregado = """
    CREATE TABLE IF NOT EXISTS agregado_mercadoria_sentido (
        id INT AUTO_INCREMENT PRIMARY KEY,
        porto VARCHAR(50) NOT NULL,
        embarcacao VARCHAR(255),
        mercadoria VARCHAR(255),
        sentido VARCHAR(50),
        data_viagem DATETIME
    );
    """

    
    try:
        db_connection_string = f"{db_url_base}/{db_name}"
        engine_db = create_engine(db_connection_string)
        
        with engine_db.connect() as connection:
            connection.execute(text(sql_create_table_paranagua))
            connection.execute(text(sql_create_table_santos))
            connection.execute(text(sql_create_table_agregado))
            connection.commit()
        print("Tabelas 'navios_paranagua', 'navios_santos' e 'agregado_mercadoria_sentido' verificadas/criadas.")
    
    except Exception as e:
        print(f"Erro ao criar as tabelas: {e}")
        raise
    
    print("--- Configuração do Banco de Dados concluída ---\n")



if __name__ == '__main__':
    DB_URL_BASE_TEST = "mysql+pymysql://root:mysqldb@localhost"
    DB_NAME_TEST = "paranagua"
    setup_database(DB_URL_BASE_TEST, DB_NAME_TEST)