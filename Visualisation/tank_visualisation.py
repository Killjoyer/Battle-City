from PyQt5.QtCore import QTimer

from Visualisation.bullet_visualisation import BulletVisualisation
from Visualisation.moving_entity_visualisation import MovingEntityVisualisation
from constants import TankTextures
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
