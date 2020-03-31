from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from constants import Cells


class CellVisualisation(QWidget):
    def __init__(self, father, cell, x, y):
        super().__init__()
        self.setParent(father)
        self.x = x * father.cell_size
        self.y = y * father.cell_size
        self.move(self.x, self.y)
        self.img_source = Cells.Textures[type(cell)]
        self.img = QPixmap(self.img_source)
        self.label = QLabel()
        self.label.setPixmap(self.img
                             .scaled(father.cell_size, father.cell_size))
        self.label.setParent(self)
        self.show()