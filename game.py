from constants import Direction
from field import Field
from tank import Tank, TankType, TankOwner


class Game:
    def __init__(self, level):
        self.field = Field(level)
        self.bullets = set()
        self.tanks = {
            TankOwner.Human: Tank(*self.field.player_pos,
                                  TankType.Default,
                                  Direction.Right,
                                  TankOwner.Human, self)
        }
        self.enemies = [Tank(i, j, t, Direction.Right,
                             TankOwner.Computer, self) for i, j, t in
                        self.field.enemies]