VC_MAX_SIZE = 7

class VirtualChannel:
    def __init__(self, id):
        self.id =  id
        self.lock = False
        self.flits = []

    def push(self, flit):
        if len(self.flitList) <= VC_MAX_SIZE:
            return False
        
        self.flitList(flit)

    def pop(self):
        if len(self.flitList) <= 0:
            return None
        return self.flitList.pop()

    def isFree(self):
        return self.lock

    def lock(self):
        self.lock = True

    def release(self):
        self.lock = False