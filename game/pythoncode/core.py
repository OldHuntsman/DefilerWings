#!/usr/bin/env python
# coding=utf-8
import random
import math
import data
import battle
import mob_data
import girls
import treasures
from data import get_modifier
from copy import deepcopy
import renpy.exports as renpy
import renpy as renpy_internal
import renpy.store as store


def tuples_sum(tuple_list):
    return sum([first for first, _ in tuple_list]), sum([second for _, second in tuple_list])


class Game(store.object):
    _sleep_lvl = 0
    _win = False
    _defeat = False
    _dragons_used = 0  # Количество использованных за игру драконво

    def __init__(self, adv_character=None, nvl_character=None):
        """
        :param base_character: Базовый класс для персонажа. Скорее всего NVLCharacter.
        """
        from points import Mobilization, Poverty, Army
        from thief import Thief
        from knight import Knight

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
        self.thief = None  # Вора не создаем, потому что его по умолчанию нет. Он возможно появится в первый сон.
        self.knight = None  # Рыцаря не создаем, потому что его по умолчанию нет. Он возможно появится в первый сон.

        self.narrator = Sayer(gameRef=self, base_character=nvl_character)
        self.girls_list = girls.Girls_list(gameRef=self, base_character=adv_character)
        self.foe = None
        self.girl = None

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
        self.set_quest()
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

    def save(self):
        '''
        Логика сохранения игры.
        '''
        renpy.rename_save("1-1", "1-2")  # Переименовываем старый сейв
        renpy.take_screenshot()  # Делаем скриншот для отображения в сейве
        renpy.save("1-1")  # Сохраняем игру
        return True

    def save_freegame(self):
        renpy.rename_save("1-3", "1-4")
        renpy.take_screenshot()
        renpy.save("1-3")

    def next_year(self):
        '''
        Логика смены года.
        Проверки на появление/левелап/рейд рыцаря/вора.
        Изменение дурной славы.
        Попытки бегства женщин.
        Что-то ещё?
        '''
        self.year += 1
        self.dragon.age += 1
        # Применяем разруху накопленную за год с учетом отстройки
        self.poverty.value -= 1
        self.poverty.apply_planned()
        # Действия с девушками каждый год
        self.girls_list.next_year()
        # Платим за службу
        for upgrade in self.lair.upgrades.keys():
            if type(self.lair.upgrades) == type(self.lair.upgrades[upgrade]) and \
                            'cost' in self.lair.upgrades[upgrade].keys():
                salary = self.lair.treasury.get_salary(self.lair.upgrades[upgrade]['cost'])
                if salary:
                    salary = self.lair.treasury.treasures_description(salary)
                    self.narrator(u"%s в качестве платы за год получают:\n %s" % (
                    self.lair.upgrades[upgrade]['name'], ' '.join(salary)))
                else:
                    self.narrator(u"%s не получили обещанной платы и уходят." % self.lair.upgrades[upgrade]['name'])
                    del self.lair.upgrades[upgrade]
        # Изменяем уровень мобилизации
        desired_mobilization = self.dragon.reputation.level - self.poverty.value  # Желаемый уровень мобилизации
        mobilization_delta = desired_mobilization - self.mobilization.level  # Считаем есть ли разница с текущим уровнем мобилизации
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
            else:
                if renpy.config.debug:
                    self.narrator(u"Вор появился.")
                self.thief.event("spawn")
        else:  # Иначе пробуем его пустить на дело
            if random.choice(range(6)) in range(
                            1 + len(self.thief.items)):  # Шанс 1 + количество шмота на воре, что он пойдет на дело
                # Идем на дело
                if renpy.config.debug:
                    self.narrator(u"Вор идет на дело")
                self.thief.steal(self.lair)
            else:
                if renpy.config.debug:
                    self.narrator(u"Вору ссыкотно, надо бы подготовиться.")
                self.thief.event("prepare")
                if random.choice(range(2)) == 0:  # C 50% шансом получаем шмотку
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
            else:
                if renpy.config.debug:
                    self.narrator(u"Рыцарь появился.")
                self.knight.event("spawn")
        else:  # Иначе пробуем его пустить на дело
            if random.choice(range(7)) in range(1 + len([i for i in self.knight.items if not self.knight.items[
                i].basic])):  # Шанс 1 + количество небазового шмота на рыцаре из 7, что он пойдет на дело
                # Идем на дело
                if renpy.config.debug:
                    self.narrator(u"Рыцарь вызывает дракона на бой")
                # TODO: Схватка рыцаря с драконом
                fight_result = self.knight.fight_dragon()
                if renpy.config.debug:
                    self.narrator(u"После схватки рыцаря")
                if fight_result in ["defeat", "retreat"]:
                    return fight_result
                    #renpy.call("lb_fight", foe=self.knight)
            else:
                if renpy.config.debug:
                    self.narrator(u"Рыцарю ссыкотно, надо бы подготовиться.")
                self.knight.event("prepare")
                if random.choice(range(2)) == 0:  # C 50% шансом получаем шмотку
                    self.knight.event("prepare_usefull")
                    self.knight.enchant_equip()
                    if renpy.config.debug:
                        self.narrator(u"Рыцарь получил %s" % self.knight.last_received_item.name)
                else:
                    if renpy.config.debug:
                        self.narrator(u"Но вместо этого рыцарь весь год бухает.")
                    self.knight.event("prepare_useless")

    def sleep(self):
        """
        Рассчитывается количество лет которое дракон проспит.
        Сброс характеристик дракона.
        """
        self._sleep_lvl += 1
        time_to_sleep = self.dragon.injuries + 1
        # Сбрасываем характеристики дракона
        self.dragon.rest()
        # Действия с девушками до начала сна
        self.girls_list.before_sleep()
        # Спим
        for i in xrange(time_to_sleep):
            if self.next_year() in ["defeat", "retreat"]:
                break
        # Обнуляем накопленные за бодрствование очки мобилизации
        self.dragon.reputation.reset_gain()
        # Действия с девушками после конца сна    
        self.girls_list.after_awakening()
        # Проверка срока выполнения квеста
        if self.quest_time <= 0:
            call('lb_location_mordor_questtime')
        self._sleep_lvl -= 1

    def _create_thief(self, thief_level=None):
        """
        Проверка на появление вора.
        """
        from thief import Thief

        if thief_level is None:
            thief_level = Thief.start_level(self.dragon.reputation.level)
        if thief_level > 0:
            self.thief = Thief(level=thief_level,
                               treasury=self.lair.treasury,
                               gameRef=self,
                               base_character=self.adv_character)
        else:
            self.thief = None

    def _create_knight(self, knight_level=None):
        """
        Проверка на появление рыцаря.
        """
        from knight import Knight

        if knight_level is None:
            knight_level = Knight.start_level(self.dragon.reputation.level)
        if knight_level > 0:
            self.knight = Knight(level=knight_level,
                                 gameRef=self,
                                 base_character=self.adv_character)
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
            # Копируем сокровищницу из прошлого логова
            self.lair.treasury = save_treas
        else:
            # определяем логово по умолчанию
            lair_list = []
            mods = self.dragon.modifiers()
            for lair in data.lair_types.iterkeys():
                if 'prerequisite' in data.lair_types[lair]:  # просматриваем логова, выдаваемые автоматически при выполнении требований
                    prerequisite_list = data.lair_types[lair]['prerequisite']  # получаем список требований к дракону
                    prerequisite_exists = True  # временная переменная для требований
                    for prerequisite in prerequisite_list:  # просматриваем список требований
                        prerequisite_exists = prerequisite_exists and prerequisite in mods  # удостоверяемся, что список требований выполнен
                    if prerequisite_exists:
                        lair_list.append((data.lair_types[lair].name, lair))  # если список требований выполнен, добавляем логово к списку
            if len(lair_list) == 0:
                lair_type = 'impassable_coomb'  # список логов пуст, выбираем начальное
            elif len(lair_list) == 1:
                lair_type = lair_list[0][1]  # в списке одно логово, выбираем его автоматически
            else:
                lair_list.insert(0, (u"Выберите логово:", None))
                lair_type = renpy.display_menu(lair_list)  # в списке больше одного логова, даём список на выбор
            self.lair = Lair(lair_type)

    def set_quest(self):
        lvl = self.dragon.level
        # проходим весь список квестов
        quests = []
        for quest_i in xrange(len(data.quest_list)):
            quest = data.quest_list[quest_i]
            # находим квест, подходящий по уровню, не уникальный или ещё не выполненный за текущую игру
            if quest['min_lvl'] <= lvl <= quest['max_lvl'] and \
                    ('unique' not in quest or quest['unique'] not in self.unique) and \
                    ('prerequisite' not in quest or quest['prerequisite'] in self.unique):
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
        quest_complete = True
        if 'task_requirements' in self._quest:
            quest_complete = False
            # проходим все варианты выполнения квеста
            for require in self._quest['task_requirements']:
                if type(require) is str:
                    reached_requirements = require in reached_list
                else:
                    # для этого варианта нужно выполнить целый список требований
                    reached_requirements = True
                    for sub_require in require:
                        if type(sub_require) is str:
                            reached_requirements = reached_requirements and sub_require in reached_list
                        else:
                            # для этого требования в списке достаточно выполнить один из нескольких вариантов
                            variant_reached = False
                            for var_sub_require in sub_require:
                                variant_reached = variant_reached or var_sub_require in reached_list
                            reached_requirements = reached_requirements and variant_reached
                quest_complete = quest_complete or reached_requirements
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

    @staticmethod
    def weighted_random(data):
        """
        :param data: list of tuples (option, weight), где option - возвращаемый вариант, а
                     weight - вес варианта. Чем больше, тем вероятнее что он выпадет.
        :return: option, или None, если сделать выбор не удалось.
        Пример использования:
        coin_flip = weighted_random([("орёл", 1), ("решка",1)])
        """
        if len(data) > 0:
            import bisect
            # Складываем вес всех доступных энкаунтеров
            accumulated = []
            total = 0
            for option, weight in data:
                assert weight >= 0
                accumulated.append(weight + total)
                total += weight
            #Проверяем, что суммарный вес не равен нулю.
            if total == 0:
                return None
            r = random.random() * accumulated[-1]
            return data[bisect.bisect(accumulated, r)][0]
        return None

    def interpolate(self, str):
        '''
        Функция заменяющая переменные в строке на актуальные данные игры
        '''
        return str % self.format_data

    @property
    def format_data(self):
        data = {
            "dragon_name": self.dragon.name,
        }
        return data

    @property
    def is_won(self):
        # Проверка параметров выиграна уже игра или нет
        if not self._win:
            #Проверяем выиграли ли мы
            pass
        return self._win

    def win(self):
        '''
        Форсируем выгирать игру
        '''
        self._win = True

    @property
    def is_lost(self):
        ##Проверка параметров проиграна уже игра или нет
        if not self._defeat:
            # Проверяем проиграли ли мы
            pass
        return self._defeat

    def defeat(self):
        '''
        Форсируем проиграть игру
        '''
        self._defeat = True


