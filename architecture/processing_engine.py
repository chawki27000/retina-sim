import logging

from engine.event import Event
from engine.event_list import EventType
from engine.global_obj import EVENT_LIST


class ProcessingEngine:
    def __init__(self):
        self.flit_arr_queue = []
        self.packets = None
        self.sending_queue = []

    def router_bind(self, router):
        self.router = router
        self.logger = logging.getLogger(' ')

    def send_to_router(self, message_instance, time):
        # Getting Packets from Message
        # self.packets = copy.deepcopy(message_instance.packets)
        # message_instance.set_depart_time(time)

        # insert message in sending queue
        self.sending_queue.append(message_instance)

        # # event push
        event = Event(EventType.ROUTER_CHECK, self.router, time)
        EVENT_LIST.push(event)

    def flit_receiving(self, flit):
        self.flit_arr_queue.append(flit)

    def __str__(self):
        return 'ProcessingEngine (%d,%d)' % (self.router.coordinate.i, self.router.coordinate.j)
