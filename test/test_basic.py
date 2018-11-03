import unittest
from communication.structure import Packet


class TestPacket(unittest.TestCase):

    def test_flit_number(self):
        packet = Packet(1, 128)


if __name__ == '__main__':
    unittest.main()