class Lair(object):
    def __init__(self, type="impassable_coomb"):
        self.type_name = type
        self.type = data.Container(type, data.lair_types[type])
        # Список модификаций(ловушки, стражи и.т.п.)
        self.upgrades = data.Container('lair_upgrades')
        if 'provide' in self.type:
            for upgrade in self.type['provide']:
                self.upgrades.add(upgrade, deepcopy(data.lair_upgrades[upgrade]))
        # Сокровищиница
        self.treasury = treasures.Treasury()

    def reachable(self, abilities):
        '''
        Функция для проверки доступности логова
        :param abilities: - список способностей у того, кто пытается достичь, например, для вора: [ 'alpinism', 'swimming' ]
        :return: Возращает True ,если до логова можно добраться и False если нет
        '''
        for r in self.requirements():
            if r not in abilities:
                return False
        return True

    def requirements(self):
        '''
        :return: Возвращает список способностей которые нужны чтобы достичь логова.
        '''
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


class Sayer(store.object):
    '''
    Базовый класс для всего что умеет говорить
    '''

    def __init__(self, gameRef=None, base_character=None, *args, **kwargs):
        """
        :param gameRef: Game object
        :param base_character: base_character базовый класс персонажа от которого будет вестись вещание
        """
        self.avatar = None  # По умолчанию аватарки нет
        self._gameRef = gameRef  # Проставляем ссылку на игру
        self._base_character = base_character  # На всякий случай если захотим пересоздать (но зачем?)
        self._real_character = base_character()  # Создаем объект от которого будет вестись вещание

    @property  # Задаем имя через свойство, чтобы при изменении его передавать в персонажа.
    def name(self):
        return self._real_character.name

    @name.setter
    def name(self, value):
        self._real_character.name = value

    def __call__(self, *args, **kwargs):
        """
        Этот метод используется при попытке сказать что-то персонажем.
        Переопределяем, чтобы сообщить игре, что сейчас говорит этот персонаж.
        """
        self._gameRef.currentCharacter = self  # Прописываем кто говорит в настоящий момент
        self._real_character(*args, **kwargs)  # На самом деле говорим

    def third(self, *args, **kwargs):
        '''
        Говорим от третьего лица. Принимаются предложения на более удачное название.
        Например прямая речь:
        $ game.person ("Что-нибудь")
        game.person "Где-нибудь"
        Рассказ о том что делает этот персонаж:
        $ game.person.third("Делая что-нибудь")
        game.person.third "Делая где-нибудь"
        '''
        self._gameRef.currentCharacter = self  # Делаем вид, что сказали сами
        self._gameRef.narrator._real_character(*args, **kwargs)  # Говорим о лица нарратора. Грязный хак.


