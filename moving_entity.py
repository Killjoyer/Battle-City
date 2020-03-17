from direction import Direction


class MovingEntity:
    def __init__(self):
        self.x: int = 0
        self.y: int = 0
        self.speed: int = 0
        self.direction: Direction = Direction.Up
        self.texture: str = ''

    def move_to_next_cell(self):
        pass
