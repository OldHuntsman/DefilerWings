#!/usr/bin/env python
# coding=utf-8

import collections


class Modifier(object):
    """
    Класс разнообразных модификаторов.
    К примеру: даров владычицы, снаряжения рыцарей, заклинаний и.т.д.
    """

    def __init__(self, attack=('base', (0, 0)), protection=('base', (0, 0)), magic=0, fear=0, energy=0):
        self.attack = attack
        self.protection = protection
        self.magic = magic
        self.fear = fear
        self.max_energy = energy

    def __contains__(self, item):
        return item in self.__dict__

    @staticmethod
    def attack_filter(attack):
        return attack


class Container(collections.defaultdict):
    """
    Класс-хранилище разнообразных свойст/модификаторов
    TODO: реверсивный поиск
    """

    def __init__(self, container_id=None, data=None, *args, **kwargs):
        super(Container, self).__init__(*args, **kwargs)
        self.id = container_id
        if data is not None:

            for key, value in data.items():
                self.add(key, value)

    def add(self, container_id, data):
        """
        :param container_id: Идентификатор свойства/модификатора
        :param data: dict, содержащий парамерты этого свойства/модификатор
        """
        if container_id not in self:
            if type(data) is dict:
                self[container_id] = Container(container_id, data)
            else:
                self[container_id] = data
        else:
            raise Exception("Already in container")

    def sum(self, parameter):
        """
        :param parameter: Значение, по которому нужно суммировать аттрибуты. Суммирование проводится
                          рекурсивно.
        """
        total = 0
        if parameter in self:
            try:
                total += self[parameter]
            except ValueError:
                pass
        for i in self:
            if type(self[i]) == type(self):
                total += self[i].sum(parameter)
        return total

    def list(self, key):
        """
        Рекурсивно возвращает лист значений по ключу
        :param key: Ключ по которому производится поиск
        :return: Список значений
        """
        result = []
        if key in self:
            if type(self[key]) is list:
                result += self[key]
            else:
                result.append(self[key])
        for i in self:
            if type(self[i]) == type(self):
                result += self[i].list(key)
        return result

    def contains(self, key, value=None):
        """
        Возвращает список айдишников, которые содержат заданный ключ и, если указано, значение.
        :param key: Ключ который должен содержать элемент
        :return: список элеметов содержащих ключ, если таких элементов нет, то пустой список
        """
        result = []
        if key in self:
            if value is None:
                result += [self.id]
            else:
                if self[key] == value:
                    result += [self.id]
        for i in self:
            if type(self[i]) == type(self):
                result += self[i].contains(key, value)
        return result

    def select(self, query):
        """
        Возвращает список айдишников которые подходят под условия указанные в query. Нерекурсивно.
        :param query: список кортежей (ключ, значение) которым должен удовлетворять объект поиска
        :return: спискок удовлетворяюищих элементво
        """
        result = []
        for (key, value) in query:
            if key in self and self[key] == value:
                continue
            else:
                break
        else:
            result.append(self.id)
        for i in self:
            if type(self[i]) == type(self):
                result += self[i].select(query)
        return result

    def type(self):
        """
        For test uses
        """
        return type(self)

    def __getattr__(self, name):
        return self[name]

    def __missing__(self, key):
        return None

def get_description_by_count(description_list, count):
    """ 
    :param description_list: словарь, ключ - минимальное целочисленное значение, при котором выведется значение с этим ключом.
    Максимальное число, при котором выведется значение - минимальное значение - 1 следующего по размеру ключа
    :param count: число, для которой нужно подобрать описание
    :return: описание для числа count из словаря description_list
    """
    count_list = reversed(sorted(description_list.keys()))
    for count_i in count_list:
        if count >= count_i:
            return description_list[count_i]

#
# Вор
#

thief_first_names = [
    u"Джек",
    u"Гарри",
    u"Cэм"
]

thief_last_names = [
    u"Лысый",
    u"Скользкий",
    u"Шустрый"
]

thief_abilities = Container(
    "thief_abilities",
    {
        "climber": {
            "name": u"Альпинист",
            "description": u"Дает \"Альпинизм\"",
            "provide": ["alpinism"]
        },
        "diver": {
            "name": u"Ныряльщик",
            "description": u"Дает \"Плавание\"",
            "provide": ["swimming"]
        },
        "greedy": {
            "name": u"Жадина",
            "description": u"Пытается украсть одно дополнительное сокровище",
            "provide": []
        },
        "mechanic": {
            "name": u"Механик",
            "description": u"Игнорирует механические ловушки",
            "avoids": ["mechanic_traps"],
            "provide": []
        },
        "magicproof": {
            "name": u"Знаток магии",
            "description": u"Игнорирует магические ловушки",
            "avoids": ["magic_traps"],
            "provide": []
        },
        "poisoner": {
            "name": u"Отравитель",
            "description": u"Игнорирует ядовитых стражей",
            "avoids": ["poison_guargs"],
            "provide": []
        },
        "assassin": {
            "name": u"Ассасин",
            "description": u"Игнорирует обычных стражей",
            "avoids": ["regular_guargs"],
            "provide": []
        },
        "night_shadow": {
            "name": u"Ночная тень",
            "description": u"Игнорирует элитных стражей",
            "avoids": ["elite_guards"],
            # Это странно, что он может быть пойман обычными стражами
            "provide": []
        },
        "trickster": {
            "name": u"Ловкач",
            "description": u"Не имеет шанса разбудить дракона",
            "provide": []
        }
    }
)

thief_items = Container(
    "thief_items",
    {
        "plan": {
            "name": u"План ограбления",
            "level": 1,
            "description": u"+1 к уровню вора"
        },
        "scheme": {
            "name": u"Схема тайных проходов",
            "description": u"Позволяет игнорировать неприступность логова"
        },
        "sleep_dust": {
            "name": u"Сонный порошок",
            "description": u"Вор не имеет шанса разбудить дракона"
        },
        "bottomless_sac": {
            "name": u"Бездонный мешок",
            "dropable": True,
            "description": u"Удваивает попытки кражи"
        },
        "antidot": {
            "name": u"Антидот",
            "description": u"Вор игнорирует ядовитых стражей",
            "avoids": ["poison_guargs"]
        },
        "enchanted_dagger": {
            "name": u"Зачарованный кинжал",  # Applied
            "dropable": True,
            "description": u"Вор игнорирует обычных стражей",
            "avoids": ["regular_guargs"]
        },
        "ring_of_invisibility": {
            "name": u"Кольцо-невидимка",  # Applied
            "dropable": True,
            "description": u"Вор элитных стражей",
            "avoids": ["elite_guargs"]
        },
        "flying_boots": {
            "name": u"Летучие сандалии",  # Applied
            "dropable": True,
            "description": u"Дает \"Полёт\"",
            "provide": ["flight"]
        },
        "cooling_amulet": {
            "name": u"Охлаждающий амулет",  # Applied
            "dropable": True,
            "description": u"Дает \"защиту от огня\"",
            "provide": ["fireproof"]
        },
        "warming_amulet": {
            "name": u"Согревающий амулет",  # Applied
            "dropable": True,
            "description": u"Дает \"защиту от холода\"",
            "provide": ["coldproof"]
        }
    })

# Одинаковые айдишники вещей спасут от того, что у вора может оказаться норамльная.
thief_items_cursed = Container(
    "thief_items_cursed",
    {
        "plan": {
            "name": u"Плохой план",  # Applied
            "level": -1,
            "cursed": True,
            "description": u"-1 к уровню вора",
            "fails": []
        },
        "bottomless_sac": {
            "name": u"Дырявый мешок",  # Applied
            "cursed": True,
            "description": u"Вор не уносит никаких сокровищ",
            "fails": []},
        "enchanted_dagger": {
            "name": u"Проклятый кинжал",  # Applied
            "cursed": True,
            "description": u"Автоматический успех обычных стражей",
            "fails": ["regular_guards"]},
        "ring_of_invisibility": {
            "name": u"Кольцо мерцания",  # Applied
            "cursed": True,
            "description": u"Автоматический успех элитных стражей",
            "fails": ["elite_guards"]
        },
        "flying_boots": {
            "name": u"Ощипанные сандалии",  # Applied
            "cursed": True,
            "description": u"Вор автоматически разбивается насмерть, если идет в логово требующее полета",
            "fails": ["flight"],
            "provide": ["flight"]
        },
        "cooling_amulet": {
            "name": u"Морозильный амулет",  # Applied
            "cursed": True,
            "description": u"Вор замораживается насмерть, если идет в огненное логово",
            "fails": ["fireproof"],
            "provide": ["fireproof"]
        },
        "warming_amulet": {
            "name": u"Шашлычный амулет",  # Applied
            "cursed": True,
            "description": u"Вор зажаривается насмерть, если идет в ледяное логово",
            "fails": ["coldproof"],
            "provide": ["coldproof"]
        }
    }
)