class Girl(Sayer):
    """
    Базовый класс для всего, с чем можно заниматься сексом.
    """

    def __init__(self, *args, **kwargs):
        super(Girl, self).__init__(*args, **kwargs)  # Инициализируем родителя
        self.virgin = True  # девственность = пригодность для оплодотворения драконом
        self.pregnant = 0  # 0 - не беременна, 1 - беременна базовым отродьем, 2 - беременна продвинутым отродьем
        self.quality = 0  # Репродуктивное качество женщины. Если коварство дракона превышает её репродуктивное качество, то отродье будет продвинутым. Иначе базовым
        self.name = ''
        self.jailed = False  # была ли уже в тюрьме, пригодится для описания
        self.treasure = []


class Mortal:
    _alive = True  # По умолчанию все живые

    @property
    def is_alive(self):
        if self._alive:
            return True
        return False

    @property
    def is_dead(self):
        if not self._alive:
            return True
        return False

    def die(self):
        self._alive = False


class Fighter(Sayer, Mortal):
    """
    Базовый класс для всего, что способно драться.
    Декоратор нужен чтобы реализовывать эффекты вроде иммунитета или ядовитого дыхания.
    То есть такие, которые воздействуют на модификаторы противника.
    """

    def __init__(self, *args, **kwargs):
        """
        :param gameRef: Game object
        """
        super(Fighter, self).__init__(*args, **kwargs)
        self._modifiers = []
        self._equip_slots = []  # Список слотов обмундирования.
        self.items = data.Container("fighter_items")  # Словарь с тем что надето
        self.descriptions = []  # По умолчанию список описаний пуст
        self.avatar = None  # По умолчанию аватарки нет, нужно выбрать в потомках.
        self.name = u""
        self.bg = None  # Бекграунд для драк

    def modifiers(self):
        raise Exception("Need to be reimplemented in derived class")

    def protection(self):
        """
        :rtype : dict
        :return: Значение защиты данного бойца в виде котртежа (защита, верная защита).
        """
        result = dict()
        for type in data.protection_types:
            result[type] = tuples_sum(
                [get_modifier(mod).protection[1]
                 for mod in self.modifiers()
                 if get_modifier(mod).protection[0] == type]
            )
        return result

    def attack(self):
        """
        :rtype : dict
        :return: Словарик, ключами которого являются типы атаки(лед, огонь, яд...),
        а значениями кортежи вида (атака, верная атака)
        """
        result = dict()
        for type in data.attack_types:
            result[type] = tuples_sum(
                [get_modifier(mod).attack[1]
                 for mod in self.modifiers()
                 if get_modifier(mod).attack[0] == type]
            )
        return result

    def immunity(self):
        """
        :return: Список типов атаки(лед, огонь, яд...), к которым у данного бойца иммунитет
        """
        immun = []
        for type in data.attack_types:
            if type + '_immunity' in self._modifiers:
                immun.append(type)
        return immun

    def battle_description(self, status, dragon):
        """
        :param status: список, описывающий состояние боя
        :param dragon: ссылка на дракона, выступающего противником
        :return: текстовое описание боя
        """
        desc_list = []  # список для возможных описаний момента боя
        curr_round = 100  # переменная для определения наимее использовавшегося описания
        # цикл по всем индексам списка self.descriptions
        for desc_i in range(len(self.descriptions)):
            #получаем список переменных для строки описания из списка
            (require, desc_str, insertion, round) = self.descriptions[desc_i]
            #определяем подходит ли описание для текущего статуса
            desc_need = round <= curr_round  #предварительно проверяем на количество использований
            for req in require:
                desc_need = (req in status) and desc_need
            if desc_need:
                if round < curr_round:
                    curr_round = round  #выбираем наименьшее число использований описания
                    desc_list = []  #все предыдущие описания использовались чаще, очищаем список
                #вставляем необходимые данные в описание 
                insert_list = []
                for ins in insertion:
                    if ins == 'foe_name':
                        insert_list.append(self.name)
                    elif ins == 'dragon_name':
                        insert_list.append(dragon.name)
                desc_str = desc_str.format(*insert_list)
                #добавляем в список для описаний            
                desc_list.append([desc_str, desc_i])
        if desc_list:
            #выбираем случайное описание
            dice = random.randint(0, len(desc_list) - 1)
            desc = desc_list[dice]
            self.descriptions[desc[1]][3] += 1  #увеличиваем число использований этого описания
            return desc[0]
        else:
            return status  #список описаний пуст, возвращаем информацию для дебага

    def equip(self, item):
        # Предполагается что все подо что есть слот можно надеть без ограничений
        #И двух слотов с одинаковым типом не существует
        if item["type"] in self._equip_slots:
            self.items[item["type"]] = item
        else:
            #Пытаемся одеть под что нет слота
            raise Exception("Can't equip, no such slot. Trying to equip %s in slot %s" % (item.id, item["type"]))

    def unequip(self, type):
        # Снимаем все что в указанном слоте
        if type in self._equip_slots:
            self.items[type] = None
        else:
            #Пытаемся снять из того слота которого не существует
            raise Exception("Can't unequip, no such slot. Trying to unequip slot %s" % type)

    def _add_equip_slots(self, slot_list):
        # slot_list - список слотов которые нужно добавить
        for s in slot_list:
            if s not in self._equip_slots:
                self._equip_slots.append(s)
                self.items[s] = None


