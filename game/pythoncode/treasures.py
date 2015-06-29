# coding=utf-8

import random
from renpy import store

from utils import weighted_random


"""Словарь для драгоценных камней, ключи - названия камней, значения - кортежи вида(шанс появления, ценность)"""
gem_types = {
    "amber": (5, 3),
    "crystall": (5, 5),
    "beryll": (4, 10),
    "tigereye": (4, 10),
    "granate": (3, 20),
    "turmaline": (3, 20),
    "aqua": (3, 20),
    "pearl": (3, 10),
    "black_pearl": (3, 15),
    "elven_beryll": (2, 50),
    "topaz": (2, 50),
    "saphire": (2, 50),
    "ruby": (2, 50),
    "emerald": (2, 25),
    "goodruby": (1, 100),
    "goodemerald": (1, 100),
    "star": (1, 100),
    "diamond": (1, 75),
    "black_diamond": (1, 100),
    "rose_diamond": (1, 100),
}

"""словарь для типов материалов, ключи - названия материалов, значения - (шанс, ценность)"""
material_types = {
    "jasper": (5, 1),
    "turquoise": (5, 1),
    "jade": (5, 1),
    "malachite": (5, 1),
    "corall": (4, 5),
    "ivory": (4, 10),
    "agate": (3, 5),
    "shell": (3, 5),
    "horn": (1, 25),
}

"""словарь для описания типов материалов,
ключи - названия материалов,
значения - словарь для различных падежей русского названия материала"""
material_description_rus = {
    "jasper": {
        'nominative': u'яшма',
        'genitive': u'яшмы'
    },
    "turquoise": {
        'nominative': u'бирюза',
        'genitive': u'бирюзы'
    },
    "jade": {
        'nominative': u'нефрит',
        'genitive': u'нефрита'
    },
    "malachite": {
        'nominative': u'малахит',
        'genitive': u'малахита'
    },
    "corall": {
        'nominative': u'коралл',
        'genitive': u'коралла'
    },
    "ivory": {
        'nominative': u'слоновая кость',
        'genitive': u'слоновой кости'
    },
    "agate": {
        'nominative': u'агат',
        'genitive': u'агата'
    },
    "shell": {
        'nominative': u'перламутр',
        'genitive': u'перламутра'
    },
    "horn": {
        'nominative': u'драконий рог',
        'genitive': u'драконьего рога'
    },
}

"""словарь для описания размеров материалов,
ключи - названия размера материалов,
значения - словарь для русского прилагательного, соответствующего размеру"""
material_size_description_rus = {
    'small': {
        'he': {
            'nominative': u"мелкий ",
            'ablative': u"мелким "
        },
        'she': {
            'nominative': u"мелкая ",
            'ablative': u"мелкой "
        },
        'they': {
            'nominative': u"мелкие ",
            'genitive': u"мелких ",
            'ablative': u"мелкими "
        }
    },
    'common': {  # этот размер не отображается
        'he': {
            'nominative': u"",
            'ablative': u""
        },
        'she': {
            'nominative': u"",
            'ablative': u""
        },
        'they': {
            'nominative': u"",
            'genitive': u"",
            'ablative': u""
        }
    },
    'large': {
        'he': {
            'nominative': u"крупный ",
            'ablative': u"крупным "
        },
        'she': {
            'nominative': u"крупная ",
            'ablative': u"крупной "
        },
        'they': {
            'nominative': u"крупные ",
            'genitive': u"крупных ",
            'ablative': u"крупными "
        }
    },
    'exceptional': {
        'he': {
            'nominative': u"огромный ",
            'ablative': u"огромным "
        },
        'she': {
            'nominative': u"огромная ",
            'ablative': u"огромной "
        },
        'they': {
            'nominative': u"огромные ",
            'genitive': u"огромных ",
            'ablative': u"огромными "
        }
    }
}
"""словарь для описания степени обработки драгоценных камней,
ключи - названия степени обработки,
значения - словарь для соответствующего русского прилагательного"""
gem_cut_description_rus = {
    ' ': {
        'he': {  # эта полировка не отображается
            'nominative': u'',
            'ablative': u''
        },
        'she': {
            'nominative': u'',
            'ablative': u''
        },
        'they': {
            'nominative': u'',
            'genitive': u'',
            'ablative': u''
        }
    },
    'polished': {
        'he': {
            'nominative': u'необработанный ',
            'ablative': u''  # 'ablative' не отображается, чтобы не портить описание вещи
        },
        'they': {
            'nominative': u'необработанные ',
            'genitive': u"необработанных ",
            'ablative': u''
        }
    },
    'rough': {
        'he': {
            'nominative': u'полированный ',
            'ablative': u'полированным '
        },
        'they': {
            'nominative': u'полированные ',
            'genitive': u'полированных ',
            'ablative': u'полированными '
        }
    },
    'faceted': {
        'he': {
            'nominative': u'ограненный ',
            'ablative': u'ограненным '
        },
        'they': {
            'nominative': u'ограненные ',
            'genitive': u'ограненных ',
            'ablative': u'ограненными '
        }
    }
}

"""Словарь для драгоценных камней,
ключ - тип драгоценного камня,
значение - словарь с русским названием драгоценного камня в разных падежах"""
gem_description_rus = {
    "amber": {
        'he': {
            'nominative': u"янтарь",
            'genitive': u"янтаря",
            'ablative': u"янтарём"
        },
        'they': {
            'genitive': u"янтарей",
            'ablative': u"янтарями"
        }
    },
    "crystall": {
        'he': {
            'nominative': u'горный хрусталь',
            'genitive': u"горных хрусталя",
            'ablative': u'горным хрусталём'
        },
        'they': {
            'genitive': u"горных хрусталей",
            'ablative': u'горными хрусталями'
        }
    },
    "beryll": {
        'he': {
            'nominative': u'берилл',
            'genitive': u"берилла",
            'ablative': u'бериллом'
        },
        'they': {
            'genitive': u"бериллов",
            'ablative': u'бериллами'
        }
    },
    "tigereye": {
        'he': {
            'nominative': u'тигровый глаз',
            'genitive': u"тигровых глаза",
            'ablative': u'тигровым глазом'
        },
        'they': {
            'genitive': u"тигровых глазов",
            'ablative': u'тигровыми глазами'
        }
    },
    "granate": {
        'he': {
            'nominative': u'гранат',
            'genitive': u"граната",
            'ablative': u'гранатом'
        },
        'they': {
            'genitive': u"гранатов",
            'ablative': u'гранатами'
        }
    },
    "turmaline": {
        'he': {
            'nominative': u'турмалин',
            'genitive': u"турмалина",
            'ablative': u'турмалином'
        },
        'they': {
            'genitive': u"турмалинов",
            'ablative': u'турмалинами'
        }
    },
    "aqua": {
        'he': {
            'nominative': u'аквамарин',
            'genitive': u"аквамарина",
            'ablative': u'аквамарином'
        },
        'they': {
            'genitive': u"аквамаринов",
            'ablative': u'аквамаринами'
        }
    },
    "pearl": {
        'he': {
            'nominative': u'жемчуг',
            'genitive': u"жемчуга",
            'ablative': u'жемчугом'
        },
        'she': {
            'nominative': u'жемчужина',
            'genitive': u"жемчужины",
            'ablative': u'жемчужиной'
        },
        'they': {
            'genitive': u"жемчужин",
            'ablative': u'жемчугами'
        }
    },
    "black_pearl": {
        'he': {
            'nominative': u'чёрный жемчуг',
            'genitive': u'чёрных жемчуга',
            'ablative': u'чёрным жемчугом'
        },
        'she': {
            'nominative': u'чёрная жемчужина',
            'genitive': u'чёрных жемчужины',
            'ablative': u'чёрной жемчужиной'
        },
        'they': {
            'genitive': u"чёрных жемчужин",
            'ablative': u'чёрными жемчугами'
        }
    },
    "elven_beryll": {
        'he': {
            'nominative': u'эльфийский берилл',
            'genitive': u"эльфийских берилла",
            'ablative': u'эльфийским бериллом'
        },
        'they': {
            'genitive': u"эльфийских бериллов",
            'ablative': u'эльфийскими бериллами'
        }
    },
    "topaz": {
        'he': {
            'nominative': u'топаз',
            'genitive': u"топаза",
            'ablative': u'топазом'
        },
        'they': {
            'genitive': u"топазов",
            'ablative': u'топазами'
        }
    },
    "saphire": {
        'he': {
            'nominative': u'сапфир',
            'genitive': u"сапфира",
            'ablative': u'сапфиром'
        },
        'they': {
            'genitive': u"сапфиров",
            'ablative': u'сапфирами'
        }
    },
    "ruby": {
        'he': {
            'nominative': u'рубин',
            'genitive': u"рубина",
            'ablative': u'рубином'
        },
        'they': {
            'genitive': u"рубинов",
            'ablative': u'рубинами'
        }
    },
    "emerald": {
        'he': {
            'nominative': u'изумруд',
            'genitive': u"изумруда",
            'ablative': u'изумрудом'
        },
        'they': {
            'genitive': u"изумрудов",
            'ablative': u'изумрудами'
        }
    },
    "goodruby": {
        'he': {
            'nominative': u'яхонт',
            'genitive': u"яхонта",
            'ablative': u'яхонтом'
        },
        'they': {
            'genitive': u"яхонтов",
            'ablative': u'яхонтами'
        }
    },
    "goodemerald": {
        'he': {
            'nominative': u'смарагд',
            'genitive': u"смарагда",
            'ablative': u'смарагдом'
        },
        'they': {
            'genitive': u"смарагдов",
            'ablative': u'смарагдами'
        }
    },
    "star": {
        'he': {
            'nominative': u'звёздный сапфир',
            'genitive': u"звёздных сапфира",
            'ablative': u'звёздным сапфиром'
        },
        'they': {
            'genitive': u"звёздных сапфиров",
            'ablative': u'звёздными сапфирами'
        }
    },
    "diamond": {
        'he': {
            'nominative': u'алмаз',
            'genitive': u"алмаза",
            'ablative': u'алмазом'
        },
        'they': {
            'genitive': u"алмазов",
            'ablative': u'алмазами'
        }
    },
    "black_diamond": {
        'he': {
            'nominative': u'чёрный алмаз',
            'genitive': u"чёрных алмаза",
            'ablative': u'чёрным алмазом'
        },
        'they': {
            'genitive': u"чёрных алмазов",
            'ablative': u'чёрными алмазами'
        }
    },
    "rose_diamond": {
        'he': {
            'nominative': u'розовый алмаз',
            'genitive': u"розовых алмаза",
            'ablative': u'розовым алмазом'
        },
        'they': {
            'genitive': u"розовых алмазов",
            'ablative': u'розовыми алмазами'
        }
    },
}
"""словарь для типов металлов, ключ - металл, значение - ценность"""
metal_types = {
    "silver": 1,
    "gold": 10,
    "mithril": 25,
    "adamantine": 30,
}
"""словарь для типов сокровищ, ключ - тип сокровища,
значение - (базовая цена, пол, можно ли сделать из метала(булевое), можно ли
            сделать из поделочных материалов(булевое), является ли изображением(булевое),
            можно ли инкрустировать(булевое), возможность украшения(булевое))"""
