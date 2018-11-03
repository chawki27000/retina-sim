import enum
import math

FLIT_DEFAULT_SIZE = 32


class Message:
    def __init__(self, id, period, src, dest):
        self.id = id
        self.period = period
        self.src = src
        self.dest = dest


#############################################################
class Packet:
    def __init__(self, id, size):
        self.id = id
        self.size = size
        self.flits = []

        # Flit construct
        flitNumber = int(math.ceil(float(size / FLIT_DEFAULT_SIZE)))
        print('flit Number : %d' % flitNumber)

        for i in range(flitNumber):
            pass


#############################################################
class FlitType(enum.Enum):
    head = 1
    body = 2
    tail = 3


#############################################################
class Flit:
    def __init__(self, id, type, timeBegin):
        self.id = id
        self.type = type
        self.timeBegin = timeBegin

    def setDestinationInfo(self, destination):
        if self.type is FlitType.head:
            self.destination = destination

#############################################################


class MessageInstance(Message):
    def __init__(self):
        super().__init__()
