from constants import Direction
from field import Field
from tank import Tank, TankType, TankOwner


class Game:
    def __init__(self, level):
        self.field = Field(level)
        self.tanks = {
            TankOwner.Human: Tank(0, 0, TankType.Default, Direction.Right,
                                  TankOwner.Human)
        }
