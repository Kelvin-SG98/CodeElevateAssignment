# 🌡️ IoT Kafka Project

Este projeto simula o envio de dados de sensores IoT via Kafka, com processamento em tempo real e persistência em banco de dados SQLite.

## 🚀 Estrutura
- `producer/iot_producer.py`: Gera dados com Faker e envia ao tópico Kafka.
- `consumer/iot_consumer.py`: Consome dados, insere no SQLite e imprime os últimos registros.
- `docker-compose.yml`: Sobe Zookeeper + Kafka localmente.
- `iot_dados.db`: Banco SQLite criado automaticamente.
- `requirements.txt`: Dependências do projeto.

## ▶️ Como Rodar

1. **Subir Kafka com Docker**:
```bash
docker-compose up
```

2. **Instalar dependências (fora do docker)**:
```bash
pip install -r requirements.txt
```

3. **Terminal 1 - Rodar o producer**:
```bash
python producer/iot_producer.py
```

4. **Terminal 2 - Rodar o consumer**:
```bash
python consumer/iot_consumer.py
```

## 💾 Exemplo de dados
```json
{
  "sensor_id": "sensor_3",
  "timestamp": "2025-06-01T15:00:00",
  "temperatura": 27.5,
  "umidade": 66.2,
  "localizacao": "Campinas"
}
```

## 🧠 Destaques Técnicos
- Kafka com tópico `iot_sensores`
- Producer com geração contínua e aleatória de dados
- Consumer com salvamento em SQLite e exibição incremental