class Dragon(Fighter):
    """
    Класс дракона.
    """

    def __init__(self, parent=None, *args, **kwargs):
        '''
        parent - родитель дракона, если есть.
        '''
        from points import Reputation

        super(Dragon, self).__init__(*args, **kwargs)
        # TODO: pretty screen for name input
        # self._first_name = u"Старый"
        #self._last_name = u"Охотник"
        self.name = random.choice(data.dragon_names)
        self.age = 0
        self.reputation = Reputation()
        self._tiredness = 0  # увеличивается при каждом действии
        self.bloodiness = 0  # range 0..5
        self.lust = 3  # range 0..3, ресурс восстанавливается до 3 после каждого отдыха
        self.hunger = 3  # range 0..3, ресурс восстанавливается до 3 после каждого отдыха
        self.health = 2  # range 0..2, ресурс восстанавливается до 2 после каждого отдыха
        self._mana_used = 0  # количество использованной маны
        self.spells = []  # заклинания наложенные на дракона(обнуляются после сна)
        self._base_energy = 3  #Базовая энергия дракона, не зависящая от модификторов
        self.special_places = {}  # Список разведанных "достопримечательностей"
        self.events = []  # список событий с этим драконом
        self._gift = None  # Дар Владычицы

        # Головы
        if parent is not None:
            self.heads = deepcopy(parent.heads)  #Копируем живые головы родителя
            self.heads.extend(parent.dead_heads)  #И прибавляем к ним мертвые
            self.level = parent.level + 1  # Уровень дракона
        else:
            self.heads = ['green']  # головы дракона
            self.level = 1  # Начальный уровень дракона
        self.dead_heads = []  #мертвые головы дракона

        #Анатомия
        if parent is None:
            self.anatomy = ['size']
        else:
            self.anatomy = deepcopy(parent.anatomy)
        self._gift = self._get_ability()
        if self._gift == 'head':
            self.heads.append('green')
        elif self._gift in data.dragon_heads.keys():
            self.heads[self.heads.index('green')] = self._gift
        else:
            self.anatomy.append(self._gift)

        self.avatar = get_avatar("img/avadragon/" + self.color_eng)  #Назначаем аватарку

    @property
    def description(self):
        ddescription = u'  '
        mods = self.modifiers()
        ddescription += self._accentuation(data.dragon_size[self.size() - 1], self._gift == 'size') + u' '
        ddescription += self._accentuation(self.color, self.color_eng == self._gift) + u' '
        ddescription += self.kind() + u'. '
        ddescription += self._accentuation(data.dragon_size_description[self.size() - 1], self._gift == 'size')
        for i in xrange(len(self.heads)):
            dscrptn = u"Его %s голова " % data.head_num[i] + data.head_description[self.heads[i]]
            dscrptn = self._accentuation(dscrptn, self.heads[i] == self._gift)
            if self._gift == 'head':
                dscrptn = self._accentuation(dscrptn, i == len(self.heads) - 1)
            ddescription += u"\n  " + dscrptn

        if self.wings() == 0 and self.paws() == 0:
            ddescription += '\n  ' + data.wings_description[0]
        else:
            if self.wings() > 0:
                ddescription += '\n  ' + self._accentuation(data.wings_description[self.wings()], self._gift == 'wings')

            if self.paws() > 0:
                ddescription += '\n  ' + self._accentuation(data.paws_description[self.paws()], self._gift == 'paws')

        for i in xrange(len(data.special_features)):
            if data.special_features[i] in mods:
                ddescription += '\n  ' + self._accentuation(data.special_description[i],
                                                            self._gift == data.special_features[i])
        if self.modifiers().count('cunning') > 0:
            dscrptn = data.special_description[len(data.special_features) - 1 + self.modifiers().count('cunning')]
            ddescription += '\n  ' + self._accentuation(dscrptn, self._gift == 'cunning')

        return ddescription

    @staticmethod
    def _accentuation(text, condition):
        if condition:
            return '{b}' + text + '{/b}'
        else:
            return text

    def modifiers(self):
        """
        :return: Список модификаторов дракона
        """
        return self.anatomy + \
               [mod for head_color in self.heads for mod in data.dragon_heads[head_color]] + \
               [mod for spell in self.spells if spell in data.spell_list for mod in data.spell_list[spell]] + \
               [mod for effect in self.spells if spell in data.effects_list for mod in data.effects_list[spell]]

    def max_energy(self):
        """
        :return: Максимальная энергия(целое число)
        """
        return self._base_energy + sum([get_modifier(mod).max_energy for mod in self.modifiers()])

    def energy(self):
        """
        :return: Оставшаяся энергия(целое число)
        """
        return self.max_energy() - self._tiredness

    def drain_energy(self, drain=1):
        """
        :param drain: количество отнимаемой у дракона энергии.
        :return: True если успешно, иначе False.
        """
        if self.energy() - drain >= 0:
            self._tiredness += drain
            return True
        return False

    def gain_rage(self, gain=1):
        """
        Увеличивает раздражение дракона на :gain:
        """
        if self.bloodiness + gain <= 5:
            self.bloodiness += gain
            return True
        return False

    @property
    def magic(self):
        """
        :return: Магическая сила(целое число)
        """
        return sum([get_modifier(mod).magic for mod in self.modifiers()])

    @property
    def mana(self):
        """
        :return: Количество текущей маны (магическая сила - использованная мана, целое число)
        """
        return self.magic - self._mana_used

    def drain_mana(self, drain=1):
        """
        :param drain: количество отнимаемой у дракона маны.
        :return: True если успешно, иначе False.
        """
        if self.mana - drain >= 0:
            self._mana_used += drain
            return True
        return False

    @property
    def fear(self):
        """
        :return: Значение чудовищности(целое число)
        """
        return sum([get_modifier(mod).fear for mod in self.modifiers()])

    def rest(self):
        self._tiredness = 0  # range 0..max_energy
        self.bloodiness = 0  # range 0..5
        self.lust = 3  # range 0..3
        self.hunger = 3  # range 0..3
        self.spells = []  # заклинания сбрасываются
        self._mana_used = 0  # использованная мана сбрасывается
        self.health = 2

    @property
    def color(self):
        """
        :return: Текстовое представление базового цвета дракона
        """
        return data.heads_name_rus[self.color_eng]

    @property
    def color_eng(self):
        """
        :return: Текстовое представление базового цвета дракона
        """
        return self.heads[0]

    def kind(self):
        """
        :return: Текстовое представление 'вида' дракона
        """
        wings = self.wings()
        paws = self.paws()
        heads = len(self.heads)
        if wings == 0:
            if heads == 1:
                if paws == 0:
                    return u"ползучий гад"
                else:
                    return u"линдвурм"
            else:
                return u"%s гидрус" % data.head_count[heads]
        else:
            if paws == 0 and heads == 1:
                return u"летучий гад"
            elif paws == 0 and heads > 1:
                return u"%s летучий гад" % data.head_count[heads]
            elif paws == 1 and heads == 1:
                return u"виверн"
            elif paws == 1 and heads > 1:
                return u"%s виверн" % data.head_count[heads]
            elif paws == 2 and heads == 1:
                return u"дракон"
            elif paws > 1 and heads > 1:
                return u"%s дракон" % data.head_count[heads]
            else:
                return u"шестилапый дракон"  # название для дракона с paws == 3 and heads == 1

    def size(self):
        """
        :return: Размер дракона(число от 1 до 6)
        """
        return self.modifiers().count('size')

    def wings(self):
        """
        :return: Количество пар крыльев
        """
        return self.modifiers().count('wings')

    def paws(self):
        """
        :return: Количество пар лап
        """
        return self.modifiers().count('paws')

    def _get_ability(self):
        '''
        Возвращает способность, которую может получить дракон при рождении
        '''
        dragon_leveling = 2 * ['head']
        if self.size() < 6:
            dragon_leveling += (6 - self.size()) * ['size']
        if self.paws() < 3:
            dragon_leveling += 2 * ['paws']
        if self.wings() < 3:
            dragon_leveling += 2 * ['wings']
        if 'tough_scale' not in self.modifiers():
            dragon_leveling += ['tough_scale']
        if 'clutches' not in self.modifiers() and self.paws() > 0:
            dragon_leveling += ['clutches']
        if 'fangs' not in self.modifiers():
            dragon_leveling += ['fangs']
        if 'horns' not in self.modifiers():
            dragon_leveling += ['horns']
        if 'ugly' not in self.modifiers():
            dragon_leveling += ['ugly']
        if 'poisoned_sting' not in self.modifiers():
            dragon_leveling += ['poisoned_sting']
        if self.modifiers().count('cunning') < 3:
            dragon_leveling += 2 * ['cunning']
        if self.heads.count('green') > 0:
            dragon_leveling += [self._colorize_head()]
        new_ability = random.choice(dragon_leveling)
        return new_ability

    def _colorize_head(self):
        # На всякий случай проверяем есть ли зеленые головы.
        assert self.heads.count('green') > 0
        #Считаем доступные цвета
        available_colors = [color for color in data.dragon_heads if color not in self.heads]
        #Возвращаем один из доступных цветов
        return random.choice(available_colors)

    def struck(self):
        """
        вызывается при получении удара, наносит урон, отрубает головы и выдает описание произошедшего
        :return: описание результата удара
        """
        if self.health:
            # до удара self.health > 1 - дракон ранен, self.health = 1 - тяжело ранен
            self.health -= 1
            if self.health:
                return ['dragon_wounded']
            else:
                return ['dragon_wounded', 'dragon_heavily_wounded']
        else:
            if 'unbreakable_scale' in self.spells:
                # потеря заклинания защиты головы
                self.spells.remove('unbreakable_scale')
                return ['lost_head', 'lost_virtual']
            else:
                # жизни закончились, рубим голову (последнюю в списке)
                lost_head = self.heads.pop()
                self.dead_heads.insert(0,
                                       lost_head)  # ставим на первое место, чтобы после объединения списков порядок голов не изменился
                # потеря головы, если головы закончились - значит смертушка пришла
                if self.heads:
                    return ['lost_head', 'lost_' + lost_head]
                else:
                    self.die()
                    return ['dragon_dead']

    @property
    def injuries(self):
        return 2 - self.health

    @property
    def age(self):
        """
        Возраст дракона. integer
        """
        return self._age

    @age.setter
    def age(self, value):
        assert value >= 0
        if hasattr(self, '_age'):
            if int(value) >= self._age:
                self._age = int(value)
        self._age = int(value)

    def add_effect(self, effect_name):
        if effect_name not in self.spells:
            if effect_name in data.spell_list or effect_name in data.effects_list:
                self.spells.append(effect_name)
            else:
                raise Exception("Unknown effect: %s" % effect_name)

    @property
    def can_fly(self):
        return 'wings' in self.modifiers() or 'wings_of_wind' in self.modifiers()

    @property
    def can_swim(self):
        return 'swimming' in self.modifiers()

    @property
    def special_places_count(self):
        return len(self.special_places)

    def add_special_place(self, place_name, stage=None):
        """
        :param place_name: название достопримечательности для добавления - ключ для словаря.
        :param      stage: на каком этапе достопримечательность, ключ для словаря data.special_places, из которого берется надпись в списке и название локации для перехода. 
        Если стадия не указана (None), то ключ удаляется из словаря.
        """
        assert stage is None or stage in data.special_places, "Unknown stage: %s" % stage
        if stage:
            self.special_places[place_name] = stage
        else:
            if place_name in self.special_places: del self.special_places[place_name]

    def del_special_place(self, place_name):
        """
        :param place_name: название достопримечательности для удаления - ключ для словаря.
        """
        self.add_special_place(place_name)

    def add_event(self, event):
        assert event in data.dragon_events, "Unknown event: %s" % event
        if event not in self.events:
            self.events.append(event)


