import os
from confluent_kafka import Consumer

from kafka_admin import KafkaAdmin
from kafka_producer import KafkaProducer
from dotenv import load_dotenv


class KafkaConsumer:
    """Wrapper class for commonly used Kafka consumer methods"""

    def __init__(self, config, subscriptions):
        self.consumer = Consumer(config)
        self.consumer.subscribe(subscriptions)

    def get_messages(self):
        """Prints messages on subscribed topics"""
        while True:
            msg = self.consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            print("Received message: {}".format(msg.value().decode("utf-8")))

    def close_consumer(self):
        self.consumer.close()


if __name__ == "__main__":
    load_dotenv()
    config = {"bootstrap.servers": os.getenv('BOOTSTRAP_SERVERS')}
    cons_config = {
        "bootstrap.servers": os.getenv('BOOTSTRAP_SERVERS'),
        "group.id": os.getenv('GROUP_ID'),
        "auto.offset.reset": os.getenv('AUTO_OFFSET_RESET'),
    }

    kafka = KafkaAdmin(config)
    kafka.check_add_topic("hello_world")
    p = KafkaProducer(config)
    p.produce_data("hello_world", {"hello": "world"})
    c = KafkaConsumer(cons_config, ["hello_world"])
    c.get_messages()