treasure_types = {  # допилить типы сокровищ
    "dish": (5, "it", True, False, False, False, True),
    "goblet": (4, "he", True, False, False, True, True),
    "cup": (3, "she", False, True, False, False, True),
    "casket": (5, "she", True, True, False, True, True),
    "statue": (10, "she", True, True, True, False, False),
    "tabernacle": (5, "she", True, True, False, True, True),
    "icon": (10, "she", True, False, True, False, False),
    "tome": (10, "he", True, False, False, True, True),
    "comb": (2, "he", True, True, False, False, True),
    "phallos": (3, "he", True, True, False, False, True),
    "mirror": (4, "it", True, True, False, True, True),
    "band": (3, "he", True, False, False, False, False),
    "diadem": (10, "she", True, False, False, True, False),
    "tiara": (15, "she", True, False, False, True, False),
    "earring": (1, "she", True, False, False, True, False),
    "necklace": (5, "it", True, False, False, True, False),
    "pendant": (3, "he", True, False, False, False, True),
    "ring": (2, "it", True, True, False, False, False),
    "broch": (3, "she", True, False, False, True, False),
    "gemring": (5, "he", True, True, False, True, False),
    "seal": (3, "he", True, True, False, False, True),
    "armbrace": (3, "he", True, True, False, True, True),
    "legbrace": (4, "he", True, True, False, True, True),
    "crown": (15, "she", True, False, False, True, False),
    "scepter": (15, "he", True, False, False, True, False),
    "chain": (3, "she", True, False, False, False, False),
    "fibula": (2, "she", True, False, False, False, True),
}
"""словарь для описания типов драгоценностей,
ключ - тип драгоценностей,
значение - словарь с русским названием драгоценности в разных падежах"""
treasure_description_rus = {  # допилить типы сокровищ
    "dish": {'nominative': u'блюдо', 'ablative': u'блюде'},
    "goblet": {'nominative': u'кубок', 'ablative': u'кубке'},
    "cup": {'nominative': u'чаша', 'ablative': u'чаше'},
    "casket": {'nominative': u'шкатулка', 'ablative': u'шкатулке'},
    "statue": {'nominative': u'статуэтка', 'ablative': u'статуэтке'},
    "tabernacle": {'nominative': u'дарохранительница', 'ablative': u'дарохранительнице'},
    "icon": {'nominative': u'икона', 'ablative': u'иконе'},
    "tome": {'nominative': u'фолиант', 'ablative': u'фолианте'},
    "comb": {'nominative': u'гребень', 'ablative': u'гребене'},
    "phallos": {'nominative': u'фаллос', 'ablative': u'фаллосе'},
    "mirror": {'nominative': u'зеркальце', 'ablative': u'зеркальце'},
    "band": {'nominative': u'обруч', 'ablative': u'обруче'},
    "diadem": {'nominative': u'диадема', 'ablative': u'диадеме'},
    "tiara": {'nominative': u'тиара', 'ablative': u'тиаре'},
    "earring": {'nominative': u'серьга', 'ablative': u'серьге'},
    "necklace": {'nominative': u'ожерелье', 'ablative': u'ожерелье'},
    "pendant": {'nominative': u'кулон', 'ablative': u'кулоне'},
    "ring": {'nominative': u'колечко', 'ablative': u'колечке'},
    "broch": {'nominative': u'брошь', 'ablative': u'броше'},
    "gemring": {'nominative': u'перстень', 'ablative': u'перстне'},
    "seal": {'nominative': u'перстень-печатка', 'ablative': u'перстне-печатке'},
    "armbrace": {'nominative': u'браслет', 'ablative': u'браслете'},
    "legbrace": {'nominative': u'ножной браслет', 'ablative': u'браслете'},
    "crown": {'nominative': u'корона', 'ablative': u'короне'},
    "scepter": {'nominative': u'скипетр', 'ablative': u'скипетре'},
    "chain": {'nominative': u'цепь', 'ablative': u'цепи'},
    "fibula": {'nominative': u'фибула', 'ablative': u'фибуле'},
}
"""словарь для описания типов металлов, ключ - тип металла, значение - русское названия драгоценности в разных родах"""
metal_description_rus = {
    'silver': {
        'he': u"серебряный",
        'she': u"серебряная",
        'it': u"серебряное",
        'they': u"серебряных",
        'prepositional': u"серебряном",
        'genitive' : u"серебра",
    },
    'gold': {
        'he': u"золотой",
        'she': u"золотая",
        'it': u"золотое",
        'they': u"золотых",
        'prepositional': u"золотом",
        'genitive' : u"золота",
    },
    'mithril': {
        'he': u"мифрильный",
        'she': u"мифрильная",
        'it': u"мифрильное",
        'they': u"мифрильных",
        'prepositional': u"мифрильном",
        'genitive' : u"мифрила",
    },
    'adamantine': {
        'he': u"адамантовый",
        'she': u"адамантовая",
        'it': u"адамантовое",
        'they': u"адамантовых",
        'prepositional': u"адамантовом",
        'genitive' : u"адаманта",
    },
}
"""словарь для изображений, ключ - тип культуры, значение - кортеж из вариантов изображений"""
image_types = { 
    'human': (
        'abstract_ornament', 'concentric_circles', 'round_dance', 'fire-breathing_dragon', 'flying_dragon',
        'wingless_dragon', 'snake_with_a_crown', 'winged_serpent', 'kokatriks', 'basilisk',
        'dragon_entwine_naked_girl', 'battle_dragon_with_knight', 'dancing_girls', 'bathing_girl',
        'children_playing', 'rider_with_bow', 'horseman_with_spear_and_shield', 'dead_knight_with_sword'),
    'knight': (
        'proud_motto', 'battle_scene', 'coat_of_arms_with_rearing_unicorn', 'coat_of_arms_with_head_of_boar',
        'coat_of_arms_with_three_lilies', 'coat_of_arms_with_roaring_lion', 'coat_of_arms_with_proud_eagle',
        'coat_of_arms_with_procession_kamelopardom', 'coat_of_arms_with_crossed_swords',
        'coat_of_arms_with_shield_and_sword'),
    'cleric': (
        'saying_of_holy_scriptures', 'scene_of_holy_scriptures', 'saint_with_halo', 'angel_with_flaming_sword',
        'angel_winning_serpent', 'raising_hands_angel', 'six-winged_seraph', 'holy_maiden_and_child',
        'holy_maiden_stretches_hands', 'weeping_maiden'),
    'elf': (
        'floral_ornament', 'elegant_runes', 'running_deer', 'bear_with_raised_legs', 'wolf_hunting', 'sneaking_manul',
        'two_songbirds', 'moon_and_stars', 'branched_oak', 'blooming_vine', 'spreading_maple', 'weeping_willow',
        'dancing_nymphs', 'nymph_with_cup', 'nymph_collecting_fruits', 'nymph_playing_harp', 'winged_maiden',
        'satyr_playing_flute', 'forest_guard_bow'),
    'dwarf': (
        'geometric_pattern', 'runic_ligature', 'hammer_and_crown', 'dwarfs_holding_over_his_head_anvil',
        'armed_dwarfs_tramples_goblin', 'crossed_axes', 'entwined_rings', 'helmet_with_horns',
        'krotocherv', 'dwarfs', 'urist_makdvarf', 'dragon_smaug'),
    'merman': (
        'wavy_pattern', 'frolicking_fish', 'seahorse', 'newt_lifting_trident', 'triton_and_siren_holding_hands',
        'mermaid_brushing_hair', 'playing_mermaid', 'mermaid_playing_with_pearl', 'awesome_sea_serpent',
        'flying_seagull', 'wriggling_octopus', 'kraken_drowning_sea_vessel', 'sailing_ship'),
}
"""словарь для описания изображений,
ключ - вариант изображения,
значение - словарь из рода изображения и описания изображения в различных падежах"""
image_description_rus = {
    'abstract_ornament': {
        'gender': 'he',
        'nominative': u'абстрактный орнамент',
        'accusative': u'абстрактный орнамент',
    },
    'concentric_circles': {
        'gender': 'they',
        'nominative': u'концентрические круги',
        'accusative': u'концентрические круги',
    },
    'round_dance': {
        'gender': 'he',
        'nominative': u'хоровод',
        'accusative': u'хоровод',
    },
    'fire-breathing_dragon': {
        'gender': 'he',
        'nominative': u'огнедышащий дракон',
        'accusative': u'огнедышащего дракона',
    },
    'flying_dragon': {
        'gender': 'he',
        'nominative': u'летящий дракон',
        'accusative': u'летящего дракона',
    },
    'wingless_dragon': {
        'gender': 'he',
        'nominative': u'бескрылый дракон',
        'accusative': u'бескрылого дракона',
    },
    'snake_with_a_crown': {
        'gender': 'she',
        'nominative': u'змея с короной на голове',
        'accusative': u'змею с короной на голове',
    },
    'winged_serpent': {
        'gender': 'she',
        'nominative': u'крылатая змея',
        'accusative': u'крылатую змею',
    },
    'kokatriks': {
        'gender': 'he',
        'nominative': u'кокатрикс',
        'accusative': u'кокатрикса',
    },
    'basilisk': {
        'gender': 'he',
        'nominative': u'василиск',
        'accusative': u'василиска',
    },
    'dragon_entwine_naked_girl': {
        'gender': 'he',
        'nominative': u'дракон, обвивающий обнаженную девушку',
        'accusative': u'дракона, обвивающий обнаженную девушку',
    },
    'battle_dragon_with_knight': {
        'gender': 'he',
        'nominative': u'сражение дракона с рыцарем',
        'accusative': u'сражение дракона с рыцарем',
    },
    'dancing_girls': {
        'gender': 'they',
        'nominative': u'танцующие девушки',
        'accusative': u'танцующих девушек',
    },
    'bathing_girl': {
        'gender': 'she',
        'nominative': u'купающаяся девушка',
        'accusative': u'купающуюся девушку',
    },
    'children_playing': {
        'gender': 'they',
        'nominative': u'играющие дети',
        'accusative': u'играющих детей',
    },
    'rider_with_bow': {
        'gender': 'he',
        'nominative': u'всадник с луком',
        'accusative': u'всадника с луком',
    },
    'horseman_with_spear_and_shield': {
        'gender': 'he',
        'nominative': u'всадник с копьём и щитом',
        'accusative': u'всадника с копьём и щитом',
    },
    'dead_knight_with_sword': {
        'gender': 'he',
        'nominative': u'мертвый рыцарь с мечом, покоящимся на груди',
        'accusative': u'мертвого рыцаря с мечом, покоящимся на груди',
    },
    'proud_motto': {
        'gender': 'he',
        'nominative': u'гордый девиз',
        'accusative': u'гордый девиз',
    },
    'battle_scene': {
        'gender': 'she',
        'nominative': u'сцена сражения',
        'accusative': u'сцену сражения',
    },
    'coat_of_arms_with_rearing_unicorn': {
        'gender': 'he',
        'nominative': u'герб с единорогом, вставшим на дыбы',
        'accusative': u'герб с единорогом, вставшим на дыбы',
    },
    'coat_of_arms_with_head_of_boar': {
        'gender': 'he',
        'nominative': u'герб с головой вепря',
        'accusative': u'герб с головой вепря',
    },
    'coat_of_arms_with_three_lilies': {
        'gender': 'he',
        'nominative': u'герб с тремя лилиями',
        'accusative': u'герб с тремя лилиями',
    },
    'coat_of_arms_with_roaring_lion': {
        'gender': 'he',
        'nominative': u'герб с рыкающим львом',
        'accusative': u'герб с рыкающим львом',
    },
    'coat_of_arms_with_proud_eagle': {
        'gender': 'he',
        'nominative': u'герб с гордым орлом',
        'accusative': u'герб с гордым орлом',
    },
    'coat_of_arms_with_procession_kamelopardom': {
        'gender': 'he',
        'nominative': u'герб с шествующим камелопардом',
        'accusative': u'герб с шествующим камелопардом',
    },
    'coat_of_arms_with_crossed_swords': {
        'gender': 'he',
        'nominative': u'герб со скрещёнными мечами',
        'accusative': u'герб со скрещёнными мечами',
    },
    'coat_of_arms_with_shield_and_sword': {
        'gender': 'he',
        'nominative': u'герб со щитом и мечом',
        'accusative': u'герб со щитом и мечом',
    },
    'saying_of_holy_scriptures': {
        'gender': 'it',
        'nominative': u'изречение из святого писания',
        'accusative': u'изречение из святого писания',
    },
    'scene_of_holy_scriptures': {
        'gender': 'she',
        'nominative': u'сцена из святого писания',
        'accusative': u'сцену из святого писания',
    },
    'saint_with_halo': {
        'gender': 'he',
        'nominative': u'святой с нимбом',
        'accusative': u'святого с нимбом',
    },
    'angel_with_flaming_sword': {
        'gender': 'he',
        'nominative': u'ангел с огненным мечом',
        'accusative': u'ангела с огненным мечом',
    },
    'angel_winning_serpent': {
        'gender': 'he',
        'nominative': u'ангел, побеждающий змия',
        'accusative': u'ангела, побеждающего змия',
    },
    'raising_hands_angel': {
        'gender': 'he',
        'nominative': u'воздевший руки ангел',
        'accusative': u'воздевшего руки ангела',
    },
    'six-winged_seraph': {
        'gender': 'he',
        'nominative': u'шестикрылый серафим',
        'accusative': u'шестикрылого серафима',
    },
    'holy_maiden_and_child': {
        'gender': 'she',
        'nominative': u'святая дева с младенцем',
        'accusative': u'святую деву с младенцем',
    },
    'holy_maiden_stretches_hands': {
        'gender': 'she',
        'nominative': u'святая дева, простирающая руки',
        'accusative': u'святую деву, простирающую руки',
    },
    'weeping_maiden': {
        'gender': 'she',
        'nominative': u'плачущая дева',
        'accusative': u'плачущую деву',
    },
    'floral_ornament': {
        'gender': 'he',
        'nominative': u'растительный орнамент',
        'accusative': u'растительный орнамент',
    },
    'elegant_runes': {
        'gender': 'they',
        'nominative': u'изящные руны',
        'accusative': u'изящные руны',
    },
    'running_deer': {
        'gender': 'he',
        'nominative': u'бегущий олень',
        'accusative': u'бегущего оленя',
    },
    'bear_with_raised_legs': {
        'gender': 'he',
        'nominative': u'медведь с поднятыми вверх лапами',
        'accusative': u'медведя с поднятыми вверх лапами',
    },
    'wolf_hunting': {
        'gender': 'he',
        'nominative': u'охотящийся волк',
        'accusative': u'охотящегося волка',
    },
    'sneaking_manul': {
        'gender': 'he',
        'nominative': u'крадущийся манул',
        'accusative': u'крадущегося манула',
    },
    'two_songbirds': {
        'gender': 'they',
        'nominative': u'две певчие птички',
        'accusative': u'двух певчих птичек',
    },
    'moon_and_stars': {
        'gender': 'they',
        'nominative': u'луна и звёзды',
        'accusative': u'луну и звёзды',
    },
    'branched_oak': {
        'gender': 'he',
        'nominative': u'ветвистый дуб',
        'accusative': u'ветвистый дуб',
    },
    'blooming_vine': {
        'gender': 'she',
        'nominative': u'цветущая лоза',
        'accusative': u'цветущую лозу',
    },
    'spreading_maple': {
        'gender': 'he',
        'nominative': u'раскидистый клён',
        'accusative': u'раскидистый клён',
    },
    'weeping_willow': {
        'gender': 'she',
        'nominative': u'плакучая ива',
        'accusative': u'плакучую иву',
    },
    'dancing_nymphs': {
        'gender': 'they',
        'nominative': u'танцующие нимфы',
        'accusative': u'танцующих нимф',
    },
    'nymph_with_cup': {
        'gender': 'she',
        'nominative': u'нимфа с кубком',
        'accusative': u'нимфу с кубком',
    },
    'nymph_collecting_fruits': {
        'gender': 'she',
        'nominative': u'нимфа, собирающая плоды',
        'accusative': u'нимфу, собирающую плоды',
    },
    'nymph_playing_harp': {
        'gender': 'she',
        'nominative': u'нимфа, играющая на арфе',
        'accusative': u'нимфу, играющую на арфе',
    },
    'winged_maiden': {
        'gender': 'she',
        'nominative': u'крылатая дева',
        'accusative': u'крылатую деву',
    },
    'satyr_playing_flute': {
        'gender': 'he',
        'nominative': u'сатир, играющий на дудочке',
        'accusative': u'сатира, играющего на дудочке',
    },
    'forest_guard_bow': {
        'gender': 'he',
        'nominative': u'лесной страж, стреляющий из лука',
        'accusative': u'лесного стража, стреляющего из лука',
    },
    'geometric_pattern': {
        'gender': 'he',
        'nominative': u'геометрический орнамент',
        'accusative': u'геометрический орнамент',
    },
    'runic_ligature': {
        'gender': 'she',
        'nominative': u'руническая вязь',
        'accusative': u'руническую вязь',
    },
    'hammer_and_crown': {
        'gender': 'they',
        'nominative': u'молот и корона',
        'accusative': u'молот и корону',
    },
    'dwarfs_holding_over_his_head_anvil': {
        'gender': 'he',
        'nominative': u'цверг, держащий над головой наковальню',
        'accusative': u'цверга, держащего над головой наковальню',
    },
    'armed_dwarfs_tramples_goblin': {
        'gender': 'he',
        'nominative': u'вооруженный цверг попирающий ногами гоблина',
        'accusative': u'вооруженного цверга, попирающего ногами гоблина',
    },
    'crossed_axes': {
        'gender': 'they',
        'nominative': u'скрещённые топоры',
        'accusative': u'скрещённые топоры',
    },
    'entwined_rings': {
        'gender': 'they',
        'nominative': u'переплетённые кольца',
        'accusative': u'переплетённые кольца',
    },
    'helmet_with_horns': {
        'gender': 'he',
        'nominative': u'шлем с рогами',
        'accusative': u'шлем с рогами',
    },
    'krotocherv': {
        'gender': 'he',
        'nominative': u'кроточервь',
        'accusative': u'кроточервя',
    },
    'dwarfs': {
        'gender': 'they',
        'nominative': u'цверги. Цверги работают.',
        'accusative': u'цвергов. Цверги работают.',
    },
    'urist_makdvarf': {
        'gender': 'he',
        'nominative': u'Урист МакДварф. Урист МакДварф ест мастерски сделанный ячий сыр. '
                      u'Изображение посвящено поеданию мастерски сделанного ячьего сыра цвергом Уристом МакДварфом '
                      u'ранней весной 1076 года.',
        'accusative': u'Уриста МакДварфа. Урист МакДварф ест мастерски сделанный ячий сыр. '
                      u'Изображение посвящено поеданию мастерски сделанного ячьего сыра цвергом '
                      u'Уристом МакДварфом ранней весной 1076 года.',
    },
    'dragon_smaug': {
        'gender': 'they',
        'nominative': u'Дракон Смауг и цверг Торин. Торин закрывается руками. Смауг стоит в угрожающей позе. '
                      u'Изображение посвящено убийству короля-под-горой в Эреборе поздним летом 2770 года.',
        'accusative': u'Дракона Смауга и цверга Торина. Торин закрывается руками. Смауг стоит в угрожающей позе. '
                      u'Изображение посвящено убийству короля-под-горой в Эреборе поздним летом 2770 года.',
    },
    'wavy_pattern': {
        'gender': 'he',
        'nominative': u'волнистый орнамент',
        'accusative': u'волнистый орнамент',
    },
    'frolicking_fish': {
        'gender': 'they',
        'nominative': u'резвящиеся рыбки',
        'accusative': u'резвящихся рыбок',
    },
    'seahorse': {
        'gender': 'he',
        'nominative': u'морской конёк',
        'accusative': u'морского конька',
    },
    'newt_lifting_trident': {
        'gender': 'he',
        'nominative': u'тритон, поднимающий трезубец',
        'accusative': u'тритона, поднимающего трезубец',
    },
    'triton_and_siren_holding_hands': {
        'gender': 'they',
        'nominative': u'тритон и сирена, держащиеся за руки',
        'accusative': u'тритона и сирену, держащихся за руки',
    },
    'mermaid_brushing_hair': {
        'gender': 'she',
        'nominative': u'русалка, расчёсывающая волосы',
        'accusative': u'русалку, расчёсывающую волосы',
    },
    'playing_mermaid': {
        'gender': 'they',
        'nominative': u'играющие русалки',
        'accusative': u'играющих русалок',
    },
    'mermaid_playing_with_pearl': {
        'gender': 'she',
        'nominative': u'русалка, играющая с жемчужиной',
        'accusative': u'русалку, играющую с жемчужиной',
    },
    'awesome_sea_serpent': {
        'gender': 'he',
        'nominative': u'устрашающий морской змей',
        'accusative': u'устрашающего морского змея',
    },
    'flying_seagull': {
        'gender': 'they',
        'nominative': u'летящие чайки',
        'accusative': u'летящих чаек',
    },
    'wriggling_octopus': {
        'gender': 'he',
        'nominative': u'извивающийся осьминог',
        'accusative': u'извивающегося осьминога',
    },
    'kraken_drowning_sea_vessel': {
        'gender': 'he',
        'nominative': u'кракен, топящий морское судно',
        'accusative': u'кракена, топящего морское судно',
    },
    'sailing_ship': {
        'gender': 'he',
        'nominative': u'плывущий по волнам корабль',
        'accusative': u'плывущий по волнам корабль',
    },
}
"""словарь для описания качества драгоценности,
 ключ - качество,
 значение - словарь с русским названием качества в разных родах"""
