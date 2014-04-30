#!/usr/bin/env python
# coding=utf-8


class FighterModifier(object):
    """
    Базовый класс для разнообразных модификаторов.
    К примеру: даров владычицы, снаряжения рыцарей, заклинаний и.т.д.
    """

    def __init__(self):
        self.attack = (0, 0)
        self.attack_type = "usual"
        self.protection = (0, 0)

    def __contains__(self, item):
        return item in self.__dict__

    def attack_filter(self, attack):
        return attack


class KnightEquipment(FighterModifier):
    def __init__(self):
        super(KnightEquipment, self).__init__()
        self.equipment_type = ""  # щит, меч, броня ...


class DragonModifier(FighterModifier):
    """
    Класс для разнообразных модификаторов.
    К примеру: даров владычицы, снаряжения рыцарей, заклинаний и.т.д.
    """

    def __init__(self):
        super(DragonModifier, self).__init__()
        self.magic = 0
        self.fear = 0
        self.max_energy = 0

fighter_mods = dict()
dragon_colors = dict()
dragon_gifts = dict()
magic = dict()
thief_items = dict()
knight_items = dict()
knight_abilities = dict()


def get_modifier(name):
    if name in fighter_mods:
        return fighter_mods[name]
    if name in dragon_colors:
        return dragon_colors[name]
    if name in dragon_gifts:
        return dragon_gifts[name]
    if name in magic:
        return magic[name]
    if name in thief_items:
        return thief_items[name]
    if name in knight_items:
        return knight_items[name]
    if name in knight_abilities:
        return knight_abilities[name]
    raise Exception
