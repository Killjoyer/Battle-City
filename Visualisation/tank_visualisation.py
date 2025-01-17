from queue import Queue

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from Visualisation.bullet_visualisation import BulletVisualisation
from Visualisation.moving_entity_visualisation import MovingEntityVisualisation
from bonus import Buff
from constants import TankTextures, Cells, Bonuses
from tank import Tank


class TankVisualisation(MovingEntityVisualisation):
    def __init__(self, father, tank: Tank):
        super().__init__(father, tank,
                         TankTextures.Textures[tank.type](tank.owner))
        self.can_shoot = True
        self.is_shooting = False
        self.shooting_cd = QTimer()
        self.cooldown = self.wrapping_object.cooldown
        self.shooting_cd.setInterval(self.wrapping_object.cooldown * 1000)
        self.shooting_cd.timeout.connect(self._drop_cd)
        self.show()
        self.bars = [HealthBar(self), CoolDownBar(self)]
        self.active_debuffs = []

    def update_bars(self):
        for bar in self.bars:
            bar.update_param()

    def _drop_cd(self):
        self.can_shoot = True
        # print('can shoot!')
        self.shooting_cd.stop()

    def shoot(self):
        if self.can_shoot:
            bullet = BulletVisualisation(self.father,
                                         self.wrapping_object.shoot())
            bullet.stackUnder(self)
            self.parent().bullets.add(bullet)
            self.can_shoot = False
            # print(self.wrapping_object.cooldown, self.cooldown)
            if self.wrapping_object.cooldown != self.cooldown:
                self.cooldown = self.wrapping_object.cooldown * 1000
                self.shooting_cd.setInterval(self.cooldown)
            self.shooting_cd.start()

    def treat_debuffs(self):
        for debuff in self.wrapping_object.active_debuffs:
            self.active_debuffs.append(DebuffVisualisation(self, debuff))
        self.wrapping_object.active_debuffs = []

    def stop_tank(self):
        if not self.shooting_cd.isActive():
            return
        self.shooting_cd.stop()
        for buff in self.active_debuffs:
            buff.duration.stop()
            buff.ticks.stop()

    def start_tank(self):
        if self.shooting_cd.isActive():
            return
        self.shooting_cd.start()
        for buff in self.active_debuffs:
            buff.duration.start()
            buff.ticks.start()


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
        p = self.param()
        self.param_rect.resize(p * Cells.CellSize, self.height)


class HealthBar(Bar):
    def __init__(self, tank):
        self.max_health = tank.wrapping_object.max_health
        super().__init__(tank, (59, 170, 59),
                         lambda: tank.wrapping_object.health / self.max_health,
                         0, 0, Cells.CellSize // 10)


class CoolDownBar(Bar):
    def __init__(self, tank: TankVisualisation):
        self.max_cd = tank.shooting_cd.interval()
        super().__init__(tank, (180, 180, 180),
                         lambda: (tank.shooting_cd.interval() -
                                  tank.shooting_cd.remainingTime()) /
                                 tank.shooting_cd.interval(), 0,
                         Cells.CellSize // 10,
                         Cells.CellSize // 25)


class DebuffBar(Bar):
    def __init__(self, tank, debuff):
        self.max_cd = debuff.duration.interval()
        color = Bonuses.BuffsColors[debuff.debuff.name]
        super().__init__(tank, color,
                         lambda: debuff.duration.remainingTime() / self.max_cd,
                         0,
                         Cells.CellSize - Cells.CellSize // 25 -
                         len(tank.active_debuffs) * Cells.CellSize // 25,
                         Cells.CellSize // 25)


class DebuffVisualisation(QWidget):
    def __init__(self, tank, debuff: Buff):
        super().__init__(tank)
        self.tank = tank
        self.debuff = debuff
        self.duration = QTimer()
        self.duration.setInterval(debuff.duration * 1000)
        self.duration.timeout.connect(self.stop)
        self.label = QLabel(self)
        self.label.show()
        self.label.resize(Cells.CellSize, Cells.CellSize)
        self.texture_queue = Queue()
        self.set_queue()
        self.duration.start()
        self.ticks = QTimer()
        self.ticks.setInterval(500)
        self.ticks.timeout.connect(self.do_tick)
        self.ticks.start()
        self.bar = DebuffBar(tank, self)
        self.tank.bars.append(self.bar)
        self.show()

    def set_queue(self):
        for texture in Bonuses.BuffsTextures[self.debuff.name]:
            self.texture_queue.put_nowait(
                QPixmap(texture).scaled(Cells.CellSize, Cells.CellSize))

    def update_texture(self):
        texture = self.texture_queue.get_nowait()
        self.label.setPixmap(texture)
        self.texture_queue.put_nowait(texture)

    def do_tick(self):
        self.update_texture()
        self.tank.wrapping_object.decrease_health(self.tank.parent(),
                                                  self.debuff.damage)

    def stop(self):
        self.tank.active_debuffs.remove(self)
        self.ticks.stop()
        self.bar.close()
        self.tank.bars.remove(self.bar)
        self.duration.stop()
        self.close()
