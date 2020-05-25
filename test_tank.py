import unittest

from constants import Direction
from game import Game
from tank import Tank, TankType, TankOwner
from cells import EmptyCell


class TankTests(unittest.TestCase):
    def test_moves_forward(self):
        game = Game(('P_', '__'))
        tank = game.tanks[TankOwner.Human]
        tank.move(game, 1)
        self.assertEqual(tank.x, 2)
        self.assertEqual(tank.y, 1)

    def test_moves_backward(self):
        game = Game(('P_', '_x'))
        tank = game.tanks[TankOwner.Human]
        tank.turn_right()
        tank.turn_right()
        tank.move(game, -1)
        self.assertEqual(tank.x, 2)
        self.assertEqual(tank.y, 1)

    def test_stop_at_wall(self):
        game = Game(('Px', ))
        tank = game.tanks[TankOwner.Human]
        tank.move(game, 1)
        self.assertEqual(tank.x, 1)
        self.assertEqual(tank.y, 1)

    def test_destroys_crate(self):
        game = Game(('Px', ))
        tank = game.tanks[TankOwner.Human]
        for i in range(6):
            b = tank.shoot()
            b.move(game, 1)
        self.assertTrue(isinstance(
            game.field.level[1][2], EmptyCell
        ))