thief_titles = [
    u"Мародер",
    u"Грабитель",
    u"Взломшик",
    u"Расхититель гробниц",
    u"Мастер-вор"
]

'''
Вызывает label указанный в value словаря. Если указан list, то вызваются все label'ы указанные в
списке в указанном порядке.
В качестве ключевых параметров передаются:
thief - вор стриггеривший ивент
Дополнительно для "die_trap" и "pass_trap":
obj - улучшение которое вор обошел или умер
Дополнительно для "die_item", "receive_item":
obj - вещь, которую получил вор
'''
thief_events = {
    "spawn": "lb_event_thief_spawn",
    "lair_unreachable": None,
    "prepare": None,
    "prepare_usefull": None,
    "prepare_useless": None,
    "lair_enter": None,
    "die_item": None,
    "die_inaccessability": None,
    "die_trap": None,
    "pass_trap": None,
    "receive_no_item": None,
    "receive_item": "lb_event_thief_receive_item",
    "steal_items": "lb_event_thief_steal_items",
}

#
# Рыцарь
#

knight_first_names = [
    u"Гавейн",
    u"Ланселот",
    u"Галахад",
    u"Персиваль",
    u"Борс",
    u"Кей",
    u"Мордред",
    u"Гарет",
    u"Уриенс",
    u"Ивейн",
    u"Оуэн",
    u"Бедивер",
    u"Гахерис",
    u"Агравейн"
]

knight_last_names = [
    u"Озерный",
    u"Подгорный",
    u"Лесной",
    u"Православный",
    u"Поземный",
    u"Луговой"
]

knight_abilities = Container(
    "knight_abilities",
    {
        "brave": {
            "name": u"Отважный",
            "description": u"Не боится дракона, как бы страшен он ни был",
            "modifiers": ["fearless"]
        },
        "charmed": {
            "name": u"Зачарованный",
            "description": u"Способен атаковать логово с любыми условиями доступа",
            "modifiers": ["swimming", "flight", "alpinism"]
        },
        "liberator": {
            "name": u"Освободитель",  # TODO: implement
            "description": u"+1 к защите за каждую крестьянку, "
                           u"+1 к атаке за каждую богатую и "
                           u"+1 к атаке и защите за любую другую не великаншу томящуюся в логове дракона",
            "modifiers": []
        },
        "firstborn": {
            "name": u"Первенец",  # TODO: implement
            "description": u"Получает 2 шмотки сразу со старта",
            "modifiers": []
        },
        "fiery": {
            "name": u"Вспыльчивый",
            "description": u"+2 к атаке",
            "modifiers": ['atk_up', 'atk_up']
        },
        "cautious": {
            "name": u"Осторожный",
            "description": u"+2 к защите",
            "modifiers": ['def_up', 'def_up']
        }
    }
)

knight_items = Container(
    "knight_items",
    {
        # TODO: implement
        # Нагрудники
        "basic_vest": {
            "name": u"Дубовая броня",
            "description": u"Не дает преимуществ",
            "type": "vest",
            "basic": True,
            "modifiers": []
        },
        "glittering_vest": {
            "name": u"Сверкающий доспех",
            "description": u"+2 к защите",
            "type": "vest",
            "basic": False,
            "modifiers": ['def_up', 'def_up']
        },
        "gold_vest": {
            "name": u"Золочёный доспех",
            "description": u"1 верная защита",
            "type": "vest",
            "basic": False,
            "modifiers": ['sdef_up']
        },
        "magic_vest": {
            "name": u"Волшебный доспех",  # TODO: implement
            "description": u"защита от одного типа элементов",
            "type": "vest",
            "basic": False,
            "modifiers": []
        },
        # Копья
        "basic_spear": {
            "name": u"Деревянное копье",
            "description": u"Не дает преимуществ",
            "type": "spear",
            "basic": True,
            "modifiers": []
        },
        "blued_spear": {
            "name": u"Вороненое копье",
            "description": u"+2 к атаке",
            "type": "spear",
            "basic": False,
            "modifiers": ['atk_up', 'atk_up']
        },
        "spear_with_scarf": {
            "name": u"Копье с шарфом",
            "description": u"1 верная атака",
            "type": "spear",
            "basic": False,
            "modifiers": ['satk_up']
        },
        "dragonslayer_spear": {
            "name": u"Копьё-драконобой",  # TODO: implement
            "description": u"+1 к атаке, если дракон ранен он вместо этого сразу теряет голову",
            "type": "spear",
            "basic": False,
            "modifiers": []
        },
        # Мечи
        "basic_sword": {
            "name": u"Деревянный меч",
            "description": u"Не дает преимуществ",
            "type": "sword",
            "basic": True,
            "modifiers": []
        },
        "glittering_sword": {
            "name": u"Сияющий клинок",
            "description": u"+2 к атаке",
            "type": "sword",
            "basic": False,
            "modifiers": ['atk_up', 'atk_up']
        },
        "lake_woman_sword": {
            "name": u"Клинок озёрной девы",
            "description": u"1 верная атака",
            "type": "sword",
            "basic": False,
            "modifiers": ['satk_up']
        },
        "flameberg_sword": {
            "name": u"Пылающий фламберг",
            "description": u"2 верных атаки огнём",
            "type": "sword",
            "basic": False,
            "modifiers": ['sfatk_up', 'sfatk_up']
        },
        "icecracker_sword": {
            "name": u"Ледоруб-жыдобой ^_^",
            "description": u"2 верных атаки льдом",
            "type": "sword",
            "basic": False,
            "modifiers": ['siatk_up', 'siatk_up']
        },
        "thunderer_sword": {
            "name": u"Меч-громобой",
            "description": u"2 верных атаки молнией",
            "type": "sword",
            "basic": False,
            "modifiers": ['slatk_up', 'slatk_up']
        },
        # Щиты
        "basic_shield": {
            "name": u"Деревянный щит",
            "description": u"Не дает преимуществ",
            "type": "shield",
            "basic": True,
            "modifiers": []
        },
        "polished_shield": {
            "name": u"Полированный щит",
            "description": u"+2 к защите",
            "type": "shield",
            "basic": False,
            "modifiers": ['def_up', 'def_up']
        },
        "mirror_shield": {
            "name": u"Зерцальный щит",  # TODO: Implement
            "description": u"2 верных защиты, если у дракона есть дыхание",
            "type": "shield",
            "basic": False,
            "modifiers": []
        },
        # Кони
        "basic_horse": {
            "name": u"Деревянная лошадка",
            "description": u"Не дает преимуществ",
            "type": "horse",
            "basic": True,
            "modifiers": []
        },
        "white_horse": {
            "name": u"Белый конь",
            "description": u"+1 к атаке, +1 к защите",
            "type": "horse",
            "basic": False,
            "modifiers": ['atk_up', 'def_up']
        },
        "pegasus": {
            "name": u"Пегас",
            "description": u"даёт полёт",
            "type": "horse",
            "basic": False,
            "modifiers": ['flight']
        },
        "firehorse": {
            "name": u"Конь-огонь",
            "description": u"даёт альпинизм и защиту от огня",
            "type": "horse",
            "basic": False,
            "modifiers": ['alpinism', 'fire_immunity']
        },
        "sivka": {
            "name": u"Сивка-Бурка",
            "description": u"даёт альпинизм и защиту от холода",
            "type": "horse",
            "basic": False,
            "modifiers": []
        },
        "kelpie": {
            "name": u"Келпи",
            "description": u"игнорирует недоступность морского логова",
            "type": "horse",
            "basic": False,
            "modifiers": ['swimming']
        },
        "griffon": {
            "name": u"Боевой грифон",
            "description": u"+1 к атаке, +1 к защите, даёт полёт",
            "type": "horse",
            "basic": False,
            "modifiers": ['atk_up', 'def_up', 'flight']
        },
        # Спутники
        "basic_follower": {
            "name": u"Деревянный спутник",
            "description": u"Не дает преимуществ",
            "type": "follower",
            "basic": True,
            "modifiers": []
        },
        "squire": {
            "name": u"Ловкий оруженосец",
            "description": u"даёт \"альпинизм\"",
            "type": "follower",
            "basic": False,
            "modifiers": ['alpinism']
        },
        "veteran": {
            "name": u"Старый ветеран",
            "description": u"даёт 1 верную защиту",
            "type": "follower",
            "basic": False,
            "modifiers": ['sdef_up']
        },
        "pythoness": {
            "name": u"Прорицательница",
            "description": u"даёт 1 верную атаку",
            "type": "follower",
            "basic": False,
            "modifiers": ['satk_up']
        },
        "thaumaturge": {
            "name": u"Кудесник",
            "description": u"даёт 1 верную атаку и 1 верную защиту",
            "type": "follower",
            "basic": False,
            "modifiers": ['satk_up', 'sdef_up']
        }
    }
)

