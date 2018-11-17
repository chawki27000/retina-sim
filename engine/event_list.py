import enum


class EventType(enum.Enum):
    SEND_MESSAGE = 1
    SEND_FLIT = 2
    VC_ELECTION = 3
    ARR_FLIT = 4


class EventList:
    def __init__(self):
        self.queue = dict()
        self.register = dict()  # has a purpose to avoid duplicate event in the same timestamp

    def isEmpty(self):
        return len(self.queue) == 0

    def push(self, event):
        # Avoiding duplicate event
        if self.double_event(event):
            event.time += 1

        else:
            # check if key is in dict
            if event.time in self.queue:
                self.queue[event.time].append(event)
            else:
                self.queue[event.time] = []
                self.queue[event.time].append(event)

    def pull(self, time):
        if time in self.queue:
            return self.queue[time]
        else:
            return None

    def double_event(self, event):
        if event.event_type == EventType.SEND_FLIT:
            entity = event.entity['router']
            if event.time in self.register:
                if entity in self.register[event.time]:
                    return True
                else:
                    self.register[event.time].append(entity)
                    return False
            else:
                self.register[event.time] = []
                self.register[event.time].append(entity)
                return False

    def __str__(self):
        return '\n'.join([str(i) for i in self.queue])
