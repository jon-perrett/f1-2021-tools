import os
from kafka.kafka_consumer import KafkaConsumer
from kafka.kafka_producer import KafkaProducer
from telemetry_manager import TelemetryManager

cons_config = {"bootstrap.servers": "localhost:9092", "group.id": "group"}
config = {"bootstrap.servers": "localhost:9092"}
kafka_producer = KafkaProducer(config)
TelemetryManager(kafka_producer)
c = KafkaConsumer(cons_config, ["PacketMotionData"])
while True:
    c.get_messages()
