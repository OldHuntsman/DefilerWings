#!/usr/bin/env python
# coding=utf-8

import collections

class FighterModifier(object):
    """
    Базовый класс для разнообразных модификаторов.
    К примеру: даров владычицы, снаряжения рыцарей, заклинаний и.т.д.
    """

    def __init__(self, attack=('base', (0, 0)), protection=('base', (0, 0))):
        self.attack = attack
        self.protection = protection

    def __contains__(self, item):
        return item in self.__dict__

    def attack_filter(self, attack):
        return attack


class DragonModifier(FighterModifier):
    """
    Класс для разнообразных модификаторов.
    К примеру: даров владычицы, снаряжения рыцарей, заклинаний и.т.д.
    """

    def __init__(self, attack=('base', (0, 0)), protection=('base', (0, 0)), magic=0, fear=0, energy=0):
        super(DragonModifier, self).__init__(attack=attack, protection=protection)
        self.magic = magic
        self.fear = fear
        self.max_energy = energy

class Container(collections.defaultdict):
    '''
    Класс-хранилище разнообразных свойст/модификаторов
    TODO: реверсивный поиск
    '''
    def __init__(self,id=None,data=None,*args,**kwargs):
        super(Container, self).__init__(*args,**kwargs)
        self.id = id
        if data is not None:
        
            for key, value in data.items():
                self.add(key, value)
    
    def add(self, id, data):
        '''
        :param id: Идентификатор свойства/модификатора
        :param data: dict, содержащий парамерты этого свойства/модификатор
        '''
        if id not in self:
            if type(data) is dict:
                self[id] = Container(id, data)
            else:
                self[id] = data
        else:
            raise Exception("Already in container")
    
    def sum(self, parameter):
        '''
        :param parameter: Значение, по которому нужно суммировать аттрибуты. Суммирование проводится
                          рекурсивно.
        '''
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
        '''
        Рекурсивно возвращает лист значений по ключу
        :param key: Ключ по которому производится поиск
        :return: Список значений
        '''
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
    
    def contains(self, key):
        '''
        Возвращает список айдишников, которые содержат заданный ключ
        :param key: Ключ который должен содержать элемент
        :retuкn: список элеметов содержащих ключ, если таких элементов нет, то пустой список
        '''
        result = []
        if key in self:
            result += [ self.id ]
        for i in self:
            if type(self[i]) == type(self):
                result += self[i].contains(key)
        return result
    
    def type(self):
        '''
        For test uses
        '''
        return type(self)
    
    def __getattr__(self,name):
        return self[name]
    
    def __missing__(self,key):
        return None

#
# Вор
#

thief_first_names = [ u"Джек",
                      u"Гарри",
                      u"Cэм"]
thief_last_names = [ u"Лысый",
                     u"Скользкий",
                     u"Шустрый"]

thief_abilities = Container("thief_abilities",
                            { 
                              "climber":      { "name": u"Альпинист",
                                                "description": u"Дает \"Альпинизм\"",
                                                "provide": [ "alpinism" ] },
                              "diver":        { "name": u"Ныряльщик",
                                                "description": u"Дает \"Плавание\"",
                                                "provide": [ "swimming" ] },
                              "greedy":       { "name": u"Жадина",
                                                "description": u"Пытается украсть одно дополнительное сокровище",
                                                "provide": [ ] },
                              "mechanic":     { "name": u"Механик",
                                                "description": u"Игнорирует механические ловушки",
                                                "avoids": [ "mechanic_traps" ],
                                                "provide": [ ] },
                              "magicproof":   { "name": u"Знаток магии",
                                                "description": u"Игнорирует магические ловушки",
                                                "avoids": [ "magic_traps" ],
                                                "provide": [ ] },
                              "poisoner":     { "name": u"Отравитель",
                                                "description": u"Игнорирует ядовитых стражей",
                                                "avoids": [ "poison_guargs" ],
                                                "provide": [ ] },
                              "assassin":     { "name": u"Ассасин",
                                                "description": u"Игнорирует обычных стражей",
                                                "avoids": [ "regular_guargs" ],
                                                "provide": [ ] },
                              "night_shadow": { "name": u"Ночная тень",
                                                "description": u"Игнорирует элитных стражей",
                                                "avoids": [ "elite_guards" ], # Это странно, что он может быть пойман обычными стражами
                                                "provide": [ ] }, 
                              "trickster":    { "name": u"Ловкач",
                                                "description": u"Не имеет шанса разбудить дракона",
                                                "provide": [ ]  }
                            }
                           )

