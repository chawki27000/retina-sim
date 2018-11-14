import logging

from communication.structure import FlitType, NodeArray, Node
from engine.event import Event
from engine.event_list import EventType
from engine.global_obj import EVENT_LIST


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
        self.vcs_target_pe = []

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

    def route_computation(self, flit):
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
        return inport.vc_allocator()

    def send_flit(self, vc, outport, time):

        # getting the first flit in VC
        flit = vc.dequeue()
        if flit is None:
            return

        # if is a Head Flit
        if flit.type == FlitType.head:
            self.logger.debug('Time : (%d) - %s ready to be sent' % (time, flit))

            # Get idle VC from next Input
            vc_allotted = outport.inPort.vc_allocator()

            if vc_allotted is not None:
                self.logger.debug('Time : (%d) - VC (%s) allotted' % (time, vc_allotted))
                # send flit
                vc_allotted.enqueue(flit)
                self.logger.info('Time : (%d) - %s -> sent to %s' % (time, flit, vc_allotted.router))
                vc.credit_out()
                # registering VC allotted in dictionary
                self.vcs_dictionary.add(Node(vc, vc_allotted))
            else:  # No idle VC
                vc.enqueue(flit)  # restore
                # event push
                event = Event(EventType.SEND_FLIT, {'router': self,
                                                    'vc': vc,
                                                    'outport': self.outNorth}, time + 1)

                EVENT_LIST.push(event)
                # Next routing
                event = Event(EventType.VC_ELECTION, vc_allotted.router, time)
                EVENT_LIST.push(event)
                self.logger.debug('Time : (%d) - %s was not sent - VC not allotted' % (time, flit))
                return None

        # if is a Body Flit
        elif flit.type == FlitType.body:
            self.logger.debug('Time : (%d) - %s ready to be sent' % (time, flit))
            # Getting the alloted vc
            vc_allotted = self.vcs_dictionary.get_target(vc)
            self.logger.debug('Time : (%d) - Retreiving allotted VC (%s)' % (time, vc_allotted))
            if not vc_allotted.enqueue(flit):  # No Place
                vc.enqueue(flit)  # restore
                # event push
                event = Event(EventType.SEND_FLIT, {'router': self,
                                                    'vc': vc,
                                                    'outport': self.outNorth}, time + 1)
                EVENT_LIST.push(event)
                self.logger.debug('Time : (%d) - %s was not sent - No Place in VC (%s)' % (time, flit, vc_allotted))
                return None

            else:
                # Next routing
                event = Event(EventType.VC_ELECTION, vc_allotted.router, time)
                EVENT_LIST.push(event)
                self.logger.info('Time : (%d) - %s -> sent to %s' % (time, flit, vc_allotted.router))
                vc.credit_out()

        # if is a Tail Flit
        elif flit.type == FlitType.tail:
            self.logger.debug('Time : (%d) - %s ready to be sent' % (time, flit))
            # Getting the alloted vc
            vc_allotted = self.vcs_dictionary.get_target(vc)
            if not vc_allotted.enqueue(flit):  # No Place
                vc.enqueue(flit)  # restore
                # event push
                event = Event(EventType.SEND_FLIT, {'router': self,
                                                    'vc': vc,
                                                    'outport': self.outNorth}, time + 1)
                EVENT_LIST.push(event)
                self.logger.debug('Time : (%d) - %s was not sent - No Place in VC (%s)' % (time, flit, vc_allotted))
                return None

            else:
                self.logger.info('Time : (%d) - %s -> sent to %s' % (time, flit, vc_allotted.router))
                # Next routing
                event = Event(EventType.VC_ELECTION, vc_allotted.router, time)
                EVENT_LIST.push(event)
                self.vcs_dictionary.remove(vc)
                vc.lock = False
                self.logger.debug('Time : (%d) - VC (%s) - released' % (time, vc_allotted))

        # If Quantum is finished
        if vc.quantum <= 0:
            self.logger.debug('Time : (%d) - VC (%s) - quantum finished' % (time, vc))
            # new VC Election - event push
            event = Event(EventType.VC_ELECTION, self, time + 1)
            EVENT_LIST.push(event)

        # Another Quantum
        else:
            self.logger.debug('Time : (%d) - VC (%s) - quantum NOT finished' % (time, vc))
            event = Event(EventType.SEND_FLIT, {'router': self,
                                                'vc': vc,
                                                'outport': self.outNorth}, time + 1)
            EVENT_LIST.push(event)

    def arrived_flit(self, vc, time):
        flit = vc.dequeue()

        if flit.type == FlitType.tail:
            self.vcs_dictionary.remove(vc)
            vc.lock = False

        flit.set_arrival_time(time)
        self.logger.debug('Time : (%d) - %s arrived' % (time, flit))

    def vc_target_outport(self, vc):
        if len(vc.flits) > 0:
            if self.route_computation(vc.flits[0]) == self.outNorth \
                    and vc not in self.vcs_target_north:
                self.vcs_target_north.insert(0, vc)
                vc.reset_credit()
            elif self.route_computation(vc.flits[0]) == self.outSouth \
                    and vc not in self.vcs_target_south:
                self.vcs_target_south.insert(0, vc)
            elif self.route_computation(vc.flits[0]) == self.outEast \
                    and vc not in self.vcs_target_east:
                self.vcs_target_east.insert(0, vc)
            elif self.route_computation(vc.flits[0]) == self.outWest \
                    and vc not in self.vcs_target_west:
                self.vcs_target_west.insert(0, vc)
            # elif self.route_computation(vc.flits[0]) == self.outPE \
            #         and vc not in self.vcs_target_pe:
            #     self.vcs_target_pe.insert(0, vc)

    def arbiter(self, time):
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
        if len(self.vcs_target_north) > 0:
            vc = self.vcs_target_north.pop()
            # event push
            event = Event(EventType.SEND_FLIT, {'router': self,
                                                'vc': vc,
                                                'outport': self.outNorth}, time)
            EVENT_LIST.push(event)
            return None

        # VC targeting -> South
        if len(self.vcs_target_south) > 0:
            vc = self.vcs_target_south.pop()
            # event push
            event = Event(EventType.SEND_FLIT, {'router': self,
                                                'vc': vc,
                                                'outport': self.outSouth}, time)
            EVENT_LIST.push(event)
            return None

        # VC targeting -> East
        if len(self.vcs_target_east) > 0:
            vc = self.vcs_target_east.pop()
            # event push
            event = Event(EventType.SEND_FLIT, {'router': self,
                                                'vc': vc,
                                                'outport': self.outEast}, time)
            EVENT_LIST.push(event)
            return None

        # VC targeting -> West
        if len(self.vcs_target_west) > 0:
            vc = self.vcs_target_west.pop()
            # event push
            event = Event(EventType.SEND_FLIT, {'router': self,
                                                'vc': vc,
                                                'outport': self.outWest}, time)
            EVENT_LIST.push(event)
            return None

    def __str__(self):
        return 'Router (%d,%d)' % (self.coordinate.i, self.coordinate.j)
