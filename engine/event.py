class Event:
    def __init__(self, event_type, entity, time):
        self.event_type = event_type
        self.entity = entity
        self.time = time

    def compare_to(self, event):
        return event.time < self.time

    def __str__(self):
        return '(ev: %s, t: %d, entity: %s)' % (self.event_type, self.time, self.entity)
