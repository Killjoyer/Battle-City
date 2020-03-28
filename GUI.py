import os

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QKeyEvent, QPixmap, QTransform
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel

from cells import EmptyCell, BrickWall
from direction import Direction
from tank import TankOwner, Tank


class MovingWills:
    Nowhere = 0
    Forward = 1
    Backward = -1


class GameWindow(QMainWindow):
    def __init__(self, game):
        super().__init__()
        self.cell_size = 32
        self.game = game
        self.field = [
            [CellVisualisation(self, game.field.level[i][j], i, j) for j in
             range(self.game.field.width)] for i in range(game.field.height)]
        self.setGeometry(300, 100,
                         game.field.width * self.cell_size,
                         game.field.height * self.cell_size)
        self.tanks = {}
        self.moving_wills = {}
        for owner, tank in game.tanks.items():
            self.tanks[owner] = TankVisualisation(self, tank)
            self.moving_wills[owner] = MovingWills.Nowhere
        self.show()
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.game_update)
        self.timer.start()

    def game_update(self):
        for owner, tank in self.tanks.items():
            if (abs(tank.tank.x - tank.actual_x / self.cell_size) > 1e-8 or
                    abs(tank.tank.y - tank.actual_y / self.cell_size) > 1e-8):
                tank.actual_x += (self.moving_wills[owner] *
                                  tank.tank.speed * tank.tank.direction[0])
                tank.actual_y += (self.moving_wills[owner] *
                                  tank.tank.speed * tank.tank.direction[1])
                print(f'X - {tank.actual_x}, {tank.tank.x}\n',
                      f'Y - {tank.actual_y}, {tank.tank.y}', sep='')
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
            self.game.tanks[TankOwner.Human].move_backward(self.game.field)


class TankVisualisation(QWidget):
    def __init__(self, father: GameWindow, tank: Tank):
        super().__init__()
        self.tank = tank
        self.father = father
        self.actual_x = tank.x * father.cell_size
        self.actual_y = tank.y * father.cell_size
        self.angle = 0
        self.q_trans = QTransform().rotate(self.angle)
        self.setParent(father)
        self.setGeometry(self.actual_x, self.actual_y,
                         father.cell_size, father.cell_size)
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


class CellVisualisation(QWidget):
    Textures = {
        type(BrickWall()): os.path.join('Resources', 'brick_wall.png'),
        type(EmptyCell()): os.path.join('Resources', 'empty_cell.png'),
    }

    def __init__(self, father: GameWindow, cell, y, x):
        super().__init__()
        self.setParent(father)
        self.x = x * father.cell_size
        self.y = y * father.cell_size
        self.move(self.x, self.y)
        self.img_source = CellVisualisation.Textures[type(cell)]
        self.img = QPixmap(self.img_source)
        self.label = QLabel()
        self.label.setPixmap(self.img)
        self.label.setParent(self)
        self.show()
