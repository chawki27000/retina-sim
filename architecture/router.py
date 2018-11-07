import logging

from communication.structure import FlitType, NodeArray, Node


class Router:
    def __init__(self, id, coordinate, proc_engine):
        self.id = id
        self.coordinate = coordinate
        self.proc_engine = proc_engine

        # Process Attribute
        self.vcs_dictionary = NodeArray()
        self.vcs_target_north = []
        self.vcs_target_south = []
        self.vcs_target_east = []
        self.vcs_target_west = []

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

    def get_xy_routing_output(self, flit):
        # On X axe (Column)
        # By the West
        if self.coordinate.j > flit.destination.j:
            return self.outWest
        # By the East
        elif self.coordinate.j < flit.destination.j:
            return self.outEast
        # On Y axe (Row)
        else:
            if self.coordinate.i > flit.destination.i:
                return self.outNorth
            # By the East
            elif self.coordinate.i < flit.destination.i:
                return self.outSouth
            else:
                # Destination Reached
                return self.outPE

    def reserve_idle_vc(self, inport):
        return inport.get_first_idle_vc()

    def send_flit(self, vc, output):

        # getting the first flit in VC
        flit = vc.dequeue()

        # if is a Head Flit
        if flit.type == FlitType.head:
            logging.debug('Head Flit ready to be sent')

            # Get idle VC from next Input
            vc_allotted = output.inPort.get_first_idle_vc()

            if vc_allotted is not None:
                logging.debug('VC (%s) allotted' % vc_allotted)
                # send flit
                vc_allotted.enqueue(flit)
                logging.debug('Head Flit : sent')
                # registering VC allotted in dictionary
                self.vcs_dictionary.add(Node(vc, vc_allotted))
            else:  # No idle VC
                vc.append(flit)
                logging.debug('Head Flit was not sent - VC not allotted')

        # if is a Body Flit
        elif flit.type == FlitType.body:
            logging.debug('Body Flit ready to be sent')
            # Getting the alloted vc
            vc_allotted = self.vcs_dictionary.get_target(vc)
            logging.debug('Retreiving allotted VC (%s)' % vc_allotted)
            if not vc_allotted.enqueue(flit):  # No Place
                vc.append(flit)
                logging.debug('Body Flit was not sent - No Place in VC (%s)' % vc_allotted)
            else:
                logging.debug('Body Flit : sent')

        # if is a Tail Flit
        elif flit.type == FlitType.tail:
            logging.debug('Tail Flit ready to be sent')
            # Getting the alloted vc
            vc_allotted = self.vcs_dictionary.get_target(vc)
            if not vc_allotted.enqueue(flit):  # No Place
                vc.append(flit)
                logging.debug('Tail Flit was not sent - No Place in VC (%s)' % vc_allotted)
            else:
                logging.debug('Tail Flit : sent')
                self.vcs_dictionary.remove(vc)
                vc.lock = False
                logging.debug('VC (%s) - released' % vc_allotted)

    def vc_target_outport(self, vc):
        if len(vc.flits) > 0:
            if self.get_xy_routing_output(vc.flits[0]) == self.outNorth \
                    and vc not in self.vcs_target_north:
                self.vcs_target_north.append(vc)
            elif self.get_xy_routing_output(vc.flits[0]) == self.outSouth \
                    and vc not in self.vcs_target_north:
                self.vcs_target_south.append(vc)
            elif self.get_xy_routing_output(vc.flits[0]) == self.outEast \
                    and vc not in self.vcs_target_north:
                self.vcs_target_east.append(vc)
            elif self.get_xy_routing_output(vc.flits[0]) == self.outWest \
                    and vc not in self.vcs_target_north:
                self.vcs_target_west.append(vc)

    # SIMULATION PROCESS
    def process(self, env):

        while True:

            # Checking North VC
            for vc in self.inNorth:
                self.vc_target_outport(vc)
            # Checking South VC
            for vc in self.inSouth:
                self.vc_target_outport(vc)
            # Checking East VC
            for vc in self.inEast:
                self.vc_target_outport(vc)
            # Checking West VC
            for vc in self.inWest:
                self.vc_target_outport(vc)

            # VC targeting -> North
            if len(self.vcs_target_north) > 0:  # TODO : Arbitration --> Quantum == 1
                logging.debug('VC Target North non empty at : (%d)' % env.now)
                vc = self.vcs_target_north.pop()
                logging.debug('VC (%s) poped at : %d' % (vc, env.now))
                self.send_flit(vc, self.outNorth)

            # VC targeting -> South
            if len(self.vcs_target_south) > 0:  # TODO : Arbitration --> Quantum == 1
                logging.debug('VC Target South non empty at : (%d)' % env.now)
                vc = self.vcs_target_south.pop()
                logging.debug('VC (%s) poped at : %d' % (vc, env.now))
                self.send_flit(vc, self.outSouth)

            # VC targeting -> East
            if len(self.vcs_target_east) > 0:  # TODO : Arbitration --> Quantum == 1
                logging.debug('VC Target East non empty at : (%d)' % env.now)
                vc = self.vcs_target_east.pop()
                logging.debug('VC (%s) poped at : %d' % (vc, env.now))
                self.send_flit(vc, self.outEast)

            # VC targeting -> West
            if len(self.vcs_target_west) > 0:  # TODO : Arbitration --> Quantum == 1
                logging.debug('VC Target West non empty at : (%d)' % env.now)
                vc = self.vcs_target_west.pop()
                logging.debug('VC (%s) poped at : %d' % (vc, env.now))
                self.send_flit(vc, self.outWest)

            # Simulation Cycle
            yield env.timeout(1)

    def __str__(self):
        return 'Router (%d,%d)' % (self.coordinate.i, self.coordinate.j)
