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

    def __str__(self):
        return 'Router (%d,%d)' % (self.coordinate.i, self.coordinate.j)
