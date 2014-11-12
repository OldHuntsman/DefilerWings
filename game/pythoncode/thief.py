#!/usr/bin/env python
# coding=utf-8

#TODO: реврайт вора через modifiers 

import random
import data
import renpy.exports as renpy
from core import Sayer, Mortal
from core import call
from copy import deepcopy

class Thief(Sayer, Mortal):
    """
    Класс вора.
    """
    last_received_item = None
    
    def __init__(self, level = 1, treasury = None, *args, **kwargs):
        super(Thief, self).__init__(*args, **kwargs)
        self._alive = True
        self._skill = level
        self.name = "%s %s" % (random.choice(data.thief_first_names), random.choice(data.thief_last_names))
        self.abilities = data.Container("thief_abilities")
        self.items = data.Container("thief_items")
        # Определяем способности вора
        ability_list = [ a for a in data.thief_abilities ] # Составляем список из возможных способностей
        ability_list = ability_list + [ None for i in range(len(ability_list)) ] # Добавляем невалидных вариантов
        for level in range(self._skill):
            ab = random.choice(ability_list)
            if ab is not None and ab not in self.abilities:
                self.abilities.add(ab, deepcopy(data.thief_abilities[ab]))
        # прочее
        self.treasury = treasury # Ссылка на сокровищницу.

    @property # Read-Only
    def skill(self):
        return self._skill + self.items.sum("level")
    
    def title(self):
        """
        :return: Текстовое представление 'звания' вора.
        """
        try:
            return data.thief_titles[self.skill - 1]
        except:
            raise Exception("Cannot determine title for skill level %s" % self.skill)

    def receive_item(self):
        item_list = [ i for i in data.thief_items if i not in self.items ]
        if len(item_list) > 0:
            new_item = data.thief_items[random.choice(item_list)]
            self.items.add(new_item.id, new_item)
            self.last_received_item = new_item
            self.event('receive_item', item=new_item)
            return True
        else:
            return False
    
    def description(self):
        '''
        Описание вора, возвращает строку с описанием.
        '''
        d = []
        if self.is_dead():
            d.append (u"Вор мёртв")
            return u"\n".join(d)
        d.append(u"Мастерство: %s (%d)" % (self.title(), self.skill))
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
        return u"\n".join(d)
    
    def steal(self, lair=None):
        '''
        Вор пытается урасть что-нибудь.
        :param lair: Логово из которого происходит кража
        '''
        lair = lair
        thief = self
        
        if lair is None: #Нет логова, нет краж. Вообще такого быть не должно.
            raise Exception("No lair available")
            return
        # Для начала пытаемся понять можем ли мы попасть в логово:
        if lair.reachable(thief.abilities.list("provide") + thief.items.list("provide")):
            if renpy.config.debug: thief(u"Логово доступно, пытаюсь добратья до него")
            thief.event("lair_enter")
            # Логика сломанных предметов
            if renpy.config.debug: thief(u"Проверяем предметы на работоспособность, чтобы попасть влогово")
            for i in thief.items:
                if renpy.config.debug: thief(u"Использую %s" % thief.items[i].name)
                if thief.items[i].cursed:
                    for f in thief.items[i].fails:
                        if f in lair.requirements():
                            if renpy.config.debug: thief(u"Погиб из-за %s" % thief.items[i].name)
                            thief.die(i)
                            thief.event("die_item", item=thief.items[i])
                            return
            # TODO: логика нормальных предметов
            luck = thief.skill
            # Проверка неприступности
            if renpy.config.debug: thief(u"Проверяю неприступность")
            for i in range(lair.inaccessability):
                if "scheme" not in thief.items and random.choice(range(3)) == 0:
                    luck -= 1
            if luck < 0:
                if renpy.config.debug: thief(u"Погиб из-за неприступности")
                thief.die ("inaccessability")
                thief.event("die_inaccessability")
            # Проверка ловушек и стражей
            if renpy.config.debug: thief(u"Пробую обойти ловушки и стражей")
            for upgrade in lair.upgrades:
                if upgrade in thief.items.list("fails"): #Если для апгрейда есть испорченный предмет
                    if renpy.config.debug: thief(u"Предмет для %s подвел меня" % upgrade)
                    die(upgrade)                        #Умираем
                    thief.event("die_trap", trap=upgrade)
                    return
                if ( upgrade in thief.abilities.list("avoids")   #Если у нас есть шмотка или скилл для 
                        or upgrade in thief.items.list("avoids")):  #Обхода ловушки
                    if renpy.config.debug: thief(u"Я хорошо подготовился и предметы помогли обойти мне %s" % upgrade)
                    continue                                  #Переходим к следущей
                for i in range(data.lair_upgrades[upgrade].protection):
                    if random.choice(range(3)) == 0:
                        luck -= 1
                    if luck < 0:
                        if renpy.config.debug: thief("Не сумел обойти %s" % upgrade)
                        thief.die(upgrade)
            if luck == 0:
                # Отступаем
                if renpy.config.debug: thief(u"Ниосилить, попробую в следущем году")
            else:
                assert luck > 0
                # Грабим логово
                # TODO: Добавить проклятые вещи
                if renpy.config.debug: thief(u"Начинаю вычищать логово")
                attempts = 1
                if "greedy" in thief.abilities:
                    attempts += 1
                if "bottomless_sac" in thief.items:
                    if not thief.items.bottomless_sac.cursed:
                        attempts *= 2
                    else:
                        attempts = 0
                for i in range(attempts):
                    if "sleep_dust" in thief.items or "trickster" in thief.abilities or random.choice(range(10)) in range(5 - thief.skill):
                        #Берем шмотку
                        stolen_items = lair.treasury.rob_treasury()
                        for stolen_item in stolen_items: #Вор что-то украл
                            self.event('receive_item', stolen_item)
                        thief(u"Взял бы шмотку, но ленивому хикке не написать сокровищницу")
                    else:
                        #Мы разбудили дракона
                        if renpy.config.debug: thief(u"Разбудил дракона")
                        thief.die("wake_up")
        else: #До логова добраться не получилось, получаем предмет c 50%м шансом
            if renpy.config.debug: thief(u"Не добрался до логова")
            thief.event("lair_unreachable")
            if random.choice(range(2)) == 0:
                thief.receive_item()
            else:
                thief.event("receive_no_item")
        return
    
    def check_luck(self, luck):
        '''
        Unused
        '''
        pass
    
    def die(self, reason=None):
        '''
        Вор умирает
        '''
        for i in self.items:
            self.treasury.thief_items.add(self.items[i].id, deepcopy(self.items[i]))
        if renpy.config.debug: self(u"Я погиб!")
        self._alive = False
    
    @staticmethod
    def start_level(reputation=0):
        skill = 0
        for i in range(3+reputation):
            if random.choice(range(3)) == 0:
                skill += 1
        return skill
    
    def event(self, event_type, *args, **kwargs):
        if event_type in data.thief_events and data.thief_events[event_type] is not None:
            if type(data.thief_events[event_type]) is str:
                call(data.thief_events[event_type], *args, thief=self, **kwargs)
            elif type(data.thief_events[event_type]) is list:
                for i in data.thief_events[event_type]:
                    call(i, *args, thief=self, **kwargs)
        return
