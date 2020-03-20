from enum import Enum


class Direction(Enum):
    Up = (0, -1)  # x, reversed y
    Right = (1, 0)
    Down = (0, 1)
    Left = (-1, 0)
