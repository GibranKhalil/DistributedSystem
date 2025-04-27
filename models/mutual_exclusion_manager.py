import threading
import uuid
import logging
from collections import defaultdict, deque
from models.message import Message

class MutualExclusionManager:
    def __init__(self, resource_id: str, messaging_system):
        self.resource_id = resource_id
        self.messaging_system = messaging_system
        self.lock = threading.Lock()
        self.request_queue = deque()
        self.replied = set()
        self.my_request = None
        self.using_resource = False
        self.deferred_replies = defaultdict(list)
    
    def request_resource(self, client_id: str):
        with self.lock:
            if self.using_resource or self.my_request is not None:
                return False
            
            request_id = str(uuid.uuid4())
            timestamp = self.messaging_system.global_clock.increment()
            self.my_request = (timestamp, client_id, request_id)
            
            for other_client in self.messaging_system.clients.keys():
                if other_client != client_id:
                    msg = Message(
                        sender=client_id,
                        content=f"Request for resource {self.resource_id}",
                        timestamp=timestamp,
                        msg_type="request",
                        request_id=request_id
                    )
                    self.messaging_system.unicast(client_id, other_client, msg)
            
            return True
    
    def handle_request(self, message: Message):
        with self.lock:
            if message.msg_type != "request":
                return
            
            if not self.my_request:
                reply_msg = Message(
                    sender=message.sender,
                    content=f"Reply for resource {self.resource_id}",
                    timestamp=self.messaging_system.global_clock.increment(),
                    msg_type="reply",
                    request_id=message.request_id
                )
                self.messaging_system.unicast(message.sender, message.sender, reply_msg)
            else:
                my_ts, my_id, my_req_id = self.my_request
                if message.timestamp < my_ts or (message.timestamp == my_ts and message.sender < my_id):
                    self.deferred_replies[message.sender].append(message.request_id)
                else:
                    reply_msg = Message(
                        sender=message.sender,
                        content=f"Reply for resource {self.resource_id}",
                        timestamp=self.messaging_system.global_clock.increment(),
                        msg_type="reply",
                        request_id=message.request_id
                    )
                    self.messaging_system.unicast(message.sender, message.sender, reply_msg)
    
    def handle_reply(self, message: Message):
        with self.lock:
            if message.msg_type != "reply":
                return
            
            if self.my_request and message.request_id == self.my_request[2]:
                self.replied.add(message.sender)
                
                all_clients = set(self.messaging_system.clients.keys())
                all_clients.discard(self.my_request[1])
                
                if self.replied.issuperset(all_clients):
                    self.using_resource = True
                    logging.info(f"Node {self.my_request[1]} acquired resource {self.resource_id}")
    
    def release_resource(self, client_id: str):
        with self.lock:
            if not self.using_resource or (self.my_request and self.my_request[1] != client_id):
                return False
            
            for deferred_client, req_ids in self.deferred_replies.items():
                for req_id in req_ids:
                    release_msg = Message(
                        sender=client_id,
                        content=f"Release resource {self.resource_id}",
                        timestamp=self.messaging_system.global_clock.increment(),
                        msg_type="release",
                        request_id=req_id
                    )
                    self.messaging_system.unicast(client_id, deferred_client, release_msg)
            
            self.using_resource = False
            self.my_request = None
            self.replied = set()
            self.deferred_replies = defaultdict(list)
            logging.info(f"Node {client_id} released resource {self.resource_id}")
            return True
    
    def handle_release(self, message: Message):
        with self.lock:
            if message.msg_type != "release":
                return
            
            if message.request_id in self.deferred_replies.get(message.sender, []):
                reply_msg = Message(
                    sender=message.sender,
                    content=f"Reply for resource {self.resource_id} (after release)",
                    timestamp=self.messaging_system.global_clock.increment(),
                    msg_type="reply",
                    request_id=message.request_id
                )
                self.messaging_system.unicast(message.sender, message.sender, reply_msg)
                self.deferred_replies[message.sender].remove(message.request_id)