class Enemy(Fighter):
    """
    Класс одноразового противника для энкаунтера.
    """

    def __init__(self, kind='generic', *args, **kwargs):
        """
        Создание врага.
        """
        super(Enemy, self).__init__(*args, **kwargs)
        self.kind = kind
        self.name = mob_data.mob[kind]['name']
        self.power = mob_data.mob[kind]['power']
        self.defence = mob_data.mob[kind]['defence']
        self.descriptions = mob_data.mob[kind]['descriptions']
        self._modifiers = mob_data.mob[kind]['modifiers']
        self.abilities = []
        self.equipment = []
        self.bg = '' "img/scene/fight/%s.png" % mob_data.mob[kind]['image']

    def modifiers(self):
        return self._modifiers

    def attack(self):
        return self.power

    def protection(self):
        return self.defence


def _call(label, *args, **kwargs):
    if renpy.has_label(label):
        return renpy.call_in_new_context(label, *args, **kwargs)
    else:
        return renpy.call_in_new_context("lb_missed", label=label)


def call(label, *args, **kwargs):
    if type(label) is str:
        return _call(label, *args, **kwargs)
    elif type(label) is list:
        for i in label:
            return _call(i, *args, **kwargs)


def get_avatar(folder, regex='.*'):
    '''
    Возвращает строку-путь с случайной картинкой подходящей под регекспу regex
    '''
    import re, os

    absolute_path = os.path.join(renpy.config.basedir, "game", folder)  # Cоставляем абсолютный путь где искать
    regex = re.compile(regex, re.IGNORECASE)
    filename = random.choice(filter(regex.search, os.listdir(absolute_path)))  # получаем название файла
    return folder + "/" + filename  # Возвращаем правильно отформатированно значение


get_img = get_avatar
