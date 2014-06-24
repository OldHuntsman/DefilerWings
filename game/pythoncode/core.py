#!/usr/bin/env python
# coding=utf-8
import random
import math
import data
from data import get_modifier
from copy import deepcopy
import renpy.exports as renpy


def tuples_sum(tuple_list):
    return sum([first for first, _ in tuple_list]), sum([second for _, second in tuple_list])


class Game(object):
    def __init__(self, BaseCharacter=object):
        """
        :param BaseCharacter: Базовый класс для персонажа. Скорее всего NVLCharacter.
        """
        self.thief = None
        self.lair = None  # текущее логово
        self.reputation_points = 0  # Дурная слава дракона
        self.mobilization = 0  # мобилизация королевства
        self.year = 0  # текущий год
        self.currentCharacter = None # Последний говоривший персонаж. Используется для поиска аватарки.
        
        class Narrator(BaseCharacter):
            """
            Класс, которым будет заменен narrator по-умолчанию.
            """
            def __init__(self, gameRef, *args, **kwargs):
                """
                :param gameRef: Game object
                """
                super(Narrator, self).__init__(*args, **kwargs)
                self.gameRef = gameRef
                self.avatar = None # У нарраторар нет аватарки. Ну или можно будет поставить потом.
            
            def __call__(self, *args, **kwargs):
                """
                Этот метод используется при попытке сказать что-то персонажем.
                Переопределяем, чтобы сообщить игре, что сейчас говорит этот персонаж.
                """
                self.gameRef.currentCharacter = self
                super(Narrator, self).__call__(*args, **kwargs)
                
        class Fighter(BaseCharacter):
            """
            Базовый класс для всего, что способно драться.
            Декоратор нужен чтобы реализовывать эффекты вроде иммунитета или ядовитого дыхания.
            То есть такие, которые воздействуют на модификаторы противника.
            """

            def __init__(self, gameRef, *args, **kwargs):
                """
                :param gameRef: Game object
                """
                super(Fighter, self).__init__(*args, **kwargs)
                self.gameRef = gameRef
                self._modifiers = []
                self.avatar = None # По умолчанию аватарки нет, нужно выбрать в потомках.
                
            def __call__(self, *args, **kwargs):
                """
                Этот метод используется при попытке сказать что-то персонажем.
                Переопределяем, чтобы сообщить игре, что сейчас говорит этот персонаж.
                """
                self.gameRef.currentCharacter = self
                super(Fighter, self).__call__(*args, **kwargs)

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

        class Dragon(Fighter):
            """
            Класс дракона.
            """

            def __init__(self, *args, **kwargs):
                super(Dragon, self).__init__(*args, **kwargs)
                # Здесь должна быть генерация имени.
                self.name = u"Змей Горыныч"
                self._tiredness = 0  # увеличивается при каждом действии
                self.bloodiness = 0  # range 0..5
                self.lust = 0  # range 0..2
                self.hunger = 0  # range 0..2

                self.anatomy = ['size', 'paws', 'size', 'wings', 'size', 'paws']
                self.heads = ['green', 'green']  # головы дракона
                self.spells = ['wings_of_wind']  # заклинания наложенные на дракона(обнуляются после сна)
                self.avatar = "img/avadragon/green/1.jpg"

            def _debug_print(self):
                # self(u'Дракон по имени {0}'.format(self.name))
                # self(u'Список всех модификаторов {0}'.format(', '.join(self.modifiers())))
                # self(u'Вид дракона {0}'.format(self.kind()))
                # self(u'Размер {0}'.format(data.size_texts[self.size()]))
                # self(u'Анатомия дракона {0}'.format(', '.join(self.anatomy)))
                # self(u'Наложенная на дракона магия {0}'.format(' '.join(self.spells)))
                # self(u'Цвета голов дракона {0}'.format(', '.join(self.heads)))
                # self(u'Энергия {0} из {1}'.format(self.energy(), self.max_energy()))
                # self(u'Могущество {0}'.format(', '.join(['{0} {1}'.format(k, v) for k, v in self.attack().items()])))
                # self(u'Несокрушимость {0}'.format(', '.join(['{0} {1}'.format(k, v) for k, v in self.protection().items()])))
                # self(u'Коварство {0}'.format(self.magic()))
                # self(u'Чудовищиность {0}'.format(self.fear()))
                children = self.children()
                for child in children:
                    self(u'Ребенок {0}'.format(', '.join(child.anatomy[-3:] + child.heads)))


            def modifiers(self):
                """
                :return: Список модификаторов дракона
                """
                return self.anatomy + \
                       [mod for head_color in self.heads for mod in data.dragon_heads[head_color]] + \
                       [mod for spell in self.spells for mod in data.spell_list[spell]]

            def max_energy(self):
                """
                :return: Максимальная энергия(целое число)
                """
                return sum([get_modifier(mod).max_energy for mod in self.modifiers()])

            def energy(self):
                """
                :return: Оставшаяся энергия(целое число)
                """
                return self.max_energy() - self._tiredness

            def magic(self):
                """
                :return: Магическая сила(целое число)
                """
                return sum([get_modifier(mod).magic for mod in self.modifiers()])

            def fear(self):
                """
                :return: Значение чудовищносити(целое число)
                """
                return sum([get_modifier(mod).fear for mod in self.modifiers()])

            def rest(self):
                self._tiredness = 0  # range 0..max_energy
                self.bloodiness = 0  # range 0..5
                self.lust = 3  # range 0..3
                self.hunger = 3  # range 0..3
                self.spells = []  # заклинания сбрасываются

            def kind(self):
                """
                :return: Текстовое представление 'вида' дракона
                """
                wings = self.wings()
                paws = self.paws()
                heads = len(self.heads)
                if wings == 0 and paws == 0:
                    return u"Ползучий гад"
                if wings > 0 and paws == 0:
                    return u'Летучий гад'
                if wings == 0 and paws >= 0:
                    return u'Линдвурм'
                if wings > 0 and paws == 1:
                    return u'Вирвен'
                if wings == 0 and heads > 1:
                    return u'Гидра'
                if wings == 1 and paws == 2 and heads == 1:
                    return u'Истинный дракон'
                if wings > 0 and paws >= 1 and heads > 1:
                    return u'Многоглавый дракон'

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

            def children(self):
                """
                Сгенерировать список потомков.
                Вызывается при отставке дракона.
                :return: list of Dragons
                """
                # Обнуляем заклинания, они уже не понадобятся
                self.spells = []
                # Формируем список возможных улучшений
                dragon_leveling = ['head']
                if self.size() < 6:
                    dragon_leveling += ['size']
                if self.paws() < 3:
                    dragon_leveling += ['paws']
                if self.wings() < 3:
                    dragon_leveling += ['wings']
                if 'tough_scale' not in self.modifiers():
                    dragon_leveling += ['tough_scale']
                if 'clutches' not in self.modifiers():
                    dragon_leveling += ['clutches']
                if 'fangs' not in self.modifiers() and self.paws() > 0:
                    dragon_leveling += ['fangs']
                if 'horns' not in self.modifiers():
                    dragon_leveling += ['horns']
                if 'ugly' not in self.modifiers():
                    dragon_leveling += ['ugly']
                if 'poisoned_sting' not in self.modifiers():
                    dragon_leveling += ['poisoned_sting']
                if self.modifiers().count('cunning') < 3:
                    dragon_leveling += ['cunning']
                if self.heads.count('green') > 0:
                    dragon_leveling += ['color']
                # Выбираем три случайных способности
                number_of_abilities = 3
                new_abilities = random.sample(dragon_leveling, number_of_abilities)
                children = [deepcopy(self) for i in range(0, number_of_abilities)]
                for i in range(0, number_of_abilities):
                    if new_abilities[i] == 'color':
                        # список возможных цветов
                        colors = ['red', 'white', 'blue', 'black', 'iron', 'copper', 'silver', 'gold', 'shadow']
                        children[i].heads[self.heads.index('green')] = random.choice(colors)
                    elif new_abilities[i] == 'head':
                        children[i].heads += ['green']
                    else:
                        children[i].anatomy += [new_abilities[i]]
                return children

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
                if self.power == 1:
                    return u"Бедный рыцарь"
                elif self.power == 2:
                    return u"Странствующий рыцарь"
                elif self.power == 3:
                    return u"Межевой рыцарь"
                elif self.power == 4:
                    return u"Благородный рыцарь"
                elif self.power == 5:
                    return u"Паладин рыцарь"
                elif self.power == 6:
                    return u"Прекрасный принц"
                else:
                    assert False, u"Недопустимое значение поля power"

            def upgrade(self):
                """
                Метод вызвается если рыцать не пошел драться с драконом.
                Добавляет новое снаряжение.
                """
                raise NotImplementedError

        class Thief(BaseCharacter):
            """
            Класс вора.
            """

            def __init__(self, *args, **kwargs):
                super(Thief, self).__init__(self, *args, **kwargs)
                self._skill = 1

            def skill(self):
                if "robbery_plan" in self.modifiers():
                    return self._skill + 1
                if "bad_plan" in self.modifiers():
                    return self._skill - 1
                return self._skill

            def title(self):
                """
                :return: Текстовое представление 'звания' вора.
                """
                if self.skill() == 1:
                    return u"Мародёр"
                elif self.skill() == 2:
                    return u"Грабитель"
                elif self.skill() == 3:
                    return u"Взломшик"
                elif self.skill() == 4:
                    return u"Расхититель гробниц"
                elif self.skill() >= 5:
                    return u"Мастер вор"
                else:
                    assert False, u"Недопустимое значение поля skill"

            def new_ability(self):
                raise NotImplementedError

            def new_item(self):
                """
                Метод вызвается если вор не пошел грабить дракона.
                Здесь идёт выбор новой вещи(подготовка к грабежу).
                """
                raise NotImplementedError

        class Women(BaseCharacter):
            def __init__(self, *args, **kwargs):
                super(Women, self).__init__(*args, **kwargs)
                self.magic = 0
                self.pregnant = False
                self.can_give_birth = True

        self.dragon = Dragon(self)
        self.knight = Knight(self)
        self.narrator = Narrator(self)

    def battle(self, fighter1, fighter2):
        """
        Логика сражения.
        :param fighter1: Fighter
        :param fighter2: Fighter
        :return: Текст описывающий сражение.
        """
        hit1 = sum(fighter1.attack()[key][1] for key in fighter1.attack())
        for attacks in range(1,sum(fighter1.attack()[key][0] for key in fighter1.attack()) +1):
            dice = random.randint(1,3)
            if dice ==1:
                hit1 +=1       
        hit2 = sum(fighter2.attack()[key][1] for key in fighter2.attack())
        for attacks in range(1, sum(fighter2.attack()[key][0] for key in fighter2.attack()) +1):
            dice = random.randint(1,3)
            if dice == 1:
                hit2 += 1
        prot1 = sum(fighter1.protection()[key][1] for key in fighter1.protection())
        for protects in range(1, sum(fighter1.protection()[key][1]for key in fighter1.protection())+1):
            dice = random.randint(1,3)
            if dice == 1:
                prot1 +=1
        prot2 = sum(fighter2.protection()[key][1] for key in fighter2.protection())
        for protects in range(1, sum(fighter2.protection()[key][1] for key in fighter2.protection())+1):
            dice = random.randint(1,3)
            if dice ==1:
                prot2 +=1        
        """
        Возможные результаты боя
        """
        if hit1 > prot2:#Дракон попал
            if hit2 <= prot1:
                return (True, u"%s Побеждает %s не получив ран"%(fighter1.name, fighter2.name))
            elif hit2 > prot1:
                return (True, u"%s Побеждает %s получив рану"%(fighter1.name, fighter2.name))
                #также увеличиваем показатель ранений дракона   
        elif hit1 <= prot2:#дракон не попал
            if hit2 <= prot1:
                return (False, u"%s не побеждает, ран нет"%(fighter1.name))
                #тут предлагаем игроку бежать или продолжить бой
            elif hit2 > prot1:
                return (False, u"%s не побеждает, ранен"%(fighter1.name))
                #тут предлагаем игроку бежать или продолжить бой
                #также увеличиваем показатель ранений дракона

    def next_year(self):
        """
        Логика смены года.
        Проверки на появление/левелап/рейд рыцаря/вора.
        Изменение дурной славы.
        Что-то ещё?
        """
        raise NotImplementedError

    def sleep(self):
        """
        Рассчитывается количество лет которое дракон проспит.
        Попытки бегства женщин.
        Сброс характеристик дракона.
        """
        time_to_sleep = self.dragon.injuries + 1
        # Сбрасываем характеристики дракона
        self.dragon.rest()
        # Спим
        for i in xrange(time_to_sleep):
            self.year += 1
            self.next_year()
            if self.knight:
                if 1 == random.randint(1, 3):
                    self.knight.upgrade()
            else:
                self._create_knight()
            if self.thief:
                if 1 == random.randint(1, 3):
                    self.thief.upgrade()
            else:
                self._create_knight()

    def _create_knight(self):
        """
        Проверка на появление рыцаря.
        """
        raise NotImplementedError

    def _create_thief(self):
        """
        Проверка на появление вора.
        """
        raise NotImplementedError

    def reputation(self):
        """
        Видимые игроку очки дурной славы.
        Рассчитываются по хитрой формуле.
        """
        return math.floor(math.log(self.reputation_points))


class Treasury(object):
    def __init__(self):
        self.copper_coins = 0
        self.silver_coins = 0
        self.gold_coins = 0
        # списки строк
        self.materials = []
        self.jewelry = []
        self.equipment = []

    def money(self):
        """
        :return: Суммарная стоимость всего, что есть в сокровищнице(Золотое ложе).
        """
        raise NotImplementedError


class Lair(object):
    def __init__(self):
        self.lair_type = "Буреломный овраг"
        self.inaccessibility = 0
        # Список ограничений для доступа воров/рыцарей
        self.restrictions = []
        # Сокровищиница
        self.treasury = Treasury()
        # Список модификаций(ловушки, стражи и.т.п.)
        self.modifiers = []
        # Список женщин в логове
        self.women = []