quality_description_rus = { 
    'rough': {
        'he': u"грубый ",
        'she': u"грубая ",
        'it': u"грубое ",
    },
    'common': {  # у обычного описание опускается
        'he': u"",
        'she': u"",
        'it': u"",
    },
    'skillfully': {
        'he': u"искусно сделанный ",
        'she': u"искусно сделанная ",
        'it': u"искусно сделанное ",
    },
    'mastery': {
        'he': u"мастерски изготовленный ",
        'she': u"мастерски изготовленная ",
        'it': u"мастерски изготовленное ",
    },
}
"""словарь для описания украшения, ключ - тип украшения, значение - словарь с русским словом в разных родах"""
decoration_description_rus = {
    'decoration': {
        'he': u"украшенный",
        'she': u"украшенная",
        'it': u"украшенное",
    },
    'spangled': {
        'he': u"усыпанный",
        'she': u"усыпанная",
        'it': u"усыпанное",
    },
    'inlaid': {
        'he': u"инкрустированный",
        'she': u"инкрустированная",
        'it': u"инкрустированное",
    },
    'image': {
        'he': u"изображен",
        'she': u"изображена",
        'it': u"изображено",
        'they': u"изображены",
    },
}
"""словарь для описания типа украшения на русском"""
decorate_types_description_rus = {
    'incuse': u"чеканкой",
    'engrave': u"гравировкой",
    'etching': u"травлением",
    'carving': u"резьбой"
}
"""словарь для вывода описаний массы сокровищ на русском"""
treasures_mass_description_rus = {
    'coin': {
        0: u"Монеты",
        100: u"Кучка монет",
        1000: u"Куча монет",
        10000: u"Гора монет",
        100000: u"Горы монет",
    },
    'material': {
        0: u"Материалы",
        100: u"Кучка материалов",
        1000: u"Куча материалов",
        10000: u"Гора материалов",
        100000: u"Горы материалов",
    },
    'gem': {
        0: u"Драгоценные камни",
        100: u"Кучка драгоценных камней",
        1000: u"Куча драгоценных камней",
        10000: u"Гора драгоценных камней",
        100000: u"Горы драгоценных камней",
    },
    'jewelry': {
        0: u"Безделушки",
        100: u"Кучка безделушек",
        1000: u"Куча безделушек",
        10000: u"Гора безделушек",
        100000: u"Горы безделушек",
    },
    'wealth': {
        0: u"Сокровищница практически пуста. ",
        100: u"В сокровищнице жалкие гроши, которые добропорядочному дракону иметь стыдно. ",
        1000: u"В сокровищнице смотреть не на что. ",
        10000: u"В сокровищнице вполне достойная куча сокровищ, уже не стыдно её кому-нибудь показать. ",
        100000: u"Собрать такую гору сокровищ удаётся только лучшим драконам. Есть повод для гордости. ",
        1000000: u"Горы сокровищ - гордость самого богатого дракона в мире. ",
    },
}

number_conjugation_end = {
    1: {'nominative': (u"", u"а", u"ов")},
    2: {'nominative': (u"ок", u"ка", u"ков")},
}


def number_conjugation_type(number):
    if (number % 10 == 1) and (number % 100 != 11):
        return 0
    elif (1 < number % 10 < 5) and (number % 100 < 11 or number % 100 > 21):
        return 1
    else:
        return 2


def number_conjugation_rus(number, add_name, word_form='nominative', word_type=1):
    description_end = number_conjugation_end[word_type][word_form][number_conjugation_type(number)]
    return u"%s %s%s" % (number, add_name, description_end)


def capitalize_first(string):
    return string.capitalize()


def weighted_select(d):
    weight = random.random() * sum(v[0] for k, v in d.items())
    for k, v in d.items():
        if weight < v[0]:
            return k
        weight -= v[0]
    return d.keys()[random.randint(0, len(d.keys()))]


