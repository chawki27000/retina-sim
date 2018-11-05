from communication.structure import Message, MessageInstance, Packet, Flit
from communication.routing import Coordinate


class ProcessingEngine:
    def __init__(self):
        pass

    def router_bind(self, router):
        self.router = router

    def send_message(self, m_instance):

        # Getting Packets from Message
        packets = m_instance.packets

        while len(packets) > 0:

            packet = packets.pop()

            # VC Allocation
            vc_allotted = self.router.inPE.get_first_idle_vc
            if vc_allotted is not None:
                self.send_packet(packet, vc_allotted)
            else:
                pass

        # LOG
        print('Sending message N°(%d) from R(%d,%d) to R(%d,%d)'
              % (m_instance.instance,
                 m_instance.src.i,
                 m_instance.src.j,
                 m_instance.dest.i,
                 m_instance.dest.j))

    def send_packet(self, packet, vc_allotted):

        # Getting Flits from Packet
        flits = packet.flits

        # sending to VC
        while len(flits) > 0:
            flit = flits.pop()
            vc_allotted.push(flit)

    def process(self, env, message):
        while True:
            # MessageInstance Counter
            instance_count = 1

            # MessageInstance Initialization
            m_instance = MessageInstance(message, instance_count)

            # Sending
            self.send_message(m_instance)

            # SIM
            yield env.timeout(20)

            # Increment
            instance_count += 1
