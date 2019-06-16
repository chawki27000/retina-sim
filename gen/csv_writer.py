import csv

from analysis.end_to_end_latency import QinModel, TDMA


class CSVWriter:

    def get_max_instance(self):
        max = 0
        for instance in self.messages_i:
            if instance.instance > max:
                max = instance.instance

        return max

    def __init__(self, messages_i, type, noc):
        self.messages_i = messages_i
        self.type = type
        self.noc = noc

    def simulation_trace_csv(self, link):

        # build header row
        header = ['i']
        max_instance = self.get_max_instance()
        for i in range(1, max_instance + 1):
            stri = 'L_' + str(i)
            header.append(stri)

        with open(link, mode='w') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            # File Header
            writer.writerow(header)

            # Array to dictionary
            dico = dict()

            for message in self.messages_i:
                if message.id in dico:
                    dico[message.id].append(message)
                else:
                    dico[message.id] = []
                    dico[message.id].append(message)

            # Write instance latency value
            for item in dico.items():
                instance = item[1]

                write_array = [item[0]]
                for i in range(len(instance)):
                    write_array.append(instance[i].get_latency())

                writer.writerow(write_array)

    def analysis_trace_csv(self, link, messages):
        # build header row
        header = ['i', 'WCLA']

        with open(link, mode='w') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            # File Header
            writer.writerow(header)

            # compute wcla according to arbitration mode
            if self.type == 'RR':
                tdma = TDMA(self.noc, self.noc.vc_quantum)

                for msg in messages:
                    latency = tdma.latency(msg, tdma.slot_table[3])
                    writer.writerow([msg.id, latency])

            elif self.type == 'PRIORITY_PREEMPT':
                qinModel = QinModel(self.noc, messages)

                for msg in messages:
                    latency = qinModel.latency_nth(msg)
                    writer.writerow([msg.id, latency])