knight_titles = [
    u"Бедный рыцарь",
    u"Странствующий рыцарь",
    u"Межевой рыцарь",
    u"Благородный рыцарь",
    u"Паладин рыцарь",
    u"Прекрасный принц"]

knight_events = {
    "spawn": "lb_event_knight_spawn",
    "prepare": None,
    "prepare_usefull": None,
    "prepare_useless": None,
    "receive_item": "lb_event_knight_receive_item",
}

#
# Логово
#

lair_types = Container(
    "lair_types",
    {
        "impassable_coomb": {
            "name": u"Буреломный овраг",
            "inaccessability": 0
        },
        "impregnable_peak": {
            "name": u"Неприступная вершина",
            "inaccessability": 0,
            "require": ["aplinism"],
            'prerequisite': ['wings']
        },
        "solitude_сitadel": {
            "name": u"Цитадель одиночества",
            "inaccessability": 0,
            "require": ["aplinism", "coldproof"],
            'prerequisite': ['wings', 'ice_immunity']
        },
        "vulcano_chasm": {
            "name": u"Вулканическая расселина",
            "inaccessability": 0,
            "require": ["aplinism", "fireproof"],
            'prerequisite': ['wings', 'fire_immunity']
        },
        "underwater_grot": {
            "name": u"Подводный грот",
            "inaccessability": 0,
            "require": ["swimming"],
            'prerequisite': ['swimming']
        },
        "underground_burrow": {
            "name": u"Подземная нора",
            "inaccessability": 1,
            "require": [],
            'prerequisite': ['can_dig']
        },
        "dragon_castle": {
            "name": u"Драконий замок",
            "inaccessability": 1,
            "require": []
        },
        "castle": {
            "name": u"Старые руины",
            "inaccessability": 1,
            "require": []
        },
        "ogre_den": {
            "name": u"Берлога людоеда",
            "inaccessability": 1,
            "require": []
        },
        "broad_cave": {
            "name": u"Просторная пещера",
            "inaccessability": 1,
            "require": []
        },
        "tower_ruin": {
            "name": u"Руины башни",
            "inaccessability": 0,
            "provide": ["magic_traps"]
        },
        "monastery_ruin": {
            "name": u"Руины монастыря",
            "inaccessability": 1,
            "require": []
        },
        "fortress_ruin": {
            "name": u"Руины каменной крепости",
            "inaccessability": 2,
            "require": []
        },
        "castle_ruin": {
            "name": u"Руины королевского замка",
            "inaccessability": 1,
            "require": []
        },
        "ice_citadel": {
            "name": u"Ледяная цитадель",
            "inaccessability": 1,
            "require": ["aplinism", "coldproof"]
        },
        "vulcanic_forge": {
            "name": u"Вулканическая кузница",
            "inaccessability": 1,
            "require": ["aplinism", "fireproof"]
        },
        "forest_heart": {
            "name": u"Дупло Великого Древа",
            "inaccessability": 2,
            "provide": ["magic_traps"]
        },
        "cloud_castle": {
            "name": u"Замок в облаках",
            "inaccessability": 2,
            "require": ["flight"]
        },
        "underwater_mansion": {
            "name": u"Подводные хоромы",
            "inaccessability": 1,
            "require": ["swimming"]
        },
        "underground_palaces": {
            "name": u"Подгорные чертоги",
            "inaccessability": 2,
            "require": ["aplinism"],
            "provide": ["mechanic_traps"]
        },
    }
)

lair_upgrades = Container(
    "lair_upgrades",
    {
        "mechanic_traps": {
            "name": u"Механические ловушки",
            "protection": 1
        },
        "magic_traps": {
            "name": u"Магические ловушки",
            "protection": 1
        },
        "poison_guards": {
            "name": u"Ядовитые стражи",
            "protection": 1
        },
        "regular_guards": {
            "name": u"Обычные стражи",
            "replaces": "smuggler_guards",  # какое улучшение автоматически заменяет
            "protection": 2
        },
        "smuggler_guards": {
            "name": u"Охранники",
            "cost": 100,
            "protection": 2
        },
        "elite_guards": {
            "name": u"Элитные стражи",
            "protection": 3
        },
        "gremlin_fortification": {
            "name": u"Укрепления",
            "inaccessability": 1,
            "protection": 0
        },
        "gremlin_servant": {
            "name": u"Слуги-гремлины",
            "cost": 100,
            "protection": 0
        },
        "servant": {
            "name": u"Слуги",
            "replaces": "gremlin_servant",  # какое улучшение автоматически заменяет
            "protection": 0
        }
    }
)

attack_types = ['base', 'fire', 'ice', 'poison', 'sound', 'lightning']
protection_types = ['base', 'scale', 'shield', 'armor']

#
# Дурная слава
#

reputation_levels = {
    0: 0,
    3: 1,
    6: 2,
    10: 3,
    15: 4,
    21: 5,
    28: 6,
    36: 7,
    45: 8,
    55: 9,
    66: 10,
    78: 11,
    91: 12,
    105: 13,
    120: 14,
    136: 15,
    153: 16,
    171: 17,
    190: 18,
    210: 19,
    231: 20
}

reputation_gain = {
    1: u"Этот поступок люди наверняка заметят.",
    3: u"Дурная слава о ваших поступках разносится по королевству.",
    5: u"Сегодня вы стяжали немалую дурную славу.",
    10: u"Об этом деянии услышат  жители всего королевства. И ужаснутся.",
    25: u"О деянии столь ужасном будут сложены легенды, которые не забудутся и через сотни лет"
}

#
# Дракон
#

# имена
dragon_names = [
    u'Азог',
    u'Ауринг',
    u'Алафис',
    u'Брагнор',
    u'Беливирг',
    u'Бладвинг',
    u'Беоргис',
    u'Буран',
    u'Висерин',
    u'Вазгор',
    u'Балерион',
    u'Мераксес',
    u'Вхагар',
    u'Сиракс',
    u'Тираксес',
    u'Вермакс',
    u'Арракс',
    u'Караксес',
    u'Тандрос',
    u'Мунхайд',
    u'Силвервинг',
    u'Вермитор',
    u'Шиптиф',
    u'Вермитор',
    u'Шрикос',
    u'Моргул',
    u'Урракс',
    u'Дрого',
    u'Рейегаль',
    u'Визерион',
    u'Эссовиус',
    u'Гискар',
    u'Валерион',
    u'Вермитракс',
    u'Архоней',
    u'Дестирион',
    u'Алхафтон',
    u'Торогрим',
    u'Коринстраз',
    u'Ираникус',
    u'Чарис',
    u'Итариус',
    u'Изондр',
    u'Литурган',
    u'Таэрад',
    u'Морфалаз',
    u'Нефариан',
    u'Сеарнокс',
    u'Пион',
    u'Ладон',
    u'Сципион',
    u'Эрихтон',
    u'Горонис',
    u'Горгатрокс',
    u'Артаксеркс',
    u'Айтварас',
    u'Балаур',
    u'Орлангур',
    u'Шадизар',
]