thief_items = Container("thief_items",
                        {
                          "plan":                 {"name": u"План ограбления",
                                                   "level": 1,
                                                   "description": u"+1 к уровню вора"},
                          "scheme":               {"name": u"Схема тайных проходов",
                                                   "description": u"Позволяет игнорировать неприступность логова"},
                          "sleep_dust":           {"name": u"Сонный порошок",
                                                   "description": u"Вор не имеет шанса разбудить дракона"},
                          "bottomless_sac":       {"name": u"Бездонный мешок",
                                                   "dropable": True,
                                                   "description": u"Удваивает попытки кражи"},
                          "antidot":              {"name": u"Антидот",
                                                   "description": u"Вор игнорирует ядовитых стражей",
                                                   "avoids": [ "poison_guargs" ] },
                          "enchanted_dagger":     {"name": u"Зачарованный кинжал", #Applied
                                                   "dropable": True,
                                                   "description": u"Вор игнорирует обычных стражей",
                                                   "avoids": [ "regular_guargs" ] },
                          "ring_of_invisibility": {"name": u"Кольцо-невидимка",#Applied
                                                   "dropable": True,
                                                   "description": u"Вор элитных стражей",
                                                   "avoids": [ "elite_guargs" ] },
                          "flying_boots":         {"name": u"Летучие сандалии", #Applied
                                                   "dropable": True,
                                                   "description": u"Дает \"Полёт\"",
                                                   "provide": [ "flight" ] },
                          "cooling_amulet":       {"name": u"Охлаждающий амулет", #Applied
                                                   "dropable": True,
                                                   "description": u"Дает \"защиту от огня\"",
                                                   "provide": [ "fireproof" ] },
                          "warming_amulet":       {"name": u"Согревающий амулет", #Applied
                                                   "dropable": True,
                                                   "description": u"Дает \"защиту от холода\"",
                                                   "provide": [ "coldproof" ] }
                        })

#Одинаковые айдишники вещей спасут от того, что у вора может оказаться норамльная.
thief_items_cursed = Container(
    "thief_items_cursed",
    {
      "plan":                 {"name": u"Плохой план", #Applied
                               "level": -1,
                               "cursed": True,
                               "description": u"-1 к уровню вора",
                               "fails": []},
      "bottomless_sac":       {"name": u"Дырявый мешок", #Applied
                               "cursed": True,
                               "description": u"Вор не уносит никаких сокровищ",
                               "fails": []},
      "enchanted_dagger":     {"name": u"Проклятый кинжал", #Applied
                               "cursed": True,
                               "description": u"Автоматический успех обычных стражей",
                               "fails": [ "regular_guards" ] },
      "ring_of_invisibility": {"name": u"Кольцо мерцания", #Applied
                               "cursed": True,
                               "description": u"Автоматический успех элитных стражей",
                               "fails": [ "elite_guards" ] },
      "flying_boots":         {"name": u"Ощипанные сандалии", #Applied
                               "cursed": True,
                               "description": u"Вор автоматически разбивается насмерть, если идет в логово требующее полета",
                               "fails": [ "flight" ],
                               "provide": [ "flight" ] },
      "cooling_amulet":       {"name": u"Морозильный амулет", #Applied
                               "cursed": True,
                               "description": u"Вор замораживается насмерть, если идет в огненное логово",
                               "fails": [ "fireproof" ],
                               "provide": [ "fireproof" ] },
      "warming_amulet":       {"name": u"Шашлычный амулет", #Applied
                               "cursed": True,
                               "description": u"Вор зажаривается насмерть, если идет в ледяное логово",
                               "fails": [ "coldproof" ],
                               "provide": [ "coldproof" ] }
    })

thief_titles = [ u"Мародер", 
                 u"Грабитель", 
                 u"Взломшик", 
                 u"Расхититель гробниц", 
                 u"Мастер вор" ]

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
    "spawn": None,
    "lair_unreachable": None,
    "prepare": None,
    "prepare_usefull": None,
    "prepare_unusefull": None,
    "lair_enter": "lb_test_example_lairEnter",
    "die_item": None,
    "die_inaccessability": None,
    "die_trap": None,
    "pass_trap": None,
    "receive_item": None,
    "receive_no_item": None
    }
#
# Логово
#

