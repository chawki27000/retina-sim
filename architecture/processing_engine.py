import copy
import logging

from engine.event import Event
from engine.event_list import EventType
from engine.global_obj import EVENT_LIST


class ProcessingEngine:
    def __init__(self):
        self.flit_arr_queue = []

    def router_bind(self, router):
        self.router = router
        self.logger = logging.getLogger(str(self))

    def send_packet(self, packet, vc_allotted):
        self.logger.debug('vc allotted number : %d' % vc_allotted.id)
        for flit in packet.flits:
            vc_allotted.enqueue(flit)
            self.logger.debug('sending Flit (%s)' % flit.type)

    def send_to_router(self, message_instance, time):

        # Getting Packets from Message
        packets = copy.copy(message_instance.packets)
        message_instance.set_depart_time(time)

        # We assume that we have more place in VCs than packets
        while len(packets) > 0:
            packet = packets.pop()
            self.logger.debug('Time : (%d) - packet sending number (%d)' % (time, packet.id))

            # VC Allocation
            vc_allotted = self.router.inPE.vc_allocator()

            if vc_allotted is not None:
                self.send_packet(packet, vc_allotted)
            else:
                self.logger.debug('Time : (%d) - Not VC allowed' % time)

        # event push
        event = Event(EventType.VC_ELECTION, self.router, time)
        EVENT_LIST.push(event)

    def flit_receiving(self, flit):
        self.flit_arr_queue.append(flit)

    def __str__(self):
        return 'ProcessingEngine (%d,%d)' % (self.router.coordinate.i, self.router.coordinate.j)
