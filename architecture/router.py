import logging

from communication.structure import FlitType, NodeArray, Node


class Router:
    def __init__(self, id, coordinate, proc_engine):
        self.id = id
        self.coordinate = coordinate
        self.proc_engine = proc_engine
        self.logger = logging.getLogger(str(self))

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

    def send_flit(self, vc, outport):

        # getting the first flit in VC
        flit = vc.dequeue()
        if flit is None:
            return

        # if is a Head Flit
        if flit.type == FlitType.head:
            self.logger.debug('%s ready to be sent' % flit)

            # Get idle VC from next Input
            vc_allotted = outport.inPort.get_first_idle_vc()

            if vc_allotted is not None:
                self.logger.debug('VC (%s) allotted' % vc_allotted)
                # send flit
                vc_allotted.enqueue(flit)
                self.logger.debug('%s : sent' % flit)
                # registering VC allotted in dictionary
                self.vcs_dictionary.add(Node(vc, vc_allotted))
            else:  # No idle VC
                vc.append(flit)
                self.logger.debug('%s was not sent - VC not allotted' % flit)

        # if is a Body Flit
        elif flit.type == FlitType.body:
            self.logger.debug('%s ready to be sent' % flit)
            # Getting the alloted vc
            vc_allotted = self.vcs_dictionary.get_target(vc)
            self.logger.debug('Retreiving allotted VC (%s)' % vc_allotted)
            if not vc_allotted.enqueue(flit):  # No Place
                vc.append(flit)
                self.logger.debug('%s was not sent - No Place in VC (%s)' % (flit, vc_allotted))
            else:
                self.logger.debug('%s : sent' % flit)

        # if is a Tail Flit
        elif flit.type == FlitType.tail:
            self.logger.debug('%s ready to be sent' % flit)
            # Getting the alloted vc
            vc_allotted = self.vcs_dictionary.get_target(vc)
            if not vc_allotted.enqueue(flit):  # No Place
                vc.append(flit)
                self.logger.debug('%s was not sent - No Place in VC (%s)' % (flit, vc_allotted))
            else:
                self.logger.debug('%s : sent' % flit)
                self.vcs_dictionary.remove(vc)
                vc.lock = False
                self.logger.debug('VC (%s) - released' % vc_allotted)

    def vc_target_outport(self, vc):
        if len(vc.flits) > 0:
            if self.get_xy_routing_output(vc.flits[0]) == self.outNorth \
                    and vc not in self.vcs_target_north:
                self.vcs_target_north.insert(0, vc)
            elif self.get_xy_routing_output(vc.flits[0]) == self.outSouth \
                    and vc not in self.vcs_target_north:
                self.vcs_target_south.insert(0, vc)
            elif self.get_xy_routing_output(vc.flits[0]) == self.outEast \
                    and vc not in self.vcs_target_north:
                self.vcs_target_east.insert(0, vc)
            elif self.get_xy_routing_output(vc.flits[0]) == self.outWest \
                    and vc not in self.vcs_target_north:
                self.vcs_target_west.insert(0, vc)

    # SIMULATION PROCESS
    def process(self, env):
        while True:

            # Checking North VC
            for vc in self.inPE.vcs:
                self.vc_target_outport(vc)
            for vc in self.inNorth.vcs:
                self.vc_target_outport(vc)
            # Checking South VC
            for vc in self.inSouth.vcs:
                self.vc_target_outport(vc)
            # Checking East VC
            for vc in self.inEast.vcs:
                self.vc_target_outport(vc)
            # Checking West VC
            for vc in self.inWest.vcs:
                self.vc_target_outport(vc)

            # VC targeting -> North
            if len(self.vcs_target_north) > 0:  # TODO : Arbitration --> Quantum == 1
                self.logger.debug('VC Target North non empty at : %d' % env.now)
                vc = self.vcs_target_north.pop()
                self.logger.debug('VC (%s) poped at : %d' % (vc, env.now))
                self.send_flit(vc, self.outNorth)

            # VC targeting -> South
            if len(self.vcs_target_south) > 0:  # TODO : Arbitration --> Quantum == 1
                self.logger.debug('VC Target South non empty at : %d' % env.now)
                vc = self.vcs_target_south.pop()
                self.logger.debug('VC (%s) poped at : %d' % (vc, env.now))
                self.send_flit(vc, self.outSouth)

            # VC targeting -> East
            if len(self.vcs_target_east) > 0:  # TODO : Arbitration --> Quantum == 1
                self.logger.debug('VC Target East non empty at : %d' % env.now)
                vc = self.vcs_target_east.pop()
                self.logger.debug('VC (%s) poped at : %d' % (vc, env.now))
                self.send_flit(vc, self.outEast)

            # VC targeting -> West
            if len(self.vcs_target_west) > 0:  # TODO : Arbitration --> Quantum == 1
                self.logger.debug('VC Target West non empty at : %d' % env.now)
                vc = self.vcs_target_west.pop()
                self.logger.debug('VC (%s) poped at : %d' % (vc, env.now))
                self.send_flit(vc, self.outWest)

            # Simulation Cycle
            yield env.timeout(1)

    def __str__(self):
        return 'Router (%d,%d)' % (self.coordinate.i, self.coordinate.j)
