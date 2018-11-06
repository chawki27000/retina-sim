import unittest
import simpy

from communication.structure import Packet, Message, FlitType
from communication.routing import Coordinate
from architecture.noc import NoC


class TestPacket(unittest.TestCase):

    def setUp(self):
        self.src = Coordinate(1, 1)
        self.dest = Coordinate(2, 2)
        self.packet = Packet(1, self.dest)
        self.message = Message(23, 256, self.src, self.dest)

    def test_flit_number(self):
        self.assertEqual(len(self.packet.flits), 4)

    def test_flit_type(self):
        self.assertEqual(self.packet.flits[0].type, FlitType.head)
        self.assertEqual(self.packet.flits[1].type, FlitType.body)
        self.assertEqual(self.packet.flits[2].type, FlitType.body)
        self.assertEqual(self.packet.flits[3].type, FlitType.tail)

    def test_packet_number(self):
        self.assertEqual(len(self.message.packets), 2)

    def test_head_flit(self):
        packet = self.message.packets[0]
        packet1 = self.message.packets[1]
        self.assertEqual(packet.flits[0].destination, self.dest)
        self.assertEqual(packet1.flits[0].destination, self.dest)
        self.assertIsNone(packet.flits[1].destination)
        self.assertIsNone(packet1.flits[1].destination)


class TestNoC(unittest.TestCase):

    def setUp(self):
        env = simpy.Environment()

        self.noc = NoC(env, "Network-On-Chip", 4, 4, 12)

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


class TestRouter(unittest.TestCase):

    def setUp(self):
        env = simpy.Environment()

        self.noc = NoC(env, "Network-On-Chip", 4, 4, 12)

        self.proc_engine = self.noc.router_matrix[0][0].proc_engine
        self.router = self.noc.router_matrix[0][0]

    def test_inport_vcs(self):
        self.assertEqual(self.noc.router_matrix[3][3].inNorth.nbvc, 4)
        self.assertEqual(self.noc.router_matrix[3][3].inNorth.vc_size, 12)
        self.assertEqual(len(self.noc.router_matrix[3][3].inNorth.vcs[0].flits), 0)

    def test_idle_lock_vc(self):
        allotted_vc = self.router.inPE.get_first_idle_vc()
        self.assertIsNotNone(allotted_vc)
        self.assertEqual(self.router.inPE.number_idle_vc(), 3)
        allotted_vc = self.router.inPE.get_first_idle_vc()
        self.assertEqual(self.router.inPE.number_idle_vc(), 2)
        allotted_vc = self.router.inPE.get_first_idle_vc()
        self.assertEqual(self.router.inPE.number_idle_vc(), 1)
        allotted_vc = self.router.inPE.get_first_idle_vc()
        self.assertEqual(self.router.inPE.number_idle_vc(), 0)
        allotted_vc = self.router.inPE.get_first_idle_vc()
        self.assertIsNone(allotted_vc)


class TestRouting(unittest.TestCase):

    def setUp(self):
        env = simpy.Environment()

        self.noc = NoC(env, "Network-On-Chip", 4, 4, 12)

        self.src = Coordinate(0, 0)
        self.dest = Coordinate(2, 2)
        self.message = Message(12, 256, self.src, self.dest)

        self.proc_engine = self.noc.router_matrix[0][0].proc_engine
        self.router = self.noc.router_matrix[0][0]

    def test_proc_engine_to_router(self):
        packets = self.message.packets
        allotted_vc = self.router.inPE.get_first_idle_vc()

        self.assertEqual(len(packets[0].flits), 4)

        self.proc_engine.send_packet(packets[0], allotted_vc)

        self.assertEqual(len(allotted_vc.flits), 4)
        self.assertTrue(allotted_vc.lock)
        self.assertEqual(len(packets[0].flits), 0)


if __name__ == '__main__':
    unittest.main()
