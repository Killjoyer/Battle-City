from PyQt5.QtGui import QTransform, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from constants import Cells, MovingWills, TankTextures, Direction
from tank import Tank
from Visualisation.moving_entity_visualisation import MovingEntityVisualisation
from Visualisation.bullet_visualisation import BulletVisualisation


class TankVisualisation(MovingEntityVisualisation):
    def __init__(self, father, tank: Tank):
        super().__init__(father, tank,
                         TankTextures.Textures[tank.type](tank.owner))
        self.bullets = set()

    def shoot(self):
        bullet = BulletVisualisation(self.father, self.wrapping_object.shoot())
        bullet.stackUnder(self)
        self.bullets.add(bullet)
