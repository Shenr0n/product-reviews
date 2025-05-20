FROM bitnami/spark:3.5.0

# Copy your Spark job into the container
COPY spark_consumer.py /opt/spark-apps/spark_consumer.py

# Set working directory
WORKDIR /opt/spark-apps

# Run spark-submit with required Kafka package
CMD ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0", "/opt/spark-apps/spark_consumer.py"]