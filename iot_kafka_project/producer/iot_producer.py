from kafka import KafkaProducer
import json
import time
from faker import Faker
import random

fake = Faker()

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_sensor_data():
    return {
        "sensor_id": f"sensor_{random.randint(1, 5)}",
        "timestamp": fake.iso8601(),
        "temperatura": round(random.uniform(20.0, 35.0), 2),
        "umidade": round(random.uniform(30.0, 90.0), 2),
        "localizacao": fake.city()
    }

while True:
    data = generate_sensor_data()
    producer.send('iot_sensores', value=data)
    print("Enviado:", data)
    time.sleep(1)