class Ingot(object):  # класс для генерации слитков
    weights = (1, 4, 8, 16)
    weights_description_rus = {1: u"крохотный", 4: u"небольшой", 8: u"полновесный", 16: u"массивный"}

    def __init__(self, metal_type):
        self.metal_type = metal_type
        self.metal_cost = metal_types[metal_type]
        self.weight = random.choice(self.weights)

    @property
    def cost(self):
        return self.metal_cost * self.weight

    def __repr__(self):
        return "%s pound %s ingot" % (self.weight, self.metal_type)

    def description(self, language='rus'):
        if language == 'rus':
            if self.weight in self.weights:
                return u"%s %s слиток" % (
                    self.weights_description_rus[self.weight], metal_description_rus[self.metal_type]['he'])
            else:
                return u"Несколько %s слитков общим весом %s" % (
                    metal_description_rus[self.metal_type]['they'], number_conjugation_rus(self.weight, u"фунт"))
        else:
            return self.__repr__()

    @staticmethod
    def number_conjugation(metal_type, metal_weight):
        """
        Функция для вывода описания слитков металла по типу металла и его количеству
        """
        if metal_weight in Ingot.weights:
            return u"%s %s слиток" % (
                Ingot.weights_description_rus[metal_weight], metal_description_rus[metal_type]['he'])
        else:
            return u"несколько %s слитков общим весом %s" % (
                metal_description_rus[metal_type]['they'], number_conjugation_rus(metal_weight, u"фунт"))


class Coin(object):
    coin_types = {"farting": (1, 1), "taller": (1, 10), "dublon": (1, 100)}
    coin_description_rus = {"farting": u"фартинг", "taller": u"таллер", "dublon": u"дублон"}
    """
    Монеты.
    """

    def __init__(self, name, amount):
        self.amount = amount  # количество монеток
        self.name = name
        self.value = Coin.coin_types[self.name][1]

    @property
    def cost(self):
        return self.amount * self.value

    def __repr__(self):
        return str(self.amount) + " " + "%s(s)" % self.name

    def description(self, language='rus'):
        if language == 'rus':
            return number_conjugation_rus(self.amount, Coin.coin_description_rus[self.name], 'nominative')
        else:
            return self.__repr__()

    @staticmethod
    def number_conjugation(coin_type, coin_count):
        """
        Функция для вывода описания монет по типу и количеству монет
        """
        return number_conjugation_rus(coin_count, Coin.coin_description_rus[coin_type])


class Gem(object):  # класс для генерации драг.камней
    cut_dict = {
        " ": (0, 1),
        "polished": (50, 2),
        "rough": (30, 1),
        "faceted": (20, 3)
    }
    size_dict = {
        "small": (40, 1),
        "common": (50, 5),
        "large": (8, 25),
        "exceptional": (2, 100)
    }

    def __init__(self, g_type, size, cut):
        self.g_type = g_type  # Тип камня
        self.size = size  # размер
        self.size_mod = Gem.size_dict[size][1]  # модификатор размера
        """степень обработки"""
        if self.g_type == "pearl" or self.g_type == "black_pearl":
            self.cut = " "
        else:
            self.cut = cut
        self.cut_mod = Gem.cut_dict[cut][1]  # модификатор обработки
        self.base = gem_types[self.g_type][1]  # базовая ценность, зависит от типа
        # проверяем возможность инкрустации:
        if self.size == 100:
            self.can_be_incrusted = False
        else:
            self.can_be_incrusted = True
        if self.size_mod >= 25:
            self.amount = 1
        else:
            if self.size_mod == 5:
                self.amount = 5
            else:
                self.amount = 20

    @property
    def cost(self):  # цена камня, складывается из базы(зависит от типа), размера и степени обработки
        return self.base * self.size_mod * self.cut_mod * self.amount

    def __repr__(self):
        return "%s %s %s" % (self.size, self.cut, self.g_type)

    def __eq__(self, other):
        if isinstance(other, Gem):
            return other and self.g_type == other.g_type and self.cut == other.cut \
                and self.size == other.size
        else:
            return

    def description(self, custom=False, case='nominative', gender='he', language='rus'):
        """
        Создает описание для драгоценного камня
        :custom: - если False - добавляет в описание "горсть"/"несколько" для мелких/обычных камней и
            меняет соответствующим образом род и падеж камней
        :case: - в каком падеже описываются камни
        :gender: - какого рода камни - 'he' (мужского), 'she' (женского) или 'they' (множественное число)
        """
        if language == 'rus':
            if not custom and (self.size == 'small' or self.size == 'common'):
                case = 'genitive'
                gender = 'they'
                if self.size == 'small':
                    return u"Горсть мелких %s%s" % (
                        gem_cut_description_rus[self.cut][gender][case], gem_description_rus[self.g_type][gender][case])
                else:
                    return u"Несколько %s%s" % (
                        gem_cut_description_rus[self.cut][gender][case], gem_description_rus[self.g_type][gender][case])
            else:
                if self.g_type == 'pearl' or self.g_type == 'black_pearl':
                    gender = 'she'
                elif gender != 'they':
                    gender = 'he'
                return u"%s%s%s" % (
                    material_size_description_rus[self.size][gender][case],
                    gem_cut_description_rus[self.cut][gender][case],
                    gem_description_rus[self.g_type][gender][case])
        else:
            return self.__repr__()

    @staticmethod
    def number_conjugation(gem_type, gem_count):
        """
        Функция для вывода описания камней по типу (в формате тип/размер/огранка)
        и количеству (без учета умножения мелких/обычных камней)
        """
        gem_param = gem_type.split(';')
        if gem_param[1] == 'small' or gem_param[1] == 'common':  # умножаем мелкие/обычные камни
            if gem_param[1] == 'small':
                gem_count *= 25
            else:
                gem_count *= 5
        conjugation_type = number_conjugation_type(gem_count)  # определяем тип сопряжения
        # определяем род, некрасивый вариант - лучше использовать словарь:
        if gem_param[0] == 'pearl' or gem_param[0] == 'black_pearl':
            gender = 'she'
        else:
            gender = 'he'
        # выводим результат для каждого типа сопряжения
        # единственное число - именительный падеж, род копируется
        if conjugation_type == 0:
            if gem_count != 1:  # если камень один - не ставим число
                return u"%s %s%s%s" % (gem_count, material_size_description_rus[gem_param[1]][gender]['nominative'],
                                       gem_cut_description_rus[gem_param[2]][gender]['nominative'],
                                       gem_description_rus[gem_param[0]][gender]['nominative'])
            else:
                return u"%s%s%s" % (material_size_description_rus[gem_param[1]][gender]['nominative'],
                                    gem_cut_description_rus[gem_param[2]][gender]['nominative'],
                                    gem_description_rus[gem_param[0]][gender]['nominative'])
        # маломножественная форма - родительный падеж, тип в единственном числе, прилагательные - во множественном
        elif conjugation_type == 1:
            return u"%s %s%s%s" % (gem_count, material_size_description_rus[gem_param[1]]['they']['genitive'],
                                   gem_cut_description_rus[gem_param[2]]['they']['genitive'],
                                   gem_description_rus[gem_param[0]][gender]['genitive'])
        # множественное число - родительный падеж множественного числа
        elif conjugation_type == 2:
            gender = 'they'
            return u"%s %s%s%s" % (gem_count, material_size_description_rus[gem_param[1]][gender]['genitive'],
                                   gem_cut_description_rus[gem_param[2]][gender]['genitive'],
                                   gem_description_rus[gem_param[0]][gender]['genitive'])


def generate_gem(count, *args):
    """функция для генерации камней, 1 обязательный аргумент - количество камней
    которое нужно сгенерировать, чтобы задать размер и/или качество обработки
    вызываем с аргументом {"size":("размер", "размер", ...} или {"cut":("качество, "качество", ...)}
    число будет использоваться для определения ценности
    камня, чтобы задать типы камней, вызываем с аргументом "тип камня" или
    ["тип камня", "тип камня", ...]
    на пример generate_gem(5, {"size":("common", "small")}, ["ruby", "star", "aqua"],
                       "diamond")
    создаст 5 разных камней размера common или small случайного качества огранки, 
    тип каждого будет выбран из заданных, шансы появления которых относительно
    друг друга указанны в словаре gem_types"""
    gems = []
    if len(args) != 0:
        cut = {}
        size = {}
        new_dict = {}
        for i in args:
            if isinstance(i, dict):
                if i.keys()[0] == "size":
                    for v in i["size"]:
                        if v in Gem.size_dict:
                            size[v] = Gem.size_dict[v]
                elif i.keys()[0] == "cut":
                    for v in i["cut"]:
                        if v in Gem.cut_dict:
                            cut[v] = Gem.cut_dict[v]
            elif isinstance(i, list):
                for item in i:
                    if item in gem_types:
                        new_dict[item] = gem_types[item]
            elif isinstance(i, basestring):
                if i in gem_types:
                    new_dict[i] = gem_types[i]
        while count > 0:
            if len(cut) == 0:
                cut = Gem.cut_dict
            if len(size) == 0:
                size = Gem.size_dict
            if len(new_dict) == 0:
                new_dict = gem_types
            gems.append(Gem(weighted_select(new_dict), weighted_select(size), weighted_select(cut)))
            count -= 1
        return gems
    for i in xrange(count):
        gems.append(Gem(weighted_select(gem_types), weighted_select(Gem.size_dict), weighted_select(Gem.cut_dict)))
    return gems


class Material(object):  # класс для генерации материалов
    size_dict = {"small": (40, 1), "common": (50, 5), "large": (8, 25), "exceptional": (2, 100)}

    def __init__(self, m_type, size):
        self.m_type = m_type  # название
        self.base = material_types[m_type][1]  # базовая цена
        self.size = size  # размер
        self.size_mod = Material.size_dict[size][1]  # модификатор размера

    @property
    def cost(self):  # определяем цену материала(зависит от размера и типа)
        return self.size_mod * self.base

    def __repr__(self):
        return "%s %s" % (self.size, self.m_type)

    def __eq__(self, other):
        if isinstance(other, Material):
            return other and self.m_type == other.m_type and self.size == other.size
        else:
            return

    def description(self, language='rus'):
        if language == 'rus':
            return u"%sкусок %s" % (material_size_description_rus[self.size]['he']['nominative'],
                                    material_description_rus[self.m_type]['genitive'])
        else:
            return self.__repr__()

    @staticmethod
    def number_conjugation(material_type, material_count):
        """
        Функция для вывода описания камней по типу (в формате тип/размер) и количеству
        """
        material_param = material_type.split(';')
        conjugation_type = number_conjugation_type(material_count)  # определяем тип сопряжения
        # выводим результат для каждого типа сопряжения
        if conjugation_type == 0:  # единственное число - именительный падеж, род копируется
            if material_count != 1:  # если материал один - не ставим число
                return u"%s %sкусок %s" % (
                    material_count, material_size_description_rus[material_param[1]]['he']['nominative'],
                    material_description_rus[material_param[0]]['genitive'])
            else:
                return u"%sкусок %s" % (material_size_description_rus[material_param[1]]['he']['nominative'],
                                        material_description_rus[material_param[0]]['genitive'])
        elif conjugation_type == 1:
            return u"%s %sкуска %s" % (
                material_count, material_size_description_rus[material_param[1]]['they']['genitive'],
                material_description_rus[material_param[0]]['genitive'])
        elif conjugation_type == 2:
            return u"%s %sкусков %s" % (
                material_count, material_size_description_rus[material_param[1]]['they']['genitive'],
                material_description_rus[material_param[0]]['genitive'])


def generate_mat(count, *args):
    """принцип работы такойже как для драг.камней"""
    mats = []
    if len(args) != 0:
        size = {}
        new_dict = {}
        for i in args:
            if isinstance(i, dict):
                if i.keys()[0] == "size":
                    # size = {v: Material.size_dict[v] for v in i["size"] if v in Material.size_dict}
                    for v in i["size"]:
                        if v in Material.size_dict:
                            size[v] = Material.size_dict[v]
            elif isinstance(i, list):
                for item in i:
                    if item in material_types:
                        new_dict[item] = material_types[item]
            elif isinstance(i, basestring):
                if i in material_types:
                    new_dict[i] = material_types[i]
        for i in xrange(count):
            if len(size) == 0:
                size = Material.size_dict
            if len(new_dict) == 0:
                new_dict = material_types
            mats.append(Material(weighted_select(new_dict), weighted_select(size)))
        return mats
    for i in xrange(count):
        mats.append(Material(weighted_select(material_types), weighted_select(Material.size_dict)))
    return mats


