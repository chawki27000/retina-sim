import unittest

from architecture.noc import NoC
from architecture.virtual_channel import VirtualChannel
from communication.routing import Coordinate
from communication.structure import Packet, Message, FlitType, NodeArray, Node
from engine.event import Event
from engine.event_list import EventList, EventType
from engine.simulation import Simulation
from input.generation import Generation


class TestPacket(unittest.TestCase):

    def setUp(self):
        self.src = Coordinate(1, 1)
        self.dest = Coordinate(2, 2)
        self.message = Message(1, 23, 256, 0, 0, self.src, self.dest)
        self.packet = Packet(1, self.dest, self.message)

    def test_flit_number(self):
        self.assertEqual(len(self.packet.flits), 4)

    def test_flit_type(self):
        self.assertEqual(self.packet.flits[0].type, FlitType.head)
        self.assertEqual(self.packet.flits[1].type, FlitType.body)
        self.assertEqual(self.packet.flits[2].type, FlitType.body)
        self.assertEqual(self.packet.flits[3].type, FlitType.tail)

    def test_packet_number(self):
        self.assertEqual(len(self.message.packets), 2)

    def test_destination_set(self):
        self.assertEqual(self.packet.flits[0].destination, self.dest)
        self.assertEqual(self.packet.flits[1].destination, self.dest)
        self.assertEqual(self.packet.flits[2].destination, self.dest)
        self.assertEqual(self.packet.flits[3].destination, self.dest)


