#!/usr/bin/env python
# coding=utf-8
import random
import data
import renpy.store as store
import renpy.exports as renpy

"""Словарь для драгоценных камней, ключи - названия камней, значения - кортежи вида(шанс появления, ценность)"""
gem_types = {}
gem_types["amber"] = (5,3)
gem_types["crystall"] = (5,3)
gem_types["beryll"] = (4,5)
gem_types["tigereye"] = (4,5)
gem_types["granate"] = (3,10)
gem_types["turmaline"] = (3,10)
gem_types["aqua"] = (3,10)
gem_types["pearl"] = (3,10)
gem_types["black_pearl"] = (3,10)
gem_types["elven_beryll"] = (2,25)
gem_types["topaz"] = (2,25)
gem_types["saphire"] = (2,25)
gem_types["ruby"] = (2,25)
gem_types["emerald"] = (2,25)
gem_types["goodruby"] = (1,100)
gem_types["goodemerald"] = (1,100)
gem_types["star"] = (1,100)
gem_types["diamond"] = (1,100)
gem_types["black_diamond"] = (1,100)
gem_types["rose_diamond"] = (1,100)
"""словарь для типов материалов, ключи - названия материалов, значения - (шанс, ценность)"""
material_types = {}
material_types["jasper"] = (5,1)
material_types["turquoise"] = (5,1)
material_types["jade"] = (5,1)
material_types["malachite"] = (5,1)
material_types["corall"] = (4,2)
material_types["ivory"] = (4,2)
material_types["agate"] = (3,5)
material_types["shell"] = (3,5)
material_types["horn"] = (1,10)
"""словарь для описания типов материалов, ключи - названия материалов, значения - словарь для различных падежей русского названия материала"""
material_description_rus = {}
material_description_rus["jasper"] = {'nominative': u'яшма', 'genitive': u'яшмы'}
material_description_rus["turquoise"] = {'nominative': u'бирюза', 'genitive': u'бирюзы'}
material_description_rus["jade"] = {'nominative': u'нефрит', 'genitive': u'нефрита'}
material_description_rus["malachite"] = {'nominative': u'малахит', 'genitive': u'малахита'}
material_description_rus["corall"] = {'nominative': u'коралл', 'genitive': u'коралла'}
material_description_rus["ivory"] = {'nominative': u'слоновая кость', 'genitive': u'слоновой кости'}
material_description_rus["agate"] = {'nominative': u'агат', 'genitive': u'агата'}
material_description_rus["shell"] = {'nominative': u'перламутр', 'genitive': u'перламутра'}
material_description_rus["horn"] = {'nominative': u'драконий рог', 'genitive': u'драконьего рога'}
"""словарь для описания размеров материалов, ключи - названия размера материалов, значения - словарь для русского прилагательного, соответствующего размеру"""
material_size_description_rus = {} 
material_size_description_rus['small'] = {'he' : {'nominative': u"мелкий ", 'ablative': u"мелким "}, 
                                          'she': {'nominative': u"мелкая ", 'ablative': u"мелкой "},
                                          'they': {'nominative': u"мелкие ", 'genitive': u"мелких ", 'ablative': u"мелкими "}}
material_size_description_rus['common'] = {'he' : {'nominative': u"", 'ablative': u""}, # этот размер не отображается
                                          'she' : {'nominative': u"", 'ablative': u""},
                                          'they' : {'nominative': u"",'genitive': u"", 'ablative': u""}}
material_size_description_rus['large'] = {'he' : {'nominative': u"крупный ", 'ablative': u"крупным "},
                                         'she' : {'nominative': u"крупная ", 'ablative': u"крупной "},
                                         'they' : {'nominative': u"крупные ", 'genitive': u"крупных ",'ablative': u"крупными "},}
material_size_description_rus['exceptional'] = {'he' : {'nominative': u"огромный ", 'ablative': u"огромным "},
                                               'she' : {'nominative': u"огромная ", 'ablative': u"огромной "},
                                               'they' : {'nominative': u"огромные ", 'genitive': u"огромных ", 'ablative': u"огромными "}}
"""словарь для описания степени обработки драгоценных камней, ключи - названия степени обработки, значения - словарь для соответствующего русского прилагательного"""
gem_cut_description_rus = {} 
gem_cut_description_rus[' '] = {'he': {'nominative': u'', 'ablative': u''}, # эта полировка не отображается
                                'she': {'nominative': u'', 'ablative': u''},
                                'they': {'nominative': u'', 'genitive': u'', 'ablative': u''}} 
gem_cut_description_rus['polished'] = {'he': {'nominative': u'необработанный ', 'ablative': u''}, # 'ablative' не отображается, чтобы не портить описание вещи
                                       'they': {'nominative': u'необработанные ', 'genitive': u"необработанных ", 'ablative': u''}} 
gem_cut_description_rus['rough'] = {'he': {'nominative': u'полированный ', 'ablative': u'полированным '}, 
                                    'they': {'nominative': u'полированные ', 'genitive': u'полированных ', 'ablative': u'полированными '}}
gem_cut_description_rus['faceted'] = {'he': {'nominative': u'ограненный ', 'ablative': u'ограненным '},
                                      'they': {'nominative': u'ограненные ', 'genitive': u'ограненных ', 'ablative': u'ограненными '}}
"""Словарь для драгоценных камней, ключ - тип драгоценного камня, значение - словарь с русским названием драгоценного камня в разных падежах"""
gem_description_rus = {}
gem_description_rus["amber"] = {'he': {'nominative': u"янтарь", 'genitive': u"янтаря", 'ablative': u"янтарём"}, 
                                'they': {'genitive': u"янтарей", 'ablative': u"янтарями"}}
gem_description_rus["crystall"] = {'he': {'nominative': u'горный хрусталь', 'genitive': u"горных хрусталя", 'ablative': u'горным хрусталём'},
                                   'they': {'genitive': u"горных хрусталей", 'ablative': u'горными хрусталями'}}
gem_description_rus["beryll"] = {'he': {'nominative': u'берилл', 'genitive': u"берилла",  'ablative': u'бериллом'},
                                 'they': {'genitive': u"бериллов",  'ablative': u'бериллами'}}
gem_description_rus["tigereye"] = {'he': {'nominative': u'тигровый глаз', 'genitive': u"тигровых глаза", 'ablative': u'тигровым глазом'},
                                   'they': {'genitive': u"тигровых глазов", 'ablative': u'тигровыми глазами'}}
gem_description_rus["granate"] = {'he': {'nominative': u'гранат', 'genitive': u"граната", 'ablative': u'гранатом'},
                                   'they': {'genitive': u"гранатов", 'ablative': u'гранатами'}}
gem_description_rus["turmaline"] = {'he': {'nominative': u'турмалин', 'genitive': u"турмалина", 'ablative': u'турмалином'},
                                    'they': {'genitive': u"турмалинов", 'ablative': u'турмалинами'}}
gem_description_rus["aqua"] = {'he': {'nominative': u'аквамарин', 'genitive': u"аквамарина", 'ablative': u'аквамарином'},
                               'they': {'genitive': u"аквамаринов", 'ablative': u'аквамаринами'}}
gem_description_rus["pearl"] = {'he': {'nominative': u'жемчуг', 'genitive': u"жемчуга", 'ablative': u'жемчугом'},
                               'she': {'nominative': u'жемчужина', 'genitive': u"жемчужины", 'ablative': u'жемчужиной'}, 
                               'they': {'genitive': u"жемчужин", 'ablative': u'жемчугами'}}
gem_description_rus["black_pearl"] = {'he': {'nominative': u'чёрный жемчуг', 'genitive': u'чёрных жемчуга', 'ablative': u'чёрным жемчугом'},
                                      'she': {'nominative': u'чёрная жемчужина', 'genitive': u'чёрных жемчужины', 'ablative': u'чёрной жемчужиной'}, 
                                      'they': {'genitive': u"чёрных жемчужин", 'ablative': u'чёрными жемчугами'}}
gem_description_rus["elven_beryll"] = {'he': {'nominative': u'эльфийский берилл', 'genitive': u"эльфийских берилла",  'ablative': u'эльфийским бериллом'},
                                       'they': {'genitive': u"эльфийских бериллов",  'ablative': u'эльфийскими бериллами'}}
gem_description_rus["topaz"] = {'he': {'nominative': u'топаз', 'genitive': u"топаза",  'ablative': u'топазом'},
                                'they': {'genitive': u"топазов",  'ablative': u'топазами'}}
gem_description_rus["saphire"] = {'he': {'nominative': u'сапфир', 'genitive': u"сапфира", 'ablative': u'сапфиром'},
                                  'they': {'genitive': u"сапфиров", 'ablative': u'сапфирами'}}
gem_description_rus["ruby"] = {'he': {'nominative': u'рубин', 'genitive': u"рубина", 'ablative': u'рубином'}, 
                               'they': {'genitive': u"рубинов", 'ablative': u'рубинами'}}
