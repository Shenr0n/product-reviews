import os
import time
import pandas as pd
import json
from confluent_kafka import Producer

kafka_config = {
    'bootstrap.servers': 'broker1:29092',
    'acks': 'all',
    'retries': 3
}

producer = Producer(kafka_config)

csv_dir = "./input"

# Kafka topic to send messages to
topic_name = "product-reviews"

def acknowledged(err, msg):
    if err:
        print(f"Failed to deliver message: {err}")
    else:
        print(f"Produced: {msg.value().decode('utf-8')}")

def send_csv_to_kafka(file_path):
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        msg = {
            "id": str(row["Id"]),
            "product_id": str(row["ProductId"]),
            "user_id": str(row["UserId"]),
            "profile_name": str(row["ProfileName"]),
            "score": int(row["Score"]),
            "summary": str(row["Summary"]),
            "text": str(row["Text"])
        }
        producer.produce(topic_name, value=json.dumps(msg), callback=acknowledged)
    producer.flush()

if __name__ == "__main__":
    files = sorted(f for f in os.listdir(csv_dir) if f.endswith(".csv"))[:10]
    for filename in files:
        print(f"\nProcessing file: {filename}")
        send_csv_to_kafka(os.path.join(csv_dir, filename))
        print(f"Completed sending: {filename}")
        time.sleep(10)