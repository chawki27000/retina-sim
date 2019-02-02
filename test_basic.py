import unittest

from architecture.noc import NoC
from architecture.virtual_channel import VirtualChannel
from communication.routing import Coordinate, Direction
from communication.structure import Packet, Message, FlitType, NodeArray, Node, Link
from gen.generation import Generation


class TestPacket(unittest.TestCase):

    def setUp(self):
        self.src = Coordinate(1, 1)
        self.dest = Coordinate(2, 2)
        self.message = Message(1, 23, 256, 0, 0, self.src, self.dest)
        self.packet = Packet(1, self.dest, self.message)

    def test_flit_number(self):
        self.assertEqual(len(self.packet.flits), 32)

    def test_flit_type(self):
        self.assertEqual(self.packet.flits[0].type, FlitType.head)
        self.assertEqual(self.packet.flits[1].type, FlitType.body)
        self.assertEqual(self.packet.flits[2].type, FlitType.body)
        self.assertEqual(self.packet.flits[31].type, FlitType.tail)

    def test_packet_number(self):
        self.assertEqual(len(self.message.packets), 1)

    def test_destination_set(self):
        self.assertEqual(self.packet.flits[0].destination, self.dest)
        self.assertEqual(self.packet.flits[1].destination, self.dest)
        self.assertEqual(self.packet.flits[2].destination, self.dest)
        self.assertEqual(self.packet.flits[3].destination, self.dest)


class TestNoC(unittest.TestCase):

    def setUp(self):
        self.noc = NoC("Network-On-Chip", 4, 4, 12, [1, 1, 1, 1])
        self.noc.router_linking()

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

    def test_get_router_coordinate_by_id(self):
        coord = self.noc.get_router_coordinate_by_id(1)
        self.assertEqual(coord.i, 0)
        self.assertEqual(coord.j, 0)
        coord = self.noc.get_router_coordinate_by_id(16)
        self.assertEqual(coord.i, 3)
        self.assertEqual(coord.j, 3)


class TestLink(unittest.TestCase):
    def setUp(self):
        self.noc = NoC("Network-On-Chip", 3, 4, 12, [1, 1, 1, 1])
        self.noc.router_linking()

    def test_links_array(self):
        self.noc.link_array_filling()
        self.assertEqual(len(self.noc.links.keys()), 9)
        self.assertEqual(len(self.noc.links['1']), 2)
        self.assertEqual(len(self.noc.links['5']), 4)
        self.assertEqual(len(self.noc.links['2']), 3)

    def test_links_default_utilization_rate(self):
        self.noc.link_array_filling()
        self.assertEqual(self.noc.links['1']['2'], 0)


class TestRouter(unittest.TestCase):

    def setUp(self):
        self.noc = NoC("Network-On-Chip", 4, 4, 12, [1, 1, 1, 1])

        self.proc_engine = self.noc.router_matrix[0][0].proc_engine
        self.router = self.noc.router_matrix[0][0]

    def test_inport_vcs(self):
        self.assertEqual(self.noc.router_matrix[3][3].inNorth.nbvc, 4)
        self.assertEqual(self.noc.router_matrix[3][3].inNorth.vc_size, 12)
        self.assertEqual(len(self.noc.router_matrix[3][3].inNorth.vcs[0].flits), 0)

    def test_idle_lock_vc(self):
        allotted_vc = self.router.inPE.vc_allocator()
        self.assertIsNotNone(allotted_vc)
        self.assertEqual(self.router.inPE.number_idle_vc(), 3)
        allotted_vc = self.router.inPE.vc_allocator()
        self.assertEqual(self.router.inPE.number_idle_vc(), 2)
        allotted_vc = self.router.inPE.vc_allocator()
        self.assertEqual(self.router.inPE.number_idle_vc(), 1)
        allotted_vc = self.router.inPE.vc_allocator()
        self.assertEqual(self.router.inPE.number_idle_vc(), 0)
        allotted_vc = self.router.inPE.vc_allocator()
        self.assertIsNone(allotted_vc)


class TestRouting(unittest.TestCase):

    def setUp(self):
        self.noc = NoC("Network-On-Chip", 4, 4, 12, [1, 1, 1, 1])

        self.src = Coordinate(0, 0)
        self.dest = Coordinate(2, 2)
        self.message = Message(1, 23, 256, 0, 0, self.src, self.dest)
        self.packet = Packet(1, self.dest, self.message)

        self.flit = self.packet.flits[0]

        self.proc_engine = self.noc.router_matrix[0][0].proc_engine
        self.router = self.noc.router_matrix[0][0]

    def test_proc_engine_to_router(self):
        packets = self.message.packets
        allotted_vc = self.router.inPE.vc_allocator()

        self.assertEqual(len(packets[0].flits), 32)

        self.proc_engine.send_packet(packets[0], allotted_vc)

        self.assertEqual(len(allotted_vc.flits), 32)
        self.assertTrue(allotted_vc.lock)

    def test_xy_routing_output(self):
        self.router = self.noc.router_matrix[2][2]
        dest1 = Coordinate(1, 2)
        dest2 = Coordinate(3, 2)
        dest3 = Coordinate(0, 3)
        dest4 = Coordinate(0, 0)
        dest5 = Coordinate(2, 2)

        self.flit.set_destination_info(dest1)
        self.assertEqual(self.router.route_computation(self.flit), self.router.outNorth)
        self.flit.set_destination_info(dest2)
        self.assertEqual(self.router.route_computation(self.flit), self.router.outSouth)
        self.flit.set_destination_info(dest3)
        self.assertEqual(self.router.route_computation(self.flit), self.router.outEast)
        self.flit.set_destination_info(dest4)
        self.assertEqual(self.router.route_computation(self.flit), self.router.outWest)
        self.flit.set_destination_info(dest5)
        self.assertEqual(self.router.route_computation(self.flit), self.router.outPE)

    def test_vc_target_output(self):
        self.router = self.noc.router_matrix[2][2]
        dest1 = Coordinate(1, 2)
        dest4 = Coordinate(0, 0)

        # North
        vc_north = self.router.inNorth.vcs[0]
        vc_north1 = self.router.inNorth.vcs[1]

        self.flit.set_destination_info(dest1)
        vc_north.flits.append(self.flit)
        self.router.vc_target_outport(vc_north)

        self.assertEqual(len(self.router.vcs_target_north), 1)

        vc_north1.flits.append(self.flit)
        self.router.vc_target_outport(vc_north1)
        self.assertEqual(len(self.router.vcs_target_north), 2)

        # West
        vc_west = self.router.inWest.vcs[0]

        self.flit.set_destination_info(dest4)
        vc_west.flits.append(self.flit)
        self.router.vc_target_outport(vc_west)

        self.assertEqual(len(self.router.vcs_target_west), 1)


