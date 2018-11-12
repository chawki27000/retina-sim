import logging

from communication.structure import MessageInstance
from engine.event import Event
from engine.event_list import EventType
from engine.global_obj import CLOCK, EVENT_LIST


class ProcessingEngine:
    def __init__(self):
        pass

    def router_bind(self, router):
        self.router = router
        self.logger = logging.getLogger(str(self))

    def send_packet(self, packet, vc_allotted):
        self.logger.debug('vc allotted number : %d' % vc_allotted.id)
        while len(packet.flits) > 0:
            flit = packet.get_flit()
            vc_allotted.enqueue(flit)
            self.logger.debug('sending Flit (%s)' % flit.type)

    def send_to_router(self, message_instance, time):

        # Getting Packets from Message
        packets = message_instance.packets

        # We assume that we have more place in VCs than packets
        while len(packets) > 0:
            packet = packets.pop()
            self.logger.debug('packet sending number (%d) at : (%d)' % (packet.id, time))

            # VC Allocation
            vc_allotted = self.router.inPE.vc_allocator()

            if vc_allotted is not None:
                self.send_packet(packet, vc_allotted)
                # event push
                event = Event(EventType.VC_ELECTION, self.router, time + 1)
                EVENT_LIST.push(event)

            else:
                self.logger.debug('Not VC allowed')

    # SIMULATION PROCESS
    def process(self, env, message):
        # MessageInstance Counter
        instance_count = 1
        self.logger.debug('begin PE process at : %d' % env.now)
        while True:

            if env.now % message.period == 0:
                self.logger.debug('periodic time : %d' % env.now)
                # MessageInstance Initialization
                m_instance = MessageInstance(message, instance_count)

                # START : Message Sending
                self.logger.debug('send_message : instance number (%d) ' % m_instance.instance)
                # Getting Packets from Message
                packets = m_instance.packets

                while len(packets) > 0:
                    packet = packets.pop()
                    self.logger.debug('packet sending number (%d) at : (%d)' % (packet.id, env.now))

                    # VC Allocation
                    vc_allotted = self.router.inPE.vc_allocator()

                    if vc_allotted is not None:
                        self.send_packet(packet, vc_allotted)
                    else:
                        self.logger.debug('Not VC allowed')
                        packets.insert(0, packet)

                    yield env.timeout(1)

                # Increment
                instance_count += 1

            yield env.timeout(1)

    def __str__(self):
        return 'ProcessingEngine (%d,%d)' % (self.router.coordinate.i, self.router.coordinate.j)
