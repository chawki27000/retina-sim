from .virtual_channel import VirtualChannel


class InPort:
    def __init__(self, router, direction, nbvc, vc_size, vc_quantum):
        self.router = router
        self.direction = direction
        self.nbvc = nbvc
        self.vc_size = vc_size
        self.vc_quantum = vc_quantum
        self.vcs = []

        # VCs construct
        for i in range(self.nbvc):
            self.vcs.append(VirtualChannel(i, self.direction, self.router, self.vc_size, self.vc_quantum[i]))

    def vc_allocator(self):
        for vc in self.vcs:
            if vc.isFree():
                vc.locked()
                return vc
        return None

    def priority_vc_allocator(self, priority):
        for vc in self.vcs:
            if vc.isFree() and vc.id == priority:
                vc.lock = True
                return vc
        return None

    def number_idle_vc(self):
        count = 0
        for vc in self.vcs:
            if vc.isFree():
                count += 1
        return count

    def vcs_status(self):
        for vc in self.vcs:
            print("%s -- Direction %s -- size : %d" % (vc, vc.direction, len(vc.flits)))
