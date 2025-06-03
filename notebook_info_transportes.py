# COMMAND ----------
# MAGIC # Projeto: Análise de Corridas de Transporte Privado
# MAGIC 
# MAGIC Este notebook segue a arquitetura *medallion* (bronze → silver → gold) para tratar os dados de corridas e gerar uma tabela agregada `info_corridas_do_dia`.
# MAGIC 
# MAGIC **Fonte de dados:** CSV `info_transportes.csv`  
# MAGIC **Objetivo:** Gerar métricas diárias como total de corridas, categorias, distância média/máxima/mínima e propósitos.
# MAGIC 
# COMMAND ----------
# Leitura crua do CSV
df_bronze = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("/FileStore/info_transportes.csv")
)

# Persistência como tabela Delta na camada bronze
df_bronze.write.format("delta").mode("overwrite").saveAsTable("bronze.info_transportes_raw")
display(df_bronze)

# COMMAND ----------
from pyspark.sql.functions import to_timestamp, col, coalesce
from pyspark.sql.types import DoubleType
from pyspark.sql import functions as F

# Lê da camada bronze
df_bronze = spark.table("bronze.info_transportes_raw")

# Tentativa de conversão com múltiplos formatos
df_silver = (
    df_bronze
    .withColumn("DATA_INICIO_TS",
        coalesce(
            to_timestamp("DATA_INICIO", "MM-dd-yyyy HH"),
            to_timestamp("DATA_INICIO", "yyyy-MM-dd HH"),
            to_timestamp("DATA_INICIO", "dd-MM-yyyy HH")
        )
    )
    .withColumn("DATA_FIM_TS",
        coalesce(
            to_timestamp("DATA_FIM", "MM-dd-yyyy HH"),
            to_timestamp("DATA_FIM", "yyyy-MM-dd HH"),
            to_timestamp("DATA_FIM", "dd-MM-yyyy HH")
        )
    )
    .withColumn("DISTANCIA", col("DISTANCIA").cast(DoubleType()))
    .dropna(subset=["DATA_INICIO_TS", "DISTANCIA"])
)

# Persistência como Delta na camada silver
df_silver.write.format("delta").mode("overwrite").saveAsTable("silver.info_transportes_tratado")
display(df_silver)

# COMMAND ----------
from pyspark.sql.functions import date_format, count, avg, min, max, when

df_silver = spark.table("silver.info_transportes_tratado")

df_gold = (
    df_silver
    .withColumn("DT_REFE", date_format("DATA_INICIO_TS", "yyyy-MM-dd"))
    .groupBy("DT_REFE")
    .agg(
        count("*").alias("QT_CORR"),
        count(when(col("CATEGORIA") == "Negócio", True)).alias("QT_CORR_NEG"),
        count(when(col("CATEGORIA") == "Pessoal", True)).alias("QT_CORR_PESS"),
        max("DISTANCIA").alias("VL_MAX_DIST"),
        min("DISTANCIA").alias("VL_MIN_DIST"),
        avg("DISTANCIA").alias("VL_AVG_DIST"),
        count(when(col("PROPOSITO") == "Reunião", True)).alias("QT_CORR_REUNI"),
        count(when((col("PROPOSITO").isNotNull()) & (col("PROPOSITO") != "Reunião"), True)).alias("QT_CORR_NAO_REUNI")
    )
)

df_gold.write.format("delta").mode("overwrite").saveAsTable("gold.info_corridas_do_dia")
display(df_gold)