dragon_surnames = [
    u'Яростный',
    u'Могучий',
    u'Ужасный',
    u'Бурерождённый',
    u'Зловещий',
    u'Тёмный',
    u'Жестокий',
    u'Надменный',
    u'Жадный',
    u'Алчный',
    u'Безжалостный',
    u'Беспощадный',
    u'Гордый',
    u'Прожорливый',
    u'Громогласный',
    u'Устрашающий',
    u'Погибельный',
    u'Сварливый',
    u'Великолепный',
    u'Завистливый',
    u'Порочный',
    u'Змееглазый',
    u'Длиннохвостый',
    u'Уродливый',
    u'Шипочешуйный',
    u'Злокозненный',
    u'Осквернитель',
    u'Пожиратель',
    u'Разрыватель',
    u'Роковой',
    u'Смертоносный',
    u'Скрытный',
    u'Кровавый',
    u'Саблеклык',
    u'Искуситель',
    u'Бесстыдный',
    u'Смрадный',
    u'Загребущий',
    u'Срамотряс',
    u'Пронзатель',
    u'Сластолюбивый',
    u'Гневный',
    u'Кишкодёр',
    u'Живодёр',
    u'Живоглот',
    u'Праздный',
    u'Ослизлый',
    u'Разрушитель',
    u'Змееед',
    u'Проклятый',
    u'Кровожадный',
    u'Растлитель',
    u'Безбожный',
    u'Властный',
    u'Лживый',
    u'Буревесник',
    u'Подлый',
    u'Двуличный',
    u'Мудрый',
    u'Зоркий',
    u'Стремительный',
    u'Нечистивый',
]

# Размеры
dragon_size = [
    u'Мелкий',
    u'Средних размеров',
    u'Крупный',
    u'Внушительный',
    u'Огромный',
    u'Исполинский',
]

dragon_size_description = [
    u'Его размеры вряд ли кого-то впечатлят. '
    u'Хотя и сильно вытянутый в длинну, змей весит не больше чем крупная крестьянская собака.',

    u'Он весит примерно столько же сколько и взрослый, здоровый мужчина. Ничего поразительного.',

    u'Достаточно велик чтобы пококнурировать размерами с небольшой лошадью или откормленным годовалым бычком.',

    u'В местных лесах вряд ли найдётся зверь способный потягаться с ним в размерах. '
    u'Разве что самые откормленные быки или пещерные медведи смогут с ним сравниться.',

    u'Пожалуй по своему весу и размеру он заткнёт за пояс даже африканского слона. '
    u'Не говоря уже об обитателях лесов и полей этого королевства. Тут ему равных нет.',

    u'На его фоне даже титаны смотрятся бледно, разве что кашалот или кракен весит примерно столько же. '
    u'Но могут ли они быть столь же ловкими и смертносными на суше и в воздухе?',
]

head_description = {
    'green': u'не имеет особых способностей',
    'red': u'изрыгает дымное плямя',
    'white': u'обладает леденящим дыханием',
    'blue': u'оснащена жабрами и плавниками',
    'black': u'испускает нозрдями ядовитые испарения',
    'iron': u'щетинится стальными пластинами',
    'bronze': u'способна рыть землю как бронзовый ковш',
    'silver': u'украшена гребнем по которому струятся молнии',
    'gold': u'способна видеть невидимое',
    'shadow': u'повелевает жуткой некромантией'
}

wings_description = [
    u'Он ползает извиваясь по земле подобно исполинскому змею.',
    u'Он оснащен могучими крыльями, способными нести его по воздуху.',
    u'У него на спине две пары перепончатых крыл',
    u'Он оснащён тремя парами разноразмерных крыльев, обеспечиваюих невероятную маневренность.'
]

paws_description = [
    u'Он ползает извиваясь по земле подобно исполинскому змею.',
    u'Он опирается на пару мощных когтистых лап',
    u'У него четыре когтистые лапы.',
    u'Три пары мощных когтистых лап дают ему невероятную подвижность и устойчивость.'
]

special_features = ('tough_scale', 'poisoned_sting', 'clutches', 'horns', 'fangs', 'ugly')

special_description = [
    u'Его чешуя крепче чем закалённая цвергами сталь.',

    u'На конце его длинного, извивающегося хвоста находится страшное жало, сочащееся несущим погибель ядом.',

    u'Его когти острее бритвы и способны пронзить насквозь даже самые прочные доспехи.',

    u'Величественно изогнутые рога защищают его голову с боков и делают облик дракона ещё более внушительным.',

    u'Его огромные клыки внушают трепет врагу ибо могут играючи разорвать на части даже самого крупного зверя.',

    u'Он настолько чудовищен в своём уродстве, что не каждый отважится даже взглянуть на него прямо, '
    u'а слабые сердцем бегут от одного лишь его вида.',

    u'В глазах дракона читается хитрость и коварство. Он владеет запретным колдовством.',

    u'Сверкающие подобно полированному антрациту глаза дракона обладают гипнотической силой. '
    u'Его колдовская мощь велика.',

    u'Взгляд дракона светится нечеловеческим коварством. Сила его колдовских чар просто невероятна.'
]

# TODO: Текстовый модуль с числительными
head_num = [
    u'основная',
    u'вторая',
    u'третья',
    u'четвёртая',
    u'пятая',
    u'шестая',
    u'седьмая',
    u'восьмая',
    u'девятая'
]

# описание числа голов
head_count = {
    2: u"двуглавый",
    3: u"трехглавый",
    4: u"четырёхглавый",
    5: u"пятиглавый",
    6: u"шестиглавый",
    7: u"семиглавый",
    8: u"восьмиглавый",
    9: u"многоглавый",
    10: u"многоглавый",
    11: u"многоглавый",
}

# Типы голов(цвета)
dragon_heads = {
    'green': [],
    'red': ['fire_breath', 'fire_immunity'],
    'white': ['ice_breath', 'ice_immunity'],
    'blue': ['swimming'],
    'black': ['black_power', 'poison_breath'],  # black_power -- +1 атака
    'iron': ['iron_scale', 'sound_breath'],  # iron_scale -- +1 защита
    'bronze': ['bronze_scale', 'can_dig'],  # bronze_scale -- +1 защита
    'silver': ['silver_magic', 'lightning_immunity'],
    'gold': ['gold_magic', 'greedy'],  # greedy -- -2 к шансам вора
    'shadow': ['shadow_magic', 'fear_of_dark'],  # fear_of_dark -- +2 к страху
}

heads_name_rus = {
    'red': u"красный",
    'black': u"чёрный",
    'blue': u"синий",
    'gold': u"золотой",
    'silver': u"серебряный",
    'bronze': u"бронзовый",
    'iron': u"стальной",
    'shadow': u"фантомный",
    'white': u"белый",
    'green': u"зеленый"
}

dragon_gifts = dict()

# Заклинания
spell_list = {
    # заговоры -- дают иммунитет к атаке выбранного типа
    'fire_protection': ['fire_immunity'],
    'ice_protection': ['ice_immunity'],
    'poison_protection': ['poison_immunity'],
    'lightning_protection': ['lightning_immunity'],
    'sound_protection': ['sound_immunity'],
    # сердца -- дают дыхание нужного типа
    'fire_heart': ['fire_breath'],
    'ice_heart': ['ice_breath'],
    'poison_heart': ['poison_breath'],
    'thunder_heart': ['sound_breath'],
    'lightning_heart': ['lightning_breath'],
    # прочие
    'wings_of_wind': ['wings_of_wind'],
    'aura_of_horror': ['aura_of_horror'],
    'unbreakable_scale': ['virtual_head'],
    'spellbound_trap': ['spellbound_trap']
}

