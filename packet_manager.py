from telemetry_f1_2021.packets import Packet, PacketSessionData
from threading import Thread


class PacketManager(Thread):
    """Base class for handling data packets.
    Defines methods for validation, cleaning and sending to database
    """

    def __init__(self, packet_queue) -> None:
        Thread.__init__(self)
        self.packet_queue = packet_queue
        self.daemon = True
        self.start()

    @staticmethod
    def validate_packet(packet):
        """Takes a packet and returns whether or not it is a valid packet

        Args:
            packet (Packet): a packet from the F1 2021 Telemetry client

        Returns:
            bool: True if the packet is valid, False otherwise.
        """
        if isinstance(packet, Packet):
            return True
        return False

    def send_to_db(self):
        """Checks queue length, and sends anything on the queue to the database."""
        if len(self.packet_queue) > 0:
            packet = self.packet_queue.pop_item()
            if isinstance(packet, PacketSessionData):
                # print(packet)
                pass

        if len(self.packet_queue) % 10 == 0 and len(self.packet_queue) > 0:
            print(len(self.packet_queue))

    def run(self):
        """Main entry point for starting the packet manager"""
        while True:
            self.send_to_db()
