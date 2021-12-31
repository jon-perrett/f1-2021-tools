from telemetry_manager import TelemetryManager
from packet_manager import PacketManager
from packet_queue import PacketQueue

packet_queue = PacketQueue()
TelemetryManager(packet_queue=packet_queue)
PacketManager(packet_queue=packet_queue)
while True:
    pass