class Treasure(object):  # класс для сокровищ
    decorate_types = {"incuse": (33,), "engrave": (33,), "etching": (33,), "carving": (0,)}
    quality_types = {"common": (60, 2), "skillfully": (20, 3), "rough": (10, 1), "mastery": (10, 5)}

    def __init__(self, treasure_type, alignment):
        """все значения заносятся из словаря treasure_types"""
        self.treasure_type = treasure_type
        self.base_price = treasure_types[self.treasure_type][0]
        self.gender = treasure_types[self.treasure_type][1]
        self.metal = treasure_types[self.treasure_type][2]
        self.nonmetal = treasure_types[self.treasure_type][3]
        self.image = treasure_types[self.treasure_type][4]
        self.incrustable = treasure_types[self.treasure_type][5]
        self.decorable = treasure_types[self.treasure_type][6]
        self.alignment = alignment
        """дальше генерируем характеристики в зависимости от типа сокровища"""
        self.random_mod = random.randint(0, self.base_price * 10)
        if random.randint(1, 100) <= 50 and self.incrustable:
            self.spangled = generate_gem(1, {"size": ('common',)})[0]
            # размер 'common' - хак, чтобы не писалось "мелкими":
        else:
            self.spangled = None
        if random.randint(1, 100) <= 15 and self.incrustable:
            self.inlaid = generate_gem(1, {"size": ('common',)})[0]
        else:
            self.inlaid = None
        if random.randint(1, 100) <= 5 and self.incrustable:
            self.huge = generate_gem(1, {"size": ('large',)})[0]
        else:
            self.huge = None

        def metals_available():  # проверяем принадлежность к расе(из каких металов может быть сделано)
            if self.alignment == "human" or self.alignment == "cleric" or self.alignment == "knight":
                return {"silver": (70,), "gold": (30,)}
            elif self.alignment == "elf" or self.alignment == "merman":
                return {"gold": (70,), "mithril": (30,)}
            elif self.alignment == "dwarf":
                return {"gold": (70,), "adamantine": (30,)}

        def material():
            if self.metal and self.nonmetal:
                rnd = random.randint(1, 100)
                if rnd > 50:
                    return weighted_select(material_types)
                else:
                    return weighted_select(metals_available())
            elif self.metal:
                return weighted_select(metals_available())
            else:
                return weighted_select(material_types)

        self.material = material()  # выбираем материал

        def decorate():
            if self.decorable:
                rnd = random.randint(1, 100)
                if rnd <= 15:
                    rnd = random.randint(1, 100)
                    if rnd <= 50:
                        self.decoration_image = random.choice(image_types[self.alignment])
                        if self.material in material_types:
                            return "carving"
                        else:
                            return weighted_select(Treasure.decorate_types)
                    else:
                        return None
                else:
                    return None

        self.decoration = decorate()  # выбираем орнамент
        if self.image:
            self.decoration_image = random.choice(image_types[self.alignment])

        def q_choice():  # прокидываем качество вещи
            if self.alignment == "human" or self.alignment == "cleric" or self.alignment == "knight":
                return weighted_select(Treasure.quality_types)
            else:
                from copy import deepcopy
                holder = deepcopy(Treasure.quality_types)
                holder.__delitem__('rough')
                return weighted_select(holder)

        self.quality = q_choice()
        self.obtained = u""

    def incrustation(self, gem):  # метод для икрустации камней
        if not self.incrustable:
            return "Can't be incrusted"
        if gem.size == "small":
            if self.spangled is None:
                self.spangled = gem
            return
        if gem.size[1] == "common":
            if self.inlaid is None:
                self.inlaid = gem
            return
        if gem.size[1] == "huge":
            if self.huge is None:
                self.huge = gem
            return

    @property  # качество вещи
    def quality(self):
        return self._quality

    @quality.setter
    def quality(self, value):
        self._quality = value
        if value in Treasure.quality_types:
            self.quality_mod = Treasure.quality_types[value][1]

    @property  # тип материала
    def material(self):
        return self._material

    @material.setter
    def material(self, value):
        self._material = value
        if self.material in material_types:
            self.mat_price = material_types[self._material][1]
        else:
            self.mat_price = metal_types[self._material]

    @property  # тип орнамента
    def decoration(self):
        return self._decoration

    @decoration.setter
    def decoration(self, value):
        self._decoration = value
        if value is None:
            self.dec_mod = 1
        else:
            self.dec_mod = 2  # равен двум если есть орнамент

    @property  # цена вставленных камней
    def incrustation_cost(self):
        holder = 0
        if self.spangled is not None:
            # из-за хака с размерами нужно умножить на реальный размер и поделить на "хакнутый"
            holder += self.spangled.cost * Gem.size_dict['small'][1] // Gem.size_dict['common'][1]
        if self.inlaid is not None:
            holder += self.inlaid.cost
        if self.huge is not None:
            holder += self.huge.cost
        return holder

    def craft_cost(self, base_cost, price_multiplier):  
        """
        Цена создания/покупки
        :param base_cost: базовая стоимость работы (для ремесла)
        :param price_multiplier: увеличение цены (для покупки, в процентах)
        :return: созданная вещь либо None в случае отмены
        """
        price = self.cost * price_multiplier // 100
        price += base_cost
        if self.spangled:
            price += base_cost
        if self.inlaid:
            price += base_cost
        if self.huge:
            price += base_cost
        if self.decoration:
            price += 2 * base_cost
        return price

    @property
    def cost(self):  # цена сокровища
        return \
            self.base_price * self.quality_mod * self.dec_mod * self.mat_price + \
            self.incrustation_cost + self.random_mod

    def __repr__(self):
        return "%s%s" % (self.material, self.treasure_type)

    def description(self, language='rus'):
        if language == 'rus':
            quality_str = quality_description_rus[self.quality][self.gender]  # мастерство исполнения
            treasure_str = treasure_description_rus[self.treasure_type]['nominative']  # тип драгоценности
            # совмещаем мастерство исполнения, тип и материал, из которого изготовлено
            if self.material in metal_types.keys():
                if self.treasure_type == 'icon' or self.treasure_type == 'tome':
                    desc_str = u"%s%s в %s окладе" % (
                        quality_str, treasure_str, metal_description_rus[self.material]['prepositional'])
                else:
                    desc_str = u"%s%s %s" % (
                        quality_str, metal_description_rus[self.material][self.gender], treasure_str)
            else:
                desc_str = u"%s%s из %s" % (
                    quality_str, treasure_str, material_description_rus[self.material]['genitive'])

            if self.image:
                desc_str += u", изображающая %s" % image_description_rus[self.decoration_image]['accusative']  
                # только изображение
            else:
                # добавляем различные украшения
                enchant_list = []
                if self.spangled:  # усыпанное камнями
                    enchant_list.append(u"%s %s" % (decoration_description_rus['spangled'][self.gender],
                                                    self.spangled.description(True, 'ablative', 'they')))
                if self.inlaid:  # инкрустированное камнями
                    enchant_list.append(u"%s %s" % (decoration_description_rus['inlaid'][self.gender],
                                                    self.inlaid.description(True, 'ablative', 'they')))
                if self.huge:  # с крупным камнем
                    # только ради "крупной (чёрной) жемчужины":
                    enchant_list.append(u"с %s" % self.huge.description(True, 'ablative'))
                if self.decoration:  # украшенное чеканкой/гравировкой/травлением/резьбой
                    enchant_list.append(u"%s %s" % (decoration_description_rus['decoration'][self.gender],
                                                    decorate_types_description_rus[self.decoration]))
                if len(enchant_list) == 1:
                    if not self.huge:
                        desc_str += u","  # добавляем "с крупным камнем" без запятой
                    desc_str += u" %s" % enchant_list[0]
                elif len(enchant_list) > 1:
                    while len(enchant_list) > 1:
                        desc_str += u", %s" % enchant_list[0]  # добавляем через запятую украшения
                        del enchant_list[0]
                    desc_str += u" и %s" % enchant_list[0]  # последнее добавляется союзом "и"
                if self.decoration:  # если есть изображение - ставим точку и описываем его
                    image_description = image_description_rus[self.decoration_image]  # упрощение доступа к свойству
                    desc_str = u"%s. На %s %s %s" % (desc_str, treasure_description_rus[self.treasure_type]['ablative'],
                                                     decoration_description_rus['image'][image_description['gender']],
                                                     image_description['nominative'])
            return desc_str
        else:
            return self.__repr__()


def gen_treas(count, t_list, alignment, min_cost, max_cost, obtained):
    """Генерируем рандомное сокровище
    функция генерации сокровищ,
    count - количество сокровищ,
    t_list - список строк-имен сокровищ,
    alignmet - принадлежность к определенной культуре(одно из: human, cleric, knight, merman, elf, dwarf),
    min_cost - минимальная цена сокровища,
    max_cost - максимальная цена сокровища"""
    treasures_list = []
    while count > 0:
        treas_holder = random.choice(t_list)
        if treas_holder in gem_types:
            treasures_list.extend(generate_gem(1, treas_holder))
        elif treas_holder in material_types:
            treasures_list.extend(generate_mat(1, treas_holder))
        elif treas_holder in metal_types:
            treasures_list.append(Ingot(treas_holder))
        elif treas_holder in Coin.coin_types:
            rnd = random.randint(min_cost, max_cost)
            treasures_list.append(Coin(treas_holder, rnd / Coin.coin_types[treas_holder][1]))
        elif treas_holder in treasure_types:
            t = Treasure(treas_holder, alignment)
            t.obtained = obtained
            treasures_list.append(t)
        else:
            raise Exception("Таких сокровищ не бывает")
        if not min_cost < treasures_list[-1].cost < max_cost:
            treasures_list.pop()
            count += 1
        count -= 1
    return treasures_list


