import os
from enum import Enum

from cells import PoisonousMist, BrickWall, EmptyCell, WoodenCrate


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
    Default = {
        'speed': 2,
        'damage': 10,
        'health': 100,
        'cooldown': 3,  # seconds
        'debuff': None
    }
    Flaming = {
        'speed': 2,
        'damage': 5,
        'health': 80,
        'cooldown': 5,
        'debuff': {
            'name': 'On fire!',
            'duration': 5,  # seconds
            'damage': 5
        }
    }


class TankTextures:
    Textures = {
        TankType.Default: lambda tank_owner:
        os.path.join('Resources', f'default_tank_{tank_owner}.png'),
        TankType.Flaming: lambda tank_owner:
        os.path.join('Resources', f'flaming_tank_{tank_owner}.png'),
    }


class Cells:
    GeneratingTypes = {
        'E': TankType.Default,
        'F': TankType.Flaming,
    }

    Cells = {
        'P': lambda: EmptyCell(),  # player position
        'E': lambda: EmptyCell(),
        'F': lambda: EmptyCell(),
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

    Destruction = {
        type(WoodenCrate()): [
            os.path.join('Resources', 'wooden_crate_1.png'),
            os.path.join('Resources', 'wooden_crate_2.png'),
            os.path.join('Resources', 'wooden_crate_3.png'),
        ]
    }


class WindowSettings:
    Title = 'Battle Town'
    IcoSource = os.path.join('Resources', 'icon.ico')
    TimerInterval = 10


class Bullets:
    Texture = os.path.join('Resources', 'bullet.png')
