from .processing_engine import ProcessingEngine
from .router import Router
from .inport import InPort
from .outport import OutPort
from communication.routing import Coordinate, Direction


class NoC:
    def __init__(self, name, square_size):
        self.name = name
        self.router_matrix = []
        self.square_size = square_size

        # Routers Initialisation
        count = 1
        for i in range(square_size):
            line = []
            for j in range(square_size):
                line.append(self.router_initialisation(count, i, j))
                count += 1
            self.router_matrix.append(line)

    def router_initialisation(self, id, x, y):

        # InPort
        inNorth = InPort(Direction.north)
        inSouth = InPort(Direction.south)
        inEast = InPort(Direction.east)
        inWest = InPort(Direction.west)

        # OutPort
        outNorth = OutPort(Direction.north)
        outSouth = OutPort(Direction.south)
        outEast = OutPort(Direction.east)
        outWest = OutPort(Direction.west)

        # ProcessingEngine
        proc_engine = ProcessingEngine()

        # Routers construct
        coordinate = Coordinate(x, y)
        router = Router(id, coordinate, proc_engine)
        router.inport_setting(inNorth, inSouth, inEast, inWest)
        router.outport_setting(outNorth, outSouth, outEast, outWest)

        return router

    def router_linking(self):
        # Temporary router list
        temporary_list = []

        # Matrix Exploration
        for i in range(self.square_size):
            for j in range(self.square_size):
                temporary_list.append(self.router_matrix[i][j])

        # Router Linking
        for i in range(len(temporary_list)):

            # Near router IDs
            id = i
            idUp = id - self.square_size
            idRight = id + 1
            idLeft = id - 1
            idDown = id + self.square_size

            # Up Link
            if idUp >= 0:
                temporary_router = temporary_list[idUp]
                temporary_list[i].outNorth.inport_linking(temporary_router.inSouth)
            else:
                temporary_list[i].outNorth.inport_linking(None)

            # Down Link
            if idDown < self.square_size * self.square_size:
                temporary_router = temporary_list[idDown]
                temporary_list[i].outSouth.inport_linking(temporary_router.inNorth)
            else:
                temporary_list[i].outSouth.inport_linking(None)

            # Right Link
            if idRight % self.square_size != 0:
                temporary_router = temporary_list[idRight]
                temporary_list[i].outEast.inport_linking(temporary_router.inWest)
            else:
                temporary_list[i].outEast.inport_linking(None)

            # Left Link
            if id % self.square_size != 0:
                temporary_router = temporary_list[idLeft]
                temporary_list[i].outWest.inport_linking(temporary_router.inEast)
            else:
                temporary_list[i].outWest.inport_linking(None)
