# coding=utf-8

from copy import deepcopy

import data
import treasures


class Lair(object):
    def __init__(self, lair_type="impassable_coomb"):
        self.type_name = lair_type
        self.type = data.Container(lair_type, data.lair_types[lair_type])
        # improvements list
        self.upgrades = data.Container('lair_upgrades')
        if 'provide' in self.type:
            for upgrade in self.type['provide']:
                self.add_upgrade(upgrade)
        # Сокровищиница
        self.treasury = treasures.Treasury()

    def reachable(self, abilities):
        """
        Function for checking lair approachabillity
        :param abilities: - list of abilities of that who tries to reach lair
            thief example: [ 'alpinism', 'swimming' ]
        :return: return True ,if lair is reachable and False if not
        """
        for r in self.requirements():
            if r not in abilities:
                return False
        return True

    def requirements(self):
        """
        :return: Return list of abilities needed to reach lair.
        """
        r = []
        if self.type.require:  # If lair type requests something, we add it
            r += self.type.require
        for u in self.upgrades:  # Same for improvements
            if self.upgrades[u].require:
                r += self.upgrades[u].require
        return r

    @property
    def inaccessability(self):
        return self.type.inaccessability + self.upgrades.sum("inaccessability")

    def add_upgrade(self, upgrade):
        """
        Function for lair improvements
        :param upgrade: - name of added improvement
        """
        self.upgrades.add(upgrade, deepcopy(data.lair_upgrades[upgrade]))
        # replace improvement if necesary
        if 'replaces' in self.upgrades[upgrade].keys() and \
            self.upgrades[upgrade]['replaces'] in self.upgrades:
            del self.upgrades[self.upgrades[upgrade]['replaces']]
