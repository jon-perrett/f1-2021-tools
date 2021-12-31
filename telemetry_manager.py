from threading import Thread

from telemetry_f1_2021.listener import TelemetryListener


class TelemetryManager(Thread):
    def __init__(self, packet_queue):
        Thread.__init__(self)
        self.packet_queue = packet_queue
        self.daemon = True
        self.telemetry_listener = TelemetryListener()
        self.start()

    def run(self):
        while True:
            packet = self.telemetry_listener.get()
            self.packet_queue.add_item(packet)