gem_description_rus["emerald"] = {'he': {'nominative': u'изумруд', 'genitive': u"изумруда", 'ablative': u'изумрудом'},
                                  'they': {'genitive': u"изумрудов", 'ablative': u'изумрудами'}}
gem_description_rus["goodruby"] = {'he': {'nominative': u'яхонт', 'genitive': u"яхонта", 'ablative': u'яхонтом'},
                                   'they': {'genitive': u"яхонтов", 'ablative': u'яхонтами'}}
gem_description_rus["goodemerald"] = {'he': {'nominative': u'смарагд', 'genitive': u"смарагда", 'ablative': u'смарагдом'},
                                      'they': {'genitive': u"смарагдов", 'ablative': u'смарагдами'}}
gem_description_rus["star"] = {'he': {'nominative': u'звёздный сапфир', 'genitive': u"звёздных сапфира", 'ablative': u'звёздным сапфиром'},
                               'they': {'genitive': u"звёздных сапфиров", 'ablative': u'звёздными сапфирами'}}
gem_description_rus["diamond"] = {'he': {'nominative': u'алмаз', 'genitive': u"алмаза", 'ablative': u'алмазом'},
                                  'they': {'genitive': u"алмазов", 'ablative': u'алмазами'}}
gem_description_rus["black_diamond"] = {'he': {'nominative': u'чёрный алмаз', 'genitive': u"чёрных алмаза", 'ablative': u'чёрным алмазом'},
                                        'they': {'genitive': u"чёрных алмазов", 'ablative': u'чёрными алмазами'}}
gem_description_rus["rose_diamond"] = {'he': {'nominative': u'розовый алмаз', 'genitive': u"розовых алмаза", 'ablative': u'розовым алмазом'}, 
                                       'they': {'genitive': u"розовых алмазов", 'ablative': u'розовыми алмазами'}}
"""словарь для типов металлов, ключ - металл, значение - ценность"""
metal_types = {"silver": 1, "gold":10, "mithril":50, "adamantine":50}
"""словарь для типов сокровищ, ключ - тип сокровища,
значение - (базовая цена, пол, можно ли сделать из метала(булевое), можно ли
            сделать из поделочных материалов(булевое), является ли изображением(булевое),
            можно ли инкрустировать(булевое), возможность украшения(булевое))"""
treasure_types = {}#допилить типы сокровищ
treasure_types["dish"] = (5,"it", True, False, False, False, True)
treasure_types["goblet"] = (4, "he", True, False, False, True, True)
treasure_types["cup"] = (3, "she", False, True, False, False, True)
treasure_types["casket"] = (5, "she", True, True, False, True, True)
treasure_types["statue"] = (10, "she", True, True, True, False, False)
treasure_types["tabernacle"] = (5, "she", True, True, False, True, True)
treasure_types["icon"] = (10, "she", True, False, True, False, False)
treasure_types["tome"] = (10, "he", True, False, False, True, True)
treasure_types["comb"] = (3, "he", True, True, False, False, True)
treasure_types["phallos"] = (3, "he", True, True, False, False, True)
treasure_types["mirror"] = (4, "it", True, True, False, True, True)
treasure_types["band"] = (3, "he", True, False, False, False, False)
treasure_types["diadem"] = (3, "she", True, False, False, True, False)
treasure_types["tiara"] = (4, "she", True, False, False, True, False)
treasure_types["earring"] = (1, "she", True, False, False, True, False)
treasure_types["necklace"] = (4, "it", True, False, False, True, False)
treasure_types["pendant"] = (2, "he", True, False, False, False, True)
treasure_types["ring"] = (1, "it", True, True, False, False, False)
treasure_types["broch"] = (2, "she", True, False, False, True, False)
treasure_types["gemring"] = (2, "he", True, True, False, True, False)
treasure_types["seal"] = (3, "he", True, True, False, False, True)
treasure_types["armbrace"] = (3, "he", True, True, False, True, True)
treasure_types["legbrace"] = (3, "he", True, True, False, True, True)
treasure_types["crown"] = (5, "she", True, False, False, True, False)
treasure_types["scepter"] = (10, "he", True, False, False, True, False)
treasure_types["chain"] = (3, "she", True, False, False, False, False)
treasure_types["fibula"] = (2, "she", True, False, False, False, True)
"""словарь для описания типов драгоценностей, ключ - тип драгоценностей, значение - словарь с русским названием драгоценности в разных падежах"""
treasure_description_rus = {}#допилить типы сокровищ
treasure_description_rus["dish"] = {'nominative': u'блюдо', 'ablative': u'блюде'}
treasure_description_rus["goblet"] = {'nominative': u'кубок', 'ablative': u'кубке'}
treasure_description_rus["cup"] = {'nominative': u'чаша', 'ablative': u'чаше'}
treasure_description_rus["casket"] = {'nominative': u'шкатулка', 'ablative': u'шкатулке'}
treasure_description_rus["statue"] = {'nominative': u'статуэтка', 'ablative': u'статуэтке'}
treasure_description_rus["tabernacle"] = {'nominative': u'дарохранительница', 'ablative': u'дарохранительнице'}
treasure_description_rus["icon"] = {'nominative': u'икона', 'ablative': u'иконе'}
treasure_description_rus["tome"] = {'nominative': u'фолиант', 'ablative': u'фолианте'}
treasure_description_rus["comb"] = {'nominative': u'гребень', 'ablative': u'гребене'}
treasure_description_rus["phallos"] = {'nominative': u'фаллос', 'ablative': u'фаллосе'}
treasure_description_rus["mirror"] = {'nominative': u'зеркальце', 'ablative': u'зеркальце'}
treasure_description_rus["band"] = {'nominative': u'обруч', 'ablative': u'обруче'}
treasure_description_rus["diadem"] = {'nominative': u'диадема', 'ablative': u'диадеме'}
treasure_description_rus["tiara"] = {'nominative': u'тиара', 'ablative': u'тиаре'}
treasure_description_rus["earring"] = {'nominative': u'серьга', 'ablative': u'серьге'}
treasure_description_rus["necklace"] = {'nominative': u'ожерелье', 'ablative': u'ожерелье'}
treasure_description_rus["pendant"] = {'nominative': u'кулон', 'ablative': u'кулоне'}
treasure_description_rus["ring"] = {'nominative': u'колечко', 'ablative': u'колечке'}
treasure_description_rus["broch"] = {'nominative': u'брошь', 'ablative': u'броше'}
treasure_description_rus["gemring"] = {'nominative': u'перстень', 'ablative': u'перстне'}
treasure_description_rus["seal"] = {'nominative': u'перстень-печатка', 'ablative': u'перстне-печатке'}
treasure_description_rus["armbrace"] = {'nominative': u'браслет', 'ablative': u'браслете'}
treasure_description_rus["legbrace"] = {'nominative': u'ножной браслет', 'ablative': u'браслете'}
treasure_description_rus["crown"] = {'nominative': u'корона', 'ablative': u'короне'}
treasure_description_rus["scepter"] = {'nominative': u'скипетр', 'ablative': u'скипетре'}
treasure_description_rus["chain"] = {'nominative': u'цепь', 'ablative': u'цепи'}
treasure_description_rus["fibula"] = {'nominative': u'фибула', 'ablative': u'фибуле'}
"""словарь для описания типов металлов, ключ - тип металла, значение - русское названия драгоценности в разных родах"""
metal_description_rus = {}
metal_description_rus['silver'] = {'he': u"серебряный", 'she': u"серебряная", 'it': u"серебряное", 'prepositional': u"серебряном", 'they': u"серебряных"}
metal_description_rus['gold'] = {'he': u"золотой", 'she': u"золотая", 'it': u"золотое", 'prepositional': u"золотом", 'they': u"золотых"}
metal_description_rus['mithril'] = {'he': u"мифрильный", 'she': u"мифрильная", 'it': u"мифрильное", 'prepositional': u"мифрильном", 'they': u"мифрильных"}
metal_description_rus['adamantine'] = {'he': u"адамантовый", 'she': u"адамантовая", 'it': u"адамантовое", 'prepositional': u"адамантовом", 'they': u"адамантовых"}
"""словарь для изображений, ключ - тип культуры, значение - кортеж из вариантов изображений"""
image_types = {}
image_types['human'] = ('abstract_ornament', 'concentric_circles', 'round_dance', 'fire-breathing_dragon', 'flying_dragon',
                        'wingless_dragon', 'snake_with_a_crown',  'winged_serpent', 'kokatriks', 'basilisk', 
                        'dragon_entwine_naked_girl', 'battle_dragon_with_knight', 'dancing_girls', 'bathing_girl',
                        'children_playing', 'rider_with_bow', 'horseman_with_spear_and_shield', 'dead_knight_with_sword')