class Treasury(store.object):
    def __init__(self):
        self.farting = 0  # медная монетка
        self.taller = 0  # серебряная монетка
        self.dublon = 0  # золотая монетка
        # списки строк
        self.materials = {}  # словарь с количеством материала
        self.metals = {}  # словарь с количеством металла
        self.jewelry = []  # список драгоценностей
        self.equipment = []
        self.gems = {}  # словарь с количеством драгоценных камней
        # TODO: multiple same equipment
        self.thief_items = []

    @property
    def money(self):
        return self.farting + 10 * self.taller + 100 * self.dublon

    @money.setter
    def money(self, value):
        if value < 0:  # Защита от ухода денег в минус
            raise NotImplementedError(u"Денег недостаточно для выполнения операции")
        money_diff = value - self.money  # считаем разницу между прошлым значением и новым
        if money_diff < 0:
            # разница отрицательна или ноль - производим вычитание
            money_diff = -money_diff  # для удобства получаем число, которое необходимо вычесть
            if self.farting < money_diff % 10:
                # медных монет недостаточно для выплаты, меняем серебряную
                self.taller -= 1
                self.farting += 10
            self.farting -= money_diff % 10
            money_diff //= 10
            if self.taller < money_diff % 10:
                if (self.farting // 10 + self.taller) < money_diff % 10:
                    # серебряных монет даже с учетом медных недостаточно для выплаты, меняем золотую
                    self.dublon -= 1
                    self.taller += 10
                else:
                    # серебряных монет с учетом медных достаточно для выплаты, меняем по максимуму медные на серебряные
                    self.taller += self.farting // 10
                    self.farting %= 10
            self.taller -= money_diff % 10
            money_diff //= 10
            if self.dublon < money_diff % 10:
                # золотых монет недостаточно для выплаты
                self.taller += self.farting // 10  # меняем по максимуму медные на серебряные
                self.farting %= 10
                self.dublon += self.taller // 10  # меняем по максимуму серебряные на золотые
                self.taller %= 10
            self.dublon -= money_diff
        else:
            # разница положительна - производим добавление монет по разрядам
            self.dublon += money_diff // 100
            money_diff %= 100
            self.taller += money_diff // 10
            self.farting += money_diff % 10

    @property
    def wealth(self):
        """
        Стоимость всех сокровищ дракона
        """
        calc_wealth = self.money  # деньги
        for metal in self.metals.iterkeys():  # металлы
            calc_wealth += self.metals[metal] * metal_types[metal]
        for material_i in self.materials.iterkeys():  # материалы
            material = material_i.split(';')
            calc_wealth += self.materials[material_i] * material_types[material[0]][1] * \
                           Material.size_dict[material[1]][1]
        for gem_i in self.gems.iterkeys():  # драгоценные камни
            gem = gem_i.split(';')
            calc_wealth += self.gems[gem_i] * gem_types[gem[0]][1] * Gem.size_dict[gem[1]][1] * Gem.cut_dict[gem[2]][1]
        for treas_i in xrange(len(self.jewelry)):  # украшения
            calc_wealth += self.jewelry[treas_i].cost
        return calc_wealth

    def receive_treasures(self, treasure_list):
        """
        Помещает сокровища в сокровищницу
        :param treasure_list: Список сокровищ, помещаемых в сокровищницу
        """
        from data import achieve_target
        for treas in treasure_list:
            achieve_target(treas.cost, "treasure")#Событие для ачивок
            if isinstance(treas, Coin):
                # сохраняется число медных, серебряных и золотых монет в соответствующих переменных
                if treas.name == 'farting':
                    self.farting += treas.amount
                elif treas.name == 'taller':
                    self.taller += treas.amount
                else:
                    self.dublon += treas.amount
            elif isinstance(treas, Ingot):
                # сохраняется в словаре metals, где ключ - название металла, а значение - его вес в фунтах
                if treas.metal_type in self.metals:
                    self.metals[treas.metal_type] += treas.weight
                else:
                    self.metals[treas.metal_type] = treas.weight
            elif isinstance(treas, Material):
                # сохраняется в словаре materials, где
                # ключ - "название материала;размер материала", а
                # значение - число материалов такого типа и размера
                type_str = treas.m_type + ';' + treas.size
                if type_str in self.materials:
                    self.materials[type_str] += 1
                else:
                    self.materials[type_str] = 1
            elif isinstance(treas, Gem):
                # сохраняется в словаре gems, где
                # ключ - "название драгоценности;размер драгоценности;обработка драгоценности", а
                # значение - число камней такого типа, размера и обработки
                type_str = treas.g_type + ';' + treas.size + ';' + treas.cut
                if type_str in self.gems:
                    self.gems[type_str] += 1
                else:
                    self.gems[type_str] = 1
            elif isinstance(treas, Treasure):
                self.jewelry.append(treas)
        achieve_target(self.wealth, "wealth")#Событие для ачивок

    @staticmethod
    def treasures_description(treasure_list):
        """
        :param treasure_list: Список сокровищ, для которых требуется получить описание
        :return: Возвращает список с описанием сокровищ
        """
        from copy import deepcopy

        treas_list = deepcopy(treasure_list)
        description_list = []
        # Группируем монеты, слитки, драгоценные камни и материалы
        coin_list = {}
        ingot_list = {}
        gem_list = {}
        material_list = {}
        for treas_i in reversed(xrange(len(treasure_list))):
            treas = treas_list[treas_i]
            if isinstance(treas, Coin):
                if treas.name in coin_list:
                    coin_list[treas.name] += treas.amount
                else:
                    coin_list[treas.name] = treas.amount
                del treas_list[treas_i]
            elif isinstance(treas, Ingot):
                if treas.metal_type in ingot_list:
                    ingot_list[treas.metal_type] += treas.weight
                else:
                    ingot_list[treas.metal_type] = treas.weight
                del treas_list[treas_i]
            elif isinstance(treas, Gem):
                type_str = treas.g_type + ';' + treas.size + ';' + treas.cut
                if type_str in gem_list:
                    gem_list[type_str] += 1
                else:
                    gem_list[type_str] = 1
                del treas_list[treas_i]
            elif isinstance(treas, Material):
                type_str = treas.m_type + ';' + treas.size
                if type_str in material_list:
                    material_list[type_str] += 1
                else:
                    material_list[type_str] = 1
                del treas_list[treas_i]
        for treas in coin_list.iterkeys():
            description_list.append(Coin.number_conjugation(treas, coin_list[treas]) + '.')
        for treas in ingot_list.iterkeys():
            description_list.append(capitalize_first(Ingot.number_conjugation(treas, ingot_list[treas])) + '.')
        for treas in gem_list.iterkeys():
            if gem_list[treas] > 1:
                description_list.append(capitalize_first(Gem.number_conjugation(treas, gem_list[treas])) + '.')
            else:
                description_list.append(capitalize_first(Gem(*treas.split(';')).description()) + '.')
        for treas in material_list.iterkeys():
            if material_list[treas] > 1:
                description_list.append(capitalize_first(
                    Material.number_conjugation(treas, material_list[treas])) + '.')
            else:
                description_list.append(capitalize_first(Material(*treas.split(';')).description()) + '.')
            # Выводим остальное
        for treas in treas_list:
            # TODO: найти откуда в списке сокровищ при воровстве может быть None
            if treas:
                description_list.append(capitalize_first(treas.description()) + '.')
        return description_list

    def take_ingot(self, ingot_type, weight=1):
        """
        :param ingot_type: название металла
        :param weight: вес, который мы хотели бы взять 
        :return: Возвращает тип Ingot с указанным весом или максимально возможным, либо None,
            если такого металла в сокровищнице нет
        """
        if ingot_type in self.metals and self.metals[ingot_type] > 0:  # проверяем есть ли такой металл в сокровищнице
            ingot = Ingot(ingot_type)  # создаем слиток
            # делаем вес слитка равным указанному весу или максимуму в сокровищнице:
            if weight < self.metals[ingot_type]:
                ingot.weight = weight
            else:
                ingot.weight = self.metals[ingot_type]
            self.metals[ingot_type] -= ingot.weight  # вычитаем вес слитка из сокровищницы
            if self.metals[ingot_type] == 0:
                del self.metals[ingot_type]  # удаляем тип материала из списка сокровищницы
            return ingot
        elif ingot_type in self.metals:
            del self.metals[ingot_type]  # удаляем тип металла из списка сокровищницы
        return None

    def take_material(self, material_name):
        """
        :param material_name: описание материала в формате 'тип;размер'
        :return: Возвращает тип Material или None, если такого материала в сокровищнице нет
        """
        # проверяем есть ли такой материал в сокровищнице
        if material_name in self.materials and self.materials[material_name] > 0:
            material_param = material_name.split(';')  # парсим строку
            material = Material(*material_param)  # получаем экземпляр класса с нужными параметрами
            self.materials[material_name] -= 1  # вычитаем один материал из списка сокровищницы
            if self.materials[material_name] == 0:
                del self.materials[material_name]  # удаляем тип материала из списка сокровищницы
            return material
        elif material_name in self.materials:
            del self.materials[material_name]  # удаляем тип материала из списка сокровищницы
        return None

    def take_gem(self, gem_name):
        """
        :param gem_name: описание камня в формате 'тип;размер;обработка'
        :return: Возвращает тип Gem или None, если таких камней в сокровищнице нет
        """
        if gem_name in self.gems and self.gems[gem_name] > 0:  # проверяем есть ли такой камень в сокровищнице
            gem_param = gem_name.split(';')  # парсим строку
            gem = Gem(*gem_param)  # получаем экземпляр класса с нужными параметрами
            self.gems[gem_name] -= 1  # вычитаем один камень из списка сокровищницы
            return gem
        elif gem_name in self.gems:
            del self.gems[gem_name]  # удаляем тип камня из списка сокровищницы
        return None

    def take_coin(self, coin_name, coin_count=1):
        """
        :param coin_name: название монеты
        :param coin_count: сколько монет нам бы хотелось взять
        :return: Возвращает тип Coin с указанным числом монет или максимально возможным, либо None,
            если таких монет в сокровищнице нет
        """
        if coin_name == 'farting' and self.farting > 0:
            if coin_count > self.farting:
                coin_count = self.farting
            self.farting -= coin_count
        elif coin_name == 'taller' and self.taller > 0:
            if coin_count > self.taller:
                coin_count = self.taller
            self.taller -= coin_count
        elif coin_name == 'dublon' and self.dublon > 0:
            if coin_count > self.dublon:
                coin_count = self.dublon
            self.dublon -= coin_count
        else:
            return None
        return Coin(coin_name, coin_count)

    def rob_treasury(self, treasure_count=1):
        """
        :param treasure_count: Количество сокровищ, которые необходимо взять из сокровищницы
        :return: Список самых дорогих сокровищ, взятых из сокровищницы
        """
        treasure_list = []  # список сокровищ, которые не приглянулись вору
        abducted_list = []  # список награбленного
        threshold_value = 0  # минимальная стоимость, которая будет взята

        def update_list(test_treasure):  
            """
            функция добавления награбленного в список, возвращает истину в случае успешного добавления
            """
            if not test_treasure:
                return False  # попытка взять несуществующую вещь
            elif threshold_value < test_treasure.cost:
                test_cost = test_treasure.cost  # сохраняем цену для скорости
                test_i = len(abducted_list)  # новый индекс - последний в списке
                while test_i > 0 and abducted_list[test_i - 1].cost < test_cost:
                    test_i -= 1  # сортировка
                abducted_list.insert(test_i, test_treasure)  # вставляем в нужную позицию
                if len(abducted_list) > treasure_count:  # убираем из списка вещь с наименьшей ценой
                    treasure_list.append(abducted_list.pop())
                    self.threshold_value = abducted_list[-1].cost
                return True
            else:
                # стоимость добавляемого меньше пороговой, возвращаем сокровище обратно в сокровищницу
                treasure_list.append(test_treasure)
                return False

        # цикл по всем сокровищам, начиная с конца списка, для соответствия индекса количеству вещей в списке
        for _ in reversed(xrange(len(self.jewelry))):
            # достаем сокровище из конца списка - там должны быть более дорогие сокровища и
            # пробуем добавить их в список награбленного
            update_list(self.jewelry.pop())
        self.jewelry.extend(treasure_list)  # возвращаем сокровища в сокровищницу после поиска самых дорогих
        treasure_list = []  # очищаем список возвращаемого
        for gem_type in self.gems.keys():  # просматриваем список типов камней
            while update_list(self.take_gem(gem_type)):
                pass  # пока в список добавляются камни - добавляем
        for metal_type in self.metals.keys():  # аналогично, просматриваем список типов слитков
            while update_list(self.take_ingot(metal_type, 8)):
                pass  # пока в список добавляются слитки - добавляем
        for coin_type in Coin.coin_types.keys():  # аналогично, просматриваем список типов монет
            while update_list(self.take_coin(coin_type, 100)):
                pass  # пока в список добавляются монеты - добавляем
        for material_type in self.materials.keys():  # аналогично, просматриваем список типов материалов
            while update_list(
                    self.take_material(material_type)):
                pass  # пока в список добавляются материалы - добавляем
        self.receive_treasures(treasure_list)  # возвращаем сокровища в сокровищницу
        return abducted_list

    def gem_name_count(self, gem_name):
        """
        :param gem_name: Тип драгоценных камней (в формате 'тип;размер;обработка'), для которого необходимо подсчитать
            количество камней в сокровищнице
        :return: количество камней такого типа в сокровищнице с учетом того, что мелкие идут группами по 25, а
            обычные - по 5
        """
        gem_count = self.gems[gem_name]  # берем данные о количестве из словаря
        gem_param = gem_name.split(';')  # парсим строку
        if gem_param[1] == 'small':
            gem_count *= 25
        elif gem_param[1] == 'common':
            gem_count *= 5
        return gem_count

    @property
    def gems_list(self):
        """
        :return: строка с описанием количества драгоценных камней в сокровищнице
        """
        gem_str = u"В сокровищнице находится:\n"
        gem_list = sorted(self.gems.keys())  # список драгоценных камней, отсортированных по типу/размеру/огранке
        for gem_name in gem_list:
            if self.gems[gem_name]:  # проверка наличия камней такого типа в сокровищнице
                gem_str += u"%s.\n" % capitalize_first(Gem.number_conjugation(gem_name, self.gems[gem_name]))
        return gem_str

    @property
    def materials_list(self):
        """
        :return: строка с описанием количества материалов в сокровищнице
        """
        material_str = u"В сокровищнице находится:\n"
        metal_list = sorted(self.metals.keys())
        for metal_name in metal_list:
            metal_weight = self.metals[metal_name]
            if metal_weight:
                material_str += u"%s.\n" % capitalize_first(Ingot.number_conjugation(metal_name, metal_weight))
        mat_list = sorted(self.materials.keys())
        for mat_name in mat_list:
            if self.materials[mat_name]:
                material_str += u"%s.\n" % capitalize_first(
                    Material.number_conjugation(mat_name, self.materials[mat_name]))
        return material_str

    @property
    def most_expensive_jewelry_index(self):
        """
        Индекс самого дорогого украшения в сокровищнице
        """
        if len(self.jewelry):
            most_expensive_i = 0
            most_expensive_cost = self.jewelry[most_expensive_i].cost
            for jewelry_i in xrange(len(self.jewelry)):
                if self.jewelry[jewelry_i].cost > most_expensive_cost:
                    most_expensive_cost = self.jewelry[jewelry_i].cost
                    most_expensive_i = jewelry_i
            return most_expensive_i
        else:
            return -1

    @property
    def cheapest_jewelry_index(self):
        """
        Индекс самого дешёвого украшения в сокровищнице
        """
        if len(self.jewelry):
            cheapest_i = 0
            cheapest_cost = self.jewelry[cheapest_i].cost
            for jewelry_i in xrange(len(self.jewelry)):
                if self.jewelry[jewelry_i].cost < cheapest_cost:
                    cheapest_cost = self.jewelry[jewelry_i].cost
                    cheapest_i = jewelry_i
            return cheapest_i
        else:
            return -1

    @property
    def most_expensive_jewelry_cost(self):
        """
        Стоимость самого дорогого украшения в сокровищнице
        """
        if len(self.jewelry):
            return self.jewelry[self.most_expensive_jewelry_index].cost
        else:
            return 0

    @property
    def most_expensive_jewelry(self):
        """
        Описание самого дорогого украшения в сокровищнице
        """
        if len(self.jewelry):
            most_expensive_i = self.most_expensive_jewelry_index
            return u"%s.\nСтоимость украшения: %s.\n%s" % (
                capitalize_first(self.jewelry[most_expensive_i].description()),
                number_conjugation_rus(self.jewelry[most_expensive_i].cost, u"фартинг"),
                self.jewelry[most_expensive_i].obtained)
        else:
            return u"Украшений в сокровищнице нет"

    @property
    def cheapest_jewelry(self):
        """
        Описание самого дешёвого украшения в сокровищнице
        """
        if len(self.jewelry):
            cheapest_i = self.cheapest_jewelry_index
            return u"%s.\nСтоимость украшения: %s.\n%s" % (
                capitalize_first(self.jewelry[cheapest_i].description()),
                number_conjugation_rus(self.jewelry[cheapest_i].cost, u"фартинг"),
                self.jewelry[cheapest_i].obtained)
        else:
            return u"Украшений в сокровищнице нет"

    @property
    def random_jewelry(self):
        if len(self.jewelry):
            random_jewelry = random.choice(self.jewelry)
            return u"%s.\nСтоимость украшения: %s.\n%s" % (capitalize_first(random_jewelry.description()),
                                                           number_conjugation_rus(random_jewelry.cost, u"фартинг"),
                                                           random_jewelry.obtained)
        else:
            return u"Украшений в сокровищнице нет"

    @property
    def all_jewelries(self):
        """
        Стоимость всех украшений дракона
        """
        calc_all_jewelries = 0
        for treas_i in xrange(len(self.jewelry)):  
            calc_all_jewelries += self.jewelry[treas_i].cost
        return calc_all_jewelries

    @staticmethod
    def get_mass_description(description_key, mass):
        """ 
        :param description_key: ключ для словаря treasures_mass_description_rus
        :param mass: число, для которой нужно подобрать описание
        :return: описание массы в сокровищнице
        """
        if mass > 0:
            from data import get_description_by_count
            return get_description_by_count(treasures_mass_description_rus[description_key], mass)
        else:
            return u""

    @property
    def coin_mass(self):
        """
        :return: масса монет в сокровищнице
        """
        return self.farting + self.taller + self.dublon

    @property
    def coin_mass_description(self):
        """
        :return: описание массы монет в сокровищнице
        """
        return Treasury.get_mass_description('coin', self.coin_mass)

    @property
    def metal_mass(self):
        """
        :return: вес металла в сокровищнице
        """
        metal_weight = 0
        for metal_i in self.metals.values():
            metal_weight += metal_i
        return metal_weight

    @property
    def materials_mass_description(self):
        """
        :return: описание массы материалов и металлов в сокровищнице
        """
        return Treasury.get_mass_description('material', self.metal_mass + self.material_mass)

    @property
    def gem_mass(self):
        """
        :return: масса драгоценных камней в сокровищнице
        """
        gem_summ = 0
        for gem_i in self.gems.keys():
            gem_size = gem_i.split(';')
            gem_size = gem_size[1]
            if gem_size == 'small':
                gem_summ += 25
            elif gem_size == 'common':
                gem_summ += 15
            elif gem_size == 'large':
                gem_summ += 5
            else:
                gem_summ += 7
        return gem_summ

    @property
    def gems_mass_description(self):
        """
        :return: описание массы драгоценных камней в сокровищнице
        """
        return Treasury.get_mass_description('gem', self.gem_mass)

    @property
    def material_mass(self):
        """
        :return: масса материала в сокровищнице
        """
        mat_summ = 0
        for mat_i in self.materials.keys():
            mat_size = mat_i.split(';')
            mat_size = mat_size[1]
            mat_summ += Material.size_dict[mat_size][1]
        return mat_summ

    @property
    def jewelry_mass(self):
        """
        :return: масса украшений в сокровищнице
        """
        jewelry_summ = 0
        for jewelry_i in self.jewelry:
            jewelry_summ += jewelry_i.base_price
        return jewelry_summ

    @property
    def jewelry_mass_description(self):
        """
        :return: описание массы драгоценных камней в сокровищнице
        """
        return Treasury.get_mass_description('jewelry', self.jewelry_mass)
        
    @property
    def wealth_description(self):
        """
        :return: описание всех сокровищ в сокровищнице
        """
        wealth = self.wealth
        if wealth > 0:
            wealth_str = Treasury.get_mass_description('wealth', wealth)
            wealth_str += u"Общая стоимость сокровищ: " + number_conjugation_rus(wealth, u"фартинг") + u"."
            return wealth_str 
        else:
            return u"Сокровищница пуста."

    def get_salary(self, amount):
        """
        :param amount: требуемая сумма, фартингов
        :return: список того, что взяли, чтобы получить сумму, либо None, если в сокровищнице недостаточно денег.
        """
        # TODO: Сделать рефакторинг без использования `self`
        self.salary_list = []  # список сокровищ, которые можно взять в качестве платы
        self.salary_item = None  # предмет, который можно взять в качестве платы
        self.min_salary_value = 0  # цена предмета
        self.max_salary_value = 0  # цена списка сокровищ
        self.treasure_list = []  # список сокровищ, которые не приглянулись гремлинам

        def update_list(test_treasure):
            """
            функция добавления в список, возвращает истину если нужно добавить такую же вещь
            """
            if not test_treasure:
                return False  # попытка взять несуществующую вещь
            elif test_treasure.cost >= amount:
                # стоимость сокровища больше или равно необходимой суммы, можно взять только его в качестве оплаты
                if self.min_salary_value == 0:
                    # это первая вещь, которая стоит дороже, чем нам нужно - берём её
                    self.min_salary_value = test_treasure.cost
                    self.salary_item = test_treasure
                elif self.min_salary_value > test_treasure.cost:
                    # это не первая вещь, которая стоит дороже, чем нам нужно - берём её только если она дешевле прошлой
                    self.treasure_list.append(self.salary_item)  # возвращаем прошлую вещь в сокровищницу
                    self.min_salary_value = test_treasure.cost  # берём новую
                    self.salary_item = test_treasure
                else:
                    self.treasure_list.append(test_treasure)  # возвращаем вещь в сокровищницу
                return False  # больше такой не нужно
            else:
                # стоимость сокровища меньше необходимой суммы, придётся "скрести по сусекам"
                if self.max_salary_value < amount:
                    # стоимость списка недостаточно, добавляем ещё
                    self.max_salary_value += test_treasure.cost
                    self.salary_list.append(test_treasure)
                    return True
                else:
                    # стоимость списка достаточно, больше ничего не нужно
                    self.treasure_list.append(test_treasure)  # возвращаем вещь в сокровищницу
                    return False

        if self.wealth >= amount:
            if self.money >= amount:
                self.money -= amount
                self.salary_list.append(Coin('farting', amount))
                return self.salary_list  # взяли деньгами сколько нужно
            else:
                for coin_type in Coin.coin_types.keys():  # просматриваем список типов монет
                    while update_list(self.take_coin(coin_type)):
                        pass  # пока в список добавляются монеты - добавляем
                # цикл по всем сокровищам, начиная с конца списка, для соответствия индекса количеству вещей в списке
                for _ in reversed(xrange(len(self.jewelry))):
                    # достаем сокровище из конца списка - там должны быть более дорогие сокровища и
                    # пробуем добавить их в список
                    update_list(self.jewelry.pop())
                for gem_type in self.gems.keys():  # просматриваем список типов камней
                    while update_list(self.take_gem(gem_type)):
                        pass  # пока в список добавляются камни - добавляем
                for metal_type in self.metals.keys():  # аналогично, просматриваем список типов слитков
                    while update_list(self.take_ingot(metal_type)):
                        pass  # пока в список добавляются слитки - добавляем
                for material_type in self.materials.keys():  # аналогично, просматриваем список типов материалов
                    while update_list(self.take_material(material_type)):
                        pass  # пока в список добавляются материалы - добавляем
                if self.max_salary_value > self.min_salary_value:
                    if self.salary_list:
                        self.treasure_list.extend(self.salary_list)  # возвращаем список в сокровищницу - не пригодился
                    self.salary_list = [self.salary_item]
                elif self.salary_list:
                    self.treasure_list.append(self.salary_item)  # возвращаем предмет в сокровищницу - не пригодился
                self.receive_treasures(self.treasure_list)  # возвращаем сокровища в сокровищницу
                return self.salary_list
        else:
            return None

    def check_gem_size(self, gem_size):
        """
        Функция для проверки есть ли в сокровищнице камень требуемого размера
        :param gem_size: размер камня для проверки
        :return: есть (True) или нет (False) в сокровищнице камень указанного размера
        """
        for gem_type in self.gems:
            if gem_type.split(';')[1] == gem_size:
                return True
        return False

    def available_materials(self, item_type):
        """
        Функция для проверки есть ли материал, из которого можно сделать вещь такого типа
        :param item_type: тип вещи, который хочется смастерить
        :return: список материалов, из которых можно сделать вещь
        """
        materials = []
        if treasure_types[item_type][2]:
            # вещь можно сделать из металла, добавляем доступный список металлов
            materials += self.metals.keys()
        if treasure_types[item_type][3]:
            # вещь можно сделать из поделочного материала, добавляем доступный список материалов
            for material_type in self.materials.keys():
                # убираем повторы из-за возможной разницы в размерах поделочных материалов
                material_name = material_type.split(';')[0]
                if material_name not in materials:
                    materials.append(material_name)
        return materials

    def is_craft_possible(self, item_type, alignment):
        """
        Функция для проверки достаточно ли материалов в сокровищнице для изготовления вещи
        :param item_type: тип вещи, который хочется смастерить
        :return: достаточно (True) или нет (False) материалов для создания вещи
        """
        craft_possible = self.available_materials(item_type)
        if treasure_types[item_type][4]:
            # если сам предмет - изображение - нужен какой-то стиль
            craft_possible = craft_possible and alignment
        return craft_possible

    def craft_select_item(self, is_crafting, alignment):
        """
        Функция для вывода меню выбора типа покупаемой/создаваемой вещи
        :param is_crafting: создаётся из материалов дракона (True) или покупается (False)
        :return: выбранный тип вещи либо None в случае отмены
        """
        from renpy.exports import call_screen
        treasure_list = sorted(treasure_types.keys(), key=lambda treas: treasure_description_rus[treas]['nominative'])
        # получаем список возможных сокровищ
        if is_crafting:
            # если идёт создание вещи - ставим первыми в списке вещи, которые можем сделать
            craft_possible = []
            craft_impossible = []
            for treasure_type in treasure_list:
                if self.is_craft_possible(treasure_type, alignment):
                    craft_possible.append(treasure_type)
                else:
                    craft_impossible.append(treasure_type)
            treasure_list = craft_possible + craft_impossible
        menu_choice = None
        row_count = 10  # количество кнопок с отображаемым типом сокровища для создания/покупки
        position = 0  # начальное значение 
        while menu_choice not in treasure_list:
            # цикл для выбора типа сокровища для создания/покупки
            if row_count < len(treasure_list):
                menu_options = [(u"На предыдущую страницу", 'dec', True, position > 0)]
            else:
                menu_options = [(u"", 'blank', True, False)]
            for i in xrange(position, min(position + row_count, len(treasure_list))):
                treasure_type = treasure_list[i]
                treas_name = treasure_description_rus[treasure_type]['nominative'].capitalize()
                if is_crafting:
                    menu_options.append((treas_name, treasure_type, True, self.is_craft_possible(treasure_type, alignment)))
                else:
                    menu_options.append((treas_name, treasure_type, True, True))
            while len(menu_options) < row_count + 1:
                # заполняем пустыми вариантами для выравнивания меню
                menu_options += [(u"", 'blank', True, False)]
            if row_count < len(treasure_list):
                menu_options += [(u"На следующую страницу", 'inc', True, position + row_count < len(treasure_list))]
            else:
                menu_options += [(u"", 'blank', True, False)]
            menu_options += [(u"Отмена", 'return', True, True)]
            menu_choice = call_screen("dw_choice", menu_options)
            if menu_choice == 'dec':
                position -= row_count
            elif menu_choice == 'inc':
                position += row_count
            elif menu_choice == 'return':
                return None
        return menu_choice

    def craft_select_material(self, materials):
        """
        Функция для вывода меню выбора из списка
        :param materials: список материалов для выбора
        :return: выбранный вариант из списка либо None в случае отмены
        """
        from renpy.exports import call_screen
        menu_choice = None
        row_count = 10  # количество кнопок для отображения списка материалов
        position = 0  # начальное значение 
        while menu_choice not in materials:
            # цикл для выбора типа материала
            if row_count < len(materials):
                menu_options = [(u"На предыдущую страницу", 'dec', True, position > 0)]
            else:
                menu_options = [(u"", 'blank', True, False)]
            for i in xrange(position, min(position + row_count, len(materials))):
                material_type = materials[i]
                if material_type in metal_types.keys():
                    # получаем название материала на русском
                    option_name = u"Из %s" % metal_description_rus[material_type]['genitive']
                else:
                    option_name = u"Из %s" % material_description_rus[material_type]['genitive']
                menu_options.append((option_name, material_type, True, True))
            while len(menu_options) < row_count + 1:
                # заполняем пустыми вариантами для выравнивания меню
                menu_options += [(u"", 'blank', True, False)]
            if row_count < len(materials):
                menu_options += [(u"На следующую страницу", 'inc', True, position + row_count < len(materials))]
            else:
                menu_options += [(u"", 'blank', True, False)]
            menu_options += [(u"", 'blank', True, False)]
            menu_choice = call_screen("dw_choice", menu_options)
            if menu_choice == 'dec':
                position -= row_count
            elif menu_choice == 'inc':
                position += row_count
        return menu_choice

    def craft_select_gem(self, gem_size):
        """
        Функция для вывода меню выбора камня для инкрустации из всех доступных вариантов
        После выбора автоматически вставляет (или убирает) камень нужного размера
        :param gem_size: размер камня для инкрустации
        :return: камень для инкрустации
        """
        from renpy.exports import call_screen
        menu_choice = None
        row_count = 10  # количество кнопок для отображения списка материалов
        position = 0  # начальное значение
        gem_list = []
        for gem_type in self.gems:
            # добавляем камни требуемого размера в список
            gem_params = gem_type.split(';')
            if gem_params[1] == gem_size:
                if gem_size == 'small':
                    # изменение размера для хака описания
                    gem_params[1] = 'common'
                gem_list.append(Gem(*gem_params))
        while menu_choice is None or (menu_choice == 'inc') or (menu_choice == 'dec'):
            # цикл для выбора типа камня
            if row_count < len(gem_list):
                menu_options = [(u"На предыдущую страницу", 'dec', True, position > 0)]
            else:
                menu_options = [(u"", 'blank', True, False)]
            for i in xrange(position, min(position + row_count, len(gem_list))):
                menu_options.append((gem_list[i].description(custom=True).capitalize(), i, True, True))
            while len(menu_options) < row_count + 1:
                # заполняем пустыми вариантами для выравнивания меню
                menu_options += [(u"", 'blank', True, False)]
            if row_count < len(gem_list):
                menu_options += [(u"На следующую страницу", 'inc', True, position + row_count < len(gem_list))]
            else:
                menu_options += [(u"", 'blank', True, False)]
            menu_options += [(u"Без камня", 'clear', True, True)]
            menu_choice = call_screen("dw_choice", menu_options)
            if menu_choice == 'dec':
                position -= row_count
            elif menu_choice == 'inc':
                position += row_count
        if menu_choice == 'clear':
            return None
        else:
            return gem_list[menu_choice]

    def craft(self, is_crafting=False, quality=['random'], alignment=['random'], base_cost=0, price_multiplier=100):
        """
        Функция для вывода меню покупки/создания вещи
        :param is_crafting: создаётся из материалов дракона (True) или покупается (False)
        :param quality: список для выбора возможного качества создаваемой вещи, 
            может быть rough, common, skillfully, mastery, 
            либо random для случайного выбора из этих вариантов с весовыми коэффициентами
        :param alignment: список для выбора возможного стиля декорации создаваемой вещи, 
            может быть human, knight, cleric, elf, dwarf, merman,
            либо random для случайного выбора из этих вариантов,
            либо None, если сделать орнамент невозможно
        :param base_cost: базовая стоимость работы (для ремесла)
        :param price_multiplier: увеличение цены (для покупки, в процентах)
        :return: созданная вещь либо None в случае отмены
        """
        from renpy.exports import call_screen
        if 'random' in alignment or not alignment:
            alignment = image_types.keys()
        alignment = random.choice(alignment)
        treasure_type = self.craft_select_item(is_crafting, alignment)
        if treasure_type is None:
            return None
        # случайный выбор стиля вещи из списка
        item = Treasure(treasure_type, alignment)
        quality_options = {
            'rough': u"с грубым исполнением",
            'common': u"с обычным исполнением",
            'skillfully': u"с искусным исполнением",
            'mastery': u"с мастерским исполнением",
            'random': u"со случайным исполнением"
        }
        item.quality = quality[0]
        # первоначальный выбор качества - первый в списке
        materials = self.available_materials(treasure_type)
        item.material = self.craft_select_material(materials)
        item.spangled = None
        item.inlaid = None
        item.huge = None
        item.decoration = None
        item.decoration_image = None
        menu_choice = None
        while menu_choice is not 'create':
            menu_options = [(u"Отменить", 'return', True, True)]
            treasure_name = treasure_description_rus[treasure_type]['nominative'].capitalize()
            menu_options += [(treasure_name, treasure_type, True, False)]
            # тип вещи - не может быть изменен
            menu_options += [(quality_options[item.quality], 'quality', True, len(quality) > 1)]
            # качество вещи
            if item.material in metal_types.keys():
                material_name = u"из %s" % metal_description_rus[item.material]['genitive']
            else:
                material_name = u"из %s" % material_description_rus[item.material]['genitive']
            menu_options += [(material_name, 'material', True, True)]
            # материал вещи
            if treasure_types[treasure_type][5]:
                # проверка на возможность инкрустации
                if item.spangled:
                    spangled_description = decoration_description_rus['spangled'][treasure_types[treasure_type][1]]
                    spangled_description += u" " + item.spangled.description(True, 'ablative', 'they')
                    menu_options += [(spangled_description, 'spangled', True, True)]
                else:
                    menu_options += [(u"без блёсток", 'spangled', True, not is_crafting or self.check_gem_size('small'))]
                if item.inlaid:
                    inlaid_description = decoration_description_rus['inlaid'][treasure_types[treasure_type][1]]
                    inlaid_description += u" " + item.inlaid.description(True, 'ablative', 'they')
                    menu_options += [(inlaid_description, 'inlaid', True, True)]
                else:
                    menu_options += [(u"без инкрустации", 'inlaid', True, not is_crafting or self.check_gem_size('common'))]
                if item.huge:
                    huge_description = u"c " + item.huge.description(True, 'ablative')
                    menu_options += [(huge_description, 'huge', True, True)]
                else:
                    menu_options += [(u"без крупного камня", 'huge', True, not is_crafting or self.check_gem_size('large'))]
            if alignment and item.decorable:
                if item.decoration:
                    decor_image = decoration_description_rus['image'][image_description_rus[item.decoration_image]['gender']]
                    decor_image += u" " + image_description_rus[item.decoration_image]['nominative']
                else:
                    decor_image = u"без изображения"
                menu_options += [(decor_image, 'decoration', True, True)]
            if is_crafting:
                if item.craft_cost(base_cost, price_multiplier) > 0:
                    price_msg = number_conjugation_rus(item.craft_cost(base_cost, price_multiplier), u"фартинг")
                    craft_msg = u"Смастерить за %s (есть %s)" % (price_msg, self.money)
                else:
                    craft_msg = u"Смастерить"
            else:
                price_msg = number_conjugation_rus(item.craft_cost(base_cost, price_multiplier), u"фартинг")
                craft_msg = u"Купить за %s (есть %s)" % (price_msg, self.money)
            menu_options += [(craft_msg, 'create', True, item.craft_cost(base_cost, price_multiplier) <= self.money)]
            menu_choice = call_screen("dw_choice", menu_options)
            # показ меню
            if menu_choice == 'return':
                return None
            elif menu_choice == 'quality':
                menu_options = []
                for quality_type in quality:
                    menu_options += [(quality_options[quality_type], quality_type, True, True)]
                item.quality = call_screen("dw_choice", menu_options)
            elif menu_choice == 'material':
                item.material = self.craft_select_material(materials)
            elif menu_choice == 'spangled':
                item.spangled = self.craft_select_gem('small')
            elif menu_choice == 'inlaid':
                item.inlaid = self.craft_select_gem('common')
            elif menu_choice == 'huge':
                item.huge = self.craft_select_gem('large')
            elif menu_choice == 'decoration':
                menu_options = [(u"Украсить изображением", 'yes', True, True)]
                menu_options += [(u"Без изображения", 'no', True, True)]
                menu_choice = call_screen("dw_choice", menu_options)
                if menu_choice == 'yes':
                    item.decoration_image = random.choice(image_types[item.alignment])
                    if item.material in material_types:
                        item.decoration = 'carving'
                    else:
                        item.decoration = weighted_select(Treasure.decorate_types)
                else:
                    item.decoration = None
                    item.decoration_image = None
        if item.quality =='random':
            # случайный выбор качества вещи
            quality_list = (('rough', 25), ('common', 50), ('skillfully', 20), ('mastery', 10),)
            item.quality = weighted_random(quality_list)
        self.money -= item.craft_cost(base_cost, price_multiplier)
        if is_crafting:
            # если делается из материалов дракона - убираем материалы из сокровищницы
            if item.material in material_types:
                material = None
                materials_size = sorted(Material.size_dict.keys(), key=lambda mat_size: Material.size_dict[mat_size][1]) 
                # сортировка по размеру, т.к. дракон жадный - зачем отдавать большой кусок, если можно сделать из любого?
                for material_size in materials_size:
                    # ищем из какого бы куска изготовить вещь
                    if not material:
                        material = self.take_material(item.material + u";" + material_size)
            else:
                self.take_ingot(item.material)
            if item.spangled:
                self.take_gem(item.spangled.g_type + u';small;' + item.spangled.cut)
            if item.inlaid:
                self.take_gem(item.inlaid.g_type + u';common;' + item.inlaid.cut)
            if item.huge:
                self.take_gem(item.huge.g_type + u';large;' + item.huge.cut)
            if item.image:
                item.decoration_image = random.choice(image_types[item.alignment])
        return item