class VirtualChannel:
    def __init__(self, id, max_size):
        self.id = id
        self.lock = False
        self.max_size = max_size
        self.flits = []

    def push(self, flit):
        if len(self.flits) <= self.max_size:
            return False

        self.flits.append(flit)
        return True

    def pop(self):
        if len(self.flits) <= 0:
            return None
        return self.flits.pop()

    def isFree(self):
        return self.lock

    def lock(self):
        self.lock = True

    def release(self):
        self.lock = False
