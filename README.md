# Pipeline de Dados - Portos de Santos e Paranaguá

Este projeto implementa um pipeline de dados para coletar, processar e unificar informações sobre a programação de navios esperados dos portos de Santos e Paranaguá.

## Funcionalidades

* **Extração Automática**: Coleta de dados diretamente dos sites oficiais dos portos via web scraping e automação de navegador.
Santos: https://www.portodesantos.com.br/informacoes-operacionais/operacoes-portuarias/navegacao-e-movimento-de-navios/navios-esperados-carga/
Paranaguá: https://www.appaweb.appa.pr.gov.br/appaweb/pesquisa.aspx?WCI=relLineUpRetroativo
* **Setup Automatizado do Banco de Dados**: O pipeline verifica e cria o banco de dados e as tabelas necessárias na primeira execução.
* **Estrutura de Camadas**: O projeto utiliza a arquitetura Medallion (Bronze, Silver, Gold). 
* **Limpeza e Padronização**: Os dados brutos são limpos, formatados e estruturados em tabelas SQL.
* **Agregação de Dados**: As informações dos dois portos são unificadas em uma tabela final (camada Gold) pronta para consumo.

## Arquitetura do Pipeline

O pipeline é dividido da seguinte maneira:

1.  **Setup do Banco de Dados (`/src/modelo_database.py`)**: Garante que toda a estrutura de banco de dados e tabelas esteja pronta para receber os dados.
2.  **Camada Bronze (`/src/bronze`)**: Responsável pela extração dos dados brutos dos sites. Os dados são salvos localmente sem nenhuma modificação.
3.  **Camada Silver (`/src/silver`)**: Responsável por ler os dados brutos, aplicar regras de limpeza, conversão de tipos e carregar os dados em tabelas SQL.
4.  **Camada Gold (`/src/gold`)**: Responsável por ler os dados já limpos da camada Silver, unificar as informações e salvar o resultado em uma tabela agregada final.

## Estrutura do Projeto

```

/projeto\_portos/
|-- data/
|   |-- bronze/
|-- src/
|   |-- modelo\_database.py
|   |-- bronze/
|   |   |-- extractor\_santos.py
|   |   |-- scrape\_paranagua.py
|   |-- silver/
|   |   |-- inserir\_paranagua.py
|   |   |-- inserir\_santos\_2\_.py
|   |-- gold/
|   |   |-- agregados.py
|
|-- main.py
|-- requirements.txt
|-- README.md

````

## Tecnologias Utilizadas

* **Linguagem**: Python 3.9+
* **Bibliotecas**:
    * Pandas, SQLAlchemy, PyMySQL
    * Playwright, Requests, BeautifulSoup4
    * lxml, openpyxl
* **Banco de Dados**: MySQL

---

## Instalação e Configuração

Siga os passos abaixo para configurar o ambiente e rodar o projeto.

### 1. Pré-requisitos

* Python 3.9 ou superior instalado.
* Acesso a um servidor de banco de dados MySQL.

### 2. Clone o Repositório (Exemplo)

```bash
git clone <url-do-seu-repositorio>
cd projeto_portos
````

### 3\. Crie um Ambiente Virtual (Recomendado)

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 4\. Instale as Dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias.

```bash
pip install -r requirements.txt
```

### 5\. Instale os Navegadores do Playwright

Este passo é para a extração de dados de Santos.

```bash
playwright install
```

### 6\. Configure a Conexão com o Banco de Dados

Este é um passo de configuração manual. Abra o arquivo `main.py` e edite as variáveis de conexão para apontar para o seu servidor MySQL.

```python

DB_URL_BASE = "mysql+pymysql://root:mysqldb@localhost"
DB_NAME = "lineup"
DB_CONNECTION_STR = f"{DB_URL_BASE}/{DB_NAME}"

```

O script `modelo_database.py` usará essas variáveis para criar o banco de dados (`lineup`) e todas as tabelas automaticamente na primeira execução, caso ainda não existam.

-----

## Como Executar o Pipeline

Com tudo configurado, basta executar o script `main.py` a partir da pasta raiz do projeto. Ele irá orquestrar todas as etapas em sequência.

```bash
python main.py
```

O terminal exibirá o progresso de cada etapa:

1.  **Configuração do Banco de Dados**: Verificação e/ou criação do schema.
2.  **Etapa Bronze**: Extração dos dados dos portos.
3.  **Etapa Silver**: Limpeza e carga nas tabelas individuais.
4.  **Etapa Gold**: Agregação dos dados na tabela final.

```
