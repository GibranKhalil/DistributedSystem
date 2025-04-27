class Clock:
    def __init__(self):
        self.counter = 0
    
    def increment(self):
        self.counter += 1
        return self.counter
    
    def update(self, received_time):
        self.counter = max(self.counter, received_time) + 1
        return self.counter
    
    def get_time(self):
        return self.counter