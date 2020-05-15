from constants import Direction
from field import Field
from tank import Tank, TankType, TankOwner


class Game:
    def __init__(self, level):
        self.field = Field(level)
        self.tanks = {
            TankOwner.Human: Tank(*self.field.player_pos,
                                  TankType.Default,
                                  Direction.Right,
                                  TankOwner.Human)
        }
        self.enemies = [Tank(i, j, TankType.Default, Direction.Right,
                             TankOwner.Computer) for i, j in
                        self.field.enemies]
