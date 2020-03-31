from constants import Direction
from field import Field


class MovingEntity:
    def __init__(self, x: int, y: int, direction: Direction):
        self.direction = direction
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