image_types['knight'] = ('proud_motto', 'battle_scene', 'coat_of_arms_with_rearing_unicorn', 'coat_of_arms_with_head_of_boar', 
                        'coat_of_arms_with_three_lilies', 'coat_of_arms_with_roaring_lion', 'coat_of_arms_with_proud_eagle',
                        'coat_of_arms_with_procession_kamelopardom', 'coat_of_arms_with_crossed_swords', 'coat_of_arms_with_shield_and_sword')
image_types['cleric'] = ('saying_of_holy_scriptures', 'scene_of_holy_scriptures', 'saint_with_halo', 'angel_with_flaming_sword',
                        'angel_winning_serpent', 'raising_hands_angel', 'six-winged_seraph', 'holy_maiden_and_child',
                        'holy_maiden_stretches_hands', 'weeping_maiden')
image_types['elf'] =    ('floral_ornament', 'elegant_runes', 'running_deer', 'bear_with_raised_legs', 'wolf_hunting', 'sneaking_manul',
                        'two_songbirds',  'moon_and_stars',  'branched_oak', 'blooming_vine', 'spreading_maple',  'weeping_willow', 
                        'dancing_nymphs', 'nymph_with_cup', 'nymph_collecting_fruits', 'nymph_playing_harp', 'winged_maiden', 
                        'satyr_playing_flute', 'forest_guard_bow')
image_types['dwarf'] =  ('geometric_pattern', 'runic_ligature',  'hammer_and_crown', 'dwarfs_holding_over_his_head_anvil', 
                        'armed_dwarfs_tramples_goblin', 'crossed_axes', 'entwined_rings', 'helmet_with_horns',  
                        'krotocherv', 'dwarfs', 'urist_makdvarf', 'dragon_smaug')
image_types['merman'] = ('wavy_pattern', 'frolicking_fish', 'seahorse', 'newt_lifting_trident', 'triton_and_siren_holding_hands', 
                        'mermaid_brushing_hair', 'playing_mermaid', 'mermaid_playing_with_pearl', 'awesome_sea_serpent', 
                        'flying_seagull', 'wriggling_octopus', 'kraken_drowning_sea_vessel', 'sailing_ship')
