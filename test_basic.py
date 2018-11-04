import unittest
from communication.structure import Packet, Message
from communication.routing import Coordinate
from architecture.noc import NoC


class TestPacket(unittest.TestCase):

    def setUp(self):
        self.packet = Packet(1)
        self.src = Coordinate(1, 1)
        self.dest = Coordinate(2, 2)
        self.message = Message(1, 23, 0, self.src, self.dest)

    def test_flit_number(self):
        self.assertEqual(len(self.packet.flits), 4)

    def test_packet_number(self):
        self.assertEqual(len(self.message.packets), 2)


class TestNoC(unittest.TestCase):

    def setUp(self):
        self.noc = NoC("Network-On-Chip", 4)

    def test_noc_initialisation(self):
        self.assertEqual(len(self.noc.router_matrix), 4)
        self.assertEqual(self.noc.square_size, 4)

    def test_noc_routers(self):
        self.assertEqual(str(self.noc.router_matrix[0][0]), 'Router (0,0)')
        self.assertEqual(str(self.noc.router_matrix[3][3]), 'Router (3,3)')
        self.assertEqual(str(self.noc.router_matrix[2][1]), 'Router (2,1)')
        self.assertEqual(str(self.noc.router_matrix[1][0]), 'Router (1,0)')

        self.assertEqual(self.noc.router_matrix[0][0].id, 1)
        self.assertEqual(self.noc.router_matrix[3][3].id, 16)

    def test_noc_links(self):
        self.noc.router_linking()

        self.assertEqual(self.noc.router_matrix[0][0].outEast.inPort, self.noc.router_matrix[0][1].inWest)
        self.assertEqual(self.noc.router_matrix[0][0].outSouth.inPort, self.noc.router_matrix[1][0].inNorth)
        self.assertIsNone(self.noc.router_matrix[0][0].outNorth.inPort)
        self.assertIsNone(self.noc.router_matrix[0][0].outWest.inPort)

        self.assertEqual(self.noc.router_matrix[3][3].outNorth.inPort, self.noc.router_matrix[2][3].inSouth)
        self.assertEqual(self.noc.router_matrix[3][3].outWest.inPort, self.noc.router_matrix[3][2].inEast)
        self.assertIsNone(self.noc.router_matrix[3][3].outSouth.inPort)
        self.assertIsNone(self.noc.router_matrix[3][3].outEast.inPort)

        self.assertEqual(self.noc.router_matrix[2][2].outNorth.inPort, self.noc.router_matrix[1][2].inSouth)
        self.assertEqual(self.noc.router_matrix[2][2].outWest.inPort, self.noc.router_matrix[2][1].inEast)
        self.assertEqual(self.noc.router_matrix[2][2].outSouth.inPort, self.noc.router_matrix[3][2].inNorth)
        self.assertEqual(self.noc.router_matrix[2][2].outEast.inPort, self.noc.router_matrix[2][3].inWest)


if __name__ == '__main__':
    unittest.main()
