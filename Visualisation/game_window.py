from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QKeyEvent, QIcon
from PyQt5.QtWidgets import QMainWindow

from Visualisation.bonus_visualisation import BonusVisualisation
from Visualisation.cell_visualisation import CellVisualisation
from Visualisation.cell_visualisation import DestructibleCellVisualisation
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
            self.field[i[2]][i[1]] = DestructibleCellVisualisation(self, *i)
        self.show()
        self.timer = QTimer()
        self.timer.setInterval(WindowSettings.TimerInterval)
        self.timer.timeout.connect(self.game_update)
        self.timer.start()
        self.paused = 0
        self.bullets = set()
        self.drawn_bonuses = {}

    def game_update(self):
        try:
            if len(self.game.enemies) == 0: self.win_game()
            if len(self.game.tanks) == 0: self.loose_game()
            self.update_bullets()
            self.update_bonuses()
            self.game.decide_to_spawn_bonus()
            for owner, tank in self.tanks.items():
                self.update_tank(tank)
                if tank.wrapping_object.is_dead:
                    self.tanks.pop(tank)
                    tank.hide()
                    continue
            for tank in self.enemies:
                self.update_tank(tank)
                tank.shoot()
                if tank.wrapping_object.is_dead:
                    self.enemies.remove(tank)
                    tank.hide()
                    continue
        except Exception as e:
            print(e)

    def update_tank(self, tank):
        if tank.is_shooting:
            tank.shoot()
        tank.update_bars()
        tank.treat_debuffs()
        tank.update_position()

    def update_bonuses(self):
        for bonus in self.game.active_bonuses:
            if bonus not in self.drawn_bonuses.keys():
                self.drawn_bonuses[bonus] = BonusVisualisation(self, bonus)
        for bonus in self.drawn_bonuses.values():
            if bonus.bonus.is_dead:
                bonus.hide()
                self.drawn_bonuses.pop(bonus.bonus)

    def update_bullets(self):
        for bullet in self.bullets:
            col = bullet.update_position()
            if bullet.wrapping_object.is_dead:
                if col and col[0] == 'destr_cell':
                    self.field[col[2]][col[1]].update_texture()
                bullet.hide()
                self.bullets.remove(bullet)

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
            self.tanks[TankOwner.Human].is_shooting = True

    def keyReleaseEvent(self, e: QKeyEvent):
        key = e.key()
        if key == Qt.Key_W or key == Qt.Key_S:
            self.tanks[TankOwner.Human].moves = False
        elif key == Qt.Key_Space:
            self.tanks[TankOwner.Human].is_shooting = False

    def win_game(self):
        print('u won')

    def loose_game(self):
        self.hide()
        
