import logging

from communication.structure import NodeArray, FlitType, Node


class Router:
    def __init__(self, env, id, coordinate, proc_engine):
        self.action = env.process(self.run())
        self.env = env
        self.id = id
        self.coordinate = coordinate
        self.proc_engine = proc_engine
        self.logger = logging.getLogger(' ')

        # Process Attribute
        self.vcs_dictionary = NodeArray()
        self.vcs_target_north = []
        self.vcs_target_south = []
        self.vcs_target_east = []
        self.vcs_target_west = []
        self.vcs_target_pe = []
        self.pipelined_sending = []

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

    def is_packet_still_in_vc(self, packet):
        if self.inPE.is_packet_still_in_vc(packet) or \
                self.inSouth.is_packet_still_in_vc(packet) or \
                self.inNorth.is_packet_still_in_vc(packet) or \
                self.inWest.is_packet_still_in_vc(packet) or \
                self.inEast.is_packet_still_in_vc(packet):
            return True
        else:
            return False

    def receiving_from_pe(self, packet):
        if self.is_packet_still_in_vc(packet):
            return False

        requested_vc = self.inPE.vc_allocator()

        if requested_vc is not None:
            for flit in packet.flits:
                requested_vc.enqueue(flit)
                self.logger.info(
                    '(%d) : %s - %s -> %s -> %s' % (self.env.now, flit, self.proc_engine, requested_vc, self))
            return True
        else:
            return False

    def vc_target_outport(self, vc):

        if len(vc.flits) > 0:
            if self.route_computation(vc.flits[0]) == self.outNorth \
                    and vc not in self.vcs_target_north:
                self.vcs_target_north.append(vc)

            elif self.route_computation(vc.flits[0]) == self.outSouth \
                    and vc not in self.vcs_target_south:
                self.vcs_target_south.append(vc)

            elif self.route_computation(vc.flits[0]) == self.outEast \
                    and vc not in self.vcs_target_east:
                self.vcs_target_east.append(vc)

            elif self.route_computation(vc.flits[0]) == self.outWest \
                    and vc not in self.vcs_target_west:
                self.vcs_target_west.append(vc)

            elif self.route_computation(vc.flits[0]) == self.outPE \
                    and vc not in self.vcs_target_pe:
                self.vcs_target_pe.append(vc)

    def arrived_flit(self, vc):
        flit = vc.dequeue()

        if flit.type == FlitType.tail:
            self.vcs_dictionary.remove(vc)
            vc.release()

        # Flit store
        self.proc_engine.flit_receiving(flit)

        self.logger.info('(%d) : %s - %s -> %s' % (self.env.now, flit, self, self.proc_engine))

    def send_flit(self, vc, outport):

        # getting the first flit in VC
        flit = vc.dequeue()

        # Flit Timestamp to avoid premature sending
        if flit.timestamp == self.env.now:
            vc.flits.insert(0, flit)
            return
        flit.timestamp = self.env.now

        # if is a Head Flit
        if flit.type == FlitType.head:
            # Get idle VC from next Input
            vc_allotted = outport.inPort.vc_allocator()

            if vc_allotted is not None:
                self.logger.debug('(%d) - VC (%s) allotted' % (self.env.now, vc_allotted))
                vc_allotted.enqueue(flit)
                self.logger.info(
                    '(%d) : %s ON %s- %s -> %s -> %s' % (self.env.now, flit, vc, self, vc_allotted, vc_allotted.router))
                vc.credit_out()

                # registering VC allotted in dictionary
                self.vcs_dictionary.add(Node(vc, vc_allotted))

            else:  # No idle VC
                vc.restore(flit)  # restore
                self.logger.debug('(%d) - %s was not sent - VC not allotted ON %s' %
                                  (self.env.now, flit, outport.inPort.router))

        # if is a Body Flit
        elif flit.type == FlitType.body:
            # Getting the alloted vc
            vc_allotted = self.vcs_dictionary.get_target(vc)
            self.logger.debug('(%d) - Retreiving allotted VC (%s)' % (self.env.now, vc_allotted))

            # Sending to the next router
            sent = vc_allotted.enqueue(flit)

            if not sent:  # No Place
                vc.restore(flit)  # restore
                self.logger.debug('(%d) - %s was not sent - No Place in VC (%s)' % (self.env.now, flit, vc_allotted))
            else:
                self.logger.info(
                    '(%d) : %s ON %s- %s -> %s -> %s' % (self.env.now, flit, vc, self, vc_allotted, vc_allotted.router))
                vc.credit_out()

        # if is a Tail Flit
        elif flit.type == FlitType.tail:
            # Getting the alloted vc
            vc_allotted = self.vcs_dictionary.get_target(vc)

            # Sending to the next router
            sent = vc_allotted.enqueue(flit)

            if not sent:  # No Place
                vc.restore(flit)  # restore
                self.logger.debug('(%d) - %s was not sent - No Place in VC (%s)' % (self.env.now, flit, vc_allotted))
            else:
                self.vcs_dictionary.remove(vc)
                vc.release()
                vc.credit_out()
                self.logger.debug('(%d) - VC (%s) - released' % (self.env.now, vc))

    def run(self):
        while True:
            yield self.env.timeout(1)

            # reset if VCs are empty
            self.inEast.reset_slot_table()
            self.inWest.reset_slot_table()
            self.inNorth.reset_slot_table()
            self.inSouth.reset_slot_table()

            # ---------- VC election ----------
            for vc in self.inPE.vcs:
                self.vc_target_outport(vc)
            # Checking North VC
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
                vc = self.vcs_target_north.pop(0)
                self.logger.debug('(%d) - %s From %s -> Elected' % (self.env.now, vc, self))
                self.send_flit(vc, self.outNorth)

            # VC targeting -> South
            if len(self.vcs_target_south) > 0:
                vc = self.vcs_target_south.pop(0)
                self.logger.debug('(%d) - %s From %s -> Elected' % (self.env.now, vc, self))
                self.send_flit(vc, self.outSouth)

            # VC targeting -> East
            if len(self.vcs_target_east) > 0:
                vc = self.vcs_target_east.pop(0)
                self.logger.debug('(%d) - %s From %s -> Elected' % (self.env.now, vc, self))
                self.send_flit(vc, self.outEast)

            # VC targeting -> West
            if len(self.vcs_target_west) > 0:
                vc = self.vcs_target_west.pop(0)
                self.logger.debug('(%d) - %s From %s -> Elected' % (self.env.now, vc, self))
                self.send_flit(vc, self.outWest)

            # VC targeting -> PE
            if len(self.vcs_target_pe) > 0:
                vc = self.vcs_target_pe.pop(0)
                self.logger.debug('(%d) - %s From %s -> Elected' % (self.env.now, vc, self))
                self.arrived_flit(vc)

    def __str__(self):
        return 'Router (%d,%d)' % (self.coordinate.i, self.coordinate.j)
