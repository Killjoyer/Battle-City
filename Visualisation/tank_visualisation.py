from PyQt5.QtGui import QTransform, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from constants import Cells, MovingWills, TankTextures, Direction
from tank import Tank


class TankVisualisation(QWidget):
    def __init__(self, father, tank: Tank):
        super().__init__()
        self.tank = tank
        self.tick_mod = Cells.CellSize // tank.speed
        self.ticks = 0
        self.father = father
        self.actual_x = tank.x * father.cell_size
        self.actual_y = tank.y * father.cell_size
        self.moves = False
        self.moving_will = MovingWills.Nowhere
        self.angle = 0
        self.q_trans = QTransform().rotate(self.angle)
        self.setParent(father)
        self.setGeometry(self.actual_x, self.actual_y,
                         father.cell_size, father.cell_size)
        self.img_source = TankTextures.Textures[tank.type](tank.owner)
        self.img = QPixmap(self.img_source).scaled(father.cell_size,
                                                   father.cell_size)
        self.label = QLabel()
        self.label.setPixmap(self.img
                             .transformed(self.q_trans))
        self.label.setParent(self)
        self.show()

    def turn(self):
        if self.tank.direction == Direction.Up:
            self.angle = 0
        elif self.tank.direction == Direction.Down:
            self.angle = 180
        elif self.tank.direction == Direction.Right:
            self.angle = 90
        else:
            self.angle = 270
        self.q_trans = QTransform().rotate(self.angle)
        self.label.setPixmap(self.img.transformed(self.q_trans))
