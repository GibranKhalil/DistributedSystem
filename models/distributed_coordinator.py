import threading
import logging
from typing import Dict
from models.clock import Clock
from models.broadcast_group import BroadcastGroup
from models.message import Message
from models.node import Node
from models.mutual_exclusion_manager import MutualExclusionManager

class DistributedCoordinator:
    def __init__(self):
        self.clients: Dict[str, Node] = {}
        self.channels: Dict[str, BroadcastGroup] = {}
        self.resources: Dict[str, MutualExclusionManager] = {}
        self.global_clock = Clock()
        self.lock = threading.Lock()
    
    def register_client(self, client_id: str):
        with self.lock:
            if client_id not in self.clients:
                self.clients[client_id] = Node(client_id, self)
                logging.info(f"Node {client_id} registered")
                return True
            return False
    
    def create_channel(self, channel_name: str):
        with self.lock:
            if channel_name not in self.channels:
                self.channels[channel_name] = BroadcastGroup(channel_name)
                logging.info(f"BroadcastGroup {channel_name} created")
                return True
            return False
        
    def create_resource(self, resource_id: str):
        with self.lock:
            if resource_id not in self.resources:
                self.resources[resource_id] = MutualExclusionManager(resource_id, self)
                logging.info(f"Resource {resource_id} created")
                return True
            return False
    
    def subscribe_to_channel(self, client_id: str, channel_name: str):
        with self.lock:
            if client_id in self.clients and channel_name in self.channels:
                self.channels[channel_name].subscribers.add(client_id)
                logging.info(f"Node {client_id} subscribed to {channel_name}")
                return True
            return False
    
    def unicast(self, sender_id: str, receiver_id: str, message: Message):
            with self.lock:
                if sender_id in self.clients and receiver_id in self.clients:
                    self.global_clock.update(message.timestamp)
                    self.clients[receiver_id].receive_message(message)
                    
                    if receiver_id in self.resources:
                        if message.msg_type == "request":
                            self.resources[receiver_id].handle_request(message)
                        elif message.msg_type == "reply":
                            self.resources[receiver_id].handle_reply(message)
                        elif message.msg_type == "release":
                            self.resources[receiver_id].handle_release(message)
                    
                    return True
                return False
        
    def multicast(self, sender_id: str, channel_name: str, content: str):
        with self.lock:
            if sender_id in self.clients and channel_name in self.channels:
                timestamp = self.global_clock.increment()
                message = Message(sender_id, content, timestamp)
                channel = self.channels[channel_name]
                channel.buffer.add_message(message)
                
                for subscriber in channel.subscribers:
                    if subscriber != sender_id:
                        self.clients[subscriber].receive_message(message)
                return True
            return False
    
    def broadcast(self, sender_id: str, content: str):
        with self.lock:
            if sender_id in self.clients:
                timestamp = self.global_clock.increment()
                message = Message(sender_id, content, timestamp)
                
                for client_id, client in self.clients.items():
                    if client_id != sender_id:
                        client.receive_message(message)
                return True
            return False
        with self.lock:
            if sender_id in self.clients:
                timestamp = self.global_clock.increment()
                message = Message(sender_id, content, timestamp)
                
                for client_id, client in self.clients.items():
                    if client_id != sender_id:
                        client.receive_message(message)
                return True
            return False