lair_types = Container("lair_types", {
                                "impassable_coomb"  : { "name": u"Буреломный овраг",
                                                        "inaccessability" : 0},
                                "impregnable_peak"  : { "name": u"Неприступная вершина",
                                                        "inaccessability" : 0,
                                                        "require" : [ "aplinism" ] },
                                "solitude_сitadel"  : { "name": u"Цитадель одиночества",
                                                        "inaccessability" : 0,
                                                        "require" : [ "aplinism", "coldproof" ] },
                                "vulcano_chasm"     : { "name": u"Вулканическая расселина",
                                                        "inaccessability" : 0,
                                                        "require" : [ "aplinism", "fireproof" ] },
                                "underwater_grot"   : { "name": u"Подводный грот",
                                                        "inaccessability" : 0,
                                                        "require" : [ "swimming" ] },
                                "underground_burrow": { "name": u"Подземная нора",
                                                        "inaccessability": 1,
                                                        "require" : [ ] },
                                "dragon_castle"     : { "name": u"Драконий замок",
                                                        "inaccessability" : 1,
                                                        "require" : [ ] },
                                "castle"            : { "name": u"Драконий замок",
                                                        "inaccessability" : 1,
                                                        "require" : [ ] },
                                "cannibal_den"      : { "name": u"Берлога людоеда",
                                                        "inaccessability" : 1,
                                                        "require" : [ ] },
                                "broad_cave"        : { "name": u"Просторная пещера",
                                                        "inaccessability" : 1,
                                                        "require" : [ ] },
                                "tower_ruin"        : { "name": u"Руины башни",
                                                        "inaccessability" : 0,
                                                        "provide": [ "magic_traps" ]},
                                "monastery_ruin"    : { "name": u"Руины монастыря",
                                                        "inaccessability" : 1,
                                                        "require" : [ ] },
                                "fortress_ruin"     : { "name": u"Руины каменной крепости",
                                                        "inaccessability" : 2,
                                                        "require" : [ ] },
                                "castle_ruin"       : { "name": u"Руины королевского замка",
                                                        "inaccessability" : 1,
                                                        "require" : [ ] },
                                "ice_citadel"       : { "name": u"Ледяная цитадель",
                                                        "inaccessability" : 1,
                                                        "require" : [ "aplinism", "coldproof" ] },
                                "vulcanic_forge"    : { "name": u"Вулканическая кузница",
                                                        "inaccessability" : 1,
                                                        "require" : [ "aplinism", "fireproof" ] },
                                "cloud_castle"      : { "name": u"Замок в облаках",
                                                        "inaccessability" : 2,
                                                        "require": [ "flight" ] },
                                "undefwater_mansion": { "name": u"Подводные хоромы",
                                                        "inaccessability" : 1,
                                                        "require" : [ "swimming" ] },
                                "underground_palaces": { "name": u"Подгорные чертоги",
                                                        "inaccessability" : 2,
                                                        "require" : [ "aplinism" ],
                                                        "provide": [ "mechanic_traps" ] },
                                })

lair_upgrades = Container("lair_upgrades", {
                                            "mechanic_traps" : { "name": u"Механические ловушки",
                                                                 "protection": 1},
                                            "magic_traps" : { "name": u"Магические ловушки",
                                                                 "protection": 1 },
                                            "poison_guards" : { "name": u"Ядовитые стражи",
                                                                 "protection": 1 },
                                            "regular_guards" : { "name": u"Обычные стражи",
                                                                 "protection": 2 },
                                            "elite_guards" : { "name": u"Элитные стражи",
                                                                 "protection": 3 }
                                            "gremlin_fortification" : {"name": u"Укрепления",
                                                                         "inaccessability": 1}
                                            })
attack_types = ['base', 'fire', 'ice', 'poison', 'sound', 'lightning']
protection_types = ['base', 'scale', 'shield', 'armor']

fighter_mods = {
    u"щит"      : FighterModifier(protection = ('base', (1, 0))),
    u"меч"      : FighterModifier(attack = ('base', (2,1))),
    u"броня"    : FighterModifier(protection = ('base', (0,1))),
    u"копьё"    : FighterModifier(attack = ('base', (1,1))),
    u"спутник"  : FighterModifier(attack = ('base', (1,0)), protection = ('base', (1,0))),
    u"скакун"   : FighterModifier(attack = ('base', (1,0)))
    }

