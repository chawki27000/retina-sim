import yaml
import logging
import sys

from communication.routing import Coordinate
from communication.structure import Message


class Generation:
    def __init__(self):
        self._quantum_tab = []

    def config(self, link):
        with open(link, 'r') as stream:
            try:
                data = yaml.load(stream)

                # parsing
                self._square_size = data['noc']['dimension']
                self._nbvc = data['noc']['numberOfVC']
                self._vc_size = data['noc']['VCBufferSize']

                # VC Quatum
                quantum = data['quantum']
                if len(quantum) != self._nbvc:
                    logging.info('Config Error : VC Quantum settings is not identical to the number of VC')
                    sys.exit()
                else:
                    for q in quantum.items():
                        self._quantum_tab.append(q[1])

            except yaml.YAMLError as exc:
                print(exc)

    def scenario(self, link):
        with open(link, 'r') as stream:
            try:
                data = yaml.load(stream)

                # Messages
                messages = data['scenario']
                message_tab = []
                count = 0
                for m in messages:
                    src = m['src']
                    dest = m['dest']
                    size = m['size']
                    offset = m['offset']
                    deadline = m['deadline']
                    period = m['period']

                    message_tab.append(Message(count,
                                               period,
                                               size,
                                               offset,
                                               deadline,
                                               Coordinate(src['i'], src['j']),
                                               Coordinate(dest['i'], dest['j']),
                                               ))
                    count += 1

                return message_tab

            except yaml.YAMLError as exc:
                print(exc)

    def square_size(self):
        return self._square_size

    def nbvc(self):
        return self._nbvc

    def vc_size(self):
        return self._vc_size

    def vc_quantum(self):
        return self._quantum_tab