"""словарь для описания изображений, ключ - вариант изображения, значение - словарь из рода изображения и описания изображения в различных падежах"""
image_description_rus = {}
image_description_rus['abstract_ornament'] = {'gender': 'he', 'nominative': u'абстрактный орнамент', 'accusative': u'абстрактный орнамент'}
image_description_rus['concentric_circles'] = {'gender': 'they', 'nominative': u'концентрические круги', 'accusative': u'концентрические круги'}
image_description_rus['round_dance'] = {'gender': 'he', 'nominative': u'хоровод', 'accusative': u'хоровод'}
image_description_rus['fire-breathing_dragon'] = {'gender': 'he', 'nominative': u'огнедышащий дракон', 'accusative': u'огнедышащего дракона'}
image_description_rus['flying_dragon'] = {'gender': 'he', 'nominative': u'летящий дракон', 'accusative': u'летящего дракона'}
image_description_rus['wingless_dragon'] = {'gender': 'he', 'nominative': u'бескрылый дракон', 'accusative': u'бескрылого дракона'}
image_description_rus['snake_with_a_crown'] = {'gender': 'she', 'nominative': u'змея с короной на голове', 'accusative': u'змею с короной на голове'}
image_description_rus['winged_serpent'] = {'gender': 'she', 'nominative': u'крылатая змея', 'accusative': u'крылатую змею'}
image_description_rus['kokatriks'] = {'gender': 'he', 'nominative': u'кокатрикс', 'accusative': u'кокатрикса'}
image_description_rus['basilisk'] = {'gender': 'he', 'nominative': u'василиск', 'accusative': u'василиска'}
image_description_rus['dragon_entwine_naked_girl'] = {'gender': 'he', 'nominative': u'дракон, обвивающий обнаженную девушку', 'accusative': u'дракона, обвивающий обнаженную девушку'}
image_description_rus['battle_dragon_with_knight'] = {'gender': 'he', 'nominative': u'сражение дракона с рыцарем', 'accusative': u'сражение дракона с рыцарем'}
image_description_rus['dancing_girls'] = {'gender': 'they', 'nominative': u'танцующие девушки', 'accusative': u'танцующих девушек'}
image_description_rus['bathing_girl'] = {'gender': 'she', 'nominative': u'купающаяся девушка', 'accusative': u'купающуюся девушку'}
image_description_rus['children_playing'] = {'gender': 'they', 'nominative': u'играющие дети', 'accusative': u'играющих детей'}
image_description_rus['rider_with_bow'] = {'gender': 'he', 'nominative': u'всадник с луком', 'accusative': u'всадника с луком'}
image_description_rus['horseman_with_spear_and_shield'] = {'gender': 'he', 'nominative': u'всадник с копьём и щитом', 'accusative': u'всадника с копьём и щитом'}
image_description_rus['dead_knight_with_sword'] = {'gender': 'he', 'nominative': u'мертвый рыцарь с мечом, покоящимся на груди', 'accusative': u'мертвого рыцаря с мечом, покоящимся на груди'}
image_description_rus['proud_motto'] = {'gender': 'he', 'nominative': u'гордый девиз', 'accusative': u'гордый девиз'}
image_description_rus['battle_scene'] = {'gender': 'she', 'nominative': u'сцена сражения', 'accusative': u'сцену сражения'}
image_description_rus['coat_of_arms_with_rearing_unicorn'] = {'gender': 'he', 'nominative': u'герб с единорогом, вставшим на дыбы', 'accusative': u'герб с единорогом, вставшим на дыбы'}
image_description_rus['coat_of_arms_with_head_of_boar'] = {'gender': 'he', 'nominative': u'герб с головой вепря', 'accusative': u'герб с головой вепря'}
image_description_rus['coat_of_arms_with_three_lilies'] = {'gender': 'he', 'nominative': u'герб с тремя лилиями', 'accusative': u'герб с тремя лилиями'}
image_description_rus['coat_of_arms_with_roaring_lion'] = {'gender': 'he', 'nominative': u'герб с рыкающим львом', 'accusative': u'герб с рыкающим львом'}
image_description_rus['coat_of_arms_with_proud_eagle'] = {'gender': 'he', 'nominative': u'герб с гордым орлом', 'accusative': u'герб с гордым орлом'}
image_description_rus['coat_of_arms_with_procession_kamelopardom'] = {'gender': 'he', 'nominative': u'герб с шествующим камелопардом', 'accusative': u'герб с шествующим камелопардом'}
image_description_rus['coat_of_arms_with_crossed_swords'] = {'gender': 'he', 'nominative': u'герб со скрещёнными мечами', 'accusative': u'герб со скрещёнными мечами'}
image_description_rus['coat_of_arms_with_shield_and_sword'] = {'gender': 'he', 'nominative': u'герб со щитом и мечом', 'accusative': u'герб со щитом и мечом'}
image_description_rus['saying_of_holy_scriptures'] = {'gender': 'it', 'nominative': u'изречение из святого писания', 'accusative': u'изречение из святого писания'}
image_description_rus['scene_of_holy_scriptures'] = {'gender': 'she', 'nominative': u'сцена из святого писания', 'accusative': u'сцену из святого писания'}
image_description_rus['saint_with_halo'] = {'gender': 'he', 'nominative': u'святой с нимбом', 'accusative': u'святого с нимбом'}
image_description_rus['angel_with_flaming_sword'] = {'gender': 'he', 'nominative': u'ангел с огненным мечом', 'accusative': u'ангела с огненным мечом'}
image_description_rus['Angel_winning_serpent'] = {'gender': 'he', 'nominative': u'ангел, побеждающий змия', 'accusative': u'ангела, побеждающего змия'}
image_description_rus['raising_hands_angel'] = {'gender': 'he', 'nominative': u'воздевший руки ангел', 'accusative': u'воздевшего руки ангела'}
image_description_rus['six-winged_seraph'] = {'gender': 'he', 'nominative': u'шестикрылый серафим', 'accusative': u'шестикрылого серафима'}
image_description_rus['holy_maiden_and_child'] = {'gender': 'she', 'nominative': u'святая дева с младенцем', 'accusative': u'святую деву с младенцем'}
image_description_rus['holy_maiden_stretches_hands'] = {'gender': 'she', 'nominative': u'святая дева, простирающая руки', 'accusative': u'святую деву, простирающую руки'}
image_description_rus['weeping_maiden'] = {'gender': 'she', 'nominative': u'плачущая дева', 'accusative': u'плачущую деву'}
image_description_rus['floral_ornament'] = {'gender': 'he', 'nominative': u'растительный орнамент', 'accusative': u'растительный орнамент'}
image_description_rus['elegant_runes'] = {'gender': 'they', 'nominative': u'изящные руны', 'accusative': u'изящные руны'}
image_description_rus['running_deer'] = {'gender': 'he', 'nominative': u'бегущий олень', 'accusative': u'бегущего оленя'}
image_description_rus['bear_with_raised_legs'] = {'gender': 'he', 'nominative': u'медведь с поднятыми вверх лапами', 'accusative': u'медведя с поднятыми вверх лапами'}
image_description_rus['wolf_hunting'] = {'gender': 'he', 'nominative': u'охотящийся волк', 'accusative': u'охотящегося волка'}
image_description_rus['sneaking_manul'] = {'gender': 'he', 'nominative': u'крадущийся манул', 'accusative': u'крадущегося манула'}
image_description_rus['two_songbirds'] = {'gender': 'they', 'nominative': u'две певчие птички', 'accusative': u'двух певчих птичек'}
image_description_rus['moon_and_stars'] = {'gender': 'they', 'nominative': u'луна и звёзды', 'accusative': u'луну и звёзды'}
image_description_rus['branched_oak'] = {'gender': 'he', 'nominative': u'ветвистый дуб', 'accusative': u'ветвистый дуб'}
image_description_rus['blooming_vine'] = {'gender': 'she', 'nominative': u'цветущая лоза', 'accusative': u'цветущую лозу'}
image_description_rus['spreading_maple'] = {'gender': 'he', 'nominative': u'раскидистый клён', 'accusative': u'раскидистый клён'}
image_description_rus['weeping_willow'] = {'gender': 'she', 'nominative': u'плакучая ива', 'accusative': u'плакучую иву'}
image_description_rus['dancing_nymphs'] = {'gender': 'they', 'nominative': u'танцующие нимфы', 'accusative': u'танцующих нимф'}
image_description_rus['nymph_with_cup'] = {'gender': 'she', 'nominative': u'нимфа с кубком', 'accusative': u'нимфу с кубком'}
image_description_rus['nymph_collecting_fruits'] = {'gender': 'she', 'nominative': u'нимфа, собирающая плоды', 'accusative': u'нимфу, собирающую плоды'}
image_description_rus['nymph_playing_harp'] = {'gender': 'she', 'nominative': u'нимфа, играющая на арфе', 'accusative': u'нимфу, играющую на арфе'}
image_description_rus['winged_maiden'] = {'gender': 'she', 'nominative': u'крылатая дева', 'accusative': u'крылатую деву'}
image_description_rus['satyr_playing_flute'] = {'gender': 'he', 'nominative': u'сатир, играющий на дудочке', 'accusative': u'сатира, играющего на дудочке'}
image_description_rus['forest_guard_bow'] = {'gender': 'he', 'nominative': u'лесной страж, стреляющий из лука', 'accusative': u'лесного стража, стреляющего из лука'}
image_description_rus['geometric_pattern'] = {'gender': 'he', 'nominative': u'геометрический орнамент', 'accusative': u'геометрический орнамент'}
image_description_rus['runic_ligature'] = {'gender': 'she', 'nominative': u'руническая вязь', 'accusative': u'руническую вязь'}
image_description_rus['hammer_and_crown'] = {'gender': 'they', 'nominative': u'молот и корона', 'accusative': u'молот и корону'}
image_description_rus['dwarfs_holding_over_his_head_anvil'] = {'gender': 'he', 'nominative': u'цверг, держащий над головой наковальню', 'accusative': u'цверга, держащего над головой наковальню'}
image_description_rus['armed_dwarfs_tramples_goblin'] = {'gender': 'he', 'nominative': u'вооруженный цверг попирающий ногами гоблина', 'accusative': u'вооруженного цверга, попирающего ногами гоблина'}
image_description_rus['crossed_axes'] = {'gender': 'they', 'nominative': u'скрещённые топоры', 'accusative': u'скрещённые топоры'}
image_description_rus['entwined_rings'] = {'gender': 'they', 'nominative': u'переплетённые кольца', 'accusative': u'переплетённые кольца'}
image_description_rus['helmet_with_horns'] = {'gender': 'he', 'nominative': u'шлем с рогами', 'accusative': u'шлем с рогами'}
image_description_rus['krotocherv'] = {'gender': 'he', 'nominative': u'кроточервь', 'accusative': u'кроточервя'}
image_description_rus['dwarfs'] = {'gender': 'they', 'nominative': u'цверги. Цверги работают.', 'accusative': u'цвергов. Цверги работают.'}
image_description_rus['urist_makdvarf'] = {'gender': 'he', 
'nominative': u'Урист МакДварф. Урист МакДварф ест мастерски сделанный ячий сыр. Изображение посвящено поеданию мастерски сделанного ячьего сыра цвергом Уристом МакДварфом ранней весной 1076 года.', 
'accusative': u'Уриста МакДварфа. Урист МакДварф ест мастерски сделанный ячий сыр. Изображение посвящено поеданию мастерски сделанного ячьего сыра цвергом Уристом МакДварфом ранней весной 1076 года.'}
image_description_rus['dragon_smaug'] = {'gender': 'they', 
'nominative': u'Дракон Смауг и цверг Торин. Торин закрывается руками. Смауг стоит в угрожающей позе. Изображение посвящено убийству короля-под-горой в Эреборе поздним летом 2770 года.', 
'accusative': u'Дракона Смауга и цверга Торина. Торин закрывается руками. Смауг стоит в угрожающей позе. Изображение посвящено убийству короля-под-горой в Эреборе поздним летом 2770 года.'}
image_description_rus['wavy_pattern'] = {'gender': 'he', 'nominative': u'волнистый орнамент', 'accusative': u'волнистый орнамент'}
image_description_rus['frolicking_fish'] = {'gender': 'they', 'nominative': u'резвящиеся рыбки', 'accusative': u'резвящихся рыбок'}
image_description_rus['seahorse'] = {'gender': 'he', 'nominative': u'морской конёк', 'accusative': u'морского конька'}
image_description_rus['newt_lifting_trident'] = {'gender': 'he', 'nominative': u'тритон, поднимающий трезубец', 'accusative': u'тритона, поднимающего трезубец'}
image_description_rus['triton_and_siren_holding_hands'] = {'gender': 'they', 'nominative': u'тритон и сирена, держащиеся за руки', 'accusative': u'тритона и сирену, держащихся за руки'}
image_description_rus['mermaid_brushing_hair'] = {'gender': 'she', 'nominative': u'русалка, расчёсывающая волосы', 'accusative': u'русалку, расчёсывающую волосы'}
image_description_rus['playing_mermaid'] = {'gender': 'they', 'nominative': u'играющие русалки', 'accusative': u'играющих русалок'}
image_description_rus['mermaid_playing_with_pearl'] = {'gender': 'she', 'nominative': u'русалка, играющая с жемчужиной', 'accusative': u'русалку, играющую с жемчужиной'}
image_description_rus['awesome_sea_serpent'] = {'gender': 'he', 'nominative': u'устрашающий морской змей', 'accusative': u'устрашающего морского змея'}
image_description_rus['flying_seagull'] = {'gender': 'they', 'nominative': u'летящие чайки', 'accusative': u'летящих чаек'}
image_description_rus['wriggling_octopus'] = {'gender': 'he', 'nominative': u'извивающийся осьминог', 'accusative': u'извивающегося осьминога'}
image_description_rus['kraken_drowning_sea_vessel'] = {'gender': 'he', 'nominative': u'кракен, топящий морское судно', 'accusative': u'кракена, топящего морское судно'}
image_description_rus['sailing_ship'] = {'gender': 'he', 'nominative': u'плывущий по волнам корабль', 'accusative': u'плывущий по волнам корабль'}
"""словарь для описания качества драгоценности, ключ - качество, значение - словарь с русским названием качества в разных родах"""
quality_description_rus = {}
quality_description_rus['rough'] = {'he': u"грубый ", 'she': u"грубая ", 'it': u"грубое "}
quality_description_rus['common'] = {'he': u"", 'she': u"", 'it': u""} # у обычного описание опускается
quality_description_rus['skillfully'] = {'he': u"искусно сделанный ", 'she': u"искусно сделанная ", 'it': u"искусно сделанное "}
quality_description_rus['mastery'] = {'he': u"мастерски изготовленный ", 'she': u"мастерски изготовленная ", 'it': u"мастерски изготовленное "}
"""словарь для описания украшения, ключ - тип украшения, значение - словарь с русским словом в разных родах"""
decoration_description_rus = {}
decoration_description_rus['decoration'] = {'he': u"украшенный", 'she': u"украшенная", 'it': u"украшенное"}
decoration_description_rus['spangled'] = {'he': u"усыпанный", 'she': u"усыпанная", 'it': u"усыпанное"}
decoration_description_rus['inlaid'] = {'he': u"инкрустированный", 'she': u"инкрустированная", 'it': u"инкрустированное"}
decoration_description_rus['image'] = {'he': u"изображен", 'she': u"изображена", 'it': u"изображено", 'they': u"изображены"}
"""словарь для описания типа украшения на русском"""
decorate_types_description_rus = {'incuse': u"чеканкой", 'engrave': u"гравировкой", 'etching': u"травлением", 'carving': u"резьбой"}
"""словарь для вывода описаний массы сокровищ на русском"""
treasures_mass_description_rus = {}
treasures_mass_description_rus['coin'] = {
    0     : u"Монеты",
    100   : u"Кучка монет",
    1000  : u"Куча монет",
    10000 : u"Гора монет",
    100000: u"Горы монет",
    }
