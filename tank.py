from direction import Direction
from moving_entity import MovingEntity
from enum import Enum


class TankType(Enum):
    Default = 0


class Tank(MovingEntity):
    def __init__(self, x: int, y: int, type: TankType):
        super().__init__()
