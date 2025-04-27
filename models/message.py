class Message:
    def __init__(self, sender: str, content: str, timestamp: int, msg_type: str = "normal", request_id: str = None):
        self.sender = sender
        self.content = content
        self.timestamp = timestamp
        self.consumption_time = None
        self.msg_type = msg_type
        self.request_id = request_id
    
    def __str__(self):
        return f"{self.content} (sender={self.sender}, ts={self.timestamp}, consumed_ts={self.consumption_time}, type={self.msg_type})"