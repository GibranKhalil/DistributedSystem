from models.message_queue import MessageQueue;

class BroadcastGroup:
    def __init__(self, name: str):
        self.name = name
        self.buffer = MessageQueue()
        self.subscribers = set()