#!/usr/bin/env python
# coding=utf-8
import random
size_dict = {"small":(40, 1), "common":(50, 5), "large":(8, 25),\
             "exceptional":(2, 100)}
"""Словари , ключи - типы камней, значения - кортежи вида(шанс появления, ценность)"""
gem_types = {"amber":(5,3), "crystall":(5,3), "beryll":(4,5),\
             "tigerye":(4,5), "granate":(3,10), "turmaline":(3,10),\
             "aqua":(3,10), "pearl":(3,10),"black_pearl":(3,10),\
             "elven_beryll":(2,25), "topaz":(2,25), "saphire":(2,25),\
             "ruby":(2,25), "emerald":(2,25), "goodruby":(1,100),\
             "goodemerald":(1,100), "star":(1,100), "diamond":(1,100),\
             "black_diamond":(1,100), "rose_diamond":(1,100)}
material_types = {"jasper":(5,1), "turquoise":(5,1), "jade":(5,1),\
                  "malachite":(5,1), "corall":(4,2), "ivory":(4,2),\
                  "agate":(3,5), "shell":(3,5), "horn":(1,10)}
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
def cut_chose():#прокидывает шансы обработки, возвращает кортежи вида(число, текст)
    rnd = random.randint(1,100)
    if rnd <= 50:
        if rnd >20:
            return (1, "rough")
        else:
            return (3, "faceted")
    else:
        return (2, "polished")
def weighted_select(d):
    weight = random.random()*sum(v[0] for k, v in d.items())
    for k, v in d.items():
        if weight < v[0]:
            return k
        weight -= v[0]
    return d.keys()[random.randint(0,len(d.keys()))]
class Ingot(object):#класс для генерации слитков
    weights = (1,2,4,8,16)
    def __init__(self, metal_type):
        self.metal_type = metal_type
        self.metal_cost = metal_types[metal_type]
        self.weight = random.choice(self.weights)
    @property
    def cost(self):
        return self.metal_cost*self.weight
    def __repr__(self):
        return "%s pound %s ingot"%(self.weight, self.metal_type)
class Coins(object):
    """
    Монеты.
    """
    def __init__(self, amount):
        self.amount = amount # количество монеток

    @property
    def cost(self):
        return self.amount

    def __str__(self):
        return str(self.cost) + ' coins'
class Gem(object):#класс для генерации драг.камней
    def __init__(self, g_type, size,cut_chose ):
        self.g_type = g_type#Тип камня
        self.size = (size, size_dict[size][1])
        """степень обработки"""
        self.cut_mod = (1,"") if self.g_type == "pearl" or self.g_type == "black_pearl" else cut_chose
        self.base = gem_types[self.g_type][1]#базовая ценность, зависит от типа
        self.can_be_incrusted = False if self.size==100 else True #проверяем возможность инкрустации
        self.amount = 1 if self.size[1] >= 25 else 5 if self.size[1] == 5 else 20
    @property
    def cost(self):#цена камня, складывается из базы(зависит от типа), размера и степени обработки
        return self.base*self.size[1]*self.cut_mod[0]
    def __str__(self):
        return "%s %s %s %s" %(self.amount, self.size[0], self.cut_mod[1], self.g_type)
    def __repr__(self):
        return "%s %s %s %s" %(self.amount, self.size[0], self.cut_mod[1], self.g_type)
"""функция для генерации камней, 1 обязательный аргумент - количество камней
которое нужно сгенерировать, чтобы задать размер и/или качество обработки
вызываем с аргументом {"size":("размер", "размер", ...} или {"cut":(число, "качество)}
число будет использоваться для определения ценности
камня, чтобы задать типы камней, вызываем с аргументом "тип камня" или
["тип камня", "тип камня", ...]
на пример generate_gem(5, {"size":("common", "small")}, ["ruby", "star", "aqua"],
                       "diamond")
создаст 5 разных камней размера common или small случайного качества огранки, 
тип каждого будет выбран из заданных, шансы появления которых относительно
друг друга указанны в словаре gem_types"""
def generate_gem(count, *args):
    cut = None
    gems = []
    if len(args) != 0:
        size = {}
        new_dict = {}
        args_holder = [i for i in args]
        for i in args_holder:
            if type(i) == dict:
                if i.keys()[0] == "size":
                    for v in i["size"]:
                        if size_dict.has_key(v) != False:
                            size[v] = size_dict[v]
                elif i.keys()[0] == "cut":
                    cut = i.values()[0]
            elif type(i) == list:
                for item in i:
                    if gem_types.has_key(item) != False:
                        new_dict[item] = gem_types[item]
            elif type(i) == str:
                if gem_types.has_key(i) != False:
                    new_dict[i] = gem_types[i]              
        while count != 0:
            if cut == None:
                cut = cut_chose()
            if len(size) == 0:
                size = size_dict
            if len(new_dict) == 0:
                new_dict = gem_types
            gems.append(Gem(weighted_select(new_dict), weighted_select(size), cut))
            count -= 1
        return gems
    for i in xrange(count):
        cut = cut_chose()
        gems.append(Gem(weighted_select(gem_types), weighted_select(size_dict), cut))
    return gems
