from communication.structure import MessageInstance
from engine.event import Event
from engine.event_list import EventType
from engine.global_obj import EVENT_LIST
from gen.trace import TraceSet

CLOCK = 0
TRACESET = TraceSet()


class Simulation:

    def __init__(self, noc, hyperperiod):
        self.hyperperiod = hyperperiod  # HyperPeriod
        self.noc = noc
        self._message_instance_tab = []

    def send_message(self, message):

        instance_count = 1
        for i in range(self.hyperperiod):
            if i % message.period == 0:
                message_instance = MessageInstance(message, instance_count)
                event = Event(EventType.SEND_MESSAGE, message_instance,
                              i + message_instance.offset)
                EVENT_LIST.push(event)

                # Instance Saving
                self._message_instance_tab.append(message_instance)
                instance_count += 1

    def simulate(self, arbitration):
        global CLOCK
        global TRACESET
        while not EVENT_LIST.isEmpty() and CLOCK < self.hyperperiod:

            # time.sleep(1)

            events = EVENT_LIST.pull(CLOCK)

            # print('------------------- %d -------------------' % CLOCK)
            # if events is not None:
            #     for ev in events:
            #         print(ev)

            # for key in EVENT_LIST.register.keys():
            #     for router in EVENT_LIST.register[key]:
            #         print('%d -> %s' % (key, router))

            if events is not None and len(events) > 0:
                current_event = events.pop()

                #### Processing Engine Events ####
                if current_event.event_type == EventType.SEND_MESSAGE:
                    # get Event Entity
                    message = current_event.entity

                    # get source and destination message
                    src = message.src

                    # get Processing Engine
                    proc_engine = self.noc.router_matrix[src.i][src.j].proc_engine

                    # Send Message
                    proc_engine.send_to_router(message, CLOCK)

                elif current_event.event_type == EventType.PE_SEND_PACKET:
                    # Get event Entity
                    pe = current_event.entity

                    pe.send_packet(CLOCK)


                #### Router Events ####
                elif current_event.event_type == EventType.SEND_FLIT:
                    # get Event Entity
                    router = current_event.entity['router']
                    vc = current_event.entity['vc']
                    outport = current_event.entity['outport']

                    # FLIT Sending
                    if arbitration == 'RR':
                        router.send_flit_by_credit(vc, outport, CLOCK)
                    elif arbitration == 'PRIORITY_PREEMPT':
                        router.send_flit_by_priority(vc, outport, CLOCK)

                elif current_event.event_type == EventType.VC_ELECTION:
                    # Get Event Entity
                    router = current_event.entity

                    # VC Election
                    if arbitration == 'RR':
                        router.rr_arbiter(CLOCK)
                    elif arbitration == 'PRIORITY_PREEMPT':
                        router.priority_arbiter(CLOCK)
                    elif arbitration == 'PRIORITY_NON_PREEMPT':
                        router.preemptive_priority_arbiter(CLOCK)

                elif current_event.event_type == EventType.ARR_FLIT:
                    # get Event Entity
                    router = current_event.entity['router']
                    vc = current_event.entity['vc']

                    # Flit -> PE
                    router.arrived_flit(vc, CLOCK)

                elif current_event.event_type == EventType.ROUTER_CHECK:
                    # get Event Entity
                    router = current_event.entity

                    router.router_check(CLOCK, arbitration)

            else:
                CLOCK += 1

    def reset_clock(self):
        global CLOCK
        CLOCK = 0

    def get_message_instance_tab(self):
        return self._message_instance_tab