# Русское название для отображения заклинания
spell_list_rus = {
    # заговоры -- дают иммунитет к атаке выбранного типа
    'fire_protection': u"Заговор от огня",
    'ice_protection': u"Заговор от льда",
    'poison_protection': u"Заговор от яда",
    'lightning_protection': u"Заговор от молнии",
    'sound_protection': u"Заговор от грома",
    # сердца -- дают дыхание нужного типа
    'fire_heart': u"Огненное сердце",
    'ice_heart': u"Ледяное сердце",
    'poison_heart': u"Отравленное сердце",
    'thunder_heart': u"Громовое сердце",
    'lightning_heart': u"Сердце молнии",
    # прочие
    'wings_of_wind': u"Крылья ветра",
    'aura_of_horror': u"Аура ужаса",
    'unbreakable_scale': u"Второй шанс",
    'spellbound_trap': u"Колдовская западня"
}

effects_list = {
    # спецеффекты от еды и других прокачек дракона помимо собственных заклинаний
    'boar_meat': ['atk_up'],
    'bear_meat': ['def_up'],
    'griffin_meat': ['mg_up'],
}

modifiers = {
    # global
    'fire_immunity': Modifier(),
    'ice_immunity': Modifier(),
    'poison_immunity': Modifier(),
    'lightning_immunity': Modifier(),
    'sound_immunity': Modifier(),
    'magic_immunity': Modifier(),

    'flight': Modifier(),
    'alpinism': Modifier(),
    'swimming': Modifier(),

    'atk_up': Modifier(attack=('base', (1, 0))),  # 1 простая атака
    'satk_up': Modifier(attack=('base', (0, 1))),  # 1 верная атака
    'sfatk_up': Modifier(attack=('fire', (0, 1))),  # 1 верная атака огнем
    'siatk_up': Modifier(attack=('ice', (0, 1))),  # 1 верная атака льдом
    'slatk_up': Modifier(attack=('lightning', (0, 1))),  # 1 верная атака молнией
    'def_up': Modifier(protection=('base', (1, 0))),  # 1 защита
    'sdef_up': Modifier(protection=('base', (0, 1))),  # 1 верная защита
    # Knight-specific
    'fearless': Modifier(),
    # Dragon-specific
    'can_dig': Modifier(),
    'greedy': Modifier(),
    'virtual_head': Modifier(),
    'spellbound_trap': Modifier(),

    'fire_breath': Modifier(attack=('fire', (0, 1))),
    'ice_breath': Modifier(attack=('ice', (0, 1))),
    'poison_breath': Modifier(attack=('poison', (0, 1))),
    'sound_breath': Modifier(attack=('sound', (0, 1))),
    'lightning_breath': Modifier(attack=('lightning', (0, 1))),
    'black_power': Modifier(attack=('base', (1, 0))),
    'iron_scale': Modifier(protection=('scale', (1, 0))),
    'bronze_scale': Modifier(protection=('scale', (1, 0))),
    'silver_magic': Modifier(magic=1),
    'gold_magic': Modifier(magic=1),
    'shadow_magic': Modifier(magic=1),
    'fear_of_dark': Modifier(fear=2),
    'aura_of_horror': Modifier(fear=1),
    'wings_of_wind': Modifier(energy=1),
    #
    'size': Modifier(attack=('base', (1, 0)), protection=('base', (1, 0)), fear=1),
    'paws': Modifier(attack=('base', (1, 0)), energy=1),
    'wings': Modifier(protection=('base', (1, 0)), energy=1),
    'tough_scale': Modifier(protection=('scale', (0, 1))),
    'clutches': Modifier(attack=('base', (0, 1))),
    'fangs': Modifier(attack=('base', (2, 0)), fear=1),
    'horns': Modifier(protection=('base', (2, 0)), fear=1),
    'ugly': Modifier(fear=2),
    'poisoned_sting': Modifier(attack=('poison', (1, 1))),
    'cunning': Modifier(magic=1),
    #
    'mg_up': Modifier(magic=1),
}


def get_modifier(name):
    if name in modifiers:
        return modifiers[name]
    raise NotImplementedError(name)

# логова, картинки
lair_image = {
    'ravine': 'ravine'
}

# Словарь с "достопримечательностями",
# ключ - название этапа,
# значение - кортеж из названия этапа для меню и названия метки, к которой нужно совершить переход
special_places = {
    # лесная пещера с огром
    'enc_ogre': (u"Пещера людоеда", 'lb_enc_fight_ogre'),
    'explore_ogre_den': (u"Исследовать пещеру людоеда", 'lb_enc_explore_ogre_den'),
    'create_ogre_lair': (u"Поселиться в пещере людоеда", 'lb_enc_create_ogre_lair'),
    # йотун
    'jotun_full': (u"Ледяная цитадель", 'lb_jotun'),
    'jotun_empty': (u"Пустой замок в горах", 'lb_jotun_empty'),
    # Ифрит
    'ifrit_full': (u"Вулканическая кузня", 'lb_ifrit'),
    'ifrit_empty': (u"Пустая вулканическая кузня", 'lb_ifrit_empty'),
    # Тритон
    'triton_full': (u"Подводные хоромы", 'lb_triton'),
    'triton_empty': (u"Подводные руины", 'lb_triton_empty'),
    # Титан
    'titan_full': (u"Облачный замок", 'lb_titan'),
    'titan_empty': (u"Разорённый облачный замок", 'lb_titan_empty'),
    # рыцарский манор
    'manor_full': (u"Укреплённая усадьба", 'lb_manor'),
    'manor_empty': (u"Заброшенная усадьба", 'lb_manor_empty'),
    # деревянный замок
    'wooden_fort_full': (u"Деревянный замок", 'lb_wooden_fort'),
    'wooden_fort_empty': (u"Опустевший форт", 'lb_wooden_fort_empty'),
    # монастрыь
    'abbey_full': (u"Укреплённый монастрыь", 'lb_abbey'),
    'abbey_empty': (u"Разорённый монастырь", 'lb_abbey_empty'),
    # каменный замок
    'castle_full': (u"Каменная крепость", 'lb_castle'),
    'castle_empty': (u"Пустая крепость", 'lb_castle_empty'),
    # королевский замок
    'palace_full': (u"Королевский замок", 'lb_palace'),
    'palace_empty': (u"Пустой дворец", 'lb_palace_empty'),
    # зачарованный лес
    'enter_ef': (u"Зачарованный лес", 'lb_enchanted_forest'),
    'dead_grove': (u"Заброшенная роща альвов", 'lb_dead_grove'),
    # задний проход в морию
    'backdor_open': (u"Задний проход", 'lb_backdor'),
    'backdor_sealed': (u"Задний проход", 'lb_backdor_sealed'),
    # мория
    'frontgates_guarded': (u"Врата Подгорного Царства", 'lb_frontgates'),
    'frontgates_open': (u"Разбитые врата", 'lb_frontgates_open'),
}

