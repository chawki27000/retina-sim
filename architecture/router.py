from communication.routing import Direction


class Router:
    def __init__(self, id, coordinate, proc_engine):
        self.id = id
        self.coordinate = coordinate
        self.proc_engine = proc_engine

    def inport_setting(self, inNorth, inSouth, inEast, inWest):
        self.inNorth = inNorth
        self.inSouth = inSouth
        self.inEast = inEast
        self.inWest = inWest

    def outport_setting(self, outNorth, outSouth, outEast, outWest):
        self.outNorth = outNorth
        self.outSouth = outSouth
        self.outEast = outEast
        self.outWest = outWest

    def proc_engine_setting(self, inPE, outPE):
        self.inPE = inPE
        self.outPE = outPE

    def get_non_empty_vc(self):
        self.vcs_target_north = []
        self.vcs_target_south = []
        self.vcs_target_east = []
        self.vcs_target_west = []

        # Collecting VCs that target North Output
        # TODO : Doing later

    def get_xy_routing_direction(self, dest):
        # On X axe (Column)
        # By the West
        if self.coordinate.j > dest.j:
            return Direction.west
        # By the East
        elif self.coordinate.j < dest.j:
            return Direction.east
        # On Y axe (Row)
        else:
            if self.coordinate.i > dest.i:
                return Direction.north
            # By the East
            elif self.coordinate.i < dest.i:
                return Direction.south
            else:
                # Destination Reached
                return None

    def get_routing_output(self, direction):
        if direction == Direction.north:
            return self.outNorth
        elif direction == Direction.south:
            return self.outSouth
        elif direction == Direction.east:
            return self.outEast
        elif direction == Direction.west:
            return self.outWest

    def reserve_idle_vc(self, inport):
        return inport.get_first_idle_vc()

    def send_head_flit(self, direction):
        pass

    # SIMULATION PROCESS
    def process(self, env):
        pass

    def __str__(self):
        return 'Router (%d,%d)' % (self.coordinate.i, self.coordinate.j)
