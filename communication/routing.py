import enum


class Direction(enum.Enum):
    north = 1
    south = 2
    east = 3
    west = 4


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
