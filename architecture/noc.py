from communication.routing import Coordinate, Direction
from communication.structure import MessageInstance
from .inport import InPort
from .outport import OutPort
from .processing_engine import ProcessingEngine
from .router import Router


class NoC:
    def __init__(self, env, name, square_size, nbvc, vc_size, vc_quantum):
        self.action = env.process(self.run())
        self.env = env
        self.name = name
        self.router_matrix = []
        self.square_size = square_size
        self.nbvc = nbvc
        self.vc_size = vc_size
        self.vc_quantum = vc_quantum
        self.links = dict()
        self.messages = None
        self.messages_instance = []

        # Routers Initialisation
        count = 1
        for i in range(square_size):
            line = []
            for j in range(square_size):
                line.append(self.router_initialisation(env, count, i, j))
                count += 1
            self.router_matrix.append(line)

        # Routers linking
        self.router_linking()

    def router_initialisation(self, env, id, x, y):

        # ProcessingEngine
        proc_engine = ProcessingEngine(env)

        # Routers construct
        coordinate = Coordinate(x, y)
        router = Router(env, id, coordinate, proc_engine)

        # InPort
        inNorth = InPort(router, Direction.north, self.nbvc, self.vc_size, self.vc_quantum)
        inSouth = InPort(router, Direction.south, self.nbvc, self.vc_size, self.vc_quantum)
        inEast = InPort(router, Direction.east, self.nbvc, self.vc_size, self.vc_quantum)
        inWest = InPort(router, Direction.west, self.nbvc, self.vc_size, self.vc_quantum)
        inPE = InPort(router, Direction.pe, self.nbvc, 10000,
                      self.vc_quantum)  # TODO : regler le probleme des Nb VC dans PE

        # OutPort
        outNorth = OutPort(Direction.north)
        outSouth = OutPort(Direction.south)
        outEast = OutPort(Direction.east)
        outWest = OutPort(Direction.west)
        outPE = OutPort(Direction.pe)

        # In/Out Port settings
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

    def link_array_filling(self):
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

            # router himself
            router_himself = temporary_list[i]
            self.links[str(router_himself.id)] = dict()

            # Up Link
            if idUp >= 0:
                temporary_router = temporary_list[idUp]
                # Link Array filling
                self.links[str(router_himself.id)][str(temporary_router.id)] = 0

            # Down Link
            if idDown < self.square_size * self.square_size:
                temporary_router = temporary_list[idDown]
                # Link Array filling
                self.links[str(router_himself.id)][str(temporary_router.id)] = 0

            # Right Link
            if idRight % self.square_size != 0:
                temporary_router = temporary_list[idRight]
                # Link Array filling
                self.links[str(router_himself.id)][str(temporary_router.id)] = 0

            # Left Link
            if id % self.square_size != 0:
                temporary_router = temporary_list[idLeft]
                # Link Array filling
                self.links[str(router_himself.id)][str(temporary_router.id)] = 0

    def link_array_clean(self):
        for key in self.links.keys():
            for key2 in self.links[key]:
                self.links[key][key2] = 0

    def get_router_coordinate_by_id(self, router_id):
        for i in range(self.square_size):
            for j in range(self.square_size):
                if self.router_matrix[i][j].id == router_id:
                    return self.router_matrix[i][j].coordinate
        return None

    def run(self):

        while True:
            for message in self.messages:
                coord = message.src
                router = self.router_matrix[coord.i][coord.j]

                if self.env.now % message.period == 0:
                    mi = MessageInstance(message, 0)
                    self.messages_instance.append(mi)
                    router.proc_engine.send_to_router(mi)

            yield self.env.timeout(1)

    def __str__(self):
        string = ''
        for i in range(self.square_size):
            for j in range(self.square_size):
                string += str(self.router_matrix[i][j]) + ' '
            string += '\n'

        return string
