VC_NUMBER = 8

from communication.routing import Direction
from .virtual_channel import VirtualChannel


class InPort:
    def __init__(self, direction, nbvc, vc_size):
        self.direction = direction
        self.vcs = []

        # VCs construct
        for i in range(VC_NUMBER):
            self.vcs.append(VirtualChannel(i))

    def vc_allocation(self):
        for vc in self.vcs:
            if vc.isFree():
                return vc
            return None
