from cells import DestructibleCell
from constants import Direction, TankType, TankOwner
from moving_enity import MovingEntity


class Tank(MovingEntity):
    def __init__(self, x: int, y: int, tank_type: TankType,
                 direction: Direction, owner: TankOwner, game):
        super().__init__(x, y, direction)
        self.type = tank_type
        self.game = game
        self.owner = owner
        self.speed = tank_type.value['speed']
        self.damage = tank_type.value['damage']
        self.health = tank_type.value['health']
        self.cooldown = tank_type.value['cooldown']
        if tank_type.value['debuff']:
            self.debuff = Debuff(tank_type.value['debuff'])
        else:
            self.debuff = None
        self.active_debuffs = []

    def shoot(self):
        bullet = Bullet(self, self.x, self.y, self.direction)
        self.game.bullets.add(bullet)
        return bullet

    def die(self, game):
        self.is_dead = True
        if self.owner == TankOwner.Human:
            self.game.tanks.pop(TankOwner.Human)
        else:
            self.game.enemies.remove(self)

    def decrease_health(self, game, damage: int):
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

    def get_debuff_from(self, tank):
        if tank.debuff:
            self.active_debuffs.append(tank.debuff)


class Bullet(MovingEntity):
    def __init__(self, shooter: Tank, x: int, y: int, direction: Direction):
        super().__init__(x, y, direction)
        self.shooter = shooter

    def collision(self, x, y, entity, game):
        if isinstance(entity, Tank):
            if entity != self.shooter:
                self.die(game)
                entity.decrease_health(game, self.shooter.damage)
                entity.get_debuff_from(self.shooter)
                return 'tank', x, y
        if isinstance(entity, DestructibleCell):
            entity.decrease_health(self.shooter.damage, game, x, y)
            self.die(game)
            return 'destr_cell', x, y
        self.die(game)
        return 'indestr_cell', x, y

    def die(self, game):
        self.is_dead = True
        game.bullets.remove(self)


class Debuff:
    def __init__(self, debuff_data: dict):
        self.duration = debuff_data['duration']
        self.damage = debuff_data['damage']
        self.name = debuff_data['name']
