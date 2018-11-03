import enum
import math

FLIT_DEFAULT_SIZE = 32
PACKET_DEFAULT_SIZE = 32


class Packet:
    def __init__(self, id):
        self.id = id
        self.flits = []

        # Flit construct
        flitNumber = int(math.ceil(float(size / FLIT_DEFAULT_SIZE)))
        print('flit Number : %d' % flitNumber)

        for i in range(flitNumber):
            if i == 0:  # Head Flit
                self.flits.append(Flit(i, FlitType.head, 0))  # TODO : Clock
            elif i == flitNumber - 2:  # Tail Flit
                self.flits.append(Flit(i, FlitType.tail, 0))  # TODO : Clock
            else:  # Body Flit
                self.flits.append(Flit(i, FlitType.body, 0))  # TODO : Clock

    def setHeadFlit(self, destination):
        self.flits[O].setDestinationInfo(destination)


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


class Message:
    def __init__(self, id, period, size, src, dest):
        self.id = id
        self.period = period
        self.src = src
        self.dest = dest
        self.packets = []

    # Packet construct
    packetNumber = int(math.ceil(float(size / PACKET_DEFAULT_SIZE)))

    for i in range(packetNumber):
        self.packets.append(Packet(i))

#############################################################


class MessageInstance(Message):
    def __init__(self, message, instance, arr):
        super().__init__(message.id, m.period, m.size, m.src, m.dest)
        self.instance = instance
        self.arr = arr
