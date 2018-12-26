import copy
import enum
import math

from analysis.end_to_end_latency import EndToEndLatency
from communication.routing import Coordinate

FLIT_DEFAULT_SIZE = 32
PACKET_DEFAULT_SIZE = 128


class Packet:
    def __init__(self, id, dest, message):
        self.id = id
        self.message = message
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

    def __str__(self):
        return 'Packet(%d) from Message(%d)' % (self.id, self.message.id)


#############################################################
class FlitType(enum.Enum):
    head = 1
    body = 2
    tail = 3


#############################################################
class Flit:
    def __init__(self, id, type, begin_time, packet):
        self.id = id
        self.type = type
        self.begin_time = begin_time
        self.destination = None
        self.packet = packet

    def set_destination_info(self, destination):
        self.destination = destination

    def set_arrival_time(self, arrival_time):
        self.arrival_time = arrival_time

    def __str__(self):
        return '%s %d-%d-%d' % (self.type, self.id, self.packet.id, self.packet.message.id)


#############################################################
class Message:
    def __init__(self, id, period, size, offset, deadline, src, dest):
        self.id = id
        self.period = period
        self.offset = offset
        self.deadline = deadline
        self.src = src
        self.dest = dest
        self.size = size
        self.packets = []

        # Packet construct
        packetNumber = int(math.ceil(float(self.size / PACKET_DEFAULT_SIZE)))

        for i in range(packetNumber):
            self.packets.append(Packet(i, self.dest, self))

    def get_link_utilization(self):
        return round(self.size / self.period, 2)

    def set_priority(self, priority):
        self.priority = priority

    def get_analysis_latency(self):
        # Routing Distance Computing
        nR = EndToEndLatency.routing_distance(self.src, self.dest)
        # Iteration Number
        nI = EndToEndLatency.iteration_number(len(self.packets), 4)  # TODO : change to dynamic

        # Network Latency
        # nI: Number of iteration
        # oV: Total VC occupied(pessimistic)
        # nR: Routing Distance
        nL = EndToEndLatency.network_latency(nI, 4, nR)

        return int((EndToEndLatency.NETWORK_ACCESS_LAT * 2) + nL)

    def get_basic_network_latency(self):
        # Routing Distance Computing
        h = EndToEndLatency.routing_distance(self.src, self.dest)

        return EndToEndLatency.basic_network_latency(PACKET_DEFAULT_SIZE,
                                                     FLIT_DEFAULT_SIZE,
                                                     h)

    def get_priority_analysis_latency(self, intersection):
        # Basic Network Latency (without contention)
        c = self.get_basic_network_latency()

        # network latency
        last_r = 0
        r = c
        while r < self.deadline:
            tmp_r = c
            last_r = r
            for msg in intersection:
                tmp_r += math.ceil(r / msg.period) * msg.get_basic_network_latency

            # iterate until Ri > Di
            r = tmp_r

        return last_r

    def get_xy_path_coordinate(self):
        src = copy.copy(self.src)
        dest = self.dest

        # put the first router
        link_array = LinkArray()
        path_array = [self.src]

        while True:
            # On X axe (Column)
            # By the West
            if src.j > dest.j:
                src.j -= 1
                path_array.append(Coordinate(src.i, src.j))
            # By the East
            elif src.j < dest.j:
                src.j += 1
                path_array.append(Coordinate(src.i, src.j))
            # On Y axe (Row)
            else:
                if src.i > dest.i:
                    src.i -= 1
                    path_array.append(Coordinate(src.i, src.j))
                # By the East
                elif src.i < dest.i:
                    src.i += 1
                    path_array.append(Coordinate(src.i, src.j))
                else:
                    break

        # fill path
        for i in range(len(path_array) - 1):
            link_array.add_link(Link(path_array[i], path_array[i + 1]))

        return link_array

    def __str__(self):
        return '[id: %d -- size: %d -- period: %d -- offset: %d -- deadline: %d -- src: %s -- dest: %s]' \
               % (self.id, self.size, self.period, self.offset, self.deadline, self.src, self.dest)


#############################################################


class MessageInstance(Message):
    def __init__(self, message, instance):
        super().__init__(message.id, message.period, message.size, message.offset,
                         message.deadline, message.src, message.dest)
        self.instance = instance

    def set_depart_time(self, depart_time):
        self._depart_time = depart_time

    def get_depart_time(self):
        return self._depart_time

    def get_arriving_time(self):
        arr = -1

        packets = self.packets
        for packet in packets:
            flits = packet.flits
            for flit in flits:
                if flit.type == FlitType.tail:
                    if arr < flit.arrival_time:
                        arr = flit.arrival_time

        return arr

    def get_latency(self):
        return self.get_arriving_time() - self.get_depart_time()

    def __str__(self):
        return 'Message (%d)(instance = %d)' % (self.id, self.instance)


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


#############################################################
class Link:
    def __init__(self, trans, receiv):
        self.trans = trans
        self.receiv = receiv
        self.utilization_rate = 0

    def add_utilization(self, rate):
        self.utilization_rate += rate

    def __str__(self):
        return '%s -> %s' % (self.trans, self.receiv)


class LinkArray:
    def __init__(self):
        self.array = []

    def add_link(self, link):
        self.array.append(link)

    def size(self):
        return len(self.array)

    def check_utilization_rate(self, val, rate, error):
        for link in self.array:
            if link.utilization_rate + val > rate + error:
                return False
        return True

    def add_utilization(self, rate):
        for link in self.array:
            link.add_utilization(rate)

    def clear_utilization_rate(self):
        for link in self.array:
            link.utilization_rate = 0
