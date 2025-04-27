from models.message_queue import MessageQueue
from models.message import Message
from models.clock import Clock
from typing import List, Optional

class Node:
    def __init__(self, client_id: str, messaging_system: 'DistributedCoordinator'): # type: ignore
        self.id = client_id
        self.messaging_system = messaging_system
        self.inbox = MessageQueue()
        self.local_clock = Clock()
    
    def send_unicast(self, receiver_id: str, content: str, msg_type: str = "normal", request_id: str = None):
        timestamp = self.messaging_system.global_clock.increment()
        message = Message(self.id, content, timestamp, msg_type, request_id)
        return self.messaging_system.unicast(self.id, receiver_id, message)
    
    def send_multicast(self, channel_name: str, content: str):
        return self.messaging_system.multicast(self.id, channel_name, content)
    
    def send_broadcast(self, content: str):
        return self.messaging_system.broadcast(self.id, content)
    
    def request_resource(self, resource_id: str) -> bool:
        if resource_id in self.messaging_system.resources:
            return self.messaging_system.resources[resource_id].request_resource(self.id)
        return False
    
    def release_resource(self, resource_id: str) -> bool:
        if resource_id in self.messaging_system.resources:
            return self.messaging_system.resources[resource_id].release_resource(self.id)
        return False
    
    def receive_message(self, message: Message):
        self.inbox.add_message(message)
    
    def consume_message(self) -> Optional[Message]:
        return self.inbox.get_message(self.id)
    
    def get_message_log(self) -> List[str]:
        return self.inbox.get_log()