from kafka import KafkaConsumer
import os
import json
import pandas as pd

import uuid

TOPIC = "product-reviews"
BOOTSTRAP_SERVERS = "localhost:9092"
OUTPUT_DIR = "./output/product_reviews"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Create Kafka consumer
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="consumer-group-1",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

# Buffer to collect messages
buffer = []

try:
    for message in consumer:
        data = message.value
        buffer.append(data)

        # Parquet file for every 500 messages
        if len(buffer) >= 500:
            df = pd.DataFrame(buffer)
            file_path = os.path.join(OUTPUT_DIR, f"batch_{uuid.uuid4().hex}.parquet")
            df.to_parquet(file_path, engine="fastparquet", index=False)
            print(f"Wrote {len(buffer)} records to {file_path}")
            buffer.clear()

except KeyboardInterrupt:
    print("Stopped consumer with Ctrl+C")

finally:
    # Write any remaining records in buffer
    if buffer:
        df = pd.DataFrame(buffer)
        file_path = os.path.join(OUTPUT_DIR, f"final_{uuid.uuid4().hex}.parquet")
        df.to_parquet(file_path, engine="fastparquet", index=False)
        print(f"Flushed final {len(buffer)} records to {file_path}")

    consumer.close()