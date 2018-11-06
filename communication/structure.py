import copy
import enum
import math

FLIT_DEFAULT_SIZE = 32
PACKET_DEFAULT_SIZE = 128


class Packet:
    def __init__(self, id, dest):
        self.id = id
        self.flits = []

        # Flit construct
        flitNumber = int(math.ceil(float(PACKET_DEFAULT_SIZE / FLIT_DEFAULT_SIZE)))

        for i in range(flitNumber):
            if i == 0:  # Head Flit
                self.flits.append(Flit(i, FlitType.head, 0))  # TODO : Clock
            elif i == flitNumber - 1:  # Tail Flit
                self.flits.append(Flit(i, FlitType.tail, 0))  # TODO : Clock
            else:  # Body Flit
                self.flits.append(Flit(i, FlitType.body, 0))  # TODO : Clock

        self.set_head_flit(dest)

    def set_head_flit(self, destination):
        self.flits[0].set_destination_info(destination)

    def get_flit(self):
        flit = copy.deepcopy(self.flits[0])
        del self.flits[0]
        return flit


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
        self.destination = None

    def set_destination_info(self, destination):
        if self.type is FlitType.head:
            self.destination = destination


#############################################################


class Message:
    def __init__(self, period, size, src, dest):
        self.period = period
        self.src = src
        self.dest = dest
        self.size = size
        self.packets = []

        # Packet construct
        packetNumber = int(math.ceil(float(self.size / PACKET_DEFAULT_SIZE)))

        for i in range(packetNumber):
            self.packets.append(Packet(i, self.dest))


#############################################################


class MessageInstance(Message):
    def __init__(self, message, instance):
        super().__init__(message.period, message.size, message.src, message.dest)
        self.instance = instance

    def arrived(self, arr):
        self.arr = arr
