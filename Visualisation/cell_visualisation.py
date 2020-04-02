from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from Visualisation.tank_visualisation import TankVisualisation
from constants import Cells


class FieldCellVisualisation:
    def __init__(self, father, cell, x, y):
        self.back_ground = CellVisualisation(father, cell.back_ground, x, y)
        self.active_ground = lambda: TankVisualisation(father,
                                                       cell.active_ground)
        self.fore_ground = CellVisualisation(father, cell.fore_ground, x, y)


class CellVisualisation(QWidget):
    def __init__(self, father, cell, x, y):
        super().__init__()
        self.father = father
        self.setParent(father)
        self.x = x * father.cell_size
        self.y = y * father.cell_size
        self.move(self.x, self.y)
        self.cell = cell
        self.label = ''
        self.img = ''
        self.img_source = ''
        self.show()

    def set_texture(self):
        self.img_source = Cells.Textures[type(self.cell)]
        self.img = QPixmap(self.img_source)
        self.label = QLabel()
        self.label.setPixmap(self.img.scaled(self.father.cell_size,
                                             self.father.cell_size))
        self.label.setParent(self)
        self.label.show()
