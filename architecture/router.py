from communication.routing import Direction


class Router:
    def __init__(self, id, coordinate, proc_engine):
        self.id = id
        self.coordinate = coordinate
        self.proc_engine = proc_engine

        # Process Attribute
        self.vcs_dictionnary = dict()
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

    def send_head_flit(self, flit, output):

        # Get idle VC from next Input
        vc_allotted = output.inPort.get_first_idle_vc()

        if vc_allotted is not None:
            vc_allotted.enqueue(flit)
            return vc_allotted
        else:
            return None

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


            # Simulation Cycle
            yield env.timeout(1)

    def __str__(self):
        return 'Router (%d,%d)' % (self.coordinate.i, self.coordinate.j)
