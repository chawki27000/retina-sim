from architecture.noc import NoC
from communication.structure import MessageInstance
from engine.event import Event
from engine.event_list import EventType
from engine.global_obj import CLOCK, EVENT_LIST


class Simulation:

    def __init__(self, hyperiod):
        self.hyperiod = hyperiod  # HyperPeriod
        self.noc = NoC('Network-On-Chip', 4, 6, 12)

    def send_message(self, message):

        for i in range(self.hyperiod):
            if i % message.period == 0:
                message_instance = MessageInstance(message, i)
                event = Event(EventType.SEND_MESSAGE, message_instance, i)  # TODO : replace i by the task offset
                EVENT_LIST.push(event)

    def simulate(self):
        global CLOCK
        while not EVENT_LIST.isEmpty() and CLOCK < self.hyperiod:
            current_event = EVENT_LIST.pull()

            if current_event.event_type == EventType.SEND_MESSAGE:
                # get Event Entity
                message = current_event.entity

                # get source and destination message
                src = message.src

                # get Processing Engine
                proc_engine = self.noc.router_matrix[src.i][src.j].proc_engine

                # Send Message
                proc_engine.send_to_router(message, current_event.time)

                CLOCK = current_event.time

            elif current_event.event_type == EventType.SEND_FLIT:
                # get Event Entity
                router = current_event.entity['router']
                vc = current_event.entity['vc']
                outport = current_event.entity['outport']

                router.send_flit(vc, outport, current_event.time)

                CLOCK = current_event.time

            elif current_event.event_type == EventType.VC_ELECTION:
                # Get Event Entity
                router = current_event.entity

                # VC Election
                router.arbiter(current_event.time)

                CLOCK = current_event.time