treasures_mass_description_rus['material'] = {
    0     : u"Материалы",
    100   : u"Кучка материалов",
    1000  : u"Куча материалов",
    10000 : u"Гора материалов",
    100000: u"Горы материалов",
    }
treasures_mass_description_rus['gem'] = {
    0     : u"Драгоценные камни",
    100   : u"Кучка драгоценных камней",
    1000  : u"Куча драгоценных камней",
    10000 : u"Гора драгоценных камней",
    100000: u"Горы драгоценных камней",
    }
treasures_mass_description_rus['jewelry'] = {
    0     : u"Безделушки",
    100   : u"Кучка безделушек",
    1000  : u"Куча безделушек",
    10000 : u"Гора безделушек",
    100000: u"Горы безделушек",
    }

number_conjugation_end = {1 : {'nominative' : (u"", u"а", u"ов")},
                          2 : {'nominative' : (u"ок", u"ка", u"ков")},
                          }
 
def number_conjugation_type(number):
    if (number % 10 == 1) and (number % 100 <> 11):
        return 0
    elif (number % 10 > 1 and number % 10 < 5) and (number % 100 < 11 or number % 100 > 21):
        return 1
    else:
        return 2
 
def number_conjugation_rus(number, add_name, word_form = 'nominative', word_type = 1):
    description_end = number_conjugation_end[word_type][word_form][number_conjugation_type(number)]
    return u"%s %s%s"%(number, add_name, description_end)

def capitalizeFirst (string):
    if string:
        return string[0].upper() + string[1:]
    else:
        return string[:]
    
def weighted_select(d):
    weight = random.random()*sum(v[0] for k, v in d.items())
    for k, v in d.items():
        if weight < v[0]:
            return k
        weight -= v[0]
    return d.keys()[random.randint(0,len(d.keys()))]
class Ingot(object):#класс для генерации слитков
    weights = (1,4,8,16)
    weights_description_rus = {1: u"крохотный", 4: u"небольшой", 8: u"полновесный", 16: u"массивный"}
    def __init__(self, metal_type):
        self.metal_type = metal_type
        self.metal_cost = metal_types[metal_type]
        self.weight = random.choice(self.weights)
    @property
    def cost(self):
        return self.metal_cost*self.weight
    def __repr__(self):
        return "%s pound %s ingot"%(self.weight, self.metal_type)
        
    def description(self, language = 'rus'):
        if language == 'rus':
            if self.weight in self.weights:
                return u"%s %s слиток" % (self.weights_description_rus[self.weight], metal_description_rus[self.metal_type]['he'])
            else:
                return u"Несколько %s слитков общим весом %s" % (metal_description_rus[self.metal_type]['they'], number_conjugation_rus(self.weight, u"фунт"))
        else:
            return self.__repr__()
       
    @staticmethod
    def number_conjugation(metal_type, metal_weight):
        """
        Функция для вывода описания слитков металла по типу металла и его количеству
        """
        if metal_weight in Ingot.weights:
            return u"%s %s слиток" % (Ingot.weights_description_rus[metal_weight], metal_description_rus[metal_type]['he'])
        else:
            return u"несколько %s слитков общим весом %s" % (metal_description_rus[metal_type]['they'], number_conjugation_rus(metal_weight, u"фунт"))
class Coin(object):
    coin_types = {"farting":(1, 1), "taller":(1, 10), "dublon":(1, 100)}
    coin_description_rus = {"farting": u"фартинг", "taller": u"таллер", "dublon": u"дублон"}
    """
    Монеты.
    """
    def __init__(self, name, amount):
        self.amount = amount # количество монеток
        self.name = name
        self.value = Coin.coin_types[self.name][1]
    @property
    def cost(self):
        return self.amount*self.value

    def __repr__(self):
        return str(self.amount) +" " + "%s(s)" %(self.name)
        
    def description(self, language = 'rus'):
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
class Gem(object):#класс для генерации драг.камней
    cut_dict = {" " : (0, 1), "polished":(50, 2), "rough":(30, 1), "faceted":(20, 3)}
    size_dict = {"small":(40, 1), "common":(50, 5), "large":(8, 25),\
             "exceptional":(2, 100)}
    def __init__(self, g_type, size,cut):
        self.g_type = g_type#Тип камня
        self.size = size#размер
        self.size_mod = Gem.size_dict[size][1]#модификатор размера
        """степень обработки"""
        self.cut = " " if self.g_type == "pearl" or self.g_type == "black_pearl" else cut
        self.cut_mod = Gem.cut_dict[cut][1]#модификатор обработки
        self.base = gem_types[self.g_type][1]#базовая ценность, зависит от типа
        self.can_be_incrusted = False if self.size==100 else True #проверяем возможность инкрустации
        self.amount = 1 if self.size_mod >= 25 else 5 if self.size_mod == 5 else 20
    @property
    def cost(self):#цена камня, складывается из базы(зависит от типа), размера и степени обработки
        return self.base*self.size_mod*self.cut_mod*self.amount
    def __repr__(self):
        return "%s %s %s" %(self.size, self.cut, self.g_type)
    def __eq__(self, other):
        if isinstance(other, Gem):
            return other and self.g_type == other.g_type and self.cut == other.cut\
            and self.size == other.size
        else:
            return
            
    def description(self, custom = False, case = 'nominative', gender = 'he', language = 'rus'):
        """
        Создает описание для драгоценного камня
        :custom: - если False - добавляет в описание "горсть"/"несколько" для мелких/обычных камней и меняет соответствующим образом род и падеж камней
        :case: - в каком падеже описываются камни
        :gender: - какого рода камни - 'he' (мужского), 'she' (женского) или 'they' (множественное число)
        """
        if language == 'rus':
            if not custom and (self.size == 'small' or self.size == 'common'):
                case = 'genitive'
                gender = 'they'
                if self.size == 'small':
                    return u"Горсть мелких %s%s"%(gem_cut_description_rus[self.cut][gender][case], gem_description_rus[self.g_type][gender][case])
                else:
                    return u"Несколько %s%s"%(gem_cut_description_rus[self.cut][gender][case], gem_description_rus[self.g_type][gender][case])
            else:
                return u"%s%s%s"%(material_size_description_rus[self.size][gender][case], gem_cut_description_rus[self.cut][gender][case], gem_description_rus[self.g_type][gender][case])
        else:
            return self.__repr__()
            
    @staticmethod
    def number_conjugation(gem_type, gem_count):
        """
        Функция для вывода описания камней по типу (в формате тип/размер/огранка) и количеству (без учета умножения мелких/обычных камней)
        """
        gem_param = gem_type.split(';')
        if gem_param[1] == 'small' or gem_param[1] == 'common': # умножаем мелкие/обычные камни
            if gem_param[1] == 'small':
                gem_count *= 25
            else:
                gem_count *= 5
        conjugation_type = number_conjugation_type(gem_count) # определяем тип сопряжения
        gender = 'he' if gem_param[0] <> 'pearl' and gem_param[0] <> 'black_pearl' else 'she' # определяем род, некрасивый вариант - лучше использовать словарь
        # выводим результат для каждого типа сопряжения
        if conjugation_type == 0: # единственное число - именительный падеж, род копируется
            if gem_count <> 1: # если камень один - не ставим число
                return u"%s %s%s%s"%(gem_count, material_size_description_rus[gem_param[1]][gender]['nominative'], \
                        gem_cut_description_rus[gem_param[2]][gender]['nominative'], gem_description_rus[gem_param[0]][gender]['nominative'])
            else:
                return u"%s%s%s"%(material_size_description_rus[gem_param[1]][gender]['nominative'], \
                        gem_cut_description_rus[gem_param[2]][gender]['nominative'], gem_description_rus[gem_param[0]][gender]['nominative'])
        elif conjugation_type == 1: # маломножественная форма - родительный падеж, тип в единственном числе, прилагательные - во множественном
            return u"%s %s%s%s"%(gem_count, material_size_description_rus[gem_param[1]]['they']['genitive'], \
                    gem_cut_description_rus[gem_param[2]]['they']['genitive'], gem_description_rus[gem_param[0]][gender]['genitive'])
        elif conjugation_type == 2: # множественное число - родительный падеж множественного числа
            gender = 'they'
            return u"%s %s%s%s"%(gem_count, material_size_description_rus[gem_param[1]][gender]['genitive'], \
                    gem_cut_description_rus[gem_param[2]][gender]['genitive'], gem_description_rus[gem_param[0]][gender]['genitive'])
        
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
        args_holder = [i for i in args]
        for i in args_holder:
            if type(i) == dict:
                if i.keys()[0] == "size":
                    for v in i["size"]:
                        if Gem.size_dict.has_key(v) != False:
                            size[v] = Gem.size_dict[v]
                elif i.keys()[0] == "cut":
                    for v in i["cut"]:
                        if cut_dict.has_key(v) != False:
                            cut[v] = cut_dict[v]
            elif type(i) == list:
                for item in i:
                    if gem_types.has_key(item) != False:
                        new_dict[item] = gem_types[item]
            elif type(i) == str:
                if gem_types.has_key(i) != False:
                    new_dict[i] = gem_types[i]              
        while count != 0:
            if len(cut) == 0:
                cut = Gem.cut_dict
            if len(size) == 0:
                size = Gem.size_dict
            if len(new_dict) == 0:
                new_dict = gem_types
            gems.append(Gem(weighted_select(new_dict), weighted_select(size),weighted_select(cut)))
            count -= 1
        return gems
    for i in xrange(count):
        gems.append(Gem(weighted_select(gem_types), weighted_select(Gem.size_dict),weighted_select(Gem.cut_dict)))
    return gems
