from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from constants import Cells


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
        self.set_texture(Cells.Textures[type(self.cell)])
        self.show()

    def set_texture(self, texture):
        self.img_source = texture
        self.img = QPixmap(self.img_source)
        self.label = QLabel()
        self.label.setPixmap(self.img.scaled(self.father.cell_size,
                                             self.father.cell_size))
        self.label.setParent(self)
        self.label.show()
