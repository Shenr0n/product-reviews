#producer/Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . /app

# installing pandas and confluent-kafka for the producer to extract and send messages to kafka topics
RUN pip install --no-cache-dir pandas confluent-kafka

#running the producer.py file
CMD ["python", "producer.py"]