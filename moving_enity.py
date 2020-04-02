from builtins import staticmethod


class MovingEntity:
    def __init__(self, x: int, y: int, direction, speed=1):
        self.direction = direction
        self.speed = speed
        self.x = x
        self.y = y

    def collision(self, collided_cell):
        print(f'collided {self.x} {self.y} with {collided_cell.fore_ground}',
              f'{collided_cell.active_ground}', sep=' ')
        return

    @staticmethod
    def is_not_wall(cell):
        return cell.fore_ground is None or cell.fore_ground.passable

    def has_activity(self, cell):
        return cell.active_ground is not None

    def start_moving(self, field, d):
        try:
            cell = field.level[self.y + d * self.direction[1]][
                self.x + d * self.direction[0]]
            if not MovingEntity.is_not_wall(cell):
                return self.collision(cell)
            if self.has_activity(cell):
                return self.collision(cell)
            self.x += self.direction[0]
            self.y += self.direction[1]
            cell.active_ground = self
        except Exception as e:
            print(e)

    def stop_moving(self, field, d):
        cell = field.level[self.y - d * self.direction[1]][
            self.x - d * self.direction[0]]
        cell.active_ground = None
