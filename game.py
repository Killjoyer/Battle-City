from random import randint

from bonus import Bonus
from cells import DestructibleCell, EmptyCell
from constants import Direction, Bonuses, BonusesTypes
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
        if self.field.second_player_pos[0] != -1:
            self.tanks[TankOwner.SecondPlayer] = Tank(
                *self.field.second_player_pos,
                TankType.Default,
                Direction.Right,
                TankOwner.SecondPlayer,
                self)
        self.enemies = [Tank(i, j, t, Direction.Right,
                             TankOwner.Computer, self) for i, j, t in
                        self.field.enemies]
        self.active_bonuses = set()

    def decide_to_spawn_bonus(self):
        if len(self.active_bonuses) >= 3: return None
        roll = randint(*Bonuses.RollBorders)
        if roll <= Bonuses.BingoThreshold:
            return self.spawn_bonus()
        return None

    def spawn_bonus(self):
        x = randint(1, self.field.width - 1)
        y = randint(1, self.field.height - 1)
        if isinstance(self.field.level[y][x], EmptyCell):
            bonus = BonusesTypes.Roll[randint(*BonusesTypes.RollRange)]
            bonus = Bonus(self, x, y, bonus['name'])
            self.active_bonuses.add(bonus)
            return bonus
        return None
