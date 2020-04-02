from constants import Cells


class Field:
    def __init__(self, start_position: list):
        self.width = len(start_position[0]) + 2
        self.height = len(start_position) + 2
        self.player_pos = (0, 0)
        self.level = self.read_level(start_position)

    def read_level(self, start_position):
        field = [[Cells.Cells['#'](0, 0) for i in range(self.width)]]
        for i in range(1, self.height - 1):
            field.append(
                [Cells.Cells['#'](0, 0)] + [''] * (self.width - 2) + [
                    Cells.Cells['#'](0, 0)])
            for j in range(1, self.width - 1):
                field[i][j] = Cells.Cells[start_position[i - 1][j - 1]](j, i)
                if field[i][j].active_ground is not None:
                    self.player_pos = (i, j)
        field.append([Cells.Cells['#'](0, 0) for i in range(self.width)])
        return field
