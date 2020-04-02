from constants import Direction
from field import Field


class MovingEntity:
    def __init__(self, x: int, y: int, direction: Direction, speed=1):
        self.direction = direction
        self.speed = speed
        self.x = x
        self.y = y

    def collision(self):
        return

    def move_forward(self, field: Field):
        if (not field.level[self.y + self.direction[1]][
                self.x + self.direction[0]].passable):
            return self.collision()
        self.x += self.direction[0]
        self.y += self.direction[1]

    def move_backward(self, field):
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