class Material(object):#класс для генерации материалов
    size_dict = {"small":(40, 1), "common":(50, 5), "large":(8, 25),\
                 "exceptional":(2, 100)}
    def __init__(self, m_type, size):
        self.m_type = m_type#название
        self.base = material_types[m_type][1]#базовая цена
        self.size = size#размер
        self.size_mod = Material.size_dict[size][1]#модификатор размера
    @property
    def cost(self):#определяем цену материала(зависит от размера и типа)
        return self.size_mod*self.base
    def __repr__(self):
        return "%s %s" %(self.size, self.m_type)
    def __eq__(self, other):
        if isinstance(other, Material):
            return other and self.m_type == other.m_type and self.size == other.size
        else:
            return
            
    def description(self, language = 'rus'):
        if language == 'rus':
            return u"%sкусок %s"%(material_size_description_rus[self.size]['he']['nominative'], material_description_rus[self.m_type]['genitive'])
        else:
            return self.__repr__()
    
    @staticmethod
    def number_conjugation(material_type, material_count):
        """
        Функция для вывода описания камней по типу (в формате тип/размер) и количеству
        """
        material_param = material_type.split(';')
        conjugation_type = number_conjugation_type(material_count) # определяем тип сопряжения
        # выводим результат для каждого типа сопряжения
        if conjugation_type == 0: # единственное число - именительный падеж, род копируется
            if material_count <> 1: # если материал один - не ставим число
                return u"%s %sкусок %s"%(material_count, material_size_description_rus[material_param[1]]['he']['nominative'], \
                        material_description_rus[material_param[0]]['genitive'])
            else:
                return u"%sкусок %s"%(material_size_description_rus[material_param[1]]['he']['nominative'], \
                        material_description_rus[material_param[0]]['genitive'])
        elif conjugation_type == 1: 
            return u"%s %sкуска %s"%(material_count, material_size_description_rus[material_param[1]]['they']['genitive'], \
                    material_description_rus[material_param[0]]['genitive'])
        elif conjugation_type == 2: 
            return u"%s %sкусков %s"%(material_count, material_size_description_rus[material_param[1]]['they']['genitive'], \
                    material_description_rus[material_param[0]]['genitive'])
def generate_mat(count, *args):
    """принцип работы такойже как для драг.камней"""
    mats = []
    if len(args) != 0:
        size = {}
        new_dict = {}
        args_holder = [i for i in args]
        for i in args_holder:
            if type(i) == dict:
                if i.keys()[0] == "size":
                    for v in i["size"]:
                        if Material.size_dict.has_key(v) != False:
                            size[v] = Material.size_dict[v]
            elif type(i) == list:
                for item in i:
                    if material_types.has_key(item) != False:
                        new_dict[item] = material_types[item]
            elif type(i) == str:
                if material_types.has_key(i) != False:
                    new_dict[i] = material_types[i]
        for i in xrange(count):
            if len(size) == 0:
                size = size = Material.size_dict
            if len(new_dict) == 0:
                new_dict = material_types
            mats.append(Material(weighted_select(new_dict), weighted_select(size)))
        return mats
    for i in xrange(count):
        mats.append(Material(weighted_select(material_types), weighted_select(Material.size_dict)))
    return mats        
class Treasure(object):#класс для сокровищ
    decorate_types = {"incuse":(33,), "engrave":(33,), "etching":(33,), "carving":(0,)}
    quality_types = {"common":(60, 2), "skillfully":(20, 3),\
                    "rough":(10, 1), "mastery":(10, 5)}
    def __init__(self, treasure_type, alignment):
        """все значения заносятся из словаря treasure_types"""
        self.treasure_type = treasure_type
        self.base_price = treasure_types[self.treasure_type][0]
        self.gender = treasure_types[self.treasure_type][1]
        self.metall = treasure_types[self.treasure_type][2]
        self.nonmetall = treasure_types[self.treasure_type][3]
        self.image = treasure_types[self.treasure_type][4]
        self.incrustable = treasure_types[self.treasure_type][5]
        self.decorable = treasure_types[self.treasure_type][6]
        self.alignment = alignment
        """дальше генерируем характеристики в зависимости от типа сокровища"""
        self.random_mod = random.randint(0, self.base_price*10)
        self.spangled = generate_gem(1,{"size":('common',)})[0] if random.randint(1,100) <= 50 and self.incrustable != False else None # размер 'common' - хак, чтобы не писалось "мелкими"
        self.inlaid = generate_gem(1,{"size":('common',)})[0] if random.randint(1,100)  <=15 and self.incrustable != False  else None
        self.huge = generate_gem(1,{"size":('large',)})[0] if random.randint(1,100) <= 5 and self.incrustable != False else None 
                
        def metalls_available():#проверяем принадлежность к расе(из каких металов может быть сделано)
            if self.alignment == "human" or self.alignment ==  "cleric" or self.alignment == "knight":
                return {"silver":(70,), "gold":(30,)}
            elif self.alignment == "elf" or self.alignment == "merman":
                return {"gold":(70,), "mithril":(30,)}
            elif self.alignment == "dwarf":
                return {"gold":(70,), "adamantine":(30,)}
        
        def material():
            if self.metall and self.nonmetall:
                rnd = random.randint(1,100)
                if rnd > 50:
                    return weighted_select(material_types)
                else:
                    return weighted_select(metalls_available())
            elif self.metall:
                return weighted_select(metalls_available())
            else:
                return weighted_select(material_types)
        self.material = material()#выбираем материал
        
        self.mat_price = material_types[self.material][1] if material_types.has_key(self.material) else metal_types[self.material]
        
        def decorate():
            if self.decorable:#todo: словарь, откуда будем брать варианты орнаментов
                rnd = random.randint(1,100)
                if rnd <= 15:
                    rnd = random.randint(1,100)
                    if rnd <=50:
                        self.decoration_image = random.choice(image_types[self.alignment])
                        if material_types.has_key(self.material):
                            return ("carving")
                        else:
                            return (weighted_select(Treasure.decorate_types))
                    else:
                        return None
                else:
                    return None
        self.decoration = decorate()#выбираем орнамент
        if self.image: self.decoration_image = random.choice(image_types[self.alignment]) 
        self.dec_mod = 1 if self.decoration == None else 2#равен двум если есть орнамент
        def q_choice():#прокидываем качество вещи
            if self.alignment == "human" or self.alignment ==  "cleric" or self.alignment == "knight":
                return weighted_select(Treasure.quality_types)
            else:
                holder = {k:v for k, v in Treasure.quality_types.items()}
                holder.__delitem__("rough")
                return weighted_select(holder)
        self.quality =  q_choice()
        self.quality_mod = Treasure.quality_types[self.quality][1]
    def incrustation(self, gem):#метод для икрустации камней
        if self.incrustable == False:
            return "Can't be incrusted"
        if gem.size == "small":
            if self.spangled == None:
                self.spangled = gem
            return
        if gem.size[1] == "common":
            if self.inlaid == None:
                self.inlaid = gem
            return
        if gem.size[1] == "huge":
            if self.huge == None:
                self.huge = gem
            return
    @property#цена вставленных камней
    def incrustation_cost(self):
        holder = 0
        if self.spangled != None:
            holder += self.spangled.cost * Gem.size_dict['small'][1] // Gem.size_dict['common'][1] # из-за хака с размерами
        if self.inlaid != None:
            holder += self.inlaid.cost
        if self.huge != None:
            holder += self.huge.cost
        return holder
    @property
    def cost(self):#цена сокровища
        return self.base_price*self.quality_mod*self.dec_mod*self.mat_price+\
               self.incrustation_cost+self.random_mod
    def __repr__(self):
        return "%s%s" %(self.material, self.treasure_type)
        
    def description(self, language = 'rus'):
        if language == 'rus':
            quality_str = quality_description_rus[self.quality][self.gender] # мастерство исполнения
            treasure_str = treasure_description_rus[self.treasure_type]['nominative'] # тип драгоценности
            if self.material in metal_types.keys(): # совмещаем мастерство исполнения, тип и материал, из которого изготовлено
                if self.treasure_type == 'icon' or self.treasure_type == 'tome': 
                    desc_str = u"%s%s в %s окладе"%(quality_str, treasure_str, metal_description_rus[self.material]['prepositional']) 
                else:
                    desc_str = u"%s%s %s"%(quality_str, metal_description_rus[self.material][self.gender], treasure_str)
            else:
                desc_str = u"%s%s из %s" % (quality_str, treasure_str, material_description_rus[self.material]['genitive'])
                
            if self.image: 
                desc_str += u", изображающая %s"% image_description_rus[self.decoration_image]['accusative'] # только изображение
            else:
                # добавляем различные украшения
                enchant_list = []
                if self.spangled: # усыпанное камнями
                    enchant_list.append(u"%s %s" % (decoration_description_rus['spangled'][self.gender], self.spangled.description(True, 'ablative', 'they')))
                if self.inlaid: # инкрустированное камнями
                    enchant_list.append(u"%s %s" % (decoration_description_rus['inlaid'][self.gender], self.inlaid.description(True, 'ablative', 'they')))
                if self.huge: # с крупным камнем
                    gem_gender = 'she' if self.huge.g_type == 'pearl' or self.huge.g_type == 'black_pearl' else 'he' # только ради "крупной (чёрной) жемчужины"
                    enchant_list.append(u"с %s" % self.huge.description(True, 'ablative', gem_gender))
                if self.decoration: # украшенное чеканкой/гравировкой/травлением/резьбой
                    enchant_list.append(u"%s %s" % (decoration_description_rus['decoration'][self.gender], decorate_types_description_rus[self.decoration]))
                if len(enchant_list) == 1:  
                    if not self.huge: desc_str += u"," # добавляем "с крупным камнем" без запятой
                    desc_str += u" %s" % enchant_list[0] 
                elif len(enchant_list) > 1:
                    while len(enchant_list) > 1:
                        desc_str += u", %s" % enchant_list[0] # добавляем через запятую украшения
                        del enchant_list[0]
                    desc_str += u" и %s" % enchant_list[0] # последнее добавляется союзом "и"
                if self.decoration: # если есть изображение - ставим точку и описываем его
                    image_description = image_description_rus[self.decoration_image] # упрощение доступа к свойству
                    desc_str = u"%s. На %s %s %s" % (desc_str, treasure_description_rus[self.treasure_type]['ablative'], \
                                    decoration_description_rus['image'][image_description['gender']], image_description['nominative'])
            return desc_str
        else:
            return self.__repr__()
        
