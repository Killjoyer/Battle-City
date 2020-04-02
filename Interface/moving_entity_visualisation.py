from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtWidgets import QWidget, QLabel

from constants import Cells, Direction, MovingWills
from moving_enity import MovingEntity


class MovingEntityVisualisation(QWidget):
    def __init__(self, father, wrapping_object: MovingEntity, texture: str):
        super().__init__()
        self.setParent(father)
        self.x = wrapping_object.x * father.cell_size
        self.y = wrapping_object.y * father.cell_size
        self.tick_mod = Cells.CellSize // wrapping_object.speed
        self.ticks = 0
        self.father = father
        self.angle = 0
        self.q_trans = None
        self.screen_x = wrapping_object.x * father.cell_size
        self.screen_y = wrapping_object.y * father.cell_size
        self.moves = False
        self.moving_will = MovingWills.Nowhere
        self.wrapping_object = wrapping_object
        self.setGeometry(self.screen_x, self.screen_y,
                         father.cell_size, father.cell_size)
        self.label = QLabel()
        self.img = None
        self.set_texture(texture)
        self.adjust_direction()
        self.show()

    def set_texture(self, texture):
        self.img = QPixmap(texture).scaled(self.father.cell_size,
                                           self.father.cell_size)
        self.label.setPixmap(self.img)
        self.label.setParent(self)
        self.label.show()

    def adjust_direction(self):
        if self.wrapping_object.direction == Direction.Up:
            self.angle = 0
        elif self.wrapping_object.direction == Direction.Down:
            self.angle = 180
        elif self.wrapping_object.direction == Direction.Right:
            self.angle = 90
        else:
            self.angle = 270
        self.q_trans = QTransform().rotate(self.angle)
        self.label.setPixmap(self.img.transformed(self.q_trans))

    def update_position(self):
        try:
            if self.ticks == 0 and self.moves:
                self.wrapping_object.move(self.father.game.field, self.moving_will)
            if (abs(self.wrapping_object.x -
                    self.screen_x / self.father.cell_size) > 1e-8 or
                    abs(self.wrapping_object.y -
                        self.screen_y / self.father.cell_size) > 1e-8):
                self.screen_x += (self.moving_will *
                                  self.wrapping_object.speed *
                                  self.wrapping_object.direction[0])
                self.screen_y += (self.moving_will *
                                  self.wrapping_object.speed *
                                  self.wrapping_object.direction[1])
                self.move(self.screen_x, self.screen_y)
                self.ticks = (self.ticks + 1) % self.tick_mod
            else:
                self.ticks = 0
                self.moving_will = MovingWills.Nowhere
            self.adjust_direction()
        except Exception as e:
            print(e)
