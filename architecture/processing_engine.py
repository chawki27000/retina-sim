import logging

from communication.structure import Message, MessageInstance, Packet, Flit
from communication.routing import Coordinate


class ProcessingEngine:
    def __init__(self):
        pass

    def router_bind(self, router):
        self.router = router

    # def send_message(self, env, m_instance):
    #     logging.debug('send_message : instance number (%d) ' % m_instance.instance)
    #     # Getting Packets from Message
    #     packets = m_instance.packets
    #
    #     while len(packets) > 0:
    #         packet = packets.pop()
    #         logging.debug('packet sending number : (%d) at : (%d)' % (packet.id, env.now))
    #
    #         # VC Allocation
    #         vc_allotted = self.router.inPE.get_first_idle_vc()
    #
    #         if vc_allotted is not None:
    #             vc_allotted.lock() # LOCK
    #             logging.debug('vc allotted number : %d' % vc_allotted.id)
    #             while len(packet) > 0:
    #                 flit = packet.pop()
    #                 vc_allotted.push(flit)
    #         else:
    #             pass
    #
    #         yield env.timeout(1)

    def send_packet(self, packet, vc_allotted):
        logging.debug('vc allotted number : %d' % vc_allotted.id)
        while len(packet.flits) > 0:
            flit = packet.flits.pop()
            vc_allotted.enqueue(flit)

    def process(self, env, message):
        # MessageInstance Counter
        instance_count = 1
        logging.debug('begin PE process at : %d' % env.now)
        while True:

            if env.now % message.period == 0:
                logging.debug('periodic time : %d' % env.now)
                # MessageInstance Initialization
                m_instance = MessageInstance(message, instance_count)

                # START : Message Sending
                logging.debug('send_message : instance number (%d) ' % m_instance.instance)
                # Getting Packets from Message
                packets = m_instance.packets

                while len(packets) > 0:
                    packet = packets.pop()
                    logging.debug('packet sending number : (%d) at : (%d)' % (packet.id, env.now))

                    # VC Allocation
                    vc_allotted = self.router.inPE.get_first_idle_vc()

                    if vc_allotted is not None:
                        self.send_packet(packet, vc_allotted)
                    else:
                        logging.debug('Not VC allotted ')

                    yield env.timeout(1)

                # Increment
                instance_count += 1

            yield env.timeout(1)
