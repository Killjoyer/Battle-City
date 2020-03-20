from enum import Enum

from direction import Direction
from field import Field
from moving_entity import MovingEntity


class TankOwner(Enum):
    Computer = 0
    Human = 1


class TankType(Enum):
    Default = {'speed': 10,
               'shooting_rate': 10,
               'damage': 10,}


class Tank(MovingEntity):
    def __init__(self, x: int, y: int, tank_type: TankType,
                 direction: Direction, owner: TankOwner):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = tank_type.value['speed']
        self.shooting_rate = tank_type.value['shooting_rate']
        self.damage = tank_type.value['damage']
        self.direction = direction

    def shoot(self):
        pass

    def die(self):
        pass

    def turn_to(self, direction: Direction):
        self.direction = direction
        return self.direction

    def is_wall(self, field: Field, direction: Direction):
        pass


class Bullet(MovingEntity):
    def __init__(self, shooter: Tank, x: int, y: int, direction: Direction):
        super().__init__()
        self.x = x
        self.y = y
        self.direction = direction
        self.shooter = shooter
