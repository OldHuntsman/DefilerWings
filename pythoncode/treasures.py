import random


class Coins(object):
    def __init__(self, amount):
        self.amount = amount

    @property
    def cost(self):
        return self.amount

    def __str__(self):
        return str(self.cost) + ' coins'


class Treasure(object):
    materials_cost = {'Copper': 20,
                      'Silver': 50,
                      'Gold': 75,
                      'Platinum': 100,
                      'Diamond': 150}
    forms_cost = {'Ring': 20,
                  'Amulet': 40,
                  'Scepter': 70,
                  'Crown': 100}

    def __init__(self, material, form):
        self.material = material
        self.form = form
        self.rnd_modifier = random.random() * 0.2 + 0.9

    @property
    def cost(self):
        return int(self.materials_cost[self.material] * self.forms_cost[self.form] * self.rnd_modifier)

    def __str__(self):
        return '%s %s (%s)' % (self.material.capitalize(), self.form.lower(), self.cost)


def generate_treasures(count):
    def gen():
        rnd = random.randint(0, 100)
        if rnd > 50:
            return Treasure(random.choice(Treasure.materials_cost.keys()),
                            random.choice(Treasure.forms_cost.keys()))
        else:
            return Coins(random.randint(10, 1000))

    gold = Coins(0)
    treasures = []
    for i in xrange(count):
        treasure = gen()
        if isinstance(treasure, Coins):
            gold.amount += treasure.amount
        else:
            treasures.append(treasure)

    treasures.append(gold)

    return treasures