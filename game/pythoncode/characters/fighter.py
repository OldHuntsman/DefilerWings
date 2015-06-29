# coding=utf-8

import random

from pythoncode import data

from pythoncode.utils import tuples_sum

from talker import Talker
from mortal import Mortal


class Fighter(Talker, Mortal):
    """
    Базовый класс для всего, что способно драться.
    Декоратор нужен чтобы реализовывать эффекты вроде иммунитета или ядовитого дыхания.
    То есть такие, которые воздействуют на модификаторы противника.
    """

    def __init__(self, *args, **kwargs):
        """
        :param game_ref: Game object
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
        """Список модификаторов бойца
        :rtype: list
        :return: Список модификаторов
        """
        raise Exception("Need to be reimplemented in derived class")

    def protection(self):
        """
        :rtype : dict
        :return: Словарь, ключами которого являются типы защиты,
        а значениями - кортежи вида (защита, верная защита).
        """
        result = dict()
        for protect_type in data.protection_types:
            result[protect_type] = tuples_sum(
                [data.get_modifier(mod).protection[1]
                 for mod in self.modifiers()
                 if data.get_modifier(mod).protection[0] == protect_type]
            )
        return result
    
    def defence_power(self):
        """
        :return: Суммарная защита бойца в виде кортежа (защита, верная защита).
        """
        defence = self.protection()
        result = [0, 0]
        for protect_type in defence.keys():
            result[0] += defence[protect_type][0]
            result[1] += defence[protect_type][1]
        return tuple(result)

    def attack(self):
        """Словарь с атаками бойца
        :rtype : dict
        :return: Словарик, ключами которого являются типы атаки(лед, огонь, яд...),
        а значениями кортежи вида (атака, верная атака)
        """
        result = {}
        for attack_type in data.attack_types:
            result[attack_type] = tuples_sum(
                [data.get_modifier(mod).attack[1]
                 for mod in self.modifiers()
                 if data.get_modifier(mod).attack[0] == attack_type]
            )
        return result

    def attack_strength(self, target_immunity=[]):
        """Вычисляет силу атаки по цели 
        :target_immunity: список иммунитетов цели
        :return: кортеж силы атаки по цели: (атака, верная атака)
        """
        power = self.attack()
        result = [0, 0]
        for attack_type in power.keys():
            if attack_type not in target_immunity:
                (r, p) = power[attack_type]
                result[0] += r
                result[1] += p
        return tuple(result)

    def immunity(self):
        """
        :return: Список типов атаки(лед, огонь, яд...), к которым у данного бойца иммунитет
        """
        immun = []
        for immune_type in data.attack_types:
            if immune_type + '_immunity' in self._modifiers:
                immun.append(immune_type)
        return immun

    def battle_description(self, status, dragon):
        """
        :param status: список, описывающий состояние боя
        :param dragon: ссылка на дракона, выступающего противником
        :return: текстовое описание боя
        """
        insertion = {
            'dragon_name': dragon.name,
            'dragon_name_full': dragon.fullname,
            'dragon_type': dragon.kind,
            'dragon_type_cap': dragon.kind.capitalize(),
            'foe_name': self.name,
        }
        desc_list = []  # список для возможных описаний момента боя
        curr_round = 100  # переменная для определения наимее использовавшегося описания
        for desc_i in range(len(self.descriptions)):
            # цикл по всем индексам списка self.descriptions
            (require, desc_str, battle_round) = self.descriptions[desc_i]
            # получаем список переменных для строки описания из списка
            desc_need = battle_round <= curr_round  # предварительно проверяем на количество использований
            for req in require:
                # определяем подходит ли описание для текущего статуса
                desc_need = (req in status) and desc_need
            if desc_need:
                if battle_round < curr_round:
                    curr_round = battle_round  # выбираем наименьшее число использований описания
                    desc_list = []  # все предыдущие описания использовались чаще, очищаем список
                # вставляем необходимые данные в описание
                desc_str = desc_str % insertion
                # добавляем в список для описаний
                desc_list.append((desc_str, desc_i))
        if desc_list:
            desc = random.choice(desc_list)
            # выбираем случайное описание
            self.descriptions[desc[1]][2] += 1  # увеличиваем число использований этого описания
            return desc[0]
        else:
            return status  # список описаний пуст, возвращаем информацию для дебага

    def equip(self, item):
        # Предполагается что все подо что есть слот можно надеть без ограничений
        # И двух слотов с одинаковым типом не существует
        if item["type"] in self._equip_slots:
            self.items[item["type"]] = item
        else:
            # Пытаемся одеть под что нет слота
            raise Exception("Can't equip, no such slot. Trying to equip %s in slot %s" % (item.id, item["type"]))

    def unequip(self, slot_type):
        # Снимаем все что в указанном слоте
        if slot_type in self._equip_slots:
            self.items[slot_type] = None
        else:
            # Пытаемся снять из того слота которого не существует
            raise Exception("Can't unequip, no such slot. Trying to unequip slot %s" % slot_type)

    def _add_equip_slots(self, slot_list):
        # slot_list - список слотов которые нужно добавить
        for s in slot_list:
            if s not in self._equip_slots:
                self._equip_slots.append(s)
                self.items[s] = None

