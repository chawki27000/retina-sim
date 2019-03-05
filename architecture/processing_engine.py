import copy
import logging

from engine.event import Event
from engine.event_list import EventType
from engine.global_obj import EVENT_LIST
from engine.simulation import TRACESET
from gen.trace import Trace


class ProcessingEngine:
    def __init__(self):
        self.flit_arr_queue = []
        self.packets = None

    def router_bind(self, router):
        self.router = router
        self.logger = logging.getLogger(' ')

    def send_packet(self, time):

        # Message Fully Sent
        if len(self.packets) <= 0:
            return

        # VC Allocation
        print("######### prio : %d" % self.packets[-1].priority)
        vc_allotted = self.router.inPE.priority_vc_allocator(self.packets[-1].priority)

        if vc_allotted is not None:
            self.logger.debug('VC(%d) : allotted' % vc_allotted.id)
            # getting the remaining packet
            packet = self.packets.pop(0)

            # put all flits on the InPE at the same time
            i = 0
            while len(packet.flits) > 0:
                flit = packet.flits.pop(0)
                vc_allotted.enqueue(flit)

                # trace create
                TRACESET.add_trace(Trace(flit, time + i))
                i += 1

            # event push
            event = Event(EventType.VC_ELECTION, self.router, time + 1)
            EVENT_LIST.push(event)

        else:
            self.logger.debug('(%d) - Not VC allotted' % time)

        # Send another packet if PE VC is available
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
