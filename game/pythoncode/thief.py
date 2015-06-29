#!/usr/bin/env python
# coding=utf-8

# TODO: реврайт вора через modifiers

import random
import data
import renpy.exports as renpy
from core import get_avatar
from utils import call
from copy import deepcopy
from characters import Mortal, Talker

class Thief(Talker, Mortal):
    """
    Класс вора.
    """
    last_received_item = None

    def __init__(self, level=1, treasury=None, *args, **kwargs):
        super(Thief, self).__init__(*args, **kwargs)
        self._alive = True
        self._skill = level
        self.name = "%s %s" % (random.choice(data.thief_first_names), random.choice(data.thief_last_names))
        self.abilities = data.Container("thief_abilities")
        self.items = data.Container("thief_items")
        # Определяем способности вора
        ability_list = [a for a in data.thief_abilities]  # Составляем список из возможных способностей
        ability_list += [None for _ in range(len(ability_list))]  # Добавляем невалидных вариантов
        for level in range(self._skill):
            ab = random.choice(ability_list)
            if ab is not None and ab not in self.abilities:
                self.abilities.add(ab, deepcopy(data.thief_abilities[ab]))
        # прочее
        self.treasury = treasury  # Ссылка на сокровищницу.
        self.avatar = get_avatar(u"img/avahuman/thief")
        self.forced_to_rob = False    # Обязан ли ограбить дракона, когда тот пойдет спать.

    @property  # Read-Only
    def skill(self):
        return self._skill + self.items.sum("level")

    @property
    def title(self):
        """
        :return: Текстовое представление 'звания' вора.
        """
        try:
            return data.thief_titles[self.skill - 1]
        except:
            raise Exception("Cannot determine title for skill level %s" % self.skill)

    def receive_item(self):
        item_list = [i for i in data.thief_items if i not in self.items]
        if len(item_list) > 0:
            new_item = data.thief_items[random.choice(item_list)]
            self.items.add(new_item.id, new_item)
            self.last_received_item = new_item
            self.event('receive_item', item=new_item)
            return True
        else:
            return False

    def description(self):
        """
        Описание вора, возвращает строку с описанием.
        """
        d = []
        if self.is_dead:
            d.append(u"Вор мёртв")
            return u"\n".join(d)
        d.append(u"Мастерство: %s (%d)" % (self.title, self.skill))
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
        """
        Вор пытается урасть что-нибудь.
        :param lair: Логово из которого происходит кража
        """
        thief = self

        if lair is None:  # Нет логова, нет краж. Вообще такого быть не должно.
            raise Exception("No lair available")
        # Для начала пытаемся понять можем ли мы попасть в логово:
        if lair.reachable(thief.abilities.list("provide") + thief.items.list("provide")):
            if renpy.config.debug:
                thief(u"Логово доступно, пытаюсь добратья до него")
            thief.event("lair_enter")
            # Логика сломанных предметов
            if renpy.config.debug:
                thief(u"Проверяем предметы на работоспособность, чтобы попасть влогово")
            self.event("checking_items")
            for i in thief.items:
                if renpy.config.debug:
                    thief(u"Использую %s" % thief.items[i].name)
                self.event("checking_item", item=thief.items[i])
                if thief.items[i].cursed:
                    for f in thief.items[i].fails:
                        if f in lair.requirements():
                            if renpy.config.debug:
                                thief(u"Погиб из-за %s" % thief.items[i].name)
                            thief.die(i)
                            thief.event("die_item", item=thief.items[i])
                            return
                    else:
                        if renpy.config.debug:
                            thief(u"Item: %s is good!" % thief.items[i].name)
                        self.event("checking_item_success", item=thief.items[i])
                else:
                    if renpy.config.debug:
                        thief(u"Item: %s is good!" % thief.items[i].name)
                    self.event("checking_item_success", item=thief.items[i])

            if renpy.config.debug:
                thief(u"All items passed!")
            self.event("checking_items_success")
            
            # TODO: логика нормальных предметов
            luck = thief.skill
            # Проверка неприступности
            if renpy.config.debug:
                thief(u"Проверяю неприступность")
            self.event("checking_accessability")
            for i in range(lair.inaccessability):
                if "scheme" not in thief.items and random.choice(range(3)) == 0:
                    luck -= 1
            if luck < 0:
                if renpy.config.debug:
                    thief(u"Погиб из-за неприступности")
                thief.die("inaccessability")
                thief.event("die_inaccessability")
                return
                
            if renpy.config.debug:
                thief(u"I can get into the Layer!")
            self.event("checking_accessability_success")
            
            # Проверка ловушек и стражей
            if renpy.config.debug:
                thief(u"Пробую обойти ловушки и стражей")
            self.event("trying_to_avoid_traps_and_guards")    
                
            for upgrade in lair.upgrades:
                if renpy.config.debug:
                    thief(u"Обхожу %s" % upgrade)
                thief.event("start_trap", trap=upgrade)
                if upgrade in thief.items.list("fails"):  # Если для апгрейда есть испорченный предмет
                    if renpy.config.debug:
                        thief(u"Предмет для %s подвел меня" % upgrade)
                    self.die(upgrade)  # Умираем
                    thief.event("die_trap", trap=upgrade)
                    return
                # Если у нас есть шмотка или скилл для обхода ловушки
                if upgrade in thief.abilities.list("avoids") or upgrade in thief.items.list("avoids"):
                    if renpy.config.debug:
                        thief(u"Я хорошо подготовился и предметы помогли обойти мне %s" % upgrade)
                    self.event("pass_trap", trap=upgrade)
                    # То переходим к следущей ловушке
                    continue
                # Если улучшение не дает защиты
                if data.lair_upgrades[upgrade].protection == 0:
                    if renpy.config.debug:
                        thief(u"Обошел %s, т.к. он не защищает от меня." % upgrade)
                    thief.event("pass_trap_no_influence", trap=upgrade)
                else:
                    for i in range(data.lair_upgrades[upgrade].protection):
                        luck_drain = 0
                        if random.choice(range(3)) == 0:
                            if renpy.config.debug:
                                thief(u"luck -= 1, %d remaining" % luck)
                            luck -= 1
                            luck_drain += 1
                        else:
                            thief(u"На удаче затащил %s" % upgrade)
                        if luck >= 0:
                            thief.event("pass_trap_by_luck", trap=upgrade, luck_drain=luck_drain)
                        if luck < 0:
                            if renpy.config.debug:
                                thief(u"Не сумел обойти %s" % upgrade)
                            thief.die(upgrade)
                            thief.event("die_trap", trap=upgrade)
                            return
                thief.event("end_trap", trap=upgrade)
            if luck == 0:
                # Отступаем
                if renpy.config.debug:
                    thief(u"Ниосилить, попробую в следущем году")
                self.event("retreat_and_try_next_year") 
            else:
                assert luck > 0
                # Грабим логово
                # TODO: Добавить проклятые вещи
                if renpy.config.debug:
                    thief(u"Начинаю вычищать логово")
                self.event("starting_to_rob_the_lair")
                attempts = luck
                if "greedy" in thief.abilities:
                    attempts += 1
                if "bottomless_sac" in thief.items:
                    if not thief.items.bottomless_sac.cursed:
                        attempts *= 2
                    else:
                        attempts = 0
                if lair.treasury.wealth > 0:  # Если в сокровищнице хоть что-нибудь есть
                    # Берем шмотки
                    stolen_items = lair.treasury.rob_treasury(attempts)  # Вор что-то украл
                    for i in xrange(len(stolen_items)):
                        if "sleep_dust" in thief.items or "trickster" in thief.abilities or random.choice(
                                range(10)) in range(5 - thief.skill):
                            if renpy.config.debug:
                                thief(u"Взял шмотку %s" % stolen_items[i])
                            self.event("took_an_item", item=stolen_items[i])
                        else:
                            # Мы разбудили дракона
                            if renpy.config.debug:
                                thief(u"Разбудил дракона")
                            self._gameRef.dragon.add_event('thief_killer')
                            lair.treasury.receive_treasures(stolen_items)  # Дракон возвращает что награбил вор.
                            self.event("awakened_the_dragon", stolen_items=stolen_items)
                            thief.die("wake_up")
                            return
                else:
                    if renpy.config.debug:
                        thief(u"В сокровищнице нечего брать. Сваливаю.")
                    self.event("lair_empty")
                    # Закончили грабить. Уходим на пенсию.
                    self.retire()
                    return
                from data import achieve_fail
                achieve_fail("lost_treasure")#событие для ачивок
                self.event('steal_items', items=stolen_items)
                # Закончили грабить. Уходим на пенсию.
                self.retire()
        else:  # До логова добраться не получилось, получаем предмет c 50%м шансом
            if renpy.config.debug:
                thief(u"Не добрался до логова")
            thief.event("lair_unreachable")
            if random.choice(range(2)) == 0:
                thief.receive_item()
            else:
                thief.event("receive_no_item")
        return

    def die(self, reason=None):
        """
        Вор умирает
        """
        for i in self.items:
            self.treasury.thief_items.append(deepcopy(self.items[i]))
        if renpy.config.debug:
            self(u"Я погиб!")
        self._alive = False

    def retire(self):
        self.event("retire")
        # Делаем вид что умерли и концы в воду.
        self._alive = False
        return

    @staticmethod
    def start_level(reputation=0):
        skill = 0
        for i in range(3 + reputation):
            if random.choice(range(3)) == 0:
                skill += 1
        return skill if skill < Thief.max_level() else Thief.max_level()

    @staticmethod
    def max_level():
        return len(data.thief_titles)

    def event(self, event_type, *args, **kwargs):
        if event_type in data.thief_events:
            if data.thief_events[event_type] is not None:
                call(data.thief_events[event_type], *args, thief=self, **kwargs)
        else:
            raise Exception("Unknown event: %s" % event_type)
        return
