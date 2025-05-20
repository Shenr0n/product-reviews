from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType

# Schema based on kafka messages
schema = StructType() \
    .add("id", StringType()) \
    .add("product_id", StringType()) \
    .add("user_id", StringType()) \
    .add("profile_name", StringType()) \
    .add("score", IntegerType(), nullable=True) \
    .add("summary", StringType(), nullable=True) \
    .add("text", StringType(), nullable=True)

spark = SparkSession.builder.appName("KafkaToParquet").getOrCreate()


# Read stream from Kafka, with the broker endpoint, using kafka connector
#.option("kafka.bootstrap.servers", "broker1:29092")
# subscribe to product-reviews topic
# startingOffsets to read from start
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker1:29092") \
    .option("subscribe", "product-reviews") \
    .option("startingOffsets", "earliest") \
    .load()

# parse and convert entire binary kafka message to json string
# convert json string into dataframe based on schema and flatten it
df_parsed = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")


#write as parquet with microbatch of 10 seconds, append mode to write only new rows
# start to start query and run it for 10 minutes
df_parsed.writeStream \
    .trigger(processingTime = '10 seconds') \
    .format("parquet") \
    .option("path", "/opt/output") \
    .option("checkpointLocation", "/opt/output/checkpoint") \
    .outputMode("append") \
    .start() \
    .awaitTermination(600)