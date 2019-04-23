class stack:
    def __init__(self):
        self.data = []
    def push(self,data):
        self.data.append(data)
    def pop(self):
        return self.data.pop()
    def peek(self):
        return self.data[-1]
    def size(self):
        return len(self.data)
    def is_empty(self):
        return len(self.data) == 0
