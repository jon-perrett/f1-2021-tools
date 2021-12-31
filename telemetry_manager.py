import logging
from threading import Thread

from telemetry_f1_2021.listener import TelemetryListener

from kafka.kafka_admin import KafkaAdmin


class TelemetryManager(Thread):
    """Class for adding packets to the packet queue.

    Derived from the Thread class, this is run as part of a multithreaded program.

    The class initialises a TelemetryListener object and uses this to gather packets
    from the UDP stream. These are then added to a separate packet queue by reference.

    Methods:
        run - called as part of the start method in Thread. Gets packets and adds them to the queue.
    """

    def __init__(self, producer):
        Thread.__init__(self)
        self.producer = producer
        self.daemon = True
        self.telemetry_listener = TelemetryListener()
        self.start()

    def run(self):
        admin = KafkaAdmin(self.producer.config)
        while True:
            packet = self.telemetry_listener.get()
            topic_name = type(packet).__name__
            admin.check_add_topic(topic_name)
            self.producer.produce_data(topic_name, packet)
