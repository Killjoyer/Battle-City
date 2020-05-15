from constants import Direction, TankType, TankOwner
from moving_enity import MovingEntity


class Tank(MovingEntity):
    def __init__(self, x: int, y: int, tank_type: TankType,
                 direction: Direction, owner: TankOwner):
        super().__init__(x, y, direction)
        self.type = tank_type
        self.owner = owner
        self.speed = tank_type.value['speed']
        self.shooting_rate = tank_type.value['shooting_rate']
        self.damage = tank_type.value['damage']
        self.health = tank_type.value['health']
        self.cooldown = tank_type.value['cooldown']
        self.bullets = set()

    def shoot(self):
        bullet = Bullet(self, self.x, self.y, self.direction)
        self.bullets.add(bullet)
        return bullet

    def die(self, game):
        self.is_dead = True
        if self.owner == TankOwner.Human:
            game.tanks.pop(TankOwner.Human)
        else:
            game.enemies.remove(self)

    def decrease_health(self, game, damage: int ):
        self.health -= damage
        if self.health <= 0:
            self.die(game)

    def turn_right(self):
        x = -self.direction[1]
        y = self.direction[0]
        self.direction = (x, y)

    def turn_left(self):
        x = self.direction[1]
        y = -self.direction[0]
        self.direction = (x, y)

    def collision(self, x, y, entity, game):
        if isinstance(entity, Bullet):
            if entity.shooter != self:
                self.is_dead = True
                return True


class Bullet(MovingEntity):
    def __init__(self, shooter: Tank, x: int, y: int, direction: Direction):
        super().__init__(x, y, direction)
        self.shooter = shooter

    def collision(self, x, y, entity, game):
        if isinstance(entity, Tank):
            if entity != self.shooter:
                self.die(game)
                entity.decrease_health(game, self.shooter.damage)
                return True
        else:
            self.die(game)

    def die(self, game):
        self.is_dead = True
        self.shooter.bullets.remove(self)
