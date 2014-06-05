init python:
    def tuples_sum(tuple_list):
        return sum([first for first, _ in tuple_list]), sum([second for _, second in tuple_list])

    class Fighter(NVLCharacter):
        def __init__(self, *args, **kwargs):
            NVLCharacter.__init__(self, *args, kind=nvl, **kwargs)
            self._modifiers = []

        def protection(self):
            """
            :rtype : dict
            :return: Значение защиты данного бойца в виде котртежа (защита, верная защита).
            """
            result = dict()
            for type in data.protection_types:
                result[type] = tuples_sum(
                    [data.get_modifier(mod).protection[1]
                     for mod in self.modifiers()
                     if data.get_modifier(mod).protection[0] == type]
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
                    [data.get_modifier(mod).attack[1]
                     for mod in self.modifiers()
                     if data.get_modifier(mod).attack[0] == type]
                )            
            return result
        
    class Dragon(Fighter):
        """
        Класс дракона.
        """

        def __init__(self, *args, **kwargs):
            Fighter.__init__(self, *args, color="#c8ffc8", **kwargs)
            # Здесь должна быть генерация имени.
            self.name = u"Змей Горыныч"
            self._tiredness = 0  # увеличивается при каждом действии
            self.bloodiness = 0  # range 0..5
            self.lust = 0  # range 0..2
            self.hunger = 0  # range 0..2

            self.anatomy = ['size', 'paws', 'size', 'wings', 'size', 'paws']
            self.heads = ['black']  # головы дракона
            self.spells = ['wings_of_wind']  # заклинания наложенные на дракона(обнуляются после сна)

        def _debug_print(self):
            self(u'Дракон по имени {0}'.format(self.name))
            self(u'Список всех модификаторов {0}'.format(', '.join(self.modifiers())))
            self(u'Вид дракона {0}'.format(self.kind()))
            self(u'Размер {0}'.format(data.size_texts[self.size()]))
            self(u'Анатомия дракона {0}'.format(', '.join(self.anatomy)))
            self(u'Наложенная на дракона магия {0}'.format(' '.join(self.spells)))
            self(u'Цвета голов дракона {0}'.format(', '.join(self.heads)))
            self(u'Энергия {0} из {1}'.format(self.energy(), self.max_energy()))
            self(u'Могущество {0}'.format(', '.join(['{0} {1}'.format(k, v) for k, v in self.attack().items()])))
            self(u'Несокрушимость {0}'.format(', '.join(['{0} {1}'.format(k, v) for k, v in self.protection().items()])))
            self(u'Коварство {0}'.format(self.magic()))
            self(u'Чудовищиность {0}'.format(self.fear()))


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
            return sum([data.get_modifier(mod).max_energy for mod in self.modifiers()])

        def energy(self):
            """
            :return: Оставшаяся энергия(целое число)
            """
            return self.max_energy() - self._tiredness

        def magic(self):
            """
            :return: Магическая сила(целое число)
            """
            return sum([data.get_modifier(mod).magic for mod in self.modifiers()])

        def fear(self):
            """
            :return: Значение чудовищносити(целое число)
            """
            return sum([data.get_modifier(mod).fear for mod in self.modifiers()])

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
            raise NotImplementedError