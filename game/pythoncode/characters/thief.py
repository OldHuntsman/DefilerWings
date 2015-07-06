#!/usr/bin/env python
# coding=utf-8

# TODO: реврайт вора через modifiers

import random
from pythoncode import data
import renpy.exports as renpy
from pythoncode.utils import call, get_random_image
from pythoncode.data import achieve_fail
from copy import deepcopy
from mortal import Mortal
from talker import Talker
                
                
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
        self.avatar = get_random_image(u"img/avahuman/thief")
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

    def steal(self, lair=None, dragon=None):
        """
        Вор пытается урасть что-нибудь.
        :param lair: Логово из которого происходит кража
        :param dragon: Дракон, логово которого грабим
        """
        thief = self

        if lair is None:  # Нет логова, нет краж. Вообще такого быть не должно.
            raise Exception("No lair available")
        if dragon is None:
            raise Exception("No dragon available")

        # Для начала пытаемся понять можем ли мы попасть в логово:
        if not lair.reachable(thief.abilities.list("provide") + thief.items.list("provide")):
            # Добраться не можем, с 50% шансом получаем шмотку
            thief.event("lair_unreachable")
            if random.choice(range(2)) == 0:
                thief.receive_item()
            else:
                thief.event("receive_no_item")

        thief.event("lair_enter")

        luck = thief.skill
        # Проверка неприступности
        self.event("checking_accessability")
        # Если нет схемы тайных проходов, то с 33% шансом снижаем удачу вора за каждую единицу неприступности
        if "scheme" not in thief.items:
            for i in range(lair.inaccessability):
                if random.choice(range(3)) == 0:
                    luck -= 1

        # Проверка, осилили ли неприступность
        if luck < 0:
            thief.die("inaccessability")
            thief.event("die_inaccessability")
            return
        else:
            self.event("checking_accessability_success")

        # Проверка ловушек и стражей
        self.event("trying_to_avoid_traps_and_guards")

        # Выбираем ловушки которые имеет смысл "обходить"
        # Обходим только ловушки с ненулевой защитой
        upgrades = (u for u in lair.upgrades if data.lair_upgrades[u].protection != 0)
        for upgrade in upgrades:

            thief.event("start_trap", trap=upgrade)
            # Если у нас есть шмотка или скилл для обхода ловушки
            if upgrade in thief.abilities.list("avoids") or upgrade in thief.items.list("avoids"):
                self.event("pass_trap", trap=upgrade)
                # То переходим к следущей ловушке
                continue

            # 1/3 что вора ловушка заденет
            for i in range(data.lair_upgrades[upgrade].protection):
                if random.choice(range(3)) > 0:
                    luck -= 1

            if luck > 0:
                thief.event("pass_trap", trap=upgrade)
            elif luck == 0:
                self.event("retreat_and_try_next_year")
                return
            elif luck < 0:
                thief.die(upgrade)
                thief.event("die_trap", trap=upgrade)
                return
            thief.event("end_trap", trap=upgrade)

        # У вора кончилась удача, отступаем
        if luck == 0:
            self.event("retreat_and_try_next_year")
            return

        # На всякий случай проверяем что у нас еще осталась удача.
        assert luck > 0

        # Начинаем вычищать логово
        self.event("starting_to_rob_the_lair")

        # Если сокровищница пуста, то вор уходит на пенсию
        if lair.treasury.wealth <= 0:
            self.event("lair_empty")
            # Закончили грабить. Уходим на пенсию.
            self.retire()
            return

        attempts = luck
        if "greedy" in thief.abilities:
            attempts += 1
        if "bottomless_sac" in thief.items:
            attempts *= 2

        # Берем шмотки
        stolen_items = lair.treasury.rob_treasury(attempts)  # Вор что-то украл
        for i in xrange(len(stolen_items)):
            if "sleep_dust" in thief.items or "trickster" in thief.abilities or random.choice(
                    range(10)) in range(5 - thief.skill):
                self.event("took_an_item", item=stolen_items[i])
            else:
                # Мы разбудили дракона
                if renpy.config.debug:
                    thief(u"Разбудил дракона")
                dragon.add_event('thief_killer')
                lair.treasury.receive_treasures(stolen_items)  # Дракон возвращает что награбил вор.
                self.event("awakened_the_dragon", stolen_items=stolen_items)
                thief.die("wake_up")
                return

        achieve_fail("lost_treasure")  # Отмечаем для ачивки, что потеряли сокровище из-за вора
        self.event('steal_items', items=stolen_items)
        # Закончили грабить. Уходим на пенсию.
        self.retire()
        return

    def die(self, reason=None):
        """
        Вор умирает
        """
        for i in self.items:
            self.treasury.thief_items.append(deepcopy(self.items[i]))
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
