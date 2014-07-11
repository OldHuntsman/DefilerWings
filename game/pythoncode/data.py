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
            if type(self[i]) == 'pythoncode.data.Container':
                total += self[i].sum(parameter)
        return total
    
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
                                                   "description": u"Вор игнорирует ядовитых стражей"},
                          "enchanted_dagger":     {"name": u"Зачарованный кинжал",
                                                   "dropable": True,
                                                   "description": u"Вор игнорирует обычных стражей"},
                          "ring_of_invisibility": {"name": u"Кольцо-невидимка",
                                                   "dropable": True,
                                                   "description": u"Вор элитных стражей"},
                          "flying_boots":         {"name": u"Летучие сандалии",
                                                   "dropable": True,
                                                   "description": u"Дает \"Полёт\""},
                          "cooling_amulet":       {"name": u"Охлаждающий амулет",
                                                   "dropable": True,
                                                   "description": u"Дает \"защиту от огня\""},
                          "warming_amulet":      {"name": u"Согревающий амулет",
                                                   "dropable": True,
                                                   "description": u"Дает \"защиту от холода\""}
                        })

thief_titles = [ u"Мародер", 
                 u"Грабитель", 
                 u"Взломшик", 
                 u"Расхититель гробниц", 
                 u"Мастер вор" ]

#
# Логово
#

lair_types = Container("lair_types", {
                                "impassable_coomb"  : { "name": u"Буреломный овраг"},
                                "impregnable_peak"  : { "name": u"Неприступная вершина",
                                                        "require" : [ "aplinism" ] },
                                "solitude_сitadel"  : { "name": u"Цитадель одиночества",
                                                        "require" : [ "aplinism", "coldproof" ] },
                                "vulcano_chasm"     : { "name": u"Вулканическая расселина",
                                                        "require" : [ "aplinism", "fireproof" ] },
                                "underwater_grot"   : { "name": u"Подводный грот",
                                                        "require" : [ "swimming" ] },
                                "underground_burrow": { "name": u"Подземная нора",
                                                        "inaccessability": 1,
                                                        "require" : [ ] },
                                "dragon_castle"     : { "name": u"Драконий замок",
                                                        "inaccessabitity" : 1,
                                                        "require" : [ ] },
                                "castle"            : { "name": u"Драконий замок",
                                                        "inaccessabitity" : 1,
                                                        "require" : [ ] },
                                "cannibal_den"      : { "name": u"Берлога людоеда",
                                                        "inaccessabitity" : 1,
                                                        "require" : [ ] },
                                "broad_cave"        : { "name": u"Просторная пещера",
                                                        "inaccessabitity" : 1,
                                                        "require" : [ ] },
                                "tower_ruin"        : { "name": u"Руины башни",
                                                        "provide": [ "magic_traps" ]},
                                "monastery_ruin"    : { "name": u"Руины монастыря",
                                                        "inaccessabitity" : 1,
                                                        "require" : [ ] },
                                "fortress_ruin"     : { "name": u"Руины каменной крепости",
                                                        "inaccessabitity" : 2,
                                                        "require" : [ ] },
                                "castle_ruin"       : { "name": u"Руины королевского замка",
                                                        "inaccessabitity" : 1,
                                                        "require" : [ ] },
                                "ice_citadel"       : { "name": u"Ледяная цитадель",
                                                        "inaccessabitity" : 1,
                                                        "require" : [ "aplinism", "coldproof" ] },
                                "vulcanic_forge"    : { "name": u"Вулканическая кузница",
                                                        "inaccessabitity" : 1,
                                                        "require" : [ "aplinism", "fireproof" ] },
                                "cloud_castle"      : { "name": u"Замок в облаках",
                                                        "inaccessabitity" : 2,
                                                        "require": [ "flight" ] },
                                "undefwater_mansion": { "name": u"Подводные хоромы",
                                                        "inaccessabitity" : 1,
                                                        "require" : [ "swimming" ] },
                                "underground_palaces": { "name": u"Подгорные чертоги",
                                                        "inaccessabitity" : 2,
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
    'copper': ['copper_scale', 'can_dig'],  # copper_scale -- +1 защита
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

    'fire_breath'       : DragonModifier(attack=('fire', (0, 1))),
    'ice_breath'        : DragonModifier(attack=('ice', (0, 1))),
    'poison_breath'     : DragonModifier(attack=('poison', (0, 1))),
    'sound_breath'      : DragonModifier(attack=('sound', (0, 1))),
    'lightning_breath'  : DragonModifier(attack=('lightning', (0, 1))),
    'black_power'       : DragonModifier(attack=('base', (1, 0))),
    'iron_scale'        : DragonModifier(protection=('scale', (1, 0))),
    'copper_scale'      : DragonModifier(protection=('scale', (1, 0))),
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
    raise NotImplementedError
