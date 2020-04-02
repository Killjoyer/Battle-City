class FieldCell:
    def __init__(self, back_ground, active_ground=None, fore_ground=None):
        self.back_ground = back_ground
        self.active_ground = active_ground
        self.fore_ground = fore_ground


class DestructibleCell:
    def __init__(self, health=50):
        self.destructible = True
        self.passable = False
        self.overlays = False
        self.health = health

    def destroy(self):
        pass


class ImmortalCell:
    def __init__(self, passable):
        self.destructible = False
        self.passable = passable
        self.overlays = False


class BrickWall(ImmortalCell):
    def __init__(self):
        super().__init__(False)


class EmptyCell(ImmortalCell):
    def __init__(self):
        super().__init__(True)


class WoodenCrate(DestructibleCell):
    def __init__(self):
        super().__init__()


class PoisonousMist(ImmortalCell):
    def __init__(self):
        super().__init__(True)
        self.overlays = True
