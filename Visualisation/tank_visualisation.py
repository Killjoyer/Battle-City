from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QLabel

from Visualisation.bullet_visualisation import BulletVisualisation
from Visualisation.moving_entity_visualisation import MovingEntityVisualisation
from constants import TankTextures, Cells
from tank import Tank


class TankVisualisation(MovingEntityVisualisation):
    def __init__(self, father, tank: Tank):
        super().__init__(father, tank,
                         TankTextures.Textures[tank.type](tank.owner))
        self.bullets = set()
        self.can_shoot = True
        self.shooting_cd = QTimer()
        self.shooting_cd.setInterval(self.wrapping_object.cooldown * 250)
        self.shooting_cd.timeout.connect(self._drop_cd)
        self.show()
        self.bars = [HealthBar(self), CoolDownBar(self)]

    def update_bars(self):
        for bar in self.bars:
            bar.update_param()

    def _drop_cd(self):
        self.can_shoot = True
        self.shooting_cd.stop()

    def shoot(self):
        if self.can_shoot:
            bullet = BulletVisualisation(self.father,
                                         self.wrapping_object.shoot())
            bullet.stackUnder(self)
            self.bullets.add(bullet)
            self.can_shoot = False
            self.shooting_cd.start()


class Bar(QWidget):
    def __init__(self, tank, color, param, x, y, h):
        super().__init__()
        self.setParent(tank)
        self.tank = tank
        self.param = param
        self.label = QLabel()
        self.height = h
        self.label.move(x, y)
        self.label.resize(Cells.CellSize, h)
        self.label.setParent(self)
        self.label.setStyleSheet('background-color: rgb(59, 59, 59);')
        self.label.show()
        self.show()
        self.param_rect = QLabel()
        self.param_rect.move(x, y)
        self.param_rect.resize(Cells.CellSize, h)
        self.param_rect.setParent(self)
        self.param_rect.setStyleSheet(f'background-color: rgb{color};')
        self.param_rect.show()

    def update_param(self):
        self.param_rect.resize(self.param() * Cells.CellSize, self.height)


class HealthBar(Bar):
    def __init__(self, tank):
        self.max_health = tank.wrapping_object.health
        super().__init__(tank, (59, 170, 59),
                         lambda: tank.wrapping_object.health / self.max_health,
                         0, 0, Cells.CellSize // 10)


class CoolDownBar(Bar):
    def __init__(self, tank: TankVisualisation):
        self.max_cd = tank.shooting_cd.interval()
        super().__init__(tank, (180, 180, 180),
                         lambda: (self.max_cd -
                         tank.shooting_cd.remainingTime()) /
                         self.max_cd, 0, Cells.CellSize // 10,
                         Cells.CellSize // 25)
