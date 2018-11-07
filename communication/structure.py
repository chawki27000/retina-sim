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
                self.flits.append(Flit(i, FlitType.head, 0, self))
            elif i == flitNumber - 1:  # Tail Flit
                self.flits.append(Flit(i, FlitType.tail, 0, self))
            else:  # Body Flit
                self.flits.append(Flit(i, FlitType.body, 0, self))

        self.set_destination(dest)

    def set_destination(self, dest):
        for flit in self.flits:
            flit.set_destination_info(dest)

    def get_flit(self):
        flit = copy.deepcopy(self.flits[0])
        del self.flits[0]
        return flit

    def __str__(self):
        return 'Packet (%d)' % self.id


#############################################################
class FlitType(enum.Enum):
    head = 1
    body = 2
    tail = 3


#############################################################
class Flit:
    def __init__(self, id, type, timeBegin, packet):
        self.id = id
        self.type = type
        self.timeBegin = timeBegin
        self.destination = None
        self.packet = packet

    def set_destination_info(self, destination):
        self.destination = destination

    def __str__(self):
        return 'Flit (%s) from %s' % (self.type, self.packet)


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


#############################################################
class Node:
    def __init__(self, vc_src, vc_target):
        self.vc_src = vc_src
        self.vc_target = vc_target


class NodeArray:
    def __init__(self):
        self.array = []

    def add(self, node):
        self.array.append(node)

    def remove(self, vc_src):
        for node in self.array:
            if node.vc_src == vc_src:
                self.array.remove(node)

    def get_target(self, vc_src):
        for node in self.array:
            if node.vc_src == vc_src:
                return node.vc_target
        return None
