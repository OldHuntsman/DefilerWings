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
                 u"Мастер-вор" ]

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
                                "ogre_den"          : { "name": u"Берлога людоеда",
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
                                                                 "protection": 3 },
                                            "gremlin_fortification" : {"name": u"Укрепления",
                                                                         "inaccessability": 1},
                                            "gremlin_servant" : {"name": u"Слуги-гремлины",
                                                                         "recruitment_time": 0},     
                                            "servant" : {"name": u"Слуги"},                               
                                            })
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
    10: u"Об этом деянии услышат  жители всего королевства. И ужаснутся." ,
    25: u"О деянии столь ужасном будут сложены легенды, которые не забудутся и через сотни лет"
    }

fighter_mods = {
    u"щит"      : FighterModifier(protection = ('base', (1, 0))),
    u"меч"      : FighterModifier(attack = ('base', (2,1))),
    u"броня"    : FighterModifier(protection = ('base', (0,1))),
    u"копьё"    : FighterModifier(attack = ('base', (1,1))),
    u"спутник"  : FighterModifier(attack = ('base', (1,0)), protection = ('base', (1,0))),
    u"скакун"   : FighterModifier(attack = ('base', (1,0)))
    }

#
# Дракон
#

# имена
dragon_names = [u'Азог', 
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
    u'Его размеры вряд ли кого-то впечатлят. Хотя и сильно вытянутый в длинну, змей весит не больше чем крупная крестьянская собака.',
    u'Он весит примерно столько же сколько и взрослый, здоровый мужчина. Ничего поразительного.',
    u'Достаточно велик чтобы пококнурировать размерами с небольшой лошадью или откормленным годовалым бычком.',
    u'В местных лесах вряд ли найдётся зверь способный потягаться с ним в размерах. Разве что самые откормленные быки или пещерные медведи смогут с ним сравниться.',
    u'Пожалуй по своему весу и размеру он заткнёт за пояс даже африканского слона. Не говоря уже об обитателях лесов и полей этого королевства. Тут ему равных нет.',
    u'На его фоне даже титаны смотрятся бледно, разве что кашалот или кракен весит примерно столько же. Но могут ли они быть столь же ловкими и смертносными на суше и в воздухе?',
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

special_description = [
    u'Его чешуя крепче чем закалённая цвергами сталь.',
    u'На конце его длинного, извивающегося хвоста находится страшное жало, сочащееся несущим погибель ядом.',
    u'Его когти острее бритвы и способны пронзить насквозь даже самые прочные доспехи.',
    u'Величественно изогнутые рога защищают его голову с боков и делают облик дракона ещё более внушительным.',
    u'Его огромные клыки внушают трепет врагу ибо могут играючи разорвать на части даже самого крупного зверя.',
    u'Он настолько чудовищен в своём уродстве, что не каждый отважится даже взглянуть на него прямо, а слабые сердцем бегут от одного лишь его вида.',
    u'В глазах дракона читается хитрость и коварство. Он владеет запретным колдовством.',
    u'Сверкающие подобно полированному антрациту глаза дракона обладают гипнотической силой. Его колдовская мощь велика.',
    u'Взгляд дракона светится нечеловеческим коварством. Сила его колдовских чар просто невероятна.'
    ]
    
head_num = [ #TODO: Текстовый модуль с числительными
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
    2 : u"двуглавый",
    3 : u"трехглавый",
    4 : u"четырёхглавый",
    5 : u"пятиглавый",
    6 : u"шестиглавый",
    7 : u"семиглавый",
    8 : u"восьмиглавый",
    9 : u"многоглавый",
    10: u"многоглавый",
    11: u"многоглавый",
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
    'unbreakable_scale'     : ['virtual_head'],
    'spellbound_trap'       : ['spellbound_trap']
    }
    
# Русское название для отображения заклинания
spell_list_rus = {
    # заговоры -- дают иммунитет к атаке выбранного типа
    'fire_protection'       : u"Заговор от огня",
    'ice_protection'        : u"Заговор от льда",
    'poison_protection'     : u"Заговор от яда",
    'lightning_protection'  : u"Заговор от молнии",
    'sound_protection'      : u"Заговор от грома",
    # сердца -- дают дыхание нужного типа
    'fire_heart'            : u"Огненное сердце",
    'ice_heart'             : u"Ледяное сердце",
    'poison_heart'          : u"Отравленное сердце",
    'thunder_heart'         : u"Громовое сердце",
    'lightning_heart'       : u"Сердце молнии",
    # прочие
    'wings_of_wind'         : u"Крылья ветра",
    'aura_of_horror'        : u"Аура ужаса",
    'unbreakable_scale'     : u"Второй шанс",
    'spellbound_trap'       : u"Колдовская западня"
    }

effects_list = {
    # спецеффекты от еды и других прокачек дракона помимо собственных заклинаний
    'boar_meat'         : ['atk_up'],
    'bear_meat'         : ['def_up'],
    'griffin_meat'      : ['mg_up'],
                }

dragon_modifiers = {
    'fire_immunity'     : DragonModifier(),
    'ice_immunity'      : DragonModifier(),
    'poison_immunity'   : DragonModifier(),
    'lightning_immunity': DragonModifier(),
    'sound_immunity'    : DragonModifier(),
    
    'can_swim'          : DragonModifier(),
    'can_dig'           : DragonModifier(),
    'greedy'            : DragonModifier(),
    'virtual_head'      : DragonModifier(),
    'spellbound_trap'   : DragonModifier(),

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
    'cunning'       : DragonModifier(magic=1),
    #
    'atk_up'        : DragonModifier(attack=('base', (1, 0))),
    'def_up'        : DragonModifier(protection=('base', (1, 0))),
    'mg_up'         : DragonModifier(magic=1),
    }

knight_items = dict()
knight_abilities = dict()

def get_modifier(name):
    if name in dragon_modifiers:
        return dragon_modifiers[name]
    elif name in fighter_mods:
        return fighter_mods[name]
    raise NotImplementedError, name

#логова, картинки
lair_image = {
              'ravine' : 'ravine'
              }
              
# Словарь с "достопримечательностями", ключ - название этапа, значение - кортеж из названия этапа для меню и названия метки, к которой нужно совершить переход
special_places = {
    # лесная пещера с огром
    'enc_ogre' : (u"Пещера людоеда", 'lb_enc_fight_ogre'),   
    'explore_ogre_den': (u"Исследовать пещеру людоеда", 'lb_enc_explore_ogre_den'), 
    'create_ogre_lair': (u"Поселиться в пещере людоеда", 'lb_enc_create_ogre_lair'), 
    }
    
quest_list = ( #TODO: внести все выполнимые на сегодня квесты
        {
            'min_lvl' : 1,  # минимальный уровень дракона для получения квеста
            'max_lvl' : 20, # максимальный уровень дракона для получения квеста
            'text'    : u"Проживи 5 лет.", # текст квеста
            'fixed_time': 5, # количество лет на выполнение квеста, не зависящее от уровня дракона
            'task'  : 'autocomplete', # ключевое слово для описания задачи, 'autocomplete' - задача выполняется автоматически 
        },
        {
            'min_lvl' : 2, # минимальный уровень дракона для получения квеста
            'max_lvl' : 2, # максимальный уровень дракона для получения квеста
            'text'    : u"Стяжать дурную славу {0} или более.", # текст квеста, {0} будет заменён на требуемый уровень
            'fixed_time': 5, # количество лет на выполнение квеста, не зависящее от уровня дракона
            'task'  : 'reputation', # ключевое слово для описания задачи, 'reputation' - проверяется уровень дурной славы
            'fixed_threshold' : 1, # 'fixed_'+ ключевое слово для задания фиксированного требуемого значения
        },
        {
            'min_lvl' : 6, # минимальный уровень дракона для получения квеста
            'max_lvl' : 11, # максимальный уровень дракона для получения квеста
            'text'    : u"Стяжать дурную славу {0} или более.", # текст квеста, {0} будет заменён на требуемый уровень
            'lvlscale_time' : 5, # на что нужно умножить уровень дракона, чтобы получить число лет на выполнение
            'task'  : 'reputation', # ключевое слово для описания задачи, 'reputation' - проверяется уровень дурной славы
            'fixed_threshold' : 1, # задаёт фиксированное значения для задачи
            'lvlscale_threshold' : 1, # число, на которое нужно умножить уровень дракона, чтобы получить необходимый уровень 
        },
        {
            'min_lvl' : 6, # минимальный уровень дракона для получения квеста
            'max_lvl' : 11, # максимальный уровень дракона для получения квеста
            'text'    : u"Достичь суммарной стоимости золотого ложа не менее {0} фартингов.", # текст квеста, {0} будет заменён на требуемый уровень
            'lvlscale_time' : 5, # на что нужно умножить уровень дракона, чтобы получить число лет на выполнение
            'task'  : 'wealth', # ключевое слово для описания задачи, 'wealth' - проверяется стоимость сокровищ
            'fixed_threshold' : 5000, # задаёт фиксированное значения для задачи
            'lvlscale_threshold' : 1000, # число, на которое нужно умножить уровень дракона, чтобы получить необходимый уровень 
        },
    )

# Различный лут
loot = {
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
        'dublon'
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
    