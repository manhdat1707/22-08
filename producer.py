
import json
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
def send_data(msg):
    producer.send('topic-test2', msg)
    producer.flush()
    print("done")

if __name__ == "__main__":
    send_data()
    