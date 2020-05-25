from bonus import Buff, Bonus
from cells import DestructibleCell
from constants import Direction, TankType, TankOwner
from moving_enity import MovingEntity


class Tank(MovingEntity):
    def __init__(self, x: int, y: int, tank_type: TankType,
                 direction: Direction, owner: TankOwner, game):
        super().__init__(x, y, direction)
        self.type = tank_type
        self.points = 0
        self.game = game
        self.owner = owner
        self.speed = tank_type.value['speed']
        self.cost = tank_type.value['cost']
        self.damage = tank_type.value['damage']
        self.health = tank_type.value['health']
        self.max_health = self.health
        self.cooldown = tank_type.value['cooldown']
        if tank_type.value['debuff']:
            self.debuff = Buff(tank_type.value['debuff'])
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
        if self.is_dead: return
        self.health -= damage
        if self.health <= 0:
            self.die(game)
        if self.health >= self.max_health:
            self.health = self.max_health

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
                return 'bullet', x, y
        if isinstance(entity, Bonus):
            entity.action.apply(self)
            game.active_bonuses.remove(entity)
            entity.is_dead = True
            return 'bonus', x, y
        return False

    def get_debuff(self, debuff):
        if debuff:
            self.active_debuffs.append(debuff)

    def move(self, game, direction: int):
        new_x = self.x + direction * self.direction[0]
        new_y = self.y + direction * self.direction[1]
        for tank in game.enemies + list(game.tanks.values()):
            if tank.x == new_x and tank.y == new_y:
                return self.collision(new_x, new_y, tank, game)
        for bonus in game.active_bonuses:
            if new_x == bonus.x and new_y == bonus.y:
                self.x = new_x
                self.y = new_y
                return self.collision(new_x, new_y, bonus, game)

        if not game.field.level[new_y][new_x].passable:
            return self.collision(new_x, new_y, game.field.level[new_y][new_x],
                                  game)
        self.x = new_x
        self.y = new_y


class Bullet(MovingEntity):
    def __init__(self, shooter: Tank, x: int, y: int, direction: Direction):
        super().__init__(x, y, direction)
        self.shooter = shooter

    def collision(self, x, y, entity, game):
        if isinstance(entity, Tank):
            if entity != self.shooter:
                self.die(game)
                entity.decrease_health(game, self.shooter.damage)
                entity.get_debuff(self.shooter.debuff)
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
