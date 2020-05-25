from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from bonus import Bonus
from constants import Bonuses, Cells


class BonusVisualisation(QWidget):
    def __init__(self, father, bonus: Bonus):
        super().__init__()
        self.x = bonus.x * Cells.CellSize
        self.y = bonus.y * Cells.CellSize
        self.bonus = bonus
        self.setParent(father)
        self.setGeometry(self.x, self.y, Cells.CellSize, Cells.CellSize)
        self.label = QLabel(self)
        self.img = QPixmap(Bonuses.Texture[bonus.name]).scaled(Cells.CellSize,
                                                               Cells.CellSize)
        self.label.setPixmap(self.img)
        self.label.show()
        self.show()
