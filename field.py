from constants import Cells


class Field:
    def __init__(self, start_position: list):
        self.width = len(start_position[0]) + 2
        self.height = len(start_position) + 2
        self.player_pos = (0, 0)
        self.second_player_pos = (-1, -1)
        self.enemies = []
        self.level = self.read_level(start_position)

    def read_level(self, start_position):
        field = [[Cells.Cells['#']() for i in range(self.width)]]
        for i in range(1, self.height - 1):
            field.append([Cells.Cells['#']()] + [''] * (self.width - 2) +
                         [Cells.Cells['#']()])
            for j in range(1, self.width - 1):
                if start_position[i - 1][j - 1] == 'P':
                    self.player_pos = (j, i)
                if start_position[i - 1][j - 1] == 'S':
                    self.second_player_pos = (j, i)
                if (start_position[i - 1][j - 1] in
                        Cells.GeneratingTypes.keys()):
                    self.enemies.append((j, i,
                                         Cells.GeneratingTypes[
                                             start_position[i - 1][j - 1]]))
                field[i][j] = Cells.Cells[start_position[i - 1][j - 1]]()
        field.append([Cells.Cells['#']() for i in range(self.width)])
        return field
