import csv


class CSVWriter:
    def __init__(self, messages_i):
        self.messages_i = messages_i

    def flit_print(self):
        for message in self.messages_i:
            print('%s arrived at : %d' % (message, message.get_arriving_time()))

    def generate_csv(self, link):
        with open(link, mode='w') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            # File Header
            writer.writerow(['i', 'WCLA', 'L_1', 'L_2', 'L_3', 'L_4'])

            #