quest_list = (  # TODO: внести все выполнимые на сегодня квесты
    {  # только для дебага, не используется
       'min_lvl': 25,  # минимальный уровень дракона для получения квеста
       'max_lvl': 25,  # максимальный уровень дракона для получения квеста
       'text': u"Проживи 5 лет.",  # текст квеста
       'fixed_time': 25,  # количество лет на выполнение квеста, не зависящее от уровня дракона
       'task': 'autocomplete',
       # ключевое слово для описания задачи, 'autocomplete' - задача выполняется автоматически
    },
    {
        'min_lvl': 1,  # минимальный уровень дракона для получения квеста
        'max_lvl': 1,  # максимальный уровень дракона для получения квеста
        'text': u"Породить любое потомство.",  # текст квеста
        'fixed_time': 5,  # количество лет на выполнение квеста, не зависящее от уровня дракона
        'task': 'offspring',  # ключевое слово для описания задачи, 'offspring' - породить потомство
        'task_requirements': ('free_spawn', 'educated_spawn')
        # кортеж с требованиями, для выполнения задания нужно выполнить любое из них,
        # 'free_spawn' - потомство, рождённое на воле, 'educated_spawn' - воспитанное потомство
    },
    {
        'min_lvl': 2,  # минимальный уровень дракона для получения квеста
        'max_lvl': 2,  # максимальный уровень дракона для получения квеста
        # текст квеста, {0} будет заменён на требуемый уровень
        'text': u"Стяжать дурную славу {0} или более.",
        'fixed_time': 5,  # количество лет на выполнение квеста, не зависящее от уровня дракона
        # ключевое слово для описания задачи, 'reputation' - проверяется уровень дурной славы
        'task': 'reputation',
        'fixed_threshold': 1,  # 'fixed_'+ ключевое слово для задания фиксированного требуемого значения
    },
    {
        'min_lvl': 3,  # минимальный уровень дракона для получения квеста
        'max_lvl': 3,  # максимальный уровень дракона для получения квеста
        'text': u"Снизить боеспособность королевства.",  # текст квеста
        'fixed_time': 10,  # количество лет на выполнение квеста, не зависящее от уровня дракона
        # ключевое слово для описания задачи, 'poverty' - проверяется уровень понижения мобилизации из-за разрухи
        'task': 'poverty',
        'fixed_threshold': 1,  # 'fixed_'+ ключевое слово для задания фиксированного требуемого значения
    },
    {
        # минимальный уровень дракона для получения квеста
        'min_lvl': 4,
        # максимальный уровень дракона для получения квеста
        'max_lvl': 4,
        # текст квеста
        'text': u"Переселиться в приличное логово, сделать там любое улучшение, завести слуг и охрану.",
        # количество лет на выполнение квеста, не зависящее от уровня дракона
        'fixed_time': 10,
        # ключевое слово для описания задачи, 'lair' - проверяется тип логова и его улучшений
        'task': 'lair',
        # кортеж с описанием препятствий для выполнения квеста,
        # 'impassable_coomb' - буреломный овраг, квест не выполнится с этим типом логова
        'task_obstruction': ('impassable_coomb',),
        # кортеж с требованиями, для выполнения задания нужно выполнить любое из них,
        # чтобы потребовать список требований - нужно использовать кортеж внутри кортежа
        # а для вариантов среди списка требований - нужно использовать котреж,
        # который будет внутри кортежа для списка, который уже внутри кортежа
        'task_requirements': (
            ('mechanic_traps', 'magic_traps', 'gremlin_fortification'),
            ('gremlin_servant', 'servant'),
            ('poison_guards', 'regular_guards', 'elite_guards')
        )
    },
    {
        'min_lvl': 5,  # минимальный уровень дракона для получения квеста
        'max_lvl': 5,  # максимальный уровень дракона для получения квеста
        'text': u"Поймать вора или одолеть рыцаря в собственном логове.",  # текст квеста
        'fixed_time': 25,  # количество лет на выполнение квеста, не зависящее от уровня дракона
        'task': 'event',  # ключевое слово для описания задачи, 'event' - должно произойти какое-то событие
        # кортеж с требованиями, нужно либо 'thief_killer' - поймать вора, либо 'knight_killer' - убить рыцаря
        'task_requirements': ('thief_killer', 'knight_killer',),
    },
    {
        'min_lvl': 6,  # минимальный уровень дракона для получения квеста
        'max_lvl': 11,  # максимальный уровень дракона для получения квеста
        # текст квеста, {0} будет заменён на требуемый уровень
        'text': u"Стяжать дурную славу {0} или более.",
        'lvlscale_time': 5,  # на что нужно умножить уровень дракона, чтобы получить число лет на выполнение
        # ключевое слово для описания задачи, 'reputation' - проверяется уровень дурной славы
        'task': 'reputation',
        'fixed_threshold': 1,  # задаёт фиксированное значения для задачи
        # число, на которое нужно умножить уровень дракона, чтобы получить необходимый уровень
        'lvlscale_threshold': 1,
    },
    {
        'min_lvl': 6,  # минимальный уровень дракона для получения квеста
        'max_lvl': 11,  # максимальный уровень дракона для получения квеста
        # текст квеста, {0} будет заменён на требуемый уровень
        'text': u"Достичь суммарной стоимости золотого ложа не менее {0} фартингов.",
        'lvlscale_time': 5,  # на что нужно умножить уровень дракона, чтобы получить число лет на выполнение
        'task': 'wealth',  # ключевое слово для описания задачи, 'wealth' - проверяется стоимость сокровищ
        'fixed_threshold': 5000,  # задаёт фиксированное значения для задачи
        # число, на которое нужно умножить уровень дракона, чтобы получить необходимый уровень
        'lvlscale_threshold': 1000,
    },
    {
        'min_lvl': 6,  # минимальный уровень дракона для получения квеста
        'max_lvl': 11,  # максимальный уровень дракона для получения квеста
        # текст квеста, {0} будет заменён на требуемый уровень
        'text': u"Подарок для Владычицы. Драгоценность стоимостью {0} фартингов.",
        'lvlscale_time': 5,  # на что нужно умножить уровень дракона, чтобы получить число лет на выполнение
        'task': 'gift',  # ключевое слово для описания задачи, 'wealth' - проверяется стоимость сокровищ
        # число, на которое нужно умножить уровень дракона, чтобы получить необходимый уровень
        'lvlscale_threshold': 100,
    },
    {
        'min_lvl': 6,  # минимальный уровень дракона для получения квеста
        'max_lvl': 11,  # максимальный уровень дракона для получения квеста
        'text': u"Породить потомка от великанши.",  # текст квеста
        'fixed_time': 50,  # количество лет на выполнение квеста, не зависящее от уровня дракона
        'task': 'offspring',  # ключевое слово для описания задачи, 'offspring' - породить потомство
        # кортеж с требованиями, для выполнения задания нужно выполнить любое из них, 'giantess' - потомок от великанши
        'task_requirements': ('giantess',),
        # наличие этого ключа - задание выполняется только один раз в течение игры,
        # значение - ключ для game.unique, который добавится после выполнения
        'unique': 'giantess'
    },
    {
        'min_lvl': 6,  # минимальный уровень дракона для получения квеста
        'max_lvl': 11,  # максимальный уровень дракона для получения квеста
        'text': u"Разорить священную рощу альвов.",  # текст квеста
        'fixed_time': 75,  # количество лет на выполнение квеста, не зависящее от уровня дракона
        'prerequisite': 'giantess',  # ключ для game.unique, который необходим для получения этой задачи
        'task': 'event',  # ключевое слово для описания задачи, 'event' - должно произойти какое-то событие
        # кортеж с требованиями, для выполнения задания нужно выполнить любое из них,
        # 'ravage_sacred_grove' - разорить рощу альвов
        'task_requirements': ('ravage_sacred_grove',),
        # наличие этого ключа - задание выполняется только один раз в течение игры,
        # значение - ключ для game.unique, который добавится после выполнения
        'unique': 'ravage_sacred_grove'
    },
    {
        'min_lvl': 6,  # минимальный уровень дракона для получения квеста
        'max_lvl': 11,  # максимальный уровень дракона для получения квеста
        'text': u"Устроить логово в подгорном царстве цвергов.",  # текст квеста
        'fixed_time': 75,  # количество лет на выполнение квеста, не зависящее от уровня дракона
        'prerequisite': 'ravage_sacred_grove',  # ключ для game.unique, который необходим для получения этой задачи
        'task': 'lair',  # ключевое слово для описания задачи, 'lair' - проверяется тип логова и его улучшений
        'task_requirements': ('underground_palaces',),
        # кортеж с требованиями, для выполнения задания нужно выполнить любое из них, 'ravage_sacred_grove' - разорить рощу альвов
        'unique': 'underground_palaces'
        # наличие этого ключа - задание выполняется только один раз в течение игры, значение - ключ для game.unique, который добавится после выполнения
    },
    {
        'min_lvl': 12,  # минимальный уровень дракона для получения квеста
        'max_lvl': 20,  # максимальный уровень дракона для получения квеста
        'text': u"Собрать армию тьмы и захватить столицу королевства для Темной Госпожи.",  # текст квеста
        'fixed_time': 1000,  # количество лет на выполнение квеста, не зависящее от уровня дракона
        'task': 'event',  # ключевое слово для описания задачи, 'event' - должно произойти какое-то событие
        # кортеж с требованиями, для выполнения задания нужно выполнить любое из них,
        # 'victory' - заглушка для победы
        'task_requirements': ('victory',),
    },
)

