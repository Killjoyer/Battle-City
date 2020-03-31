from cells import BrickWall, EmptyCell, WoodenCrate, PoisonousMist


class Field:
    Cells = {
        ' ': lambda: EmptyCell(),
        '#': lambda: BrickWall(),
        'x': lambda: WoodenCrate(),
        'm': lambda: PoisonousMist(),
    }

    def __init__(self, start_position: list):
        self.width = len(start_position[0])
        self.height = len(start_position)
        self.level = self.read_level(start_position)

    def read_level(self, start_position):
        return [[Field.Cells[start_position[i][j]]()
                 for j in range(self.width)]
                for i in range(self.height)]