class TestNode(unittest.TestCase):

    def setUp(self):
        self.nodeArray = NodeArray()
        self.vc_src = VirtualChannel(1, Direction.east, None, 1, 1)
        self.vc_target = VirtualChannel(1, Direction.east, None, 1, 1)

    def test_add(self):
        node = Node(self.vc_src, self.vc_target)
        self.nodeArray.add(node)

        self.assertEqual(len(self.nodeArray.array), 1)

        node2 = Node(self.vc_src, self.vc_target)
        self.nodeArray.add(node2)

        self.assertEqual(len(self.nodeArray.array), 2)

    def test_remove(self):
        node = Node(self.vc_src, self.vc_target)
        self.nodeArray.add(node)
        node2 = Node(self.vc_src, self.vc_target)
        self.nodeArray.add(node2)

        self.nodeArray.remove(self.vc_src)
        self.assertEqual(len(self.nodeArray.array), 1)

        self.nodeArray.remove(self.vc_src)
        self.assertEqual(len(self.nodeArray.array), 0)

    def test_get_target(self):
        node = Node(self.vc_src, self.vc_target)
        self.nodeArray.add(node)

        self.assertEqual(self.nodeArray.get_target(self.vc_src), self.vc_target)

        self.nodeArray.remove(self.vc_src)

        self.assertIsNone(self.nodeArray.get_target(self.vc_src))


class TestConflictByAxe(unittest.TestCase):
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
        self.generation.set_noc(self.noc)
        self.generation.set_square_size(4)

        self.noc.link_array_filling()

    def test_xy_path_coordinate(self):
        link_array = self.message.get_xy_path_coordinate(self.noc)
        self.assertEqual(len(link_array), 4)
        self.assertEqual(link_array[0][0], 1)
        self.assertEqual(link_array[0][1], 2)
        self.assertEqual(link_array[3][0], 7)
        self.assertEqual(link_array[3][1], 11)

    def test_find_links_outside_interval(self):
        link_array = self.message.get_xy_path_coordinate(self.noc)

        outside_link = self.generation.find_links_outside_interval(link_array, 70, 30, 0)
        self.assertEqual(len(outside_link), 4)

        self.generation.add_utilization_rate_to_link(outside_link[0], 50)
        new_outside_link = self.generation.find_links_outside_interval(link_array, 70, 30, 0)
        self.assertEqual(len(new_outside_link), 4)

    def test_get_link_direction(self):
        link_array = self.message.get_xy_path_coordinate(self.noc)
        link = link_array.pop()

        self.assertEqual(self.generation.get_link_direction(link), 0)

    def test_task_communication_axe(self):
        link_array = self.message.get_xy_path_coordinate(self.noc)

        router_src = self.noc.get_router_coordinate_by_id(link_array[0][0])
        router_dest = self.noc.get_router_coordinate_by_id(link_array[0][1])

        router_src_1 = self.noc.get_router_coordinate_by_id(link_array[3][0])
        router_dest_1 = self.noc.get_router_coordinate_by_id(link_array[3][1])

        axe = (0 if router_src.i == router_dest.i else 1)
        self.assertEqual(axe, 0)
        axe = (0 if router_src_1.i == router_dest_1.i else 1)
        self.assertEqual(axe, 1)

    def test_generate_conflict_task_by_axe(self):
        link_array = self.message.get_xy_path_coordinate(self.noc)
        link = link_array.pop()

        router_src = self.noc.get_router_coordinate_by_id(link[0])
        router_dest = self.noc.get_router_coordinate_by_id(link[1])

        axe = (0 if router_src.i == router_dest.i else 1)

        conflict_task = self.generation.generate_conflict_task_by_axe([router_src, router_dest],
                                                                      link,
                                                                      axe,
                                                                      50,
                                                                      0)
        # conflict task generated by the above function has the following characteristics
        # from -> to : (0,0) -> (0,1) -> (0,2) -> (0,3) : 3 links
        # has a link utilization < 30
        self.assertEqual(len(conflict_task.get_xy_path_coordinate(self.noc)), 3)
        self.assertLessEqual(conflict_task.get_link_utilization(), 0.3)

    def test_conflict_task_by_axe(self):
        self.src = Coordinate(2, 3)
        self.dest = Coordinate(3, 0)
        self.message = Message(1, 12, 256, 0, 0, self.src, self.dest)

        self.generation.conflict_task_by_axe(self.message, 70, 40, 0)

        print('==========> %d' % len(self.generation.messages))


if __name__ == '__main__':
    unittest.main()