def gen_treas(count, t_list, alignment, min_cost, max_cost, obtained):
    """Генерируем рандомное сокровище
    функция генерации сокровищ,count - количество сокровищ, t_list - список строк-имен сокровищ, alignmet - принадлежность
    к определенной культуре(одно из: human, cleric, knight, merman, elf, dwarf), min_cost - минимальная цена сокровища,
    max_cost - максимальная цена сокровища"""
    treasures_list = []
    while count != 0:
        treas_holder = random.choice(t_list)
        if gem_types.has_key(treas_holder):
            treasures_list.extend(generate_gem(1, treas_holder))
        if material_types.has_key(treas_holder):
            treasures_list.extend(generate_mat(1, treas_holder))
        if metal_types.has_key(treas_holder):
            treasures_list.append(Ingot(treas_holder))
        if Coin.coin_types.has_key(treas_holder):
            rnd = random.randint(min_cost, max_cost)
            treasures_list.append(Coin(treas_holder,rnd/Coin.coin_types[treas_holder][1]))
        if treasure_types.has_key(treas_holder):
            t = Treasure(treas_holder, alignment)
            t.obtained = obtained
            treasures_list.append(t)
        for i in treasures_list:
            if i.cost < min_cost or i.cost > max_cost:
                treasures_list.remove(i)
                count += 1
        count -= 1
    return treasures_list


