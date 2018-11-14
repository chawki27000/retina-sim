from .virtual_channel import VirtualChannel


class InPort:
    def __init__(self, router, direction, nbvc, vc_size):
        self.router = router
        self.direction = direction
        self.nbvc = nbvc
        self.vc_size = vc_size
        self.vcs = []

        # VCs construct
        for i in range(self.nbvc):
            self.vcs.append(VirtualChannel(i, self.router, self.vc_size, 1))

    def vc_allocator(self):
        for vc in self.vcs:
            if vc.isFree():
                vc.lock = True
                return vc
        return None

    def number_idle_vc(self):
        count = 0
        for vc in self.vcs:
            if vc.isFree():
                count += 1
        return count
