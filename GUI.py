import os

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QKeyEvent, QPixmap, QTransform
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel

from tank import *


class MovingWills:
    Nowhere = 0
    Forward = 1
    Backward = -1


class GameWindow(QMainWindow):
    def __init__(self, game):
        super().__init__()
        self.cellSize = 32
        self.game = game
        self.setGeometry(300, 100,
                         game.field.width * self.cellSize,
                         game.field.height * self.cellSize)
        self.tanks = {}
        self.moving_wills = {}
        for owner, tank in game.tanks.items():
            self.tanks[owner] = TankVisualisation(self, tank)
            self.moving_wills[owner] = MovingWills.Nowhere
        self.setStyleSheet("""background-color: #ffffff;""")
        self.show()
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.game_update)
        self.timer.start()

    def game_update(self):
        for owner, tank in self.tanks.items():
            # tank.move(tank.tank.x * self.cellSize, tank.tank.y * self.cellSize)
            if (tank.tank.x != tank.actual_x // self.cellSize or
                    tank.tank.y != tank.actual_y // self.cellSize):
                tank.actual_x += (self.moving_wills[owner] *
                                  tank.tank.speed * tank.tank.direction[0])
                tank.actual_y += (self.moving_wills[owner] *
                                  tank.tank.speed * tank.tank.direction[1])
                tank.move(tank.actual_x, tank.actual_y)
            else:
                self.moving_wills[owner] = MovingWills.Nowhere
            tank.turn()

    def keyPressEvent(self, e: QKeyEvent):
        key = e.key()
        if key == Qt.Key_W:
            print('W pressed')
            self.game.tanks[TankOwner.Human].move_forward(self.game.field)
            self.moving_wills[TankOwner.Human] = MovingWills.Forward
            print(self.tanks[TankOwner.Human].actual_x // 32,
                  self.game.tanks[TankOwner.Human].x)
        elif key == Qt.Key_D:
            print('D pressed')
            if self.moving_wills[TankOwner.Human] != MovingWills.Nowhere:
                return
            self.game.tanks[TankOwner.Human].turn_right()
        elif key == Qt.Key_A:
            print('A pressed')
            if self.moving_wills[TankOwner.Human] != MovingWills.Nowhere:
                return
            self.game.tanks[TankOwner.Human].turn_left()
        elif key == Qt.Key_S:
            print('S pressed')
            self.moving_wills[TankOwner.Human] = MovingWills.Backward
            self.game.tanks[TankOwner.Human].move_backward()


class TankVisualisation(QWidget):
    def __init__(self, father: GameWindow, tank: Tank):
        super().__init__()
        self.tank = tank
        self.father = father
        self.actual_x = tank.x * father.cellSize
        self.actual_y = tank.y * father.cellSize
        self.angle = 0
        self.q_trans = QTransform().rotate(self.angle)
        self.setParent(father)
        self.setGeometry(self.actual_x, self.actual_y,
                         father.cellSize, father.cellSize)
        self.img_source = os.path.join('Resources', 'green_tank.png')
        self.img = QPixmap(self.img_source)
        self.label = QLabel()
        self.label.setPixmap(self.img.transformed(self.q_trans))
        self.label.setParent(self)
        self.show()

    def turn(self):
        self.angle = (self.angle + 90) % 360
        if self.tank.direction == Direction.Up:
            self.angle = 0
        elif self.tank.direction == Direction.Down:
            self.angle = 180
        elif self.tank.direction == Direction.Right:
            self.angle = 90
        else:
            self.angle = 270
        self.q_trans = QTransform().rotate(self.angle)
        self.img = QPixmap(self.img_source).transformed(self.q_trans)
        self.label.setPixmap(self.img)