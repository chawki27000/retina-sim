from architecture.virtual_channel import VirtualChannel


class InPort:
    def __init__(self, router, direction, nbvc, vc_size, slot_table):
        self.router = router
        self.direction = direction
        self.nbvc = nbvc
        self.vc_size = vc_size
        self.slot_table = slot_table
        self.vcs = []

        # VCs construct
        for i in range(self.nbvc):
            self.vcs.append(VirtualChannel(i, self.direction, self.router, self.vc_size, self.slot_table[i]))

    def reset_slot_table(self):
        for vc in self.vcs:
            if vc.quantum < 0:
                vc.reset_credit()

    def vc_allocator(self):
        for vc in self.vcs:
            if vc.isFree():
                vc.locked()
                return vc
        return None

    def priority_vc_allocator(self, priority):
        for vc in self.vcs:
            if vc.isFree() and vc.id == priority:
                vc.locked()
                return vc
        return None

    def number_idle_vc(self):
        count = 0
        for vc in self.vcs:
            if vc.isFree():
                count += 1
        return count

    def is_packet_still_in_vc(self, packet):
        for vc in self.vcs:
            if len(vc.flits) > 0:
                if vc.flits[0].packet.message == packet.message:
                    return True
        return False

    def vcs_status(self):
        for vc in self.vcs:
            print("%s -- Direction %s -- size : %d -- Lock : %s -- credit : %d" % (
            vc, vc.direction, len(vc.flits), vc.lock, vc.quantum))

    def add_more_vcs(self, number, slot):
        for i in range(number):
            self.vcs.append(VirtualChannel(i, self.direction, self.router, self.vc_size, slot))
