from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType

spark = SparkSession.builder     .appName("IoT Kafka to Delta Bronze")     .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")     .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")     .getOrCreate()

schema = StructType()     .add("sensor_id", StringType())     .add("timestamp", StringType())     .add("temperatura", DoubleType())     .add("umidade", DoubleType())     .add("localizacao", StringType())

df_raw = spark.readStream     .format("kafka")     .option("kafka.bootstrap.servers", "kafka:9092")     .option("subscribe", "iot_sensores")     .option("startingOffsets", "latest")     .load()

df_parsed = df_raw.selectExpr("CAST(value AS STRING) as json")     .select(from_json("json", schema).alias("data"))     .select("data.*")

df_parsed.writeStream     .format("delta")     .outputMode("append")     .option("checkpointLocation", "/tmp/delta/checkpoints/iot_bronze")     .start("/tmp/delta/bronze/iot_sensores")     .awaitTermination()