from enum import Enum

from direction import Direction
from moving_entity import MovingEntity


class TankType(Enum):
    Default = {'speed': 10,
               'shooting_rate': 10,
               'damage': 10, }


class TankOwner(Enum):
    Computer = 0
    Human = 1


class Tank(MovingEntity):
    def __init__(self, x: int, y: int, type: TankType, dir: Direction,
                 owner: TankOwner):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = type.value['speed']
        self.shooting_rate = type.value['shooting_rate']
        self.damage = type.value['damage']
        self.direction = dir

    def shoot(self):
        pass

    def die(self):
        pass

    def turn_to(self, dir: Direction):
        self.direction = dir
        return self.direction
