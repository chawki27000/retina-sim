from engine.event import Event
from engine.event_list import EventList, EventType


class Simulation:
    CLOCK = 0

    def __init__(self):
        self.event_list = EventList()
        self.max_sim_time = 100  # HyperPeriod

    def send_message(self, message):

        for i in range(self.max_sim_time):
            if i % message.period == 0:
                event = Event(EventType.send_message, message, i)
                self.event_list.push(event)

    def simulate(self):
        pass
