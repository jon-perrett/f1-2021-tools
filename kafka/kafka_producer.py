import logging
from confluent_kafka import Producer
import json


class KafkaProducer:
    """Wrapper class for Kafka producer, to provide easy interface to commonly used methods"""

    def __init__(self, config):
        self.producer = Producer(config)
        self.config = config

    @staticmethod
    def delivery_report(err, msg):
        """Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush()."""
        if err is not None:
            logging.info("Message delivery failed: {}".format(err))
        else:
            logging.info(
                "Message delivered to {} [{}]".format(msg.topic(), msg.partition())
            )

    def produce_data(self, topic: str, message: dict):
        # Trigger any available delivery report callbacks from previous produce() calls
        self.producer.poll(0)

        # Asynchronously produce a message, the delivery report callback
        # will be triggered from poll() above, or flush() below, when the message has
        # been successfully delivered or failed permanently.
        self.producer.produce(
            topic,
            json.dumps(json.loads(message.__repr__().encode("utf-8"))),
            callback=self.delivery_report,
        )

        # Wait for any outstanding messages to be delivered and delivery report
        # callbacks to be triggered.
        self.producer.flush()
