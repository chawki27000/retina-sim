import logging
import time


class ProcessingEngine:
    def __init__(self, env):
        self.action = env.process(self.run())
        self.env = env
        self.flit_arr_queue = []
        self.packets = None
        self.sending_queue = []
        self.initial_delay = 0

    def router_bind(self, router):
        self.router = router
        self.logger = logging.getLogger(' ')

    def send_to_router(self, message_instance, initial_delay=0):
        # insert message in sending queue
        self.initial_delay = initial_delay
        self.sending_queue.append(message_instance)

    def flit_receiving(self, flit):
        self.flit_arr_queue.append(flit)

    def run(self):
        yield self.env.timeout(self.initial_delay)

        while True:
            yield self.env.timeout(1)

            if len(self.sending_queue) > 0:
                message = self.sending_queue.pop(0)

                packets = message.packets

                packet = packets.pop(0)

                if not self.router.receiving_from_pe(packet):
                    message.packets.insert(0, packet)

                if len(message.packets) > 0:
                    self.sending_queue.insert(0, message)

    def __str__(self):
        return 'ProcessingEngine (%d,%d)' % (self.router.coordinate.i, self.router.coordinate.j)