# Список всех доступных для дракона событий
dragon_events = (
    'ravage_sacred_grove',  # Добавляется при уничтожении священной рощи альвов
    'thief_killer',  # Убил вора
    'knight_killer',  # Убил дакона
)

# Различный лут
loot = {
    'palace': [
        'taller',
        'taller',
        'taller',
        'taller',
        'dublon',
        'dublon',
        'dublon',
        'dish',
        'dish',
        'goblet',
        'goblet',
        'cup',
        'cup',
        'casket',
        'statue',
        'tabernacle',
        'icon',
        'tome',
        'mirror',
        'band',
        'pendant',
        'broch',
        'gemring',
        'seal',
        'crown',
        'scepter',
        'chain',
        'fibula',
        'silver',
        'gold',
        'ivory',
        'agate',
        'shell',
        'horn',
        'amber',
        'granate',
        'turmaline',
        'aqua',
        'black_pearl',
        'topaz',
        'saphire',
        'ruby',
        'emerald',
    ],

    'knight': [
        'goblet',
        'statue',
        'tome',
        'band',
        'pendant',
        'ring',
        'gemring',
        'seal',
        'armbrace',
        'chain',
        'fibula',
        'taller',
        'taller',
        'taller',
        'dublon',
        'dublon',
    ],
    'jeweler': [
        'casket',
        'phallos',
        'band',
        'diadem',
        'tiara',
        'earring',
        'necklace',
        'pendant',
        'ring',
        'broch',
        'gemring',
        'armbrace',
        'legbrace',
        'chain',
        'fibula'
    ],
    'smuggler': [
        'silver',
        'gold',
        'mithril',
        'adamantine',
        'jasper',
        'turquoise',
        'jade',
        'malachite',
        'corall',
        'ivory',
        'agate',
        'shell',
        'horn',
        'amber',
        'crystall',
        'beryll',
        'tigereye',
        'granate',
        'turmaline',
        'aqua',
        'pearl',
        'elven_beryll',
        'black_pearl',
        'topaz',
        'saphire',
        'ruby',
        'emerald',
        'goodruby',
        'goodemerald',
        'star',
        'diamond',
        'black_diamond',
        'rose_diamond',
        'taller',
        'dublon',
        'taller',
        'dublon'
    ],
    'klad': [
        'goblet',
        'statue',
        'band',
        'diadem',
        'tiara',
        'earring',
        'necklace',
        'pendant',
        'ring',
        'broch',
        'gemring',
        'seal',
        'armbrace',
        'legbrace',
        'crown',
        'scepter',
        'chain',
        'fibula',
        'silver',
        'gold',
        'mithril',
        'adamantine',
        'jasper',
        'turquoise',
        'jade',
        'malachite',
        'corall',
        'ivory',
        'agate',
        'shell',
        'horn',
        'amber',
        'crystall',
        'beryll',
        'tigereye',
        'granate',
        'turmaline',
        'aqua',
        'pearl',
        'elven_beryll',
        'black_pearl',
        'topaz',
        'saphire',
        'ruby',
        'emerald',
        'goodruby',
        'goodemerald',
        'star',
        'diamond',
        'black_diamond',
        'rose_diamond',
        'taller',
        'dublon'
    ],
    'coins': [
        'farting',
        'taller',
        'dublon'
    ],

    'church': [
        'goblet',
        'cup',
        'casket',
        'statue',
        'tabernacle',
        'icon',
        'tome',
        'seal',
    ]
}

    'any': [
        'farting',
        'taller',
        'dublon',
        'dish',
        'goblet',
        'cup',
        'casket',
        'statue',
        'tabernacle',
        'icon',
        'tome',
        'mirror',
        'comb',
        'phallos',
        'band',
        'diadem',
        'tiara',
        'earring',
        'necklace',
        'pendant',
        'ring',
        'broch',
        'gemring',
        'seal',
        'armbrace',
        'legbrace',
        'crown',
        'scepter',
        'chain',
        'fibula',
        'silver',
        'gold',
        'mithril',
        'adamantine',
        'jasper',
        'turquoise',
        'jade',
        'malachite',
        'corall',
        'ivory',
        'agate',
        'shell',
        'horn',
        'amber',
        'crystall',
        'beryll',
        'tigereye',
        'granate',
        'turmaline',
        'aqua',
        'pearl',
        'elven_beryll',
        'black_pearl',
        'topaz',
        'saphire',
        'ruby',
        'emerald',
        'goodruby',
        'goodemerald',
        'star',
        'diamond',
        'black_diamond',
        'rose_diamond'
    ]
}

# список специальных мест людей
human_special_places = [
    'lb_manor_found',
    'lb_wooden_fort_found',
    'lb_abbey_found',
    'lb_castle_found',
    'lb_palace_found',
]

game_events = {
    "mobilization_increased": "lb_event_mobilization_increase",
    "poverty_increased": "lb_event_poverty_increase",
}

