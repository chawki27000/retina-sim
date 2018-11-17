import math


class EndToEndLatency:
    PACKET_ROUTER_LAT = 1
    NETWORK_ACCESS_LAT = 1

    @staticmethod
    def routing_distance(src, dest):
        return math.fabs(src.i - dest.i) + math.fabs(src.j - dest.j)

    @staticmethod
    def iteration_number(nP, aVflow):
        return int(math.ceil(nP / float(aVflow)))

    @staticmethod
    def network_latency(nI, oV, nR):
        return int((nI * oV) + (nR - 1))
