# coding=utf-8

import random
import data
import girls_data
import mob_data
import girls
import treasures
from data import get_modifier
from copy import deepcopy
import renpy.exports as renpy
import renpy.store as store
from characters import Fighter, Mortal, Talker, Thief, Knight, Enemy
from utils import call, tuples_sum, get_random_image
from points import Mobilization, Poverty, Army
from lair import Lair

class Game(store.object):
    _win = False
    _defeat = False
    _dragons_used = 0  # Количество использованных за игру драконов
    lair = None
    _quest = None
    _quest_threshold = None
    _quest_text = None

    def __init__(self, adv_character=None, nvl_character=None):
        """
        :param adv_character: Базовый класс для ADV-режима
        :param nvl_character: Базовый класс для NVL-режима
        """
        self.adv_character = adv_character
        self.nvl_character = nvl_character
        self.mobilization = Mobilization()  # Мобилизацию нужно ввести до того как появится первый дракон
        self.poverty = Poverty()
        self.army = Army()
        self._year = 0  # текущий год
        self._quest_time = 0  # год окончания квеста
        self.currentCharacter = None  # Последний говоривший персонаж. Используется для поиска аватарки.
        self.unique = []  # список уникальных действий для квестов

        self._dragon = None

        self.narrator = Talker(game_ref=self, kind='nvl')
        self.foe = None
        self.girl = None

        self.dragon_parent = None
        
    @property
    def dragon(self):
        return self._dragon

    @dragon.setter
    def dragon(self, new_dragon):
        self.mobilization.reset()
        new_dragon._gift = None
        self._dragon = new_dragon
        if self._dragons_used > 0:  # Если это не первый дракон, то
            self.year += 10  # накидываем 10 лет на вылупление и прочие взращивание-ботву
        self._dragons_used += 1
        if not store.freeplay:
            self.set_quest()
        self.thief = None  # Вора не создаем, потому что его по умолчанию нет. Он возможно появится в первый сон.
        self.knight = None  # Рыцаря не создаем, потому что его по умолчанию нет. Он возможно появится в первый сон.
        self.girls_list = girls.GirlsList(game_ref=self, base_character=self.adv_character)
        self.create_lair()

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        if value >= self._year:
            self._year = value
        else:
            raise Exception("Время не может течь назад")

    @staticmethod
    def save():
        """
        Логика сохранения игры.
        """
        renpy.rename_save("1-1", "1-2")  # Переименовываем старый сейв
        renpy.take_screenshot()  # Делаем скриншот для отображения в сейве
        renpy.save("1-1")  # Сохраняем игру
        return True

    @staticmethod
    def save_freegame():
        renpy.rename_save("1-3", "1-4")
        renpy.take_screenshot()
        renpy.save("1-3")

    def next_year(self):
        """
        Логика смены года.
        Проверки на появление/левелап/рейд рыцаря/вора.
        Изменение дурной славы.
        Попытки бегства женщин.
        Что-то ещё?
        """
        call(data.game_events["sleep_new_year"])
        self.year += 1
        self.dragon.age += 1
        # Платим за службу, проверяется в начале года
        for upgrade in self.lair.upgrades.keys():
            if type(self.lair.upgrades) == type(self.lair.upgrades[upgrade]) and \
                    'cost' in self.lair.upgrades[upgrade].keys():
                salary = self.lair.treasury.get_salary(self.lair.upgrades[upgrade]['cost'])
                if salary:
                    if renpy.config.debug:
                        summ = 0
                        for salary_i in salary:
                            summ += salary_i.cost
                        salary_tuple = (self.lair.upgrades[upgrade]['name'], summ - self.lair.upgrades[upgrade]['cost'])
                        self.narrator(u"%s в качестве платы за год воруют: %s ф." % salary_tuple)
                    salary = self.lair.treasury.treasures_description(salary)
                    salary_tuple = (self.lair.upgrades[upgrade]['name'], ' '.join(salary))
                    self.narrator(u"%s в качестве платы за год получают:\n %s" % salary_tuple)
                else:
                    self.narrator(u"%s не получили обещанной платы и уходят." % self.lair.upgrades[upgrade]['name'])
                    del self.lair.upgrades[upgrade]
        # Применяем разруху накопленную за год с учетом отстройки
        self.poverty.value -= 1
        self.poverty.apply_planned()
        # Действия с девушками каждый год
        self.girls_list.next_year()

        # Изменяем уровень мобилизации
        # Для начала считаем желаемый уровень мобилизации
        desired_mobilization = self.dragon.reputation.level - self.poverty.value
        # Затем
        # Затем считаем есть ли разница с текущим уровнем мобилизации
        mobilization_delta = desired_mobilization - self.mobilization.level
        if mobilization_delta != 0:  # И если есть разница
            # Увеличиваем  или  уменьшаем на единицу 
            if mobilization_delta > 0:
                self.mobilization.level += 1
            else:
                self.mobilization.level -= 1

        # Если вора нет, то пробуем создать его
        if self.thief is None or self.thief.is_dead:
            if renpy.config.debug:
                self.narrator(u"Вора не было или он был мертв, попробуем его создать.")
            self._create_thief()
            if self.thief is None:
                if renpy.config.debug:
                    self.narrator(u"Вор не появился.")
                call(data.game_events["no_thief"])
            else:
                if renpy.config.debug:
                    self.narrator(u"Вор появился.")
                self.thief.event("spawn")
        else:  # Иначе пробуем его пустить на дело
            if self.thief.forced_to_rob or \
               random.choice(range(6)) in range(
                    1 + len(self.thief.items)):  # Шанс 1 + количество шмота на воре, что он пойдет на дело
                # Идем на дело
                if renpy.config.debug:
                    self.narrator(u"Вор идет на дело")
                self.thief.steal(self.lair)
            else:
                if renpy.config.debug:
                    self.narrator(u"Вору ссыкотно, надо бы подготовиться.")
                self.thief.event("prepare")
                if random.choice(range(3)) == 0:  # C 33% шансом получаем шмотку
                    self.thief.event("prepare_usefull")
                    self.thief.receive_item()
                    if renpy.config.debug:
                        self.narrator(u"Вор получил %s" % self.thief.last_received_item.name)
                else:
                    if renpy.config.debug:
                        self.narrator(u"Но вместо этого вор весь год бухает.")
                    self.thief.event("prepare_useless")
        # Если рыцаря нет, то пробуем создать его
        if self.knight is None or self.knight.is_dead:
            if renpy.config.debug:
                self.narrator(u"Рыцаря не было или он был мертв, попробуем его создать.")
            self._create_knight()
            if self.knight is None:
                if renpy.config.debug:
                    self.narrator(u"Рыцарь не появился.")
                call(data.game_events["no_knight"])
            else:
                if renpy.config.debug:
                    self.narrator(u"Рыцарь появился.")
                self.knight.event("spawn")
        else:  # Иначе пробуем его пустить на дело
            # Шанс 1 + количество небазового шмота на рыцаре из 7, что он пойдет на дело
            if self.knight.forced_to_challenge or \
               random.choice(range(7)) in range(
                    1 + self.knight.enchanted_equip_count):
                # Идем на дело
                self.knight.go_challenge()
            # Если рыцарь не идет на дело, то он пробует подготовиться получше.
            else:
                if renpy.config.debug:
                    self.narrator(u"Рыцарю ссыкотно, надо бы подготовиться.")
                self.knight.event("prepare")
                if random.choice(range(3)) == 0:  # C 33% шансом получаем шмотку
                    self.knight.event("prepare_usefull")
                    self.knight.enchant_equip()
                    if renpy.config.debug:
                        self.narrator(u"Рыцарь получил %s" % self.knight.last_received_item.name)
                else:
                    if renpy.config.debug:
                        self.narrator(u"Но вместо этого рыцарь весь год бухает.")
                    self.knight.event("prepare_useless")
        return

    def sleep(self):
        """
        Рассчитывается количество лет которое дракон проспит.
        Сброс характеристик дракона.
        """
        call(data.game_events["sleep_start"])
        time_to_sleep = self.dragon.injuries + 1
        # Сбрасываем характеристики дракона
        self.dragon.rest()
        # Действия с девушками до начала сна
        self.girls_list.before_sleep()
        # Спим
        i = 0
        while self.dragon.is_alive and i < time_to_sleep:
            i += 1
            self.next_year()
            # По идее тут мы должны завершить сон
            # if self.dragon.is_dead:
            #    return
        # Обнуляем накопленные за бодрствование очки мобилизации
        self.dragon.reputation.reset_gain()
        # Действия с девушками после конца сна    
        self.girls_list.after_awakening()
        # Проверка срока выполнения квеста
        if (self.quest_time <= 0) and not store.freeplay:
            call('lb_location_mordor_questtime')
        call(data.game_events["sleep_end"])

    def create_foe(self, foe_type):
        """ Создание противника заданного типа

        :param foe_type: Тип создаваемого противника
        :return:
        """
        self.foe = Enemy(foe_type)

    def _create_thief(self, thief_level=None):
        """
        Проверка на появление вора.
        :param thief_level: Начальный уровень вора. Если не указан, то уровень определяется исходя из Дурной славы.
        """
        # Если уровень вора не указан, то идет стандартная проверка на появление.
        if thief_level is None and random.choice(range(1, 5 + (self.dragon.reputation.level + 1), 1)) in \
                    range(self.dragon.reputation.level + 1):
            thief_level = Thief.start_level(self.dragon.reputation.level)
        if thief_level > 0:
            self.thief = Thief(level=thief_level, treasury=self.lair.treasury, game_ref=self)
        else:
            self.thief = None

    def _create_knight(self, knight_level=None):
        """
        Создание рыцаря.
        """
        # Если уровень рыцаря не указан, то идет стандартная проверка на появление.
        if knight_level is None and random.choice(range(1, 5 + (self.dragon.reputation.level + 1), 1)) in \
                    range(self.dragon.reputation.level + 1):
            knight_level = Knight.start_level(self.dragon.reputation.level)
        if knight_level > 0:
            self.knight = Knight(level=knight_level, game_ref=self)
        else:
            self.knight = None

    def create_lair(self, lair_type=None):
        """
        Создание нового логова.
        """
        # Выпускаем всех женщин в прошлом логове на свободу. 
        self.girls_list.free_all_girls()

        if lair_type is not None:
            # Если меняется логово на лучшее - сохраняем сокровищницу
            save_treas = self.lair.treasury
            # Создаем новое логово
            self.lair = Lair(lair_type)
            data.achieve_target(self.lair.type_name, "lair")#событие для ачивок
            # Копируем сокровищницу из прошлого логова
            self.lair.treasury = save_treas
        else:
            # определяем логово по умолчанию
            lair_list = []
            mods = self.dragon.modifiers()
            for lair in data.lair_types.iterkeys():
                # просматриваем логова, выдаваемые автоматически при выполнении требований
                if 'prerequisite' in data.lair_types[lair]:
                    prerequisite_list = data.lair_types[lair]['prerequisite']  # получаем список требований к дракону
                    prerequisite_exists = True  # временная переменная для требований
                    for prerequisite in prerequisite_list:  # просматриваем список требований
                        # удостоверяемся, что список требований выполнен
                        prerequisite_exists = prerequisite_exists and prerequisite in mods
                    if prerequisite_exists:
                        # если список требований выполнен, добавляем логово к списку
                        lair_list.append((data.lair_types[lair].name, lair))
            if len(lair_list) == 0:
                lair_type = 'impassable_coomb'  # список логов пуст, выбираем начальное
            elif len(lair_list) == 1:
                lair_type = lair_list[0][1]  # в списке одно логово, выбираем его автоматически
            else:
                lair_list.insert(0, (u"Выберите логово:", None))
                lair_type = renpy.display_menu(lair_list)  # в списке больше одного логова, даём список на выбор
            self.lair = Lair(lair_type)
            data.achieve_target(self.lair.type_name, "lair")# событие для ачивок

    def set_quest(self):
        lvl = self.dragon.level
        # проходим весь список квестов
        quests = []
        for quest_i in xrange(len(data.quest_list)):
            quest = data.quest_list[quest_i]
            # находим квест, подходящий по уровню, не уникальный или ещё не выполненный за текущую игру
            is_applicable = ('prerequisite' not in quest or quest['prerequisite'] in self.unique)
            is_applicable = is_applicable and ('unique' not in quest or quest['unique'] not in self.unique)
            is_applicable = is_applicable and quest['min_lvl'] <= lvl <= quest['max_lvl']
            if 'anatomy_required' in quest:
                any_applicable = False
                for require in quest['anatomy_required']:
                    curr_applicable = True
                    for subrequire in require.keys():
                        curr_applicable = curr_applicable and \
                            self.dragon.modifiers().count(subrequire) >= require[subrequire]
                    any_applicable = any_applicable or curr_applicable
                is_applicable = is_applicable and any_applicable
            if is_applicable:
                quests.append(quest)
        self._quest = random.choice(quests)
        # Задание года окончания выполнения квеста
        self._quest_time = self._year
        if 'fixed_time' in self._quest:
            self._quest_time += self._quest['fixed_time']
        if 'lvlscale_time' in self._quest:
            self._quest_time += lvl * self._quest['lvlscale_time']
        # Задание порогового значения, если это необходимо
        self._quest_threshold = 0
        if 'fixed_threshold' in self._quest:
            self._quest_threshold += self._quest['fixed_threshold']
        if 'lvlscale_threshold' in self._quest:
            self._quest_threshold += lvl * self._quest['lvlscale_threshold']
        self._quest_text = self._quest['text'].format(*[self._quest_threshold])

    @property
    def is_quest_complete(self):
        """
        Проверяет выполнен ли квест
        TODO: проверки на выполнение квестов. Сразу после добавления квестов.
        """
        task_name = self._quest['task']
        current_level = 0
        reached_list = []
        if task_name == 'autocomplete':  # задача всегда выполнена
            return True
        elif task_name == 'reputation':  # проверка уровня репутации
            current_level = self.dragon.reputation.level
        elif task_name == 'wealth':  # проверка стоимости всех сокровищ
            current_level = self.lair.treasury.wealth
        elif task_name == 'gift':  # проверка стоимости самого дорогого сокровища
            current_level = self.lair.treasury.most_expensive_jewelry_cost
        elif task_name == 'poverty':  # проверка понижения уровня мобилизации из-за разрухи
            current_level = self.mobilization.decrease
        elif task_name == 'offspring':  # проверка рождения потомка
            reached_list.extend(self.girls_list.offspring)
        elif task_name == 'lair':  # проверка типа логова и его улучшений
            reached_list.extend(self.lair.upgrades.keys())
            reached_list.append(self.lair.type_name)
        elif task_name == 'event':  # проверка событий
            reached_list.extend(self.dragon.events)
        # проверка требований
        if 'task_requirements' in self._quest and type(self._quest['task_requirements']) is str:
            quest_complete = self._quest['task_requirements'] in reached_list
        elif 'task_requirements' in self._quest:
            quest_complete = True
            for require in self._quest['task_requirements']:
                # нужно выполнить весь список требований
                if type(require) is str:
                    reached_requirements = require in reached_list
                else:
                    reached_requirements = False
                    for sub_require in require:
                        if type(sub_require) is str:
                            variant_reached = sub_require in reached_list
                        else:
                            # для этого требования в списке достаточно выполнить один из нескольких вариантов
                            variant_reached = True
                            for var_sub_require in sub_require:
                                variant_reached = variant_reached and var_sub_require in reached_list
                        reached_requirements = reached_requirements or variant_reached
                quest_complete = quest_complete and reached_requirements
        else:
            quest_complete = True
        # проверка препятствий выполнения квеста
        if 'task_obstruction' in self._quest:
            for obstruction in self._quest['task_obstruction']:
                quest_complete = quest_complete and obstruction not in reached_list
        quest_complete = quest_complete and current_level >= self._quest_threshold
        return quest_complete

    def complete_quest(self):
        """
        Посчитать текущий квест выполненным
        """
        # добавляем всё неправедно нажитое богатство в казну Владычицы
        self.army.money += self.lair.treasury.wealth
        # указываем, что уникальный квест уже выполнялся
        if 'unique' in self._quest:
            self.unique.append(self._quest['unique'])

    @property
    def quest_task(self):
        return self._quest['task']

    @property
    def quest_text(self):
        return self._quest_text

    @property
    def quest_time(self):
        """
        Сколько лет осталось до конца квеста
        """
        return self._quest_time - self._year

    @quest_time.setter
    def quest_time(self, value):
        self._quest_time = self._year + value

    @property
    def quest_time_text(self):
        number = self.quest_time
        if number == 1:
            return u"Последний год на выполнение задания!"
        elif 1 < number < 5:
            return u"Тебе нужно выполнить задание за %s года!" % str(number)
        elif (number % 100 > 20) and (number % 10 == 1):
            return u"Задание нужно выполнить за %s год." % str(number)
        elif (number % 100 > 20) and (1 < number % 10 < 5):
            return u"Задание нужно выполнить за %s года." % str(number)
        else:
            return u"Задание нужно выполнить за %s лет." % str(number)

    def choose_spell(self, back_message=u"Вернуться"):
        """
        Выводит меню для выбора заклинания
        :param back_message: название для пункта меню с отказом от выбора.
        :return: При выборе какого-либо заклинания кастует его и возвращает True,
                 при отказе от выбора возвращает False.
        """
        spells_menu = []
        for spell in data.spell_list.keys():
            # Добавляем в список только актуальные заклинания.
            if spell not in self.dragon.spells and (spell is not 'spellbound_trap' or 'magic_traps' not in self.lair.upgrades):
                spells_menu.append((data.spell_list_rus[spell], spell))
        spells_menu = sorted(spells_menu, key=lambda spell: spell[0])
        spells_menu.append((back_message, 'back'))
        spell_name = renpy.display_menu(spells_menu)
        if spell_name == 'back':
            return False
        else:
            if spell_name == 'spellbound_trap':
                self.lair.add_upgrade('magic_traps')
            else:
                self.dragon.add_effect(spell_name)
            return True

    def interpolate(self, text):
        """
        Функция заменяющая переменные в строке на актуальные данные игры
        """
        return text % self.format_data

    @property
    def format_data(self):
        substitutes = {
            "dragon_name": self.dragon.name,
            "dragon_name_full": self.dragon.fullname,
            "dragon_type": self.dragon.kind,
        }
        if self.foe is not None:
            substitutes["foe_name"] = self.foe.name
        return substitutes

    @property
    def is_won(self):
        # Проверка параметров выиграна уже игра или нет
        if not self._win:
            # Проверяем выиграли ли мы
            pass
        return self._win

    def win(self):
        """
        Форсируем выиграть игру
        """
        self._win = True

    @property
    def is_lost(self):
        # Проверка параметров проиграна уже игра или нет
        if not self._defeat:
            # Проверяем проиграли ли мы
            pass
        return self._defeat

    def defeat(self):
        """
        Форсируем проиграть игру
        """
        self._defeat = True