dark_army = {
<<<<<<< HEAD
    "grunts": [
        u"После поражения Госпожи в Битве Шести Воинств от её армии остались жалкие ошмётки. "
        u"Немногие выжившие гоблины прячутся по своим пещерам и "
        u"размножаются словно кролики в попытке пополнить ряды войск. ",

        u"Хорошая новость: на бесплодных равнинах собралось достаточно агрессивных тварей, "
        u"чтобы из них можно было собрать настоящее войско. "
        u"Плохая: это войско будет уступать по численности тому что могут собрать Вольные Народы.",

        u"Пещер и дыр уже не хватает чтобы дать укрытие всем уродливым воинам живущим под рукой Госпожи. "
        u"Бесплодные равнины стали местом огромной стройки - тут и там возникают целые городки из шатров, "
        u"трудолюбиво окружаемые рвами, насыпями и частоколами. "
        u"На первый взгляд бойцов тут не меньше чем может выставить на поле коалиция Вольных Народов.",

        u"Взглянув на бесплодные равнины в ночи трудно понять где кончается усыпанное звёздами небо и "
        u"начинается выгоревшая земля с мириадами костров дающих свет и тепло воинам Госпожи. "
        u"Днём можно увидеть многие тысячи шатров покрывающие долину словно заросли ядовитых грибов. "
        u"Тут и там снуют вестовые и дозорные. "
        u"Эта огромная Орда захлестнёт малочисленные войска Вольных Народов словно морской прибой."
    ],
    "elites": [
        u"Но каково бы не было количество этих войск их главной слабостью является отсутствие элитных бойцов. "
        u"Столкнувшись на поле боя с великанами, эльфийскими магами и боевыми машинами цвергов, "
        u"Госпожа поняла что противостоять им смогут лишь существа "
        u"многократно превосходящие по силе людей или гоблинов. Именно таких должны породить драконы. "
        u"Именно в них отчаянно нуждается войско Госпожи.",

        u"Тут и там можно заметить огромные силуэты элитных бойцов. "
        u"Их тут не много, однако в ключевой момент они встанут на острие атаки. ",

        u"На каждый отряд мелких тварей вроде гоблинов тут приходится хотя бы один элитный боец, "
        u"порождённый драконом от самой сильной крови Вольных Народов. "
        u"Каждый их этих могучих гигантов сам стоит в бою целой армии.",

        u"В этом войске столько элитных бойцов, "
        u"что обычная мелочь вроде гоблинов служит лишь для разведки и поддержки их действий. "
        u"Ударную мощь обеспечивают уродливые гиганты порождённые драконами от самой могучей крови Вольных Народов."
    ],
    "diversity": [
        u"Армия тьмы не отличается разнообразием, "
        u"подавляющее большинство бойцов относится к одному единственному виду. "
        u"Воины Вольных Народов уже отлично умеют сражаться с такими тварями и "
        u"обладают отработанной тактикой против них.",

        u"Разнообразие войск не слишком велико, "
        u"хотя порождения драконов будут выгодно дополнять обычных гоблинов на поле боя. "
        u"Тем не менее Вольным Народам не составит труда выработать тактику противодействия и "
        u"изучить сильные и слабые места всех бойцов Госпожи.",

        u"Порождения драконов собравшиеся под знамёна Госпожи очень разнообразны. "
        u"Здесь есть дылды и коротышки, стремительные лазутчики и массивные штурмовики, всех цветов, размеров и форм. "
        u"Кого-то украшает чеушая, кого-то рога. "
        u"Выгодно дополняя друг друга на поле боя "
        u"вся эта пёстрая компания не позволит Вольным Народам использовать простую и привычную тактику боя.",

        u"Тут столько разнообразных тварей что наверное даже сама Госпожа не сможет различить их всех. "
        u"Бесконтрольно смешиваясь между собой "
        u"отродья драконов порождают новые мутатнтные гибриды с невероятными свойствами. "
        u"Когда начнётся война, Вольные Народы не будут знать как бороться с ними."
    ],
    "equipment": [
        u"Денег на снаряжение армии катастрофически не хватает. Воины Госпожи ходят в одних набедренных повязках, "
        u"вооружаются кривыми дубинами и заострёнными палками вместо копий. "
        u"Только некоторые могут позволить себе грубую броню из плохо обработанных шкур.",

        u"Армия снаряжена по минимуму. Рядовые воины могут надеяться получить железное копьё, "
        u"плетёный щит и простой стёганный доспех. Элита вооружается чуть лучше, но всё же картина далека от желаемой.",

        u"Сокровища драконов позволили неплохо снарядить бойцов Госпожи. "
        u"Даже у рядовых воинов есть полный комплект вооружения и брони, "
        u"а элита закована в воронёную сталь с ног до головы. "
        u"Ряды чёрных пик и щитов на поле боя будут смотреться очень внушительно.",

        u"За долгие годы драконы скопили для Госпожи такую кучу сокровищ, "
        u"что её с лихвой хватает для вооружения всей армии по самому высшему разряду. "
        u"Тяжёлая пехота и кавалерия вооружена до зубов, а элитные бойцы щеголяют волшебным оружием и доспехами. "
    ],
    "force": [
        u"Выступать с такими силами против Вольных Народов будет просто самоубийством.",

        u"Хотя армия тьмы и окрепла за последние годы, к битве с Вольными Народами она пока не готова.",

        u"В общем и целом Армия Тьмы достаточно боеспособна чтобы иметь шансы в битвах с войском Вольных Народов. "
        u"Однако полной уверенности в победе быть не может.",

        u"За долгие годы подготовки Армия Тьмы не просто воспаряла, но и стала могущественнее чем когда либо. "
        u"Войско Вольных Народов будет смято и растоптано этой неодолимой силой."
    ]
=======
    "grunts": {
        0: u"После поражения Госпожи в Битве Шести Воинств от её армии остались жалкие ошмётки. Немногие выжившие гоблины прячутся по своим пещерам и размножаются словно кролики в попытке пополнить ряды войск. ",
        5: u"Хорошая новость: на бесплодных равнинах собралось достаточно агрессивных тварей чтобы из них можно было собрать настоящее войско. Плохая: это войско будет уступать по численности тому что могут собрать Вольные Народы.",
        10: u"Пещер и дыр уже не хватает чтобы дать укрытие всем уродливым воинам живущим под рукой Госпожи. Бесплодные равнины стали местом огромной стройки - тут и там возникают целые городки из шатров, трудолюбиво окружаемые рвами, насыпями и частоколами. На первый взгляд бойцов тут не меньше чем может выставить на поле коалиция Вольных Народов.",
        20: u"Взглянув на бесплодные равнины в ночи трудно понять где кончается усыпанное звёздами небо и начинается выгоревшая земля с мириадами костров дающих свет и тепло воинам Госпожи. Днём можно увидеть многие тысячи шатров покрывающие долину словно заросли ядовитых грибов. Тут и там снуют вестовые и дозорные. Эта огромная Орда захлестнёт малочисленные войска Вольных Народов словно морской прибой."
    },
    "elites": {
        0: u"Но каково бы не было количество этих войск их главной слабостью является отсутствие элитных бойцов. Столкнувшись на поле боя с великанами, эльфийскими магами и боевыми машинами цвергов, Госпожа поняла что противостоять им смогут лишь существа многократно превосходящие по силе людей или гоблинов. Именно таких должны породить драконы. Именно в них отчаянно нуждается войско Госпожи.",
        1: u"Тут и там можно заметить огромные силуэты элитных бойцов. Их тут не много, однако в ключевой момент они встанут на острие атаки. ",
        3: u"На каждый отряд мелких тварей вроде гоблинов тут приходится хотя бы один элитный боец, порождённый драконом от самой сильной крови Вольных Народов. Каждый их этих могучих гигантов сам стоит в бою целой армии.",
        6: u"В этом войске столько элитных бойцов, что обычная мелочь вроде гоблинов служит лишь для разведки и поддержки их действий. Ударную мощь обеспечивают уродливые гиганты порождённые драконами от самой могучей крови Вольных Народов."
    },
    "diversity": {
        0: u"Армия тьмы не отличается разнообразием, подавляющее большинство бойцов относится к одному единственному виду. Воины Вольных Народов уже отлично умеют сражаться с такими тварями и обладают отработанной тактикой против них.",
        2: u"Разнообразие войск не слишком велико, хотя порождения драконов будут выгодно дополнять обычных гоблинов на поле боя. Тем не менее Вольным Народам не составит труда выработать тактику противодействия и изучить сильные и слабые места всех бойцов Госпожи.",
        4: u"Порождения драконов собравшиеся под знамёна Госпожи очень разнообразны. Здесь есть дылды и коротышки, стремительные лазутчики и массивные штурмовики, всех цветов, размеров и форм. Кого-то украшает чеушая, кого-то рога. Выгодно дополняя друг друга на поле боя вся эта пёстрая компания не позволит Вольным Народам использовать простую и привычную тактику боя.",
        7: u"Тут столько разнообразных тварей что наверное даже сама Госпожа не сможет различить их всех. Бесконтрольно смешиваясь между собой отродья драконов порождают новые мутатнтные гибриды с невероятными свойствами. Когда начнётся война, Вольные Народы не будут знать как бороться с ними."
    },
    "equipment": {
        0: u"Денег на снаряжение армии катастрофически не хватает. Воины Госпожи ходят в одних набедренных повязках, вооружаются кривыми дубинами и заострёнными палками вместо копий. Только некоторые могут позволить себе грубую броню из плохо обработанных шкур.",
        1: u"Армия снаряжена по минимуму. Рядовые воины могут надеяться получить железное копьё, плетёный щит и простой стёганный доспех. Элита вооружается чуть лучше, но всё же картина далека от желаемой.",
        2: u"Сокровища драконов позволили неплохо снарядить бойцов Госпожи. Даже у рядовых воинов есть полный комплект вооружения и брони, а элита закована в воронёную сталь с ног до головы. Ряды чёрных пик и щитов на поле боя будут смотреться очень внушительно.",
        3: u"За долгие годы драконы скопили для Госпожи такую кучу сокровищ, что её с лихвой хватает для вооружения всей армии по самому высшему разряду. Тяжёлая пехота и кавалерия вооружена до зубов, а элитные бойцы щеголяют волшебным оружием и доспехами. "
    },
    "force": {
        0: u"Выступать с такими силами против Вольных Народов будет просто самоубийством.",
        500: u"Хотя армия тьмы и окрепла за последние годы, к битве с Вольными Народами она пока не готова.",
        1000: u"В общем и целом Армия Тьмы достаточно боеспособна чтобы иметь шансы в битвах с войском Вольных Народов. Однако полной уверенности в победе быть не может.",
        1800: u"За долгие годы подготовки Армия Тьмы не просто воспаряла, но и стала могущественнее чем когда либо. Войско Вольных Народов будет смято и растоптано этой неодолимой силой."
    }
>>>>>>> master
}
