
from sqlalchemy import create_engine
from sqlalchemy import text

connection_string = "mysql+pymysql://root:mysqldb@localhost"
engine = create_engine(connection_string, echo=True)

sql_command = f"CREATE DATABASE IF NOT EXISTS paranagua"


with engine.connect() as connection:
    connection.execute(text(sql_command))
    connection.commit()

db_connection_string = f"mysql+pymysql://root:mysqldb@localhost/paranagua"
db_engine = create_engine(db_connection_string, echo=True)

sql_create_table_command = "CREATE TABLE programacao_navios(\
    id INT PRIMARY KEY AUTO_INCREMENT,\
    programacao INT,\
    duv VARCHAR(50),\
    berco VARCHAR(10),\
    embarcacao VARCHAR(100),\
    imo INT ,\
    loa DECIMAL(7, 2),\
    dwt DECIMAL(10, 2),\
    sentido VARCHAR(20),\
    agencia VARCHAR(100),\
    operador VARCHAR(100),\
    mercadoria VARCHAR(255),\
    eta DATETIME,\
    janela_operacional VARCHAR(100),\
    prancha_t_dia VARCHAR(50),\
    previsto VARCHAR(50),\
    calado_chegada DECIMAL(5, 2),\
    calado_saida DECIMAL(5, 2)\
);"

with db_engine.connect() as connection:
    connection.execute(text(sql_create_table_command))
    connection.commit()