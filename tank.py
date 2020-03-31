from constants import Direction, TankType, TankOwner
from field import Field


class Tank:
    def __init__(self, x: int, y: int, tank_type: TankType,
                 direction: Direction, owner: TankOwner):
        super().__init__()
        self.x = x
        self.y = y
        self.type = tank_type
        self.owner = owner
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

    def move_forward(self, field: Field):
        if self.direction == Direction.Up and self.y <= 0:
            return
        if self.direction == Direction.Down and self.y >= field.height - 1:
            return
        if self.direction == Direction.Left and self.x <= 0:
            return
        if self.direction == Direction.Right and self.x >= field.width - 1:
            return
        if (not field.level[self.y + self.direction[1]][
            self.x + self.direction[0]].passable):
            return
        self.x += self.direction[0]
        self.y += self.direction[1]

    def move_backward(self, field):
        if self.direction == Direction.Down and self.y <= 0:
            return
        if self.direction == Direction.Up and self.y >= field.height - 1:
            return
        if self.direction == Direction.Right and self.x <= 0:
            return
        if self.direction == Direction.Left and self.x >= field.width - 1:
            return
        if (not field.level[self.y - self.direction[1]][
            self.x - self.direction[0]].passable):
            return
        self.x -= self.direction[0]
        self.y -= self.direction[1]

    def move(self, field: Field, direction: int):
        if direction == 1:
            self.move_forward(field)
        elif direction == -1:
            self.move_backward(field)


class Bullet:
    def __init__(self, shooter: Tank, x: int, y: int, direction: Direction):
        super().__init__()
        self.x = x
        self.y = y
        self.direction = direction
        self.shooter = shooter
