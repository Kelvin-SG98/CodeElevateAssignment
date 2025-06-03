from kafka import KafkaConsumer
import json
import sqlite3

# Banco de dados local
conn = sqlite3.connect("iot_dados.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS sensores (
    sensor_id TEXT,
    timestamp TEXT,
    temperatura REAL,
    umidade REAL,
    localizacao TEXT
)
''')
conn.commit()

# Consumidor Kafka
consumer = KafkaConsumer(
    'iot_sensores',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='iot-group'
)

print("Consumindo dados do tópico...")

for message in consumer:
    data = message.value
    cursor.execute('''
        INSERT INTO sensores (sensor_id, timestamp, temperatura, umidade, localizacao)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        data['sensor_id'],
        data['timestamp'],
        data['temperatura'],
        data['umidade'],
        data['localizacao']
    ))
    conn.commit()

    print("Inserido no banco:", data)

    # Exibe o conteúdo da tabela
    rows = cursor.execute("SELECT * FROM sensores ORDER BY ROWID DESC LIMIT 5").fetchall()
    print("Últimos registros:")
    for row in rows:
        print(row)
    print("-" * 40)