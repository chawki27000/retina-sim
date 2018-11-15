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
