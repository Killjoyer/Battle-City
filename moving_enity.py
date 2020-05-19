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
        for tank in game.enemies + list(game.tanks.values()):
            if (tank.x == self.x + direction * self.direction[0] and
                    tank.y == self.y + direction * self.direction[1]):
                print('met tank at', tank.x, tank.y)
                return self.collision(self.x + direction * self.direction[0],
                                      self.y + direction * self.direction[1],
                                      tank, game)
        if (not game.field.level[self.y + direction * self.direction[1]][
                self.x + direction * self.direction[0]].passable):
            print('met not passable ')
            return self.collision(self.x + direction * self.direction[0],
                                  self.y + direction * self.direction[1],
                                  game.field.level[
                                      self.y + direction * self.direction[1]][
                                      self.x + direction * self.direction[0]],
                                  game)
        self.x += direction * self.direction[0]
        self.y += direction * self.direction[1]
