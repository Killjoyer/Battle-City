from constants import Bullets, MovingWills
from tank import Bullet
from Visualisation.moving_entity_visualisation import MovingEntityVisualisation


class BulletVisualisation(MovingEntityVisualisation):
    def __init__(self, father, bullet: Bullet):
        bullet.speed = 8
        super().__init__(father, bullet, Bullets.Texture)
        self.moves = True
        self.moving_will = MovingWills.Forward
        self.show()
