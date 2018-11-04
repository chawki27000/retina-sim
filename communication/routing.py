import enum


class Direction(enum.Enum):
    north = 1
    south = 2
    east = 3
    west = 4
    pe = 5


class Coordinate:
    def __init__(self, i, j):
        self.i = i  # Row
        self.j = j  # Column
