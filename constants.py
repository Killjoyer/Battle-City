import os

from cells import PoisonousMist, BrickWall, EmptyCell, WoodenCrate
from enum import Enum


class Direction:
    Up = (0, -1)  # x, reversed y
    Right = (1, 0)
    Down = (0, 1)
    Left = (-1, 0)


class MovingWills:
    Nowhere = 0
    Forward = 1
    Backward = -1


class TankOwner:
    Computer = 'computer'
    Human = 'human'


class TankType(Enum):
    Default = {'speed': 2,
               'shooting_rate': 10,
               'damage': 10}


class TankTextures:
    Textures = {
        TankType.Default: lambda tank_owner:
        os.path.join('Resources', f'default_tank_{tank_owner}.png')
    }


class Cells:
    Cells = {
        '_': lambda: EmptyCell(),
        '#': lambda: BrickWall(),
        'x': lambda: WoodenCrate(),
        'm': lambda: PoisonousMist(),
    }

    CellSize = 64

    Textures = {
        type(BrickWall()): os.path.join('Resources', 'brick_wall.png'),
        type(EmptyCell()): os.path.join('Resources', 'empty_cell.png'),
        type(WoodenCrate()): os.path.join('Resources', 'wooden_crate.png'),
        type(PoisonousMist()): os.path.join('Resources', 'poisonous_mist.png'),
    }


class WindowSettings:
    Title = 'Battle Town'
    IcoSource = os.path.join('Resources', 'icon.ico')
    TimerInterval = 10
