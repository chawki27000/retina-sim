import copy
import logging

from engine.event import Event
from engine.event_list import EventType
from engine.global_obj import EVENT_LIST


class ProcessingEngine:
    def __init__(self):
        self.flit_arr_queue = []
        self.packets = None

    def router_bind(self, router):
        self.router = router
        self.logger = logging.getLogger(' ')

    # def send_packet(self, packet, vc_allotted):
    #     self.logger.debug('VC(%d) : allotted' % vc_allotted.id)
    #     for flit in packet.flits:
    #         vc_allotted.enqueue(flit)
    #         self.logger.debug('sending Flit (%s)' % flit)

    def send_flit(self, packet, vc, time):

        if len(packet.flits) <= 0:
            return

        flit = packet.flits.pop(0)
        vc.enqueue(flit)
        self.logger.info('(%d) : %s - %s -> %s -> %s' % (time, flit, self, vc, self.router))

        # event push
        event = Event(EventType.PE_SEND_FLIT, {'pe': self,
                                               'packet': packet,
                                               'vc': vc}, time + 1)
        EVENT_LIST.push(event)

        # event push
        event = Event(EventType.VC_ELECTION, self.router, time + 1)
        EVENT_LIST.push(event)

    def send_packet(self, time):

        # Message Fully Sent
        if len(self.packets) <= 0:
            return

        # VC Allocation
        vc_allotted = self.router.inPE.vc_allocator()

        if vc_allotted is not None:
            self.logger.debug('VC(%d) : allotted' % vc_allotted.id)
            packet = self.packets.pop()
            # event push
            event = Event(EventType.PE_SEND_FLIT, {'pe': self,
                                                   'packet': packet,
                                                   'vc': vc_allotted}, time + 1)
            EVENT_LIST.push(event)
        else:
            self.logger.debug('(%d) - Not VC allotted' % time)
            # event push
            event = Event(EventType.PE_SEND_PACKET, self, time + 1)
            EVENT_LIST.push(event)

    def send_to_router(self, message_instance, time):
        # Getting Packets from Message
        self.packets = copy.deepcopy(message_instance.packets)
        message_instance.set_depart_time(time)

        # event push
        event = Event(EventType.PE_SEND_PACKET, self, time)
        EVENT_LIST.push(event)

    def flit_receiving(self, flit):
        self.flit_arr_queue.append(flit)

    def __str__(self):
        return 'ProcessingEngine (%d,%d)' % (self.router.coordinate.i, self.router.coordinate.j)
