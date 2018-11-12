class VirtualChannel:
    def __init__(self, id, router, max_size, quantum):
        self.id = id
        self.lock = False
        self.router = router
        self.max_size = max_size
        self.default_quantum = quantum
        self.quantum = quantum
        self.flits = []

    def enqueue(self, flit):
        if len(self.flits) >= self.max_size:
            return False

        self.flits.insert(0, flit)
        return True

    def append(self, flit):
        self.flits.append(flit)

    def dequeue(self):
        if len(self.flits) <= 0:
            return None
        return self.flits.pop()

    def isFree(self):
        return not self.lock

    def lock(self):
        self.lock = True

    def release(self):
        self.lock = False

    def credit_out(self):
        if self.quantum <= 0:
            return False

        self.quantum -= 1

    def reset_credit(self):
        self.quantum = self.default_quantum

    def __str__(self):
        return 'VC (%d) with size (%d)' % (self.id, len(self.flits))
