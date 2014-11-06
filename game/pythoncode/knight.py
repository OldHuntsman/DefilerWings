#!/usr/bin/env python
# coding=utf-8

from core import Fighter
import random
import data

class Knight(Fighter):
    """
    Класс рыцаря.
    Набросок для тестирования боя.
    Спутников, особенности и снаряжение предпологается засовывать в переменную _modifiers
    """

    def __init__(self, *args, **kwargs):
        """
        Здесь должна быть генерация нового рыцаря.
        """
        super(Knight, self).__init__(*args, **kwargs)
        self.name = u"Сер Ланселот Озёрный"
        self.name = "Сэр %s %s" % (random.choice(data.knight_first_names), random.choice(data.knight_last_names))
        self.power = 1
        self.abilities = []
        self.equipment = [u"щит", u"меч", u"броня", u"копьё", u"скакун", u"спутник"]

    def modifiers(self):
        return self._modifiers + self.abilities + self.equipment

    def attack(self):
        a = super(Knight, self).attack()
        if "liberator" in self.modifiers():
            # TODO: подумать как получаем ссылку на логово
            # Увеличиваем атаку в соответствии со списком женщин в логове
            raise NotImplementedError
        a['base'][0] + self.power
        return a

    def protection(self):
        p = super(Knight, self).protection()
        if "liberator" in self.modifiers():
            # Увеличиваем защиту в соответствии со списком женщин в логове
            raise NotImplementedError
        p['base'][0] + self.power
        return p

    def title(self):
        """
        :return: Текстовое представление 'звания' рыцаря.
        """
        try:
            return data.knight_titles[self.power - 1]
        except:
            raise Exception(u"Недопустимое значение поля power")

    def upgrade(self):
        """
        Метод вызвается если рыцать не пошел драться с драконом.
        Добавляет новое снаряжение.
        """
        raise NotImplementedError
        
    def event(self, event_type, *args, **kwargs):
        if event_type in data.knight_events and data.knight_events[event_type] is not None:
            if type(data.knight_events[event_type]) is str:
                call(data.knight_events[event_type], *args, knight=self, **kwargs)
            elif type(data.knight_events[event_type]) is list:
                for i in data.knight_events[event_type]:
                    call(i, *args, knight=self, **kwargs)
        return
