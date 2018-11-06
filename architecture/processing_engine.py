import logging

from communication.structure import MessageInstance


class ProcessingEngine:
    def __init__(self):
        pass

    def router_bind(self, router):
        self.router = router

    def send_packet(self, packet, vc_allotted):
        logging.debug('vc allotted number : %d' % vc_allotted.id)
        while len(packet.flits) > 0:
            flit = packet.get_flit()
            vc_allotted.enqueue(flit)
            logging.debug('sending Flit (%s)' % flit.type)

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
                    logging.debug('packet sending number (%d) at : (%d)' % (packet.id, env.now))

                    # VC Allocation
                    vc_allotted = self.router.inPE.get_first_idle_vc()

                    if vc_allotted is not None:
                        self.send_packet(packet, vc_allotted)
                    else:
                        logging.debug('Not VC allowed')
                        packets.insert(0, packet)

                    yield env.timeout(1)

                # Increment
                instance_count += 1

            yield env.timeout(1)
