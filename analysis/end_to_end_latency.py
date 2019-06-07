import time

import math
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

    """
    Qin et al.
    """


class TDMA:
    def __init__(self, noc, slot_table):
        self.noc = noc
        self.slot_table = slot_table

    def total_slot(self):
        count = 0
        for slot in self.slot_table:
            count += slot

        return count

    def latency(self, message, reserved_slot):
        nbflit = len(message.packets) * len(message.packets[0].flits)
        nbhope = len(message.get_xy_path_coordinate(self.noc))

        return (nbflit * self.total_slot() / reserved_slot) + nbhope


class QinModel:
    def __init__(self, noc, taskset):
        self.taskset = taskset
        self.noc = noc

    def task_overlap(self, p1, p2):
        for m in p1:
            for n in p2:
                if m[0] == n[0] and m[1] == n[1]:
                    return True
        return False

    def path_intersection(self, t1, t2):
        # Getting XY route
        p1 = t1.get_xy_path_coordinate(self.noc)

        # Getting XY route
        p2 = t2.get_xy_path_coordinate(self.noc)

        # Testing the overlap (intersection)
        if self.task_overlap(p1, p2):
            return True
        else:
            return False

    def get_link_direction(self, ids):
        # 0 :: left -> right || up -> down
        # 1 :: right -> left || down -> up
        return 0 if ids[0] < ids[1] else 1

    def direct_interference_set(self, message):
        direct_interference_task = []

        for msg in self.taskset:
            if msg == message or msg.id > message.id:
                continue

            if self.path_intersection(message, msg):
                direct_interference_task.append(msg)

        return direct_interference_task

    def indirect_interference_set(self, message):
        indirect_interference_task = []

        direct_inter_set = self.direct_interference_set(message)

        for task in direct_inter_set:
            task_direct_inter_set = self.direct_interference_set(task)
            for indirect_task in task_direct_inter_set:
                if indirect_task not in direct_inter_set:
                    indirect_interference_task.append(indirect_task)

        return indirect_interference_task

    def upstream_indirect_interference_set(self, message):
        upstream_set = []
        indirect_inter_set = self.indirect_interference_set(message)

        # print(self.noc.get_router_coordinate_by_id(6))

    def downstream_indirect_interference_set(self, message):
        downstream_set = []

        indirect_inter_set = self.indirect_interference_set(message)

    def latency_0th(self, message):
        direct_taskset = self.direct_interference_set(message)

        latency = message.basic_network_latency(self.noc)

        for task in direct_taskset:
            indirect_taskset = self.indirect_interference_set(task)
            latency += task.basic_network_latency(self.noc)
            for indirect_task in indirect_taskset:
                latency += indirect_task.basic_network_latency(self.noc)

        return latency

    def latency_nth(self, message):
        direct_taskset = self.direct_interference_set(message)

        ri = self.latency_0th(message)
        print("RI ---------------> %d" % ri)

        while ri < message.deadline:
            time.sleep(0.3)
            print("Ri --> %d" % ri)
            tmp_ri = message.basic_network_latency(self.noc)
            for task in direct_taskset:
                indirect_taskset = self.indirect_interference_set(task)
                print("indirect_taskset --> %d" % len(indirect_taskset))

                count = 0
                for indirect_task in indirect_taskset:
                    count += indirect_task.basic_network_latency(self.noc)

                print("counter after --> %d" % count)

                tmp_ri += math.ceil((ri + count) / task.period) * task.basic_network_latency(self.noc)
                print("tmp_ri --> %d" % tmp_ri)

            ri = tmp_ri

            if tmp_ri == ri:
                break

        return ri
