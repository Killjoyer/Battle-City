from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QKeyEvent, QIcon
from PyQt5.QtWidgets import QMainWindow

from Visualisation.cell_visualisation import CellVisualisation
from Visualisation.tank_visualisation import TankVisualisation
from cells import EmptyCell
from constants import MovingWills, Cells, WindowSettings
from tank import TankOwner


class GameWindow(QMainWindow):
    def __init__(self, game):
        super().__init__()
        self.setWindowIcon(QIcon(WindowSettings.IcoSource))
        self.setWindowTitle(WindowSettings.Title)
        self.cell_size = Cells.CellSize
        self.game = game
        self.field = [[0] * (self.game.field.width + 2)]
        self.overlaying = []
        self.underlaying = []
        for i in range(0, self.game.field.height):
            self.field.append([0] * self.game.field.width)
            for j in range(0, self.game.field.width):
                if self.game.field.level[i][j].overlays:
                    self.overlaying.append((self.game.field.level[i][j], j, i))
                    self.underlaying.append(
                        CellVisualisation(self, EmptyCell(), j, i)
                    )
                    continue
                self.field[i][j] = \
                    CellVisualisation(self, self.game.field.level[i][j], j, i)
        self.setGeometry(300, 100, 1, 1)
        self.setFixedSize(game.field.width * self.cell_size,
                          game.field.height * self.cell_size)
        self.tanks = {}
        self.enemies = []
        for owner, tank in game.tanks.items():
            self.tanks[owner] = TankVisualisation(self, tank)
        for tank in game.enemies:
            self.enemies.append(TankVisualisation(self, tank))
        for i in self.overlaying:
            self.field[i[2]][i[1]] = CellVisualisation(self, *i)
        self.show()
        self.timer = QTimer()
        self.timer.setInterval(WindowSettings.TimerInterval)
        self.timer.timeout.connect(self.game_update)
        self.timer.start()
        self.paused = 0

    def game_update(self):
        try:
            for owner, tank in self.tanks.items():
                tank.update_position()
                if tank.wrapping_object.is_dead:
                    self.tanks.pop(tank)
                    tank.hide()
                    continue
                for bullet in tank.bullets:
                    if bullet.wrapping_object.is_dead:
                        tank.bullets.remove(bullet)
                        bullet.hide()
                    bullet.update_position()
            for tank in self.enemies:
                if tank.wrapping_object.is_dead:
                    self.enemies.remove(tank)
                    tank.hide()
                    continue
                tank.update_position()
                for bullet in tank.bullets:
                    if bullet.wrapping_object.is_dead:
                        tank.bullets.remove(bullet)
                        bullet.hide()
                    bullet.update_position()
        except Exception as e:
            print(e)

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
            self.tanks[TankOwner.Human].shoot()

    def keyReleaseEvent(self, e: QKeyEvent):
        key = e.key()
        if key == Qt.Key_W or key == Qt.Key_S:
            self.tanks[TankOwner.Human].moves = False
