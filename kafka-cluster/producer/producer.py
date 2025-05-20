import os
import time
import pandas as pd
import json
from confluent_kafka import Producer

# kafka configs for accessing the clusters from the producer
# acks: all so that all replicas acknowledge messages
# retries up to thrice on failure
kafka_config = {
    'bootstrap.servers': 'broker1:29092',
    'acks': 'all',
    'retries': 3
    #,'delivery.timeout.ms': 10000
}

# create kafka producer
producer = Producer(kafka_config)

csv_dir = "./input"

# the topic was created in the cluster manually 
# Kafka topic to send messages to
topic_name = "product-reviews"


# checking if message was successfully sent or delivery failed
def acknowledged(err, msg):
    if err:
        print(f"Failed to deliver message: {err}")
    else:
        print(f"Produced: {msg.value().decode('utf-8')}")

# function to read and send messages
def send_csv_to_kafka(file_path):
    try:
        #df = pd.read_csv(file_path)
        # skip bad records
        df = pd.read_csv(file_path, dtype=str, on_bad_lines='skip')
        #Convert each csv record into json, based on the following msg structure
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

            #send json string to kafka topic
            producer.produce(topic_name, value=json.dumps(msg), callback=acknowledged)

        #all pending messages are delivered
        producer.flush()
    except Exception as e:
        print(f"Sending csv to kafka topic failed: {e}")

if __name__ == "__main__":
    files = sorted(f for f in os.listdir(csv_dir) if f.endswith(".csv"))[:5]
    for filename in files:
        print(f"\nProcessing file: {filename}")
        send_csv_to_kafka(os.path.join(csv_dir, filename))
        print(f"Completed sending: {filename}")
        time.sleep(10)