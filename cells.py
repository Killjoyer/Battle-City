class DestructibleCell:
    def __init__(self, health=50):
        self.destructible = False
        self.passable = False
        self.health = health
        self.overlays = False

    def destroy(self):
        pass


class ImmortalCell:
    def __init__(self, passable):
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
