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


class DebuffType:
    OnFire = {
        'name': 'On fire!',
        'duration': 5,  # seconds
        'damage': 2
    }

    Regeneration = {
        'name': 'regeneration',
        'duration': 5,
        'damage': -8
    }


class TankType(Enum):
    Default = {
        'speed': 2,
        'damage': 15,
        'health': 10000,
        'cost': 10,
        'cooldown': 3,  # seconds
        'debuff': None
    }

    Flaming = {
        'speed': 2,
        'damage': 5,
        'health': 80,
        'cost': 15,
        'cooldown': 1,
        'debuff': DebuffType.OnFire
    }

    Quick = {
        'speed': 4,
        'damage': 10,
        'health': 70,
        'cost': 13,
        'cooldown': 3,
        'debuff': None
    }


class TankTextures:
    Textures = {
        TankType.Default: lambda tank_owner:
        os.path.join('Resources', f'default_tank_{tank_owner}.png'),
        TankType.Flaming: lambda tank_owner:
        os.path.join('Resources', f'flaming_tank_{tank_owner}.png'),
        TankType.Quick: lambda tank_owner:
        os.path.join('Resources', f'fast_tank_{tank_owner}.png'),
    }


class Cells:
    GeneratingTypes = {
        'E': TankType.Default,
        'F': TankType.Flaming,
        'Q': TankType.Quick,
    }

    Cells = {
        'P': lambda: EmptyCell(),  # player position
        'E': lambda: EmptyCell(),
        'F': lambda: EmptyCell(),
        'Q': lambda: EmptyCell(),
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


class BonusesTypes:
    RollRange = (1, 4)
    InstantHeal = {
        'name': 'instant heal',
        'amount': 60
    }
    Regeneration = DebuffType.Regeneration
    CooldownDecrease = {
        'name': 'cooldown decrease',
        'amount': 0.5
    }
    Roll = {
        1: InstantHeal,
        2: Regeneration,
        3: Regeneration,
        4: CooldownDecrease,
    }


class Bonuses:
    RollBorders = (1, 20)

    BingoThreshold = 1

    BuffsColors = {
        'On fire!': (200, 59, 59),  # Red - orange
        'regeneration': (59, 170, 59),  # Green
    }

    BuffsTextures = {
        'On fire!': [
            os.path.join('Resources', 'flames1.png'),
            os.path.join('Resources', 'flames2.png'),
            os.path.join('Resources', 'flames3.png')
        ],
        'regeneration': [
            os.path.join('Resources', 'regen1.png'),
            os.path.join('Resources', 'regen2.png'),
            os.path.join('Resources', 'regen3.png'),
        ]
    }

    Texture = {
        BonusesTypes.InstantHeal['name']:
            os.path.join('Resources', 'heal.png'),
        BonusesTypes.Regeneration['name']:
            os.path.join('Resources', 'regeneration.png'),
        BonusesTypes.CooldownDecrease['name']:
            os.path.join('Resources', 'cooldown_decrease.png')
    }
