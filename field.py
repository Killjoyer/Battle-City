from cells import BrickWall, EmptyCell


class Field:
    Cells = {
        ' ': lambda: EmptyCell(),
        '#': lambda: BrickWall(),
    }

    def __init__(self, width: int, height: int, start_position: list):
        self.width = width
        self.height = height
        self.level = self.read_level(start_position)

    def read_level(self, start_position):
        return [[Field.Cells[start_position[i][j]]() for j in range(self.width)]
                for i in range(self.height)]
