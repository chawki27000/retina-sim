from math import ceil, fabs


class EndToEndLatency:
    PACKET_ROUTER_LAT = 1
    NETWORK_ACCESS_LAT = 0.5

    @staticmethod
    def routing_distance(src, dest):
        return fabs(src.i - dest.i) + fabs(src.j - dest.j)

    """
    Giuseppe et al.
    """

    @staticmethod
    def iteration_number(nP, aVflow):
        return int(ceil(nP / float(aVflow)))

    @staticmethod
    def network_latency(nI, oV, nR):
        return int((nI * oV) + (nR - 1))

    """
    Burns et al.
    """

    @staticmethod
    def basic_network_latency(li, fsize, h):
        return (ceil(li / fsize) * fsize) + h
