VC_NUMBER = 8

from communication.routing import Direction
from .virtual_channel import VirtualChannel

class InPort:
    def __init__(self ,direction):
        self.direction = direction
        self.vcs = []

        # VCs construct
        for i in range(VC_NUMBER):
            self.vcs.append(VirtualChannel(i)) 