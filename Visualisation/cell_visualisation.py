from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from constants import Cells


class CellVisualisation(QWidget):
    def __init__(self, father, cell, x, y):
        super().__init__()
        self.setParent(father)
        self.cell = cell
        self.x = x * father.cell_size
        self.y = y * father.cell_size
        self.move(self.x, self.y)
        self.img = ''
        self.label = QLabel()
        self.label.setParent(self)
        self.img_source = Cells.Textures[type(cell)]
        self.set_texture(self.img_source)
        self.show()

    def set_texture(self, texture):
        self.img = QPixmap(texture)
        self.label.setPixmap(self.img
                             .scaled(self.parent().cell_size,
                                     self.parent().cell_size))


class DestructibleCellVisualisation(CellVisualisation):
    def __init__(self, father, cell, x, y):
        super().__init__(father, cell, x, y)

    def update_texture(self):
        if self.cell.is_dead:
            self.hide()
        elif self.cell.health <= 15:
            self.set_texture(Cells.Destruction[type(self.cell)][2])
            print('3')
        elif self.cell.health <= 30:
            print('2')
            self.set_texture(Cells.Destruction[type(self.cell)][1])
        elif self.cell.health <= 40:
            print('1')
            self.set_texture(Cells.Destruction[type(self.cell)][0])

