from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QKeyEvent, QPixmap, QTransform, QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel

from constants import Direction, MovingWills, Cells, TankTextures, \
    WindowSettings
from tank import TankOwner, Tank


class GameWindow(QMainWindow):
    def __init__(self, game):
        super().__init__()
        self.setWindowIcon(QIcon(WindowSettings.IcoSource))
        self.setWindowTitle(WindowSettings.Title)
        self.cell_size = Cells.CellSize
        self.game = game
        self.field = [
            [CellVisualisation(self, game.field.level[i][j], j, i) for j in
             range(self.game.field.width)] for i in range(game.field.height)]
        self.setGeometry(300, 100,
                         game.field.width * self.cell_size,
                         game.field.height * self.cell_size)
        self.tanks = {}
        for owner, tank in game.tanks.items():
            self.tanks[owner] = TankVisualisation(self, tank)
        self.show()
        self.timer = QTimer()
        self.timer.setInterval(WindowSettings.TimerInteerval)
        self.timer.timeout.connect(self.game_update)
        self.timer.start()
        self.paused = 0

    def game_update(self):
        for owner, tank in self.tanks.items():
            if tank.ticks == 1:
                print(f'logically x:{tank.tank.x} y:{tank.tank.y}',
                      f'on screen x:{tank.actual_x} y:{tank.actual_y}',
                      sep='\n')
            if tank.ticks == 0 and tank.moves:
                tank.tank.move(self.game.field, tank.moving_will)
            if (abs(tank.tank.x - tank.actual_x / self.cell_size) > 1e-8 or
                    abs(tank.tank.y - tank.actual_y / self.cell_size) > 1e-8):
                # print(tank.ticks)
                tank.actual_x += (tank.moving_will *
                                  tank.tank.speed * tank.tank.direction[0])
                tank.actual_y += (tank.moving_will *
                                  tank.tank.speed * tank.tank.direction[1])
                tank.move(tank.actual_x, tank.actual_y)
                tank.ticks = (tank.ticks + 1) % tank.tick_mod
            else:
                tank.ticks = 0
                tank.moving_will = MovingWills.Nowhere
            tank.turn()

    def keyPressEvent(self, e: QKeyEvent):
        key = e.key()
        if key == Qt.Key_Escape:
            self.paused = (self.paused + 1) % 2
            if self.paused:
                self.timer.stop()
                return
            else:
                self.timer.start()
        elif key == Qt.Key_W:
            self.tanks[TankOwner.Human].moves = True
            self.tanks[TankOwner.Human].moving_will = MovingWills.Forward
        elif key == Qt.Key_D:
            if self.tanks[TankOwner.Human].moving_will != MovingWills.Nowhere:
                return
            self.game.tanks[TankOwner.Human].turn_right()
        elif key == Qt.Key_A:
            if self.tanks[TankOwner.Human].moving_will != MovingWills.Nowhere:
                return
            self.game.tanks[TankOwner.Human].turn_left()
        elif key == Qt.Key_S:
            self.tanks[TankOwner.Human].moving_will = MovingWills.Backward
            self.tanks[TankOwner.Human].moves = True

    def keyReleaseEvent(self, e: QKeyEvent):
        key = e.key()
        if key == Qt.Key_W or key == Qt.Key_S:
            self.tanks[TankOwner.Human].moves = False


class TankVisualisation(QWidget):
    def __init__(self, father: GameWindow, tank: Tank):
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
        # BRANCH "FIXING MOVEMENT"
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


class CellVisualisation(QWidget):
    def __init__(self, father: GameWindow, cell, x, y):
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
