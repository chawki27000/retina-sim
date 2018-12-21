import csv


class CSVWriter:
    def __init__(self, messages_i, type):
        self.messages_i = messages_i
        self.type = type

    def flit_print(self):
        for message in self.messages_i:
            pass
            print('%s depart at : %d arrived at : %d' % (message,
                                                         message.get_depart_time(),
                                                         message.get_arriving_time()))

    def generate_csv(self, link):
        with open(link, mode='w') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            # Array to dictionary
            dico = dict()

            for message in self.messages_i:
                if message.id in dico:
                    dico[message.id].append(message)
                else:
                    dico[message.id] = []
                    dico[message.id].append(message)

            # generation
            if self.type == 0:  # Simulation
                # File Header
                writer.writerow(['i', 'L_1', 'L_2', 'L_3', 'L_4'])

                for item in dico.items():
                    instance = item[1]

                    if len(instance) == 1:
                        writer.writerow([instance[0].id,
                                         instance[0].get_latency()])

                    if len(instance) == 2:
                        writer.writerow([instance[0].id,
                                         instance[0].get_latency(),
                                         instance[1].get_latency()])

                    if len(instance) == 3:
                        writer.writerow([instance[0].id,
                                         instance[0].get_latency(),
                                         instance[1].get_latency(),
                                         instance[2].get_latency()])

                    if len(instance) == 4:
                        writer.writerow([instance[0].id,
                                         instance[0].get_latency(),
                                         instance[1].get_latency(),
                                         instance[2].get_latency(),
                                         instance[3].get_latency()])

            elif self.type == 1:  # Analysis
                # File Header
                writer.writerow(['i', 'WCLA'])

                for message in self.messages_i:
                    writer.writerow([message.id,
                                     message.get_analysis_latency()])
