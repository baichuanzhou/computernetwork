class Queue:
    """A container with a first-in-first-out (FIFO) queuing policy"""
    def __init__(self):
        self.list = []

    def push(self, elem):
        self.list.insert(0, elem)

    def pop(self):
        return self.list.pop()

    def isEmpty(self):
        return len(self.list) == 0
