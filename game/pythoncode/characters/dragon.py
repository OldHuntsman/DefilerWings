# coding=utf-8

import random

from copy import deepcopy

from pythoncode import data
from pythoncode.data import get_modifier
from pythoncode.utils import get_random_image
from pythoncode.points import Reputation

from fighter import Fighter


class Dragon(Fighter):
    """
    Класс дракона.
    """

    def __init__(self, parent=None, used_gifts=None, used_avatars=None, *args, **kwargs):
        """
        parent - родитель дракона, если есть.
        """
        super(Dragon, self).__init__(*args, **kwargs)
        # TODO: pretty screen for name input
        # self._first_name = u"Старый"
        # self._last_name = u"Охотник"
        self.name = random.choice(data.dragon_names)
        self.surname = random.choice(data.dragon_surnames)
        self._age = 0
        self.reputation = Reputation()
        self._tiredness = 0  # увеличивается при каждом действии
        self.bloodiness = 0  # range 0..5
        self.lust = 3  # range 0..3, ресурс восстанавливается до 3 после каждого отдыха
        self.hunger = 3  # range 0..3, ресурс восстанавливается до 3 после каждого отдыха
        self.health = 2  # range 0..2, ресурс восстанавливается до 2 после каждого отдыха
        self._mana_used = 0  # количество использованной маны
        self.spells = []  # заклинания наложенные на дракона(обнуляются после сна)
        self._base_energy = 3  # Базовая энергия дракона, не зависящая от модификторов
        self.special_places = {}  # Список разведанных "достопримечательностей"
        self.events = []  # список событий с этим драконом
        self._gift = None  # Дар Владычицы
        if used_gifts is None:
            used_gifts = []
        # Головы
        if parent is not None:
            self.heads = deepcopy(parent.heads)  # Копируем живые головы родителя
            self.heads.extend(parent.dead_heads)  # И прибавляем к ним мертвые
            self.level = parent.level + 1  # Уровень дракона
        else:
            self.heads = ['green']  # головы дракона
            self.level = 1  # Начальный уровень дракона
        self.dead_heads = []  # мертвые головы дракона

        # Анатомия
        if parent is None:
            self.anatomy = ['size']
        else:
            self.anatomy = deepcopy(parent.anatomy)
        self._gift = self._get_ability(used_gifts=used_gifts)
        if self._gift == 'head':
            self.heads.append('green')
        elif self._gift in data.dragon_heads.keys():
            self.heads[self.heads.index('green')] = self._gift
        else:
            self.anatomy.append(self._gift)
        self.avatar = get_random_image("img/avadragon/" + self.color_eng, used_avatars)  # Назначаем аватарку

    @property
    def fullname(self):
        return self.name + u' ' + self.surname

    @property
    def description(self):
        ddescription = u'  '
        mods = self.modifiers()
        ddescription += self._accentuation(data.dragon_size[self.size - 1], self._gift == 'size') + u' '
        ddescription += self._accentuation(self.color, self.color_eng == self._gift) + u' '
        ddescription += self.kind + u'. '
        ddescription += self._accentuation(data.dragon_size_description[self.size - 1], self._gift == 'size')
        for i in xrange(len(self.heads)):
            dscrptn = u"Его %s голова " % data.head_num[i] + data.head_description[self.heads[i]]
            dscrptn = self._accentuation(dscrptn, self.heads[i] == self._gift)
            if self._gift == 'head':
                dscrptn = self._accentuation(dscrptn, i == len(self.heads) - 1)
            ddescription += u"\n  " + dscrptn

        if self.wings == 0 and self.paws == 0:
            ddescription += '\n  ' + data.wings_description[0]
        else:
            if self.wings > 0:
                ddescription += '\n  ' + self._accentuation(data.wings_description[self.wings], self._gift == 'wings')

            if self.paws > 0:
                ddescription += '\n  ' + self._accentuation(data.paws_description[self.paws], self._gift == 'paws')

        for i in xrange(len(data.special_features)):
            if data.special_features[i] in mods:
                ddescription += '\n  ' + self._accentuation(data.special_description[i],
                                                            self._gift == data.special_features[i])
        if 'cunning' in self.modifiers():
            if self.modifiers().count('cunning') <= 3:
                dscrptn = data.cunning_description[self.modifiers().count('cunning') - 1]
                ddescription += '\n  ' + self._accentuation(dscrptn, self._gift == 'cunning')
            else:
                dscrptn = data.cunning_description[-1]  # Выдаем последнее описание (как самое мощное)
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
            [mod for effect in self.spells if effect in data.effects_list for mod in data.effects_list[effect]]

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

    @property
    def kind(self):
        """
        :return: Текстовое представление 'вида' дракона
        """
        wings = self.wings
        paws = self.paws
        heads = len(self.heads)
        # Защита от ошибок в случае мёртвого дракона
        if heads == 0:
            return u"останки дракона"
        if wings == 0:
            if heads == 1:
                if paws == 0:
                    return u"ползучий гад"
                else:
                    return u"линдвурм"
            else:
                return u"гидрус"
        else:
            if paws == 0 and heads == 1:
                return u"летучий гад"
            elif paws == 0 and heads > 1:
                return u"многоглавый летучий гад"
            elif paws == 1 and heads == 1:
                return u"виверн"
            elif paws == 1 and heads > 1:
                return u"многоглавый виверн"
            elif paws == 2 and heads == 1:
                return u"дракон"
            elif paws > 1 and heads > 1:
                return u"многоглавый дракон"
            else:
                return u"дракон"  # название для дракона с paws == 3 and heads == 1

    @property
    def size(self):
        """
        :return: Размер дракона(число от 1 до 6)
        """
        return self.modifiers().count('size')

    @property
    def wings(self):
        """
        :return: Количество пар крыльев
        """
        return self.modifiers().count('wings')

    @property
    def paws(self):
        """
        :return: Количество пар лап
        """
        return self.modifiers().count('paws')

    def _get_ability(self, used_gifts):
        """
        Возвращает способность, которую может получить дракон при рождении
        """
        dragon_leveling = 2 * ['head']
        if self.size < 6:
            dragon_leveling += (6 - self.size) * ['size']
        if self.paws < 3:
            dragon_leveling += 2 * ['paws']
        if self.wings < 3:
            dragon_leveling += 2 * ['wings']
        dragon_leveling += self.available_features
        if self.modifiers().count('cunning') < 3:
            dragon_leveling += 2 * ['cunning']
        if self.heads.count('green') > 0:
            dragon_leveling += [self._colorize_head()]
        dragon_leveling = [item for item in dragon_leveling if item not in used_gifts]
        if len(dragon_leveling) == 0:
            raise StopIteration
        new_ability = random.choice(dragon_leveling)
        return new_ability

    @property
    def available_head_colors(self):
        return [color for color in data.dragon_heads if color not in self.heads and color not in self.dead_heads]

    @property
    def available_features(self):
        ret = []
        ret += [feature for feature in data.special_features
                if feature not in self.modifiers() and feature != 'clutches']
        if 'clutches' not in self.modifiers() and self.paws > 0:
            ret.append("clutches")
        return ret

    def _colorize_head(self):
        # На всякий случай проверяем есть ли зеленые головы.
        assert self.heads.count('green') > 0
        # На всякий случай проверяем есть ли доступные цвета
        assert len(self.available_head_colors) > 0
        # Возвращаем один из доступных цветов
        return random.choice(self.available_head_colors)

    def decapitate(self):
        """Дракону отрубает голову.
        :rtype: list[str]
        :return:
        """
        if 'unbreakable_scale' in self.spells:
            # потеря заклинания защиты головы
            self.spells.remove('unbreakable_scale')
            return ['lost_head', 'lost_virtual']
        else:
            data.achieve_fail("lost_head")# событие для ачивок
            # жизни закончились, рубим голову (последнюю в списке)
            lost_head = self.heads.pop()
            # ставим её на первое место, чтобы после объединения списков порядок голов не изменился
            self.dead_heads.insert(0, lost_head)
            # потеря головы, если головы закончились - значит смертушка пришла
            if self.heads:
                return ['lost_head', 'lost_' + lost_head]
            else:
                self.die()
                return ['dragon_dead']

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
            return self.decapitate()

    @property
    def injuries(self):
        """ Количество ран дракона
        0 - дракон не ранен
        >0 - ранен
        :rtype: int
        :return: Количество ран дракона
        """
        # TODO: заменить "магическое" число 2
        return 2 - self.health

    @property
    def age(self):
        """ Возраст дракона.
        :rtype: int
        :return: Возраст дракона
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
        :param      stage: на каком этапе достопримечательность,
            ключ для словаря data.special_places, из которого берется надпись в списке и название локации для перехода.
        Если стадия не указана (None), то ключ удаляется из словаря.
        """
        assert stage is None or stage in data.special_places, "Unknown stage: %s" % stage
        if stage:
            self.special_places[place_name] = stage
        else:
            if place_name in self.special_places:
                del self.special_places[place_name]

    def del_special_place(self, place_name):
        """
        :param place_name: название достопримечательности для удаления - ключ для словаря.
        """
        self.add_special_place(place_name)

    def add_event(self, event):
        assert event in data.dragon_events, "Unknown event: %s" % event
        if event not in self.events:
            self.events.append(event)


