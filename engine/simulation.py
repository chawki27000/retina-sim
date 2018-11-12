from architecture.noc import NoC
from communication.structure import MessageInstance
from engine.event import Event
from engine.event_list import EventType
from engine.global_obj import CLOCK, EVENT_LIST


class Simulation:

    def __init__(self):
        self.max_sim_time = 100  # HyperPeriod
        self.noc = NoC('Network-On-Chip', 4, 6, 12)

    def send_message(self, message):

        for i in range(self.max_sim_time):
            if i % message.period == 0:
                message_instance = MessageInstance(message, i)
                event = Event(EventType.SEND_MESSAGE, message_instance, i)  # TODO : replace i by the task offset
                EVENT_LIST.push(event)

    def simulate(self):

        while not EVENT_LIST.isEmpty() and CLOCK < self.max_sim_time:
            current_event = EVENT_LIST.pull()

            Simulation.CLOCK = current_event.time

            if current_event.event_type == EventType.SEND_MESSAGE:
                # get Event Entity
                message = current_event.entity

                # get source and destination message
                src = message.src

                # get Processing Engine
                proc_engine = self.noc.router_matrix[src.i][src.j].proc_engine

                # Send Message
                proc_engine.send_to_router(message, current_event.time)

            elif current_event.event_type == EventType.SEND_FLIT:
                pass

            elif current_event.event_type == EventType.VC_ELECTION:
                print('EventType.VC_ELECTION')
