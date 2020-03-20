from enum import Enum


class CellType(Enum):
    BrickWall = '#'
    WoodenWall = '='
    Space = ' '
    Bushes = '@'
    StoneWall = '$'


class Cell:
    def __init__(self, cell_type: CellType):
        self.type = cell_type
