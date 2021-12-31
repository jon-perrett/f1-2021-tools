class PacketQueue:
    """Class for packet queues"""

    def __init__(self):
        self.queue = []

    def __len__(self):
        return len(self.queue)

    def add_item(self, item):
        self.queue.append(item)

    def pop_item(self):
        return self.queue.pop()