class Material(object):#класс для генерации материалов
    def __init__(self, m_type, size):
        self.m_type = m_type
        self.base = material_types[self.m_type][1]
        self.size = (size, size_dict[size][1])
    @property
    def cost(self):
        return self.size[1]*self.base
    def __repr__(self):
        return "%s %s" %(self.size[0], self.m_type)
"""принцип работы такойже как для драг.камней"""
def generate_mat(count, *args):
    mats = []
    if len(args) != 0:
        size = {}
        new_dict = {}
        args_holder = [i for i in args]
        for i in args_holder:
            if type(i) == dict:
                if i.keys()[0] == "size":
                    for v in i["size"]:
                        if size_dict.has_key(v) != False:
                            size[v] = size_dict[v]
            elif type(i) == list:
                for item in i:
                    if material_types.has_key(item) != False:
                        new_dict[item] = material_types[item]
            elif type(i) == str:
                if material_types.has_key(i) != False:
                    new_dict[i] = material_types[i]
        for i in xrange(count):
            if len(size) == 0:
                size = size = size_dict
            if len(new_dict) == 0:
                new_dict = material_types
            mats.append(Material(weighted_select(new_dict), weighted_select(size)))
        return mats
    for i in xrange(count):
        mats.append(Material(weighted_select(material_types), weighted_select(size_dict)))
    return mats        
class Treasure(object):#класс для сокровищ
    decorate_types = {"incuse":(33,), "etching":(33,), "travlenie":(33,)}
    def __init__(self, treasure_type, alignment):
        """все значения заносятся из treasure_types"""
        self.treasure_type = treasure_type
        self.base_price = treasure_types[self.treasure_type][0]
        self.gender = treasure_types[self.treasure_type][1]
        self.metall = treasure_types[self.treasure_type][2]
        self.nonmetall = treasure_types[self.treasure_type][3]
        self.image = treasure_types[self.treasure_type][4]
        self.incrustable = treasure_types[self.treasure_type][5]
        self.decorable = treasure_types[self.treasure_type][6]
        self.random_mod = random.randint(0, self.base_price*10)
        self.alignment = alignment
        self.spangled = generate_gem(1,{"size":("small",)}) if random.randint(1,100) <= 50 and self.incrustable != False else None
        self.inlaid = generate_gem(1,{"size":("common",)}) if random.randint(1,100)  <=15 and self.incrustable != False  else None
        self.huge = generate_gem(1,{"size":("large",)}) if random.randint(1,100) <= 5 and self.incrustable != False else None 
                
        def metalls_available():#проверяем принадлежность к расе(из каких металов может быть сделано)
            if self.alignment == "human" or self.alignment ==  "cleric" or self.alignment == "knight":
                return {"silver":(70,), "gold":(30,)}
            elif self.alignment == "elf" or self.alignment == "merman":
                return {"gold":(70,), "mithril":(30,)}
            elif self.alignment == "dwarf":
                return {"gold":(70,), "adamantine":(30,)}
        
        def material():
            if self.metall == True and self.nonmetall == True:
                rnd = random.randint(1,100)
                if rnd > 50:
                    return weighted_select(material_types)
                else:
                    return weighted_select(metalls_available())
            elif self.metall == True:
                return weighted_select(metalls_available())
            else:
                return weighted_select(material_types)
        self.material = material()
        
        def decorate():
            if self.decorable != False:#todo: словарь, откуда будем брать варианты орнаментов
                rnd = random.randint(1,100)
                if rnd <= 15:
                    rnd = random.randint(1,100)
                    if rnd <=50:
                        if material_types.has_key(self.material):
                            return ("carving", "")
                        else:
                            return (weighted_select(decorate_types), "")
                    else:
                        return None
                else:
                    return None
        self.decoration = decorate()
    def incrustation(self, gem):
        if self.incrustable == False:
            return "Can't be incrusted"
        if gem.size[1] == 1:
            if self.spangled == None:
                self.spangled = gem
            return
        if gem.size[1] == 5:
            if self.inlaid == None:
                self.inlaid = gem
            return
        if gem.size[1] == 25:
            if self.huge == None:
                self.huge = gem
            return
                        
    @property
    def cost(self):
        return 100
    def __repr__(self):
        return "%s%s" %(self.material, self.treasure_type)
"""Генерируем рандомное сокровище"""
def gen_treas(count, t_list, alignment, min_cost, max_cost):
    treasures_list = []
    while count != 0:
        treas_holder = random.choice(t_list)
        if gem_types.has_key(treas_holder):
            treasures_list.extend(generate_gem(1, treas_holder))
        if material_types.has_key(treas_holder):
            treasures_list.extend(generate_mat(1, treas_holder))
        if metal_types.has_key(treas_holder):
            treasures_list.append(Ingot(treas_holder))
        if treasure_types.has_key(treas_holder):
            treasures_list.append(Treasure(treas_holder, alignment))
        for i in treasures_list:
            if i.cost < min_cost or i.cost > max_cost:
                treasures_list.remove(i)
                count += 1
        count -= 1
    return treasures_list
