# coding=utf-8

from copy import deepcopy

import data
import treasures


class Lair(object):
    def __init__(self, lair_type="impassable_coomb"):
        self.type_name = lair_type
        self.type = data.Container(lair_type, data.lair_types[lair_type])
        # Список модификаций(ловушки, стражи и.т.п.)
        self.upgrades = data.Container('lair_upgrades')
        if 'provide' in self.type:
            for upgrade in self.type['provide']:
                self.add_upgrade(upgrade)
        # Сокровищиница
        self.treasury = treasures.Treasury()

    def reachable(self, abilities):
        """
        Функция для проверки доступности логова
        :param abilities: - список способностей у того, кто пытается достичь логова,
            например, для вора: [ 'alpinism', 'swimming' ]
        :return: Возращает True ,если до логова можно добраться и False если нет
        """
        for r in self.requirements():
            if r not in abilities:
                return False
        return True

    def requirements(self):
        """
        :return: Возвращает список способностей которые нужны чтобы достичь логова.
        """
        r = []
        if self.type.require:  # Если тип логова что-то требует добавляем что оно требует
            r += self.type.require
        for u in self.upgrades:  # Тоже самое для каждого апгрейда
            if self.upgrades[u].require:
                r += self.upgrades[u].require
        return r

    @property
    def inaccessability(self):
        return self.type.inaccessability + self.upgrades.sum("inaccessability")

    def add_upgrade(self, upgrade):
        """
        Функция для улучшения логова
        :param upgrade: - название добавляемого апгрейда
        """
        self.upgrades.add(upgrade, deepcopy(data.lair_upgrades[upgrade]))
        # замена улучшений, если это необходимо
        if 'replaces' in self.upgrades[upgrade].keys() and \
            self.upgrades[upgrade]['replaces'] in self.upgrades:
            del self.upgrades[self.upgrades[upgrade]['replaces']]
