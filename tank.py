from enum import Enum

from direction import Direction
from field import Field
from moving_entity import MovingEntity


class TankOwner(Enum):
    Computer = 0
    Human = 1


class TankType(Enum):
    Default = {'speed': 1,
               'shooting_rate': 10,
               'damage': 10}


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

    def turn_right(self):
        x = -self.direction[1]
        y = self.direction[0]
        self.direction = (x, y)

    def turn_left(self):
        x = self.direction[1]
        y = -self.direction[0]
        self.direction = (x, y)

    def is_wall(self, field: Field, direction: Direction):
        pass

    def move_forward(self, field: Field):
        if self.direction == Direction.Up and self.y <= 0:
            return
        if self.direction == Direction.Down and self.y >= field.height - 1:
            return
        if self.direction == Direction.Left and self.x <= 0:
            return
        if self.direction == Direction.Right and self.x >= field.width - 1:
            return
        self.x += self.direction[0]
        self.y += self.direction[1]

    def move_backward(self):
        self.x -= self.direction[0]
        self.y -= self.direction[1]


class Bullet(MovingEntity):
    def __init__(self, shooter: Tank, x: int, y: int, direction: Direction):
        super().__init__()
        self.x = x
        self.y = y
        self.direction = direction
        self.shooter = shooter
