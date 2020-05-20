from constants import Direction


class MovingEntity:
    def __init__(self, x: int, y: int, direction: Direction, speed=1):
        self.direction = direction
        self.speed = speed
        self.is_dead = False
        self.x = x
        self.y = y

    def collision(self, x, y, entity, game):
        return

    def die(self, game):
        return

    def move(self, game, direction: int):
        new_x = self.x + direction * self.direction[0]
        new_y = self.y + direction * self.direction[1]
        for tank in game.enemies + list(game.tanks.values()):
            if tank.x == new_x and tank.y == new_y:
                return self.collision(new_x, new_y, tank, game)
        if not game.field.level[new_y][new_x].passable:
            return self.collision(new_x, new_y,game.field.level[new_y][new_x],
                                  game)
        self.x = new_x
        self.y = new_y