class Treasury(store.object):
    def __init__(self):
        self.farting = 0 # медная монетка
        self.taller = 0 # серебряная монетка
        self.dublon = 0 # золотая монетка
        # списки строк
        self.materials = {} #словарь с количеством материала
        self.metals = {} #словарь с количеством металла
        self.jewelry = [] #список драгоценностей
        self.equipment = []
        self.gems = {} #словарь с количеством драгоценных камней
        #TODO: multiple same equipment
        self.thief_items = data.Container(id="equipment")
    
    @property
    def money(self):
        return self.farting + 10 * self.taller + 100 * self.dublon
    @money.setter
    def money(self, Value):
        if Value < 0: #Защита от ухода денег в минус
            raise NotImplementedError, u"Денег недостаточно для выполнения операции" 
        money_diff = Value - self.money #считаем разницу между прошлым значением и новым
        if money_diff < 0:
            #разница отрицательна или ноль - производим вычитание
            money_diff = -money_diff #для удобства получаем число, которое необходимо вычесть
            if self.farting < money_diff % 10:
                #медных монет недостаточно для выплаты, меняем серебряную
                self.taller -= 1
                self.farting += 10
            self.farting -= money_diff % 10
            money_diff = money_diff // 10
            if self.taller < money_diff % 10:
                if (self.farting // 10 + self.taller) < money_diff % 10:
                    #серебряных монет даже с учетом медных недостаточно для выплаты, меняем золотую
                    self.dublon -= 1
                    self.taller += 10
                else:
                    #серебряных монет с учетом медных достаточно для выплаты, меняем по максимуму медные на серебряные
                    self.taller += self.farting // 10
                    self.farting = self.farting % 10
            self.taller -= money_diff % 10
            money_diff = money_diff // 10
            if self.dublon < money_diff % 10:
                #золотых монет недостаточно для выплаты 
                self.taller += self.farting // 10 #меняем по максимуму медные на серебряные
                self.farting = self.farting % 10
                self.dublon += self.taller // 10 #меняем по максимуму серебряные на золотые
                self.taller = self.taller % 10
            self.dublon -= money_diff 
        else:
            #разница положительна - производим добавление монет по разрядам
            self.dublon += money_diff // 100
            money_diff = money_diff % 100
            self.taller += money_diff // 10
            self.farting += money_diff % 10
    
    @property
    def wealth(self):
        """
        Стоимость всех сокровищ дракона
        """
        calc_wealth = self.money # деньги
        for metal in self.metals.iterkeys(): # металлы
            calc_wealth += self.metals[metal] * metal_types[metal]
        for material_i in self.materials.iterkeys(): #материалы
            material = material_i.split(';')
            calc_wealth += self.materials[material_i] * material_types[material[0]][1] * Material.size_dict[material[1]][1]
        for gem_i in self.gems.iterkeys(): # драгоценные камни
            gem = gem_i.split(';')
            calc_wealth += self.gems[gem_i] * gem_types[gem[0]][1] * Gem.size_dict[gem[1]][1] * Gem.cut_dict[gem[2]][1]
        for treas_i in xrange(len(self.jewelry)): # украшения
            calc_wealth += self.jewelry[treas_i].cost
        return calc_wealth
        
    def receive_treasures(self, treasure_list):
        """
        Помещает сокровища в сокровищницу
        :param treasure_list: Список сокровищ, помещаемых в сокровищницу
        """
        for treas in treasure_list:
            type_str = str(type(treas))
            if type_str == "<class 'pythoncode.treasures.Coin'>":
                # сохраняется число медных, серебряных и золотых монет в соответствующих переменных
                if treas.name == 'farting':
                    self.farting += treas.amount
                elif treas.name == 'taller':
                    self.taller += treas.amount
                else:
                    self.dublon += treas.amount
            elif type_str == "<class 'pythoncode.treasures.Ingot'>":
                # сохраняется в словаре metals, где ключ - название металла, а значение - его вес в фунтах
                if treas.metal_type in self.metals:
                    self.metals[treas.metal_type] += treas.weight
                else:
                    self.metals[treas.metal_type] = treas.weight
            elif type_str == "<class 'pythoncode.treasures.Material'>":
                # сохраняется в словаре materials, где ключ - "название материала;размер материала", а значение - число материалов такого типа и размера
                type_str = treas.m_type + ';' + treas.size
                if type_str in self.materials:
                    self.materials[type_str] += 1
                else:
                    self.materials[type_str] = 1
            elif type_str == "<class 'pythoncode.treasures.Gem'>":
                # сохраняется в словаре gems, где ключ - "название драгоценности;размер драгоценности;обработка драгоценности", а значение - число камней такого типа, размера и обработки
                type_str = treas.g_type + ';' + treas.size + ';' + treas.cut
                if type_str in self.gems:
                    self.gems[type_str] += 1
                else:
                    self.gems[type_str] = 1
            elif type_str == "<class 'pythoncode.treasures.Treasure'>":
                self.jewelry.append(treas)
        
    def treasures_description(self, treasure_list):
        """
        :param treasure_list: Список сокровищ, для которых требуется получить описание
        :return: Возвращает список с описанием сокровищ
        """
        description_list = []
        for treas in treasure_list:
            description_list.append(capitalizeFirst(treas.description()) + '.')
        return description_list
        
    def take_ingot(self, ingot_type, weight):
        """
        :param ingot_type: название металла
        :param weight: вес, который мы хотели бы взять 
        :return: Возвращает тип Ingot с указанным весом или максимально возможным, либо None, если такого металла в сокровищнице нет
        """
        if ingot_type in self.metals and self.metals[ingot_type] > 0: # проверяем есть ли такой металл в сокровищнице
            ingot = Ingot(ingot_type) # создаем слиток
            ingot.weight = weight if weight < self.metals[ingot_type] else self.metals[ingot_type] # делаем вес слитка равным указанному весу или максимуму в сокровищнице
            self.metals[ingot_type] -= ingot.weight # вычитаем вес слитка из сокровищницы
            return ingot
        else:
            return None
            
    def take_material(self, material_name):
        """
        :param material_name: описание материала в формате 'тип;размер'
        :return: Возвращает тип Material или None, если такого материала в сокровищнице нет
        """
        if material_name in self.materials and self.materials[material_name] > 0: # проверяем есть ли такой материал в сокровищнице
            material_param = material_name.split(';') # парсим строку
            material = Material(*material_param) # получаем экземпляр класса с нужными параметрами
            self.materials[material_name] -= 1 # вычитаем один материал из списка сокровищницы
            return material
        else:
            return None
        
    def take_gem(self, gem_name):
        """
        :param gem_name: описание камня в формате 'тип;размер;обработка'
        :return: Возвращает тип Gem или None, если таких камней в сокровищнице нет
        """
        if gem_name in self.gems and self.gems[gem_name] > 0: # проверяем есть ли такой камень в сокровищнице
            gem_param = gem_name.split(';') # парсим строку
            gem = Gem(*gem_param) # получаем экземпляр класса с нужными параметрами
            self.gems[gem_name] -= 1 # вычитаем один камень из списка сокровищницы
            return gem
        else:
            return None
            
    def take_coin(self, coin_name, coin_count):  
        """
        :param coin_name: название монеты
        :param coin_count: сколько монет нам бы хотелось взять
        :return: Возвращает тип Coin с указанным числом монет или максимально возможным, либо None, если таких монет в сокровищнице нет
        """
        if coin_name == 'farting' and self.farting > 0:
            coin_count = coin_count if coin_count < self.farting else self.farting
            self.farting -= coin_count
            return Coin(coin_name, coin_count)
        elif coin_name == 'taller' and self.taller > 0:
            coin_count = coin_count if coin_count < self.taller else self.taller
            self.taller -= coin_count
            return Coin(coin_name, coin_count)
        elif coin_name == 'dublon' and self.dublon > 0:
            coin_count = coin_count if coin_count < self.dublon else self.dublon
            self.dublon -= coin_count
            return Coin(coin_name, coin_count)
        return None
        
    def rob_treasury(self, treasure_count = 1):
        """
        :param treasure_count: Количество сокровищ, которые необходимо взять из сокровищницы
        :return: Список самых дорогих сокровищ, взятых из сокровищницы
        """
        treasure_list = [] # список сокровищ, которые не приглянулись вору
        abducted_list = [] # список награбленного
        threshold_value = 0 # минимальная стоимость, которая будет взята
        
        def update_list(test_treasure): # функция добавления награбленного в список, возвращает истину в случае успешного добавления      
            if not test_treasure:
                return False # попытка взять несуществующую вещь
            elif threshold_value < test_treasure.cost: 
                test_cost = test_treasure.cost # сохраняем цену для скорости
                test_i = len(abducted_list) # новый индекс - последний в списке
                while test_i > 0 and abducted_list[test_i - 1].cost < test_cost: test_i -= 1 # сортировка
                abducted_list.insert(test_i, test_treasure) # вставляем в нужную позицию
                if len(abducted_list) > treasure_count: # убираем из списка вещь с наименьшей ценой
                    treasure_list.append(abducted_list.pop())
                    self.threshold_value = abducted_list[-1].cost
                return True
            else:
                treasure_list.append(test_treasure) # стоимость добавляемого меньше пороговой, возвращаем сокровище обратно в сокровищницу
                return False 
          
        for jewelry_i in reversed(xrange(len(self.jewelry))): # цикл по всем сокровищам, начиная с конца списка, для соответствия индекса количеству вещей в списке
            update_list(self.jewelry.pop()) # достаем сокровище из конца списка - там должны быть более дорогие сокровища и пробуем добавить их в список награбленного
        self.jewelry.extend(treasure_list) # возвращаем сокровища в сокровищницу после поиска самых дорогих
        treasure_list = [] # очищаем список возвращаемого
        for gem_type in self.gems.keys(): # просматриваем список типов камней
            while update_list(self.take_gem(gem_type)): pass # пока в список добавляются камни - добавляем
        for metal_type in self.metals.keys(): # аналогично, просматриваем список типов слитков
            while update_list(self.take_ingot(metal_type, 8)): pass # пока в список добавляются слитки - добавляем
        for coin_type in Coin.coin_types.keys(): # аналогично, просматриваем список типов монет
            while update_list(self.take_coin(coin_type, 100)): pass # пока в список добавляются монеты - добавляем
        for material_type in self.materials.keys(): # аналогично, просматриваем список типов материалов
            while update_list(self.take_material(material_type)): pass # пока в список добавляются материалы - добавляем
        self.receive_treasures(treasure_list) # возвращаем сокровища в сокровищницу
        return abducted_list

    def gem_name_count(self, gem_name):
        """
        :param gem_name: Тип драгоценных камней (в формате 'тип;размер;обработка'), для которого необходимо подсчитать количество камней в сокровищнице
        :return: количество камней такого типа в сокровищнице с учетом того, что мелкие идут группами по 25, а обычные - по 5
        """
        gem_count = self.gems[gem_name] # берем данные о количестве из словаря
        gem_param = gem_name.split(';') # парсим строку
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
        gem_list = sorted(self.gems.keys()) # список драгоценных камней, отсортированных по типу/размеру/огранке
        for gem_name in gem_list:
            if self.gems[gem_name]: # проверка наличия камней такого типа в сокровищнице
                gem_str += u"%s.\n" % capitalizeFirst(Gem.number_conjugation(gem_name, self.gems[gem_name]))
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
                material_str += u"%s.\n" % capitalizeFirst(Ingot.number_conjugation(metal_name, metal_weight))
        mat_list = sorted(self.materials.keys())
        for mat_name in mat_list:
            if self.materials[mat_name]:
                material_str += u"%s.\n" % capitalizeFirst(Material.number_conjugation(mat_name, self.materials[mat_name]))
        return material_str
        
    @property
    def most_expensive_jewelry(self):
        if len(self.jewelry):
            most_expensive_i = 0
            most_expensive_cost = self.jewelry[most_expensive_i].cost
            for jewelry_i in xrange(len(self.jewelry)):
                if self.jewelry[jewelry_i].cost > most_expensive_cost:
                    most_expensive_cost = self.jewelry[jewelry_i].cost
                    most_expensive_i = jewelry_i
            return u"%s.\nСтоимость украшения: %s.\n%s" % (capitalizeFirst(self.jewelry[most_expensive_i].description()), \
                        number_conjugation_rus(self.jewelry[most_expensive_i].cost, u"фартинг"), self.jewelry[most_expensive_i].obtained) 
        else:
            return u"Украшений в сокровищнице нет"
    
    @property
    def random_jewelry(self):
        if len(self.jewelry):
            random_jewelry = random.choice(self.jewelry)
            return u"%s.\nСтоимость украшения: %s.\n%s" % (capitalizeFirst(random_jewelry.description()), \
                        number_conjugation_rus(random_jewelry.cost, u"фартинг"), random_jewelry.obtained)
        else:
            return u"Украшений в сокровищнице нет"
            
    @staticmethod
    def get_mass_description(description_key, mass):
        """
        :param description_key: ключ для словаря treasures_mass_description_rus
        :param mass: масса, для которой нужно подобрать описание
        :return: описание массы монет в сокровищнице
        """
        if mass > 0:
            mass_list = reversed(sorted(treasures_mass_description_rus[description_key].keys()))
            for mass_i in mass_list:
                if mass >= mass_i:
                    return treasures_mass_description_rus[description_key][mass_i]
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