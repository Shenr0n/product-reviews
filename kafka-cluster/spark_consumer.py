from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType

# Define the schema matching the Kafka messages
schema = StructType() \
    .add("id", StringType()) \
    .add("product_id", StringType()) \
    .add("user_id", StringType()) \
    .add("profile_name", StringType()) \
    .add("score", IntegerType()) \
    .add("summary", StringType()) \
    .add("text", StringType())

# Create Spark session
spark = SparkSession.builder \
    .appName("KafkaToParquet") \
    .getOrCreate()

#.option("kafka.bootstrap.servers", "broker1:29092")
# Read stream from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "product-reviews") \
    .option("startingOffsets", "earliest") \
    .load()

# Parse JSON value
df_parsed = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Write stream to Parquet
df_parsed.writeStream \
    .format("parquet") \
    .option("path", "./output") \
    .option("checkpointLocation", "./checkpoint") \
    .outputMode("append") \
    .start() \
    .awaitTermination()