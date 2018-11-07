from communication.structure import Message
from .processing_engine import ProcessingEngine
from .router import Router
from .inport import InPort
from .outport import OutPort
from communication.routing import Coordinate, Direction


class NoC:
    def __init__(self, env, name, square_size, nbvc, vc_size):
        self.name = name
        self.router_matrix = []
        self.square_size = square_size
        self.nbvc = nbvc
        self.vc_size = vc_size
        self.env = env

        # Routers Initialisation
        count = 1
        for i in range(square_size):
            line = []
            for j in range(square_size):
                line.append(self.router_initialisation(count, i, j))
                count += 1
            self.router_matrix.append(line)

        # Routers linking
        self.router_linking()

    def router_initialisation(self, id, x, y):

        # InPort
        inNorth = InPort(Direction.north, self.nbvc, self.vc_size)
        inSouth = InPort(Direction.south, self.nbvc, self.vc_size)
        inEast = InPort(Direction.east, self.nbvc, self.vc_size)
        inWest = InPort(Direction.west, self.nbvc, self.vc_size)
        inPE = InPort(Direction.pe, self.nbvc, self.vc_size)

        # OutPort
        outNorth = OutPort(Direction.north)
        outSouth = OutPort(Direction.south)
        outEast = OutPort(Direction.east)
        outWest = OutPort(Direction.west)
        outPE = OutPort(Direction.pe)

        # ProcessingEngine
        proc_engine = ProcessingEngine()

        # Routers construct
        coordinate = Coordinate(x, y)
        router = Router(id, coordinate, proc_engine)
        router.inport_setting(inNorth, inSouth, inEast, inWest)
        router.outport_setting(outNorth, outSouth, outEast, outWest)

        # Processing Engine
        proc_engine.router_bind(router)
        router.proc_engine_setting(inPE, outPE)

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

    def process(self):
        src = Coordinate(0, 0)
        dest = Coordinate(0, 1)
        message = Message(200, 256, src, dest)
        self.env.process(self.router_matrix[0][0].proc_engine.process(self.env, message))

        self.env.process(self.router_matrix[0][0].process(self.env))
        self.env.process(self.router_matrix[0][1].process(self.env))

    def __str__(self):
        string = ''
        for i in range(self.square_size):
            for j in range(self.square_size):
                string += str(self.router_matrix[i][j]) + ' '
            string += '\n'

        return string
