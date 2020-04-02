import os
from enum import Enum

from cells import PoisonousMist, BrickWall, EmptyCell, WoodenCrate, FieldCell
from tank import Tank


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
               'damage': 25,
               'health': 100,
               'cooldown': 5, }  # seconds


class TankTextures:
    Textures = {
        TankType.Default: lambda tank_owner:
        os.path.join('Resources', f'default_tank_{tank_owner}.png')
    }


class Cells:
    Cells = {
        'P': lambda x, y: FieldCell(EmptyCell(),
                                    Tank(x, y,
                                         TankType.Default,
                                         Direction.Right,
                                         TankOwner.Human)),
        # player position

        '_': lambda x, y: FieldCell(EmptyCell()),
        '#': lambda x, y: FieldCell(EmptyCell(), None, BrickWall()),
        'x': lambda x, y: FieldCell(EmptyCell(), None, WoodenCrate()),
        'm': lambda x, y: FieldCell(EmptyCell(), None, PoisonousMist()),
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


class Bullets:
    Texture = os.path.join('Resources', 'bullet.png')