# class TestNoC(unittest.TestCase):
#
#     def setUp(self):
#
#         self.noc = NoC("Network-On-Chip", 4, 4, 12)
#
#     def test_noc_initialisation(self):
#         self.assertEqual(len(self.noc.router_matrix), 4)
#         self.assertEqual(self.noc.square_size, 4)
#
#     def test_noc_routers(self):
#         self.assertEqual(str(self.noc.router_matrix[0][0]), 'Router (0,0)')
#         self.assertEqual(str(self.noc.router_matrix[3][3]), 'Router (3,3)')
#         self.assertEqual(str(self.noc.router_matrix[2][1]), 'Router (2,1)')
#         self.assertEqual(str(self.noc.router_matrix[1][0]), 'Router (1,0)')
#
#         self.assertEqual(self.noc.router_matrix[0][0].id, 1)
#         self.assertEqual(self.noc.router_matrix[3][3].id, 16)
#
#     def test_noc_links(self):
#         self.noc.router_linking()
#
#         self.assertEqual(self.noc.router_matrix[0][0].outEast.inPort, self.noc.router_matrix[0][1].inWest)
#         self.assertEqual(self.noc.router_matrix[0][0].outSouth.inPort, self.noc.router_matrix[1][0].inNorth)
#         self.assertIsNone(self.noc.router_matrix[0][0].outNorth.inPort)
#         self.assertIsNone(self.noc.router_matrix[0][0].outWest.inPort)
#
#         self.assertEqual(self.noc.router_matrix[3][3].outNorth.inPort, self.noc.router_matrix[2][3].inSouth)
#         self.assertEqual(self.noc.router_matrix[3][3].outWest.inPort, self.noc.router_matrix[3][2].inEast)
#         self.assertIsNone(self.noc.router_matrix[3][3].outSouth.inPort)
#         self.assertIsNone(self.noc.router_matrix[3][3].outEast.inPort)
#
#         self.assertEqual(self.noc.router_matrix[2][2].outNorth.inPort, self.noc.router_matrix[1][2].inSouth)
#         self.assertEqual(self.noc.router_matrix[2][2].outWest.inPort, self.noc.router_matrix[2][1].inEast)
#         self.assertEqual(self.noc.router_matrix[2][2].outSouth.inPort, self.noc.router_matrix[3][2].inNorth)
#         self.assertEqual(self.noc.router_matrix[2][2].outEast.inPort, self.noc.router_matrix[2][3].inWest)
#
#
# class TestRouter(unittest.TestCase):
#
#     def setUp(self):
#
#         self.noc = NoC("Network-On-Chip", 4, 4, 12)
#
#         self.proc_engine = self.noc.router_matrix[0][0].proc_engine
#         self.router = self.noc.router_matrix[0][0]
#
#     def test_inport_vcs(self):
#         self.assertEqual(self.noc.router_matrix[3][3].inNorth.nbvc, 4)
#         self.assertEqual(self.noc.router_matrix[3][3].inNorth.vc_size, 12)
#         self.assertEqual(len(self.noc.router_matrix[3][3].inNorth.vcs[0].flits), 0)
#
#     def test_idle_lock_vc(self):
#         allotted_vc = self.router.inPE.vc_allocator()
#         self.assertIsNotNone(allotted_vc)
#         self.assertEqual(self.router.inPE.number_idle_vc(), 3)
#         allotted_vc = self.router.inPE.vc_allocator()
#         self.assertEqual(self.router.inPE.number_idle_vc(), 2)
#         allotted_vc = self.router.inPE.vc_allocator()
#         self.assertEqual(self.router.inPE.number_idle_vc(), 1)
#         allotted_vc = self.router.inPE.vc_allocator()
#         self.assertEqual(self.router.inPE.number_idle_vc(), 0)
#         allotted_vc = self.router.inPE.vc_allocator()
#         self.assertIsNone(allotted_vc)
#
#
# class TestRouting(unittest.TestCase):
#
#     def setUp(self):
#
#         self.noc = NoC("Network-On-Chip", 4, 4, 12)
#
#         self.src = Coordinate(0, 0)
#         self.dest = Coordinate(2, 2)
#         self.message = Message(1, 12, 256, self.src, self.dest)
#         self.packet = Packet(1, self.dest, self.message)
#
#         self.flit = self.packet.flits[0]
#
#         self.proc_engine = self.noc.router_matrix[0][0].proc_engine
#         self.router = self.noc.router_matrix[0][0]
#
#     def test_proc_engine_to_router(self):
#         packets = self.message.packets
#         allotted_vc = self.router.inPE.vc_allocator()
#
#         self.assertEqual(len(packets[0].flits), 4)
#
#         self.proc_engine.send_packet(packets[0], allotted_vc)
#
#         self.assertEqual(len(allotted_vc.flits), 4)
#         self.assertTrue(allotted_vc.lock)
#         self.assertEqual(len(packets[0].flits), 0)
#
#     def test_xy_routing_output(self):
#         self.router = self.noc.router_matrix[2][2]
#         dest1 = Coordinate(1, 2)
#         dest2 = Coordinate(3, 2)
#         dest3 = Coordinate(0, 3)
#         dest4 = Coordinate(0, 0)
#         dest5 = Coordinate(2, 2)
#
#         self.flit.set_destination_info(dest1)
#         self.assertEqual(self.router.route_computation(self.flit), self.router.outNorth)
#         self.flit.set_destination_info(dest2)
#         self.assertEqual(self.router.route_computation(self.flit), self.router.outSouth)
#         self.flit.set_destination_info(dest3)
#         self.assertEqual(self.router.route_computation(self.flit), self.router.outEast)
#         self.flit.set_destination_info(dest4)
#         self.assertEqual(self.router.route_computation(self.flit), self.router.outWest)
#         self.flit.set_destination_info(dest5)
#         self.assertEqual(self.router.route_computation(self.flit), self.router.outPE)
#
#     def test_vc_target_output(self):
#         self.router = self.noc.router_matrix[2][2]
#         dest1 = Coordinate(1, 2)
#         dest4 = Coordinate(0, 0)
#
#         # North
#         vc_north = self.router.inNorth.vcs[0]
#         vc_north1 = self.router.inNorth.vcs[1]
#
#         self.flit.set_destination_info(dest1)
#         vc_north.flits.append(self.flit)
#         self.router.vc_target_outport(vc_north)
#
#         self.assertEqual(len(self.router.vcs_target_north), 1)
#
#         vc_north1.flits.append(self.flit)
#         self.router.vc_target_outport(vc_north1)
#         self.assertEqual(len(self.router.vcs_target_north), 2)
#
#         # West
#         vc_west = self.router.inWest.vcs[0]
#
#         self.flit.set_destination_info(dest4)
#         vc_west.flits.append(self.flit)
#         self.router.vc_target_outport(vc_west)
#
#         self.assertEqual(len(self.router.vcs_target_west), 1)
#
#
# class TestFlitSending(unittest.TestCase):
#
#     def setUp(self):
#         pass
#
#
# class TestNode(unittest.TestCase):
#
#     def setUp(self):
#         self.nodeArray = NodeArray()
#         self.vc_src = VirtualChannel(1, 13, 1)
#         self.vc_target = VirtualChannel(2, 13, 1)
#
#     def test_add(self):
#         node = Node(self.vc_src, self.vc_target)
#         self.nodeArray.add(node)
#
#         self.assertEqual(len(self.nodeArray.array), 1)
#
#         node2 = Node(self.vc_src, self.vc_target)
#         self.nodeArray.add(node2)
#
#         self.assertEqual(len(self.nodeArray.array), 2)
#
#     def test_remove(self):
#         node = Node(self.vc_src, self.vc_target)
#         self.nodeArray.add(node)
#         node2 = Node(self.vc_src, self.vc_target)
#         self.nodeArray.add(node2)
#
#         self.nodeArray.remove(self.vc_src)
#         self.assertEqual(len(self.nodeArray.array), 1)
#
#         self.nodeArray.remove(self.vc_src)
#         self.assertEqual(len(self.nodeArray.array), 0)
#
#     def test_get_target(self):
#         node = Node(self.vc_src, self.vc_target)
#         self.nodeArray.add(node)
#
#         self.assertEqual(self.nodeArray.get_target(self.vc_src), self.vc_target)
#
#         self.nodeArray.remove(self.vc_src)
#
#         self.assertIsNone(self.nodeArray.get_target(self.vc_src))
#
#
# class TestEventList(unittest.TestCase):
#
#     def setUp(self):
#         self.event_list = EventList()
#
#         self.simulation = Simulation()
#
#     def test_list_sorting(self):
#         event1 = Event(EventType.SEND_MESSAGE, None, 2)
#         event2 = Event(EventType.SEND_MESSAGE, None, 1)
#         event3 = Event(EventType.SEND_MESSAGE, None, 6)
#         event4 = Event(EventType.SEND_MESSAGE, None, 3)
#
#         self.event_list.push(event1)
#         self.event_list.push(event2)
#         self.event_list.push(event3)
#         self.event_list.push(event4)
#
#         self.assertEqual(self.event_list.pull(), event2)
#         self.assertEqual(self.event_list.pull(), event1)
#         self.assertEqual(self.event_list.pull(), event4)
#         self.assertEqual(self.event_list.pull(), event3)
#
#     def test_message_event(self):
#         self.src = Coordinate(1, 1)
#         self.dest = Coordinate(2, 2)
#         self.message = Message(1, 40, 256, self.src, self.dest)
#
#         self.simulation.send_message(self.message)
#
#         self.assertEqual(len(self.simulation.event_list.queue), 3)
#         self.assertEqual(self.simulation.event_list.pull().event_type, EventType.SEND_MESSAGE)
#         self.assertEqual(self.simulation.event_list.pull().event_type, EventType.SEND_MESSAGE)
#         self.assertEqual(self.simulation.event_list.pull().event_type, EventType.SEND_MESSAGE)
#         self.assertTrue(self.simulation.event_list.isEmpty())

class TestConflict(unittest.TestCase):

    def setUp(self):
        self.noc = NoC("Network-On-Chip", 4, 4, 12, [1, 1, 1, 1])

        self.src = Coordinate(0, 0)
        self.dest = Coordinate(2, 2)
        self.message = Message(1, 12, 256, 0, 0, self.src, self.dest)
        self.packet = Packet(1, self.dest, self.message)

        self.flit = self.packet.flits[0]

        self.proc_engine = self.noc.router_matrix[0][0].proc_engine
        self.router = self.noc.router_matrix[0][0]

        self.generation = Generation()

    def test_xy_path_coordinate(self):
        coordinate_arr = self.generation.get_xy_path_coordinate(self.message)

        self.generation.messages.append(self.message)

        self.assertEqual(len(coordinate_arr), 4)

        link_utilization = self.generation.get_link_utilisation(self.src)

        self.assertEqual(link_utilization, self.message.get_link_utilization())

        self.generation.conflict_task_generation(self.message, 50)

        self.assertEqual(5, len(self.generation.messages))


if __name__ == '__main__':
    unittest.main()
