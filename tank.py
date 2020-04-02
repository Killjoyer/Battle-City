from moving_enity import MovingEntity


class Tank(MovingEntity):
    def __init__(self, x: int, y: int, tank_type,
                 direction, owner):
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

    def has_activity(self, cell):
        return (cell.active_ground is not None and
                ((isinstance(cell.active_ground, Tank)
                  and cell.active_ground is not self) or
                 (cell.active_ground.shooter is not self)))


class Bullet(MovingEntity):
    def __init__(self, shooter: Tank, x: int, y: int, direction):
        super().__init__(x, y, direction)
        self.shooter = shooter

    def has_activity(self, cell):
        return (cell.active_ground is not None and
                cell.active_ground is not self.shooter)
