from field import Field
from constants import TankOwner


class Game:
    def __init__(self, level):
        self.field = Field(level)
        player = self.field.player_pos
        self.tanks = {
            TankOwner.Human: self.field.level[player[0]][
                player[1]].active_ground
        }
