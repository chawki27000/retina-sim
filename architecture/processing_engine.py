from communication.structure import Message, MessageInstance, Packet, Flit
from communication.routing import Coordinate


class ProcessingEngine:
    def __init__(self):
        pass

    def router_bind(self, router):
        self.router = router

    def send_message(self, i, j, size, period, instance):

        # Coordinate Initialization
        dest = Coordinate(i, j)
        src = Coordinate(self.router.coordinate.i, self.router.coordinate.j)

        # Message Initialization
        message = Message(period, size, src, dest)

        # Message Instance
        m_instance = MessageInstance(message, instance)

        print('Sending message N°(%d) from R(%d,%d) to R(%d,%d)'
              % (m_instance.instance,
                 m_instance.src.i,
                 m_instance.src.j,
                 m_instance.dest.i,
                 m_instance.dest.j))

    def process(self, env):
        while True:
            inst = 1
            print('at  : %d' % env.now)

            self.send_message(1, 1, 300, 20, inst)
            yield env.timeout(20)

            inst += 1
