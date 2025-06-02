# 🚗 Projeto: Análise de Corridas de Transporte Privado

Este projeto demonstra a aplicação da arquitetura **Medallion** (Bronze → Silver → Gold) com **PySpark** e **Delta Lake** em um ambiente **Databricks** para tratar dados de um aplicativo de transporte privado.

---

## 📁 Estrutura do Projeto

- **Bronze**: Ingestão bruta do arquivo CSV `info_transportes.csv`.
- **Silver**: Padronização das colunas de data e criação da coluna `DT_REF` (data de referência).
- **Gold**: Agregações diárias com estatísticas por categoria e propósito das corridas.

---

## 🧪 Dataset de entrada

Arquivo: `info_transportes.csv`  
Colunas:
- `DATA_INICIO`
- `DATA_FIM`
- `CATEGORIA` (`Negócio`, `Pessoal`)
- `LOCAL_INICIO`
- `LOCAL_FIM`
- `PROPOSITO`
- `DISTANCIA`

---

## 📊 Métricas geradas (Tabela Final: `info_corridas_do_dia`)

| Coluna             | Descrição                                                                 |
|--------------------|---------------------------------------------------------------------------|
| `DT_REF`           | Data de referência no formato `yyyy-MM-dd`                                |
| `QT_CORR`          | Quantidade total de corridas no dia                                       |
| `QT_CORR_NEG`      | Quantidade de corridas com categoria **Negócio**                          |
| `QT_CORR_PESS`     | Quantidade de corridas com categoria **Pessoal**                          |
| `VL_MAX_DIST`      | Maior distância registrada em uma corrida no dia                          |
| `VL_MIN_DIST`      | Menor distância registrada em uma corrida no dia                          |
| `VL_AVG_DIST`      | Distância média das corridas no dia                                       |
| `QT_CORR_REUNI`    | Quantidade de corridas com propósito **Reunião**                          |
| `QT_CORR_NAO_REUNI`| Quantidade de corridas com propósito **diferente de Reunião**             |

---

## 🛠️ Ferramentas utilizadas

- Apache Spark (PySpark)
- Delta Lake
- Databricks Community Edition
- Pandas (para leitura inicial)

---

## 🧠 Destaques técnicos

- Implementação com **funções reutilizáveis** para tratamento e transformação
- Separação clara das camadas do Lakehouse
- Uso de funções do Spark SQL para limpeza, parsing e agregações

---

## 📌 Execução

O notebook pode ser executado diretamente no ambiente Databricks.  
Certifique-se de fazer o upload do arquivo `info_transportes.csv` para o DBFS em `/FileStore/`.

---