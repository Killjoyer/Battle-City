from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from constants import Bullets, MovingWills
from tank import Bullet
from Interface.moving_entity_visualisation import MovingEntityVisualisation


class BulletVisualisation(MovingEntityVisualisation):
    def __init__(self, father, bullet: Bullet):
        bullet.speed = 4
        super().__init__(father, bullet, Bullets.Texture)
        self.moves = True
        self.moving_will = MovingWills.Forward
