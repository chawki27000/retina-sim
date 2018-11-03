import unittest
from communication.structure import Packet, Message
from communication.routing import Coordinate

class TestPacket(unittest.TestCase):

    def test_flit_number(self):
        packet = Packet(1)
        self.assertEqual(len(packet.flits), 4)

    def test_packet_number(self):
        src = Coordinate(1,1)
        dest = Coordinate(2,2)
        message = Message(1, 23, 0, src, dest)

        self.assertEqual(len(message.packets), 2)

if __name__ == '__main__':
    unittest.main()
