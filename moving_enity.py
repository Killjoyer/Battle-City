from builtins import staticmethod


class MovingEntity:
    def __init__(self, x: int, y: int, direction, speed=1):
        self.direction = direction
        self.speed = speed
        self.x = x
        self.y = y

    def collision(self):
        return

    @staticmethod
    def is_wall(cell):
        return not (cell.fore_ground is None or cell.fore_ground.passable)

    @staticmethod
    def has_activity(cell):
        return cell.active_ground is not None

    def move_forward(self, field):
        try:
            cell = field.level[self.y + self.direction[1]][
                        self.x + self.direction[0]]
            if (MovingEntity.is_wall(
                    field.level[self.y + self.direction[1]][
                        self.x + self.direction[0]])):
                return self.collision()
            if (MovingEntity.has_activity(cell) and
                    cell.active_ground is not self):
                return self.collision()
            self.x += self.direction[0]
            self.y += self.direction[1]
        except Exception as e:
            print(e)

    def move_backward(self, field):
        if (MovingEntity.is_wall(
                field.level[self.y - self.direction[1]][
                    self.x - self.direction[0]])):
            return
        self.x -= self.direction[0]
        self.y -= self.direction[1]

    def move(self, field, direction: int):
        if direction == 1:
            self.move_forward(field)
        elif direction == -1:
            self.move_backward(field)
