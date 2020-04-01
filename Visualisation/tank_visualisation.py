from PyQt5.QtGui import QTransform, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from constants import Cells, MovingWills, TankTextures, Direction
from tank import Tank
from Visualisation.moving_entity_visualisation import MovingEntityVisualisation


class TankVisualisation(MovingEntityVisualisation):
    def __init__(self, father, tank: Tank):
        super().__init__(father, tank)
        self.bullets = set()
        self.set_texture(TankTextures.Textures[tank.type](tank.owner))
        self.adjust_direction()

    def shoot(self):
        self.tank.shoot()
