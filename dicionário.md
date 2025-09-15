# Dicionário de Dados - Pipeline Portuário


## Tabela `navios_paranagua`

Esta tabela armazena os dados limpos e estruturados da camada Silver, originários do site do Porto de Paranaguá.

* **Fonte**: [Line-Up de Navios - APPA](https://www.appaweb.appa.pr.gov.br/appaweb/pesquisa.aspx?WCI=relLineUpRetroativo)

| Nome da Coluna | Tipo de Dado | Descrição |
| :--- | :--- | :--- |
| `id` | `INT` | Identificador único da linha, gerado automaticamente pelo banco de dados. |
| `programacao` | `BIGINT` | Número da programação da atracação, fornecido pela autoridade portuária. |
| `duv` | `VARCHAR(255)` | Documento Único Virtual, um identificador da operação. |
| `berco` | `VARCHAR(255)` | Local específico de atracação do navio no porto. |
| `embarcacao` | `VARCHAR(255)` | Nome oficial do navio. |
| `imo` | `BIGINT` | Número da IMO (International Maritime Organization), identificador único mundial da embarcação. |
| `loa` | `DECIMAL(10, 2)` | "Length Over All", o comprimento máximo do navio em metros. |
| `dwt` | `DECIMAL(10, 2)` | "Deadweight Tonnage", a capacidade de carga total do navio em toneladas. |
| `sentido` | `VARCHAR(50)` | Sentido da operação, contendo os valores brutos do site (`imp`, `exp`, `imp/exp`). |
| `agencia` | `VARCHAR(255)` | Nome da agência marítima responsável pela embarcação. |
| `operador` | `VARCHAR(255)` | Nome do operador portuário que realiza a movimentação da carga. |
| `mercadoria` | `VARCHAR(255)` | Descrição da mercadoria a ser movimentada. |
| `eta` | `DATETIME` | "Estimated Time of Arrival", a data e hora estimadas de chegada do navio. |
| `janela_operacional` | `VARCHAR(255)` | Período de tempo designado para a operação do navio. |
| `prancha_t_dia` | `VARCHAR(255)` | Produtividade esperada da operação, em toneladas por dia. |
| `previsto` | `VARCHAR(255)` | Quantidade de carga prevista para a operação, geralmente em toneladas. |
| `calado_chegada` | `DECIMAL(5, 2)` | Profundidade que o casco do navio atinge na água na chegada (calado), em metros. |
| `calado_saida` | `DECIMAL(5, 2)` | Profundidade que o casco do navio atinge na água na saída (calado), em metros. |
| `data_criacao` | `TIMESTAMP` | Data e hora em que o registro foi inserido pela primeira vez no banco de dados. |
| `data_atualizacao`| `TIMESTAMP` | Data e hora da última atualização do registro. |

## Tabela `navios_santos`

Esta tabela armazena os dados limpos e estruturados da camada Silver, originários da planilha de navios esperados do Porto de Santos.

* **Fonte**: [Navios Esperados Carga - Porto de Santos](https://www.portodesantos.com.br/informacoes-operacionais/operacoes-portuarias/navegacao-e-movimento-de-navios/navios-esperados-carga/) (via botão "Exportar para planilha").

| Nome da Coluna | Tipo de Dado | Descrição |
| :--- | :--- | :--- |
| `id` | `INT` | Identificador único da linha, gerado automaticamente pelo banco de dados. |
| `navio` | `VARCHAR(100)` | Nome oficial do navio. |
| `bandeira` | `VARCHAR(50)` | País de registro da bandeira da embarcação. |
| `com` | `DECIMAL(10, 2)` | Comprimento do navio em metros (equivalente ao LOA). |
| `cal` | `DECIMAL(10, 2)` | Calado do navio em metros (profundidade do casco na água). |
| `nav` | `VARCHAR(20)` | Código ou tipo de navegação. |
| `chegada` | `DATETIME` | Data e hora de chegada registrada. |
| `carimbo` | `VARCHAR(50)` | Identificador ou carimbo de tempo associado ao registro na planilha. |
| `agencia` | `VARCHAR(150)` | Nome da agência marítima responsável. |
| `operacao` | `VARCHAR(50)` | Tipo de operação, contendo os valores brutos da planilha (`EMB`, `DESC`, `EMB/DESC`). |
| `mercadoria` | `VARCHAR(100)` | Descrição da mercadoria a ser movimentada. |
| `peso` | `INT` | Peso da carga em toneladas. |
| `viagem` | `VARCHAR(50)` | Número ou código da viagem, usado como parte da chave de negócio com `navio`. |
| `duv` | `BIGINT` | Documento Único Virtual, um identificador da operação. |
| `p` | `VARCHAR(20)` | Um código ou indicador presente na planilha original, de significado não especificado. |
| `terminal` | `VARCHAR(50)` | Terminal portuário onde a operação ocorrerá. |
| `imo` | `BIGINT` | Número da IMO, identificador único mundial da embarcação. |
| `created_at` | `TIMESTAMP` | Data e hora em que o registro foi inserido pela primeira vez. |
| `updated_at` | `TIMESTAMP` | Data e hora da última atualização do registro. |

## Tabela `agregado_mercadoria_sentido`

Esta é a tabela final da camada Gold. Ela unifica os dados de ambos os portos, pronta para análise.

| Nome da Coluna | Tipo de Dado | Descrição |
| :--- | :--- | :--- |
| `id` | `INT` | Identificador único da linha, gerado automaticamente. |
| `porto` | `VARCHAR(50)` | Nome do porto onde a viagem ocorreu. Valor adicionado ('Paranaguá' ou 'Santos'). |
| `embarcacao` | `VARCHAR(255)` | Nome padronizado da embarcação. Unificação de `navios_paranagua.embarcacao` e `navios_santos.navio`. |
| `mercadoria` | `VARCHAR(255)` | Nome padronizado da mercadoria, originário das tabelas Silver. |
| `sentido` | `VARCHAR(50)` | Sentido padronizado da operação ('Importação' ou 'Exportação'). Derivado da unificação e tradução de `navios_paranagua.sentido` e `navios_santos.operacao`. |
| `data_viagem` | `DATETIME` | Data e hora do evento (chegada/ETA). Unificação de `navios_paranagua.eta` e `navios_santos.chegada`. |