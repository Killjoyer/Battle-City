import unittest

from constants import Direction, TankType, TankOwner
from field import Field
from tank import Tank


class TankTests(unittest.TestCase):
    def test_turns_right(self):
        tank = Tank(0, 0, TankType.Default, Direction.Up, TankOwner.Human)
        tank.turn_right()
        self.assertEqual(tank.direction, Direction.Right)

    def test_turns_left(self):
        tank = Tank(0, 0, TankType.Default, Direction.Up, TankOwner.Human)
        tank.turn_left()
        self.assertEqual(tank.direction, Direction.Left)

    def test_moves_forward(self):
        tank = Tank(1, 1, TankType.Default, Direction.Right, TankOwner.Human)
        field = Field(['__', '__'])
        tank.move_forward(field)
        self.assertEqual(tank.x, 2)
        self.assertEqual(tank.y, 1)

    def test_dont_move_through_edge_UP(self):
        tank = Tank(1, 1, TankType.Default, Direction.Up, TankOwner.Human)
        field = Field(['__', '__'])
        tank.move_forward(field)
        msg = 'Penetrates the border UP FORWARD'
        self.assertEqual(tank.x, 1, msg)
        self.assertEqual(tank.y, 1, msg)
        tank.turn_right()
        tank.turn_right()
        tank.move_backward(field)
        msg = 'Penetrates the border UP BACKWARD'
        self.assertEqual(tank.x, 1, msg)
        self.assertEqual(tank.y, 1, msg)

    def test_dont_move_through_edge_RIGHT(self):
        tank = Tank(2, 2, TankType.Default, Direction.Right, TankOwner.Human)
        field = Field(['__', '__'])
        tank.move_forward(field)
        msg = 'Penetrates the border RIGHT FORWARD'
        self.assertEqual(tank.x, 2)
        self.assertEqual(tank.y, 2)
        tank.turn_right()
        tank.turn_right()
        tank.move_backward(field)
        msg = 'Penetrates the border RIGHT BACKWARD'
        self.assertEqual(tank.x, 2)
        self.assertEqual(tank.y, 2)

    def test_dont_move_through_edge_DOWN(self):
        tank = Tank(2, 2, TankType.Default, Direction.Down, TankOwner.Human)
        field = Field(['__', '__'])
        tank.move_forward(field)
        msg = 'Penetrates the border DOWN FORWARD'
        self.assertEqual(tank.x, 2)
        self.assertEqual(tank.y, 2)
        tank.turn_right()
        tank.turn_right()
        tank.move_backward(field)
        msg = 'Penetrates the border DOWN BACKWARD'
        self.assertEqual(tank.x, 2)
        self.assertEqual(tank.y, 2)

    def test_dont_move_through_edge_LEFT(self):
        tank = Tank(1, 1, TankType.Default, Direction.Left, TankOwner.Human)
        field = Field(['__', '__'])
        tank.move_forward(field)
        msg = 'Penetrates the border LEFT FORWARD'
        self.assertEqual(tank.x, 1)
        self.assertEqual(tank.y, 1)
        tank.turn_right()
        tank.turn_right()
        tank.move_backward(field)
        msg = 'Penetrates the border LEFT BACKWARD'
        self.assertEqual(tank.x, 1)
        self.assertEqual(tank.y, 1)

    def test_dont_move_into_wall(self):
        tank = Tank(1, 1, TankType.Default, Direction.Right, TankOwner.Human)
        field = Field(['_#', '##'])
        tank.move_forward(field)
        self.assertEqual(tank.x, 1)
        self.assertEqual(tank.y, 1)
