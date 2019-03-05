class Trace:
    def __init__(self, flit, start):
        self.flit = flit
        self.start = start

    def set_arrival(self, arrival):
        self.arrival = arrival


class TraceSet:
    def __init__(self):
        self.set = []

    def add_trace(self, trace):
        self.set.append(trace)

    def set_flit_arrival(self, flit, arrival):
        for trace in self.set:
            if trace.flit == flit:
                trace.set_arrival(arrival)

    def __str__(self):
        stri = '-- [ '
        for trace in self.set:
            stri += '%s -- released at : %d -- arrived at : %d -- latency : %d' % \
                    (trace.flit, trace.start, trace.arrival, trace.arrival - trace.start)
            stri += '\n'

        stri += ' ] --'
        return stri
