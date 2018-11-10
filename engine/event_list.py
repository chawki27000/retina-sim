import enum


class EventType(enum.Enum):
    send_message = 1
    send_flit = 2


class EventList:
    def __init__(self):
        self.queue = []

    def isEmpty(self):
        return len(self.queue) == []

    def push(self, event):
        self.queue.append(event)
        self.queue = sorted(self.queue, key=lambda ev: ev.time, reverse=True)

    def pull(self):
        return self.queue.pop()

    def cancel(self, event):
        self.queue.remove(event)

    def __str__(self):
        return '\n'.join([str(i) for i in self.queue])
