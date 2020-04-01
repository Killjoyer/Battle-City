from constants import Direction
from field import Field


class MovingEntity:
    def __init__(self, x: int, y: int, direction: Direction, speed=1):
        self.direction = direction
        self.speed = speed
        self.x = x
        self.y = y

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