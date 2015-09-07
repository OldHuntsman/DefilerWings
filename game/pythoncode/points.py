# coding=utf-8

import renpy.store as store
import girls_data
from utils import call
from data import reputation_levels, reputation_gain, game_events, achieve_target, get_description_by_count, dark_army


class Mobilization(store.object):
    base = 0  # Base mobilization
    max = 0  # Max mobilization
    _lvl = 0
    decrease = 0  # Mobilization decrease

    def __getinitargs__(self):
        return self.level

    def __init__(self, level=0):
        """
        level - mobilization level
        """
        self.level = level

    @property
    def level(self):  # Current mobilization
        return self._lvl

    @level.setter
    def level(self, value):
        value = int(value)
        if value >= 0:
            if value > self._lvl:
                self.max = value
                self._lvl = value
                if game_events["mobilization_increased"] is not None:
                    call(game_events["mobilization_increased"])
            if value < self._lvl:
                self.decrease += self._lvl - value
                self._lvl = value

    def reset_base(self):
        self.base = self._lvl

    def reset_max(self):
        self.max = self._lvl

    def reset_decrease(self):
        self.decrease = 0

    def reset(self):
        self.reset_base()
        self.reset_max()
        self.reset_decrease()

    @property
    def gain(self):  # Current and base mobilization difference
        return self._lvl - self.base


class Reputation(store.object):
    """
    Dragon' reputation.
    """
    _rp = 0
    _gain = 0
    _last_gain = 0

    @property
    def points(self):
        """
        Amount of reputation points
        """
        return self._rp

    @points.setter
    def points(self, value):
        if value >= 0:
            delta = int(value - self._rp)
            if delta in reputation_gain:
                self._last_gain = delta
                self._gain += delta
                self._rp = int(value)
                achieve_target(self.level, "reputation")
            else:
                raise Exception("Cannot raise reputation. Invalid gain.")

    @property
    def gain_description(self):
        if self._last_gain in reputation_gain:
            return reputation_gain[self._last_gain]

    @property
    def points_gained(self):
        return self._gain

    def reset_gain(self):
        """
        Reset reputation points gain. For example, we use this when dragon sleeps.
        """
        self._gain = 0

    @property
    def level(self):
        key = 0
        for i in sorted(reputation_levels.keys()):
            if self._rp >= int(i):
                key = int(i)
        return reputation_levels[key]


class Poverty(store.object):
    """
    Poverty counter. If poverty lowered below zero, sets it to zero.
    Использование:
    Poverty.value - returns current poverty level
    Poverty.value += 1 - plans to increase poverty by one
    Poverty.value -= 1 - plans to decrease poverty by one
    Poverty.apply_value() - applies planned poverty change
    """
    _value = 0
    _planned = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._planned += value - self._value

    def apply_planned(self):
        """
        applies planned poverty change
        """
        callback = False
        if self._planned > 0:
            callback = True
        if self._value + self._planned >= 0:
            self._value += self._planned
        else:
            self._value = 0
        self._planned = 0
        if callback and game_events["poverty_increased"] is not None:
            call(game_events["poverty_increased"])


class Army(store.object):
    """
    Army of darkness class
    """

    def __init__(self):
        self._grunts = {'goblin': 1}  # словарь для хранения рядовых войск
        self._elites = {}  # словарь для хранения элитных войск
        self.money = 0  # деньги в казне Владычицы
        self._force_residue = 100  # процент оставшейся силы армии - мощь армии

    def add_warrior(self, warrior_type):
        """
        Adds warrior to army. warrior_type - type of added warrior from girls_data.spawn_info
        """
        if 'elite' in girls_data.spawn_info[warrior_type]['modifier']:
            # elite warrior, added to list of elites
            warriors_list = self._elites
        else:
            # common warrior, added to list of grunts 
            warriors_list = self._grunts
        if warrior_type in warriors_list:
            # this warrior type allready in list, just increase amount of them
            warriors_list[warrior_type] += 1
        else:
            # no such warrior type in list, add it
            warriors_list[warrior_type] = 1

    @property
    def grunts(self):
        """
        Returns amount of grunts in army
        """
        grunts_count = 0
        for grunts_i in self._grunts.values():
            grunts_count += grunts_i
        return grunts_count

    @property
    def grunts_list(self):
        """
        Returns list of grunts in army
        """
        grunts_list = u""
        for grunt_name, grunt_count in self._grunts.iteritems():
            grunts_list += u"%s: %s. " % (girls_data.spawn_info[grunt_name]['name'], grunt_count)
        return grunts_list

    @property
    def elites(self):
        """
        Returns amount of elites in army
        """
        elites_count = 0
        for elites_i in self._elites.values():
            elites_count += elites_i
        return elites_count

    @property
    def elites_list(self):
        """
        returns list of elites in army
        """
        elites_list = u""
        for elite_name, elite_count in self._elites.iteritems():
            elites_list += u"%s: %s. " % (girls_data.spawn_info[elite_name]['name'], elite_count)
        return elites_list

    @property
    def diversity(self):
        """
        Returns diversity
        """
        diversity = len(self._elites)
        dominant_number = sorted(self._grunts.values())[-1] // 2
        for number_i in self._grunts.values():
            if dominant_number <= number_i:
                diversity += 1
        return diversity

    @property
    def equipment(self):
        """
        Returns equipment level
        """
        equipment = 1
        aod_money = self.money
        aod_cost = (self.grunts + self.elites) * 1000
        while aod_money >= aod_cost:
            aod_money //= 2
            equipment += 1
        return equipment

    @property
    def force(self):
        """
        Return summary force of army by formula:
        (force) = (grunts + 3 * elites) * diversity * equipment * текущий процент мощи
        """
        return (self.grunts + 3 * self.elites) * self.diversity * self.equipment * self._force_residue // 100

    @property
    def power_percentage(self):
        """
        Returns current percentage level of force
        """
        return self._force_residue

    @power_percentage.setter
    def power_percentage(self, value):
        """
        Sets current percentage level of force
        """
        self._force_residue = value

    @property
    def army_description(self):
        description_str = get_description_by_count(dark_army['grunts'], self.grunts) + '\n'
        description_str += get_description_by_count(dark_army['elites'], self.elites) + '\n'
        description_str += get_description_by_count(dark_army['diversity'], self.diversity) + '\n'
        description_str += get_description_by_count(dark_army['equipment'], self.equipment) + '\n'
        description_str += get_description_by_count(dark_army['force'], self.force)
        return description_str
