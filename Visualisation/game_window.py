from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QKeyEvent, QIcon
from PyQt5.QtWidgets import QMainWindow

from Visualisation.cell_visualisation import CellVisualisation
from cells import EmptyCell
from constants import MovingWills, Cells, WindowSettings
from tank import TankOwner
from Visualisation.tank_visualisation import TankVisualisation


class GameWindow(QMainWindow):
    def __init__(self, game):
        super().__init__()
        self.setWindowIcon(QIcon(WindowSettings.IcoSource))
        self.setWindowTitle(WindowSettings.Title)
        self.cell_size = Cells.CellSize
        self.game = game
        self.field = []
        self.overlaying = []
        self.underlaying = []
        for i in range(self.game.field.height):
            self.field.append([0] * self.game.field.width)
            for j in range(self.game.field.width):
                if self.game.field.level[i][j].overlays:
                    print('found 1 overlaying')
                    self.overlaying.append((self.game.field.level[i][j], j, i))
                    self.underlaying.append(CellVisualisation(self,
                                                              EmptyCell(),
                                                              j, i))
                    continue
                self.field[i][j] = CellVisualisation(self, self.game.field.level[i][j], j, i)
        self.setGeometry(300, 100,
                         game.field.width * self.cell_size,
                         game.field.height * self.cell_size)
        self.tanks = {}
        for owner, tank in game.tanks.items():
            self.tanks[owner] = TankVisualisation(self, tank)
        for i in self.overlaying:

            self.field[i[2]][i[1]] = CellVisualisation(self, *i)
        self.show()
        self.timer = QTimer()
        self.timer.setInterval(WindowSettings.TimerInterval)
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
        if key == Qt.Key_W:
            if self.tanks[TankOwner.Human].moving_will == MovingWills.Backward:
                self.tanks[TankOwner.Human].ticks = 0
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
            if self.tanks[TankOwner.Human].moving_will == MovingWills.Forward:
                self.tanks[TankOwner.Human].ticks = 0
            self.tanks[TankOwner.Human].moving_will = MovingWills.Backward
            self.tanks[TankOwner.Human].moves = True
        elif key == Qt.Key_Space:
            self.tanks[TankOwner.Human].tank.shoot()

    def keyReleaseEvent(self, e: QKeyEvent):
        key = e.key()
        if key == Qt.Key_W or key == Qt.Key_S:
            self.tanks[TankOwner.Human].moves = False
