import enum


class Direction(enum.Enum):
    north = 'North'
    south = 'South'
    east = 'East'
    west = 'West'
    pe = 'PE'


class Coordinate:
    def __init__(self, i, j):
        self.i = i  # Row
        self.j = j  # Column
        self.link_utilization = 0

    def __str__(self):
        return 'R(%d,%d)' % (self.i, self.j)

    def add_link_utilization(self, value):
        self.link_utilization += value
