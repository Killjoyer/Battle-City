from constants import BonusesTypes


class InstantHealAction:
    def __init__(self):
        self.amount = BonusesTypes.InstantHeal['amount']

    def apply(self, target):
        try:
            if target.health + self.amount > target.max_health:
                target.health = target.max_health
            else:
                target.health += self.amount
        except Exception as e:
            print(e)


class RegenerationAction:
    def __init__(self):
        self.buff = Buff(BonusesTypes.Regeneration)

    def apply(self, target):
        target.get_debuff(self.buff)


class Bonus:
    Actions = {
        BonusesTypes.InstantHeal['name']: lambda: InstantHealAction(),
        BonusesTypes.Regeneration['name']: lambda: RegenerationAction()
    }

    def __init__(self, game, x, y, name):
        self.action = Bonus.Actions[name]()
        self.is_dead = False
        self.game = game
        self.x = x
        self.y = y
        self.name = name


class Buff:
    def __init__(self, debuff_data: dict):
        self.duration = debuff_data['duration']
        self.damage = debuff_data['damage']
        self.name = debuff_data['name']
