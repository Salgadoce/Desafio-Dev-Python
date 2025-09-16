# Hipóteses e Considerações do Projeto

Este documento descreve as principais hipóteses, decisões de design e considerações adotadas durante o desenvolvimento do pipeline de dados dos portos.

## 1. Fontes de Dados

* **Fonte de Paranaguá**: No relatório HTML do Porto de Paranaguá, que contém múltiplas tabelas (Atracados, Esperados, etc.), foi adotada a premissa de que apenas a tabela "ESPERADOS" é de interesse para este projeto. O script de extração foi construído para buscar especificamente esta tabela.
* **Fonte de Santos**: A planilha CSV baixada do Porto de Santos é utilizada em sua totalidade. A hipótese é que a pesquisa no site que gera este relatório já filtra as embarcações de interesse (navios de carga esperados).
* **Estabilidade das Fontes**: Assume-se que as URLs dos sites e a estrutura geral das páginas (para Paranaguá) e do arquivo CSV (para Santos) permanecerão estáveis. Alterações na estrutura das fontes exigirão manutenção no código.

## 2. Arquitetura

* **Orquestração Centralizada**: Todas as etapas do pipeline são gerenciadas e executadas em sequência por um script orquestrador (`main.py`). Se qualquer etapa falhar, o pipeline inteiro é interrompido.
* **Banco de Dados**: O pipeline foi desenvolvido e otimizado para MySQL. A sintaxe SQL utilizada é específica deste sistema de banco de dados.

## 3. Extração (Camada Bronze)

* **Extração de Paranaguá**: A extração dos dados de Paranaguá depende da posição da tabela "ESPERADOS" no HTML (`soup.find_all('table')[5]`).  Uma alteração no layout da página de origem irá quebrar a extração.
* **Frequência de Execução**: O pipeline foi projetado para ser executado diariamente. Os nomes dos arquivos brutos gerados incluem a data da execução para manter um histórico dos arquivos extraídos na camada Bronze.

## 4. Limpeza e Carga (Camada Silver)

* **Definição das Chaves de Negócio**: Foram feitas análises para definir o que constitui um registro único em cada fonte:
    * **Paranaguá**: A chave única de uma operação é a combinação `(programacao, mercadoria)`.
    * **Santos**: A chave única de uma operação é a combinação `(navio, viagem)`.
* **Preparação para o Futuro**: No relatório de Paranaguá, os campos "Janela Operacional" e "Prancha (t/dia)" foram observados como consistentemente vazios na fonte. Mesmo assim, as colunas `janela_operacional` e `prancha_t_dia` foram criadas na tabela `navios_paranagua`. Esta decisão foi tomada para tornar a base de dados preparada para eventualmente armazenar essas informações caso a fonte de dados comece a fornecê-las no futuro.
* **Regra de Negócio para Sentidos Duplos**: Foi implementada uma regra de negócio específica para tratar registros onde o sentido da operação é duplo (ex: `imp/exp` em Paranaguá e `EMB/DESC` em Santos). A decisão foi "explodir" cada um desses registros em duas linhas separadas na camada de agregação, uma para 'Importação' e outra para 'Exportação'.

## 5. Agregação (Camada Gold)

* **Estratégia de Atualização `REPLACE`**: A tabela final `agregado_mercadoria_sentido` é completamente reconstruída a cada execução do pipeline (`if_exists='replace'`). Esta abordagem foi escolhida pela simplicidade. Para volumes de dados muito grandes no futuro, uma estratégia de carga incremental poderia ser considerada.
* **Diferenciação de Viagens**: A premissa adotada é que registros com `(embarcacao, mercadoria, sentido)` idênticos representam viagens distintas se possuírem uma (`data_viagem`) diferente. A data foi considerada o elemento chave para diferenciar eventos de negócio. 
