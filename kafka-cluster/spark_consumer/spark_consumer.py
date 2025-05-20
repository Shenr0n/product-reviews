from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType

# Schema based on kafka messages
schema = StructType() \
    .add("id", StringType()) \
    .add("product_id", StringType()) \
    .add("user_id", StringType()) \
    .add("profile_name", StringType()) \
    .add("score", IntegerType()) \
    .add("summary", StringType()) \
    .add("text", StringType())

spark = SparkSession.builder.appName("KafkaToParquet").getOrCreate()


# Read stream from Kafka
#.option("kafka.bootstrap.servers", "broker1:29092")
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker1:29092") \
    .option("subscribe", "product-reviews") \
    .option("startingOffsets", "earliest") \
    .load()

df_parsed = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")


df_parsed.writeStream \
    .trigger(processingTime = '10 seconds') \
    .format("parquet") \
    .option("path", "/opt/output") \
    .option("checkpointLocation", "/opt/output/checkpoint") \
    .outputMode("append") \
    .start() \
    .awaitTermination(600)