#!/usr/bin/env python
# coding=utf-8

from core import Fighter
import renpy.exports as renpy
import random
import os
import data
from copy import deepcopy

class Knight(Fighter):
    """
    Класс рыцаря.
    Набросок для тестирования боя.
    Спутников, особенности и снаряжение предпологается засовывать в переменную _modifiers
    """

    def __init__(self, level = 1, *args, **kwargs):
        """
        Здесь должна быть генерация нового рыцаря.
        """
        super(Knight, self).__init__(*args, **kwargs)
        self._alive = True
        self.name = u"Сер Ланселот Озёрный"
        self.name = "Сэр %s %s" % (random.choice(data.knight_first_names), random.choice(data.knight_last_names))
        self.lelel = level
        self.power = level
        self.abilities = data.Container("knight_abilities")
        ability_list = [ a for a in data.knight_abilities ] # Составляем список из возможных способностей
        ability_list += [ None for i in range(len(ability_list)) ] # Добавляем невалидных вариантов
        for i in range(level):
            ab = random.choice(ability_list)
            if ab is not None and ab not in self.abilities:
                self.abilities.add(ab, deepcopy(data.knight_abilities[ab]))
        self._add_equip_slots([ "vest", "spear", "sword", "shield", "horse", "follower" ])
        self.equip(data.knight_items.basic_vest)
        self.equip(data.knight_items.basic_spear)
        self.equip(data.knight_items.basic_sword)
        self.equip(data.knight_items.basic_shield)
        self.equip(data.knight_items.basic_horse)
        self.equip(data.knight_items.basic_follower)
        self.bg = "game/img/scene/fight/knight/" + random.choice(os.listdir(os.path.join(renpy.config.basedir, "game/img/scene/fight/knight"))) # получаем название файла
    
    def is_alive(self):
        if self._alive:
            return True
        return False
    
    def is_dead(self):
        if not self._alive:
            return True
        return False
    
    def description(self):
        '''
        Описание рыцаря, возвращает строку с описанием.
        '''
        d = []
        if self.is_dead():
            d.append (u"Рыцарь мёртв")
            return u"\n".join(d)
        d.append(u"Сила: %s (%d)" % (self.title(), self.power))
        if self.abilities:
            d.append(u"Способности: ")
            for ability in self.abilities:
                d.append(u"    %s: %s" % (self.abilities[ability].name, self.abilities[ability].description))
        else:
            d.append(u"Способности отсутствуют")
        if self.items:
            d.append(u"Вещи:")
            for item in self.items:
                d.append(u"    %s: %s" % (self.items[item].name, self.items[item].description))
        else:
            d.append(u"Вещи отсутствуют")
        if len(self.modifiers()) > 0:
            d.append(u"Модификаторы: ")
            for i in self.modifiers():
                d.append(u"    %s" % (i))
        return u"\n".join(d)

    def modifiers(self):
        return self._modifiers + self._ability_modifiers() + self._item_modifiers()
    
    def _ability_modifiers(self):
        #Возвращает список модификторов из способностей
        #TODO: implement
        result = []
        for i in self.abilities:
            result.extend(self.abilities[i].modifiers)
        return result
    
    def _item_modifiers(self):
        #Возвращает список модификторов от вещей
        result = []
        for i in self.items:
            result.extend(self.items[i].modifiers)
        return result

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
    
    def enchant_equip(self):
        '''
        Рыцарь готовится к бою улучшая шмот.
        '''
        basic_types = [ i for i in self.items if self.items[i].basic ] #Какой шмот у рыцаря базового типа
        if len(basic_types) > 0: #У рыцаря есть не улучшенный шмот
            enchanted_type = random.choice(basic_types)
            new_item = random.choice(data.knight_items.select([('type',enchanted_type),("basic", False)]))
            self.equip(data.knight_items[new_item])
            self.event("receive_item", item=new_item)
    
    @staticmethod
    def start_level(reputation=0):
        skill = 0
        for i in range(3+reputation):
            if random.choice(range(3)) == 0:
                skill += 1
        return skill