# Типы голов(цвета)
dragon_heads = {
    'green' : [],
    'red'   : ['fire_breath', 'fire_immunity'],
    'white' : ['ice_breath', 'ice_immunity'],
    'blue'  : ['can_swim'],
    'black' : ['black_power', 'poison_breath'],  # black_power -- +1 атака
    'iron'  : ['iron_scale', 'sound_breath'],  # iron_scale -- +1 защита
    'bronze': ['bronze_scale', 'can_dig'],  # bronze_scale -- +1 защита
    'silver': ['silver_magic', 'lightning_immunity'],
    'gold'  : ['gold_magic', 'greedy'],  # greedy -- -2 к шансам вора
    'shadow': ['shadow_magic', 'fear_of_dark'], # fear_of_dark -- +2 к страху
    }

dragon_gifts = dict()

# Заклинания
spell_list = {
    # заговоры -- дают иммунитет к атаке выбранного типа
    'fire_protection'       : ['fire_immunity'],
    'ice_protection'        : ['ice_immunity'],
    'poison_protection'     : ['poison_immunity'],
    'lightning_protection'  : ['lightning_immunity'],
    'fire_protection'       : ['fire_immunity'],
    'sound_protection'      : ['sound_immunity'],
    # сердца -- дают дыхание нужного типа
    'fire_heart'            : ['fire_breath'],
    'ice_heart'             : ['ice_breath'],
    'poison_heart'          : ['poison_breath'],
    'thunder_heart'         : ['sound_breath'],
    'lightning_heart'       : ['lightning_breath'],
    # прочие
    'wings_of_wind'         : ['wings_of_wind'],
    'aura_of_horror'        : ['aura_of_horror'],
    'unbreakable_scale'     : ['virtual_head']
    }

dragon_modifiers = {
    'fire_immunity'     : DragonModifier(),
    'ice_immunity'      : DragonModifier(),
    'poison_immunity'   : DragonModifier(),
    'lightning_immunity': DragonModifier(),
    'sound_immunity'    : DragonModifier(),
    
    'can_swim'          :  DragonModifier(),
    'can_dig'           : DragonModifier(),
    'greedy'            : DragonModifier(),

    'fire_breath'       : DragonModifier(attack=('fire', (0, 1))),
    'ice_breath'        : DragonModifier(attack=('ice', (0, 1))),
    'poison_breath'     : DragonModifier(attack=('poison', (0, 1))),
    'sound_breath'      : DragonModifier(attack=('sound', (0, 1))),
    'lightning_breath'  : DragonModifier(attack=('lightning', (0, 1))),
    'black_power'       : DragonModifier(attack=('base', (1, 0))),
    'iron_scale'        : DragonModifier(protection=('scale', (1, 0))),
    'bronze_scale'      : DragonModifier(protection=('scale', (1, 0))),
    'silver_magic'      : DragonModifier(magic=1),
    'gold_magic'        : DragonModifier(magic=1),
    'shadow_magic'      : DragonModifier(magic=1),
    'fear_of_dark'      : DragonModifier(fear=2),
    'aura_of_horror'    : DragonModifier(fear=1),
    'wings_of_wind'     : DragonModifier(energy=1),
    #
    'size'          : DragonModifier(attack=('base', (1, 0)), protection=('base', (1, 0)), fear=1),
    'paws'          : DragonModifier(attack=('base', (1, 0)), energy=1),
    'wings'         : DragonModifier(protection=('base', (1, 0)), energy=1),
    'tough_scale'   : DragonModifier(protection=('scale', (0, 1))),
    'clutches'      : DragonModifier(attack=('base', (0, 1))),
    'fangs'         : DragonModifier(attack=('base', (2, 0)), fear=1),
    'horns'         : DragonModifier(protection=('base', (2, 0)), fear=1),
    'ugly'          : DragonModifier(fear=2),
    'poisoned_sting': DragonModifier(attack=('poison', (1, 1))),
    'cunning'       : DragonModifier(magic=1)
    }

knight_items = dict()
knight_abilities = dict()

mob = {
        "bull" : {
            "name" : u"Бык",
            "power" : 1,
            "defence" : 1,
            "intro" : u"Грозный бык дыша паром выскакиевает из-за угла"
            }
       }

def get_modifier(name):
    if name in dragon_modifiers:
        return dragon_modifiers[name]
    elif name in fighter_mods:
        return fighter_mods[name]
    raise NotImplementedError, name
