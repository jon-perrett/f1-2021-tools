import logging
from confluent_kafka import Consumer


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
                logging.error("Consumer error: {}".format(msg.error()))
                continue

            print("Received message: {}".format(msg.value().decode("utf-8")))

    def close_consumer(self):
        self.consumer.close()
