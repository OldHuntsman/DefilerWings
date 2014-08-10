#!/usr/bin/env python
# coding=utf-8
import random
import core
coin_types = {"farting":(1, 1), "taller":(1, 10), "dublon":(1, 100)}

size_dict = {"small":(40, 1,u"маленький"), "common":(50, 5,u"обычный"), "large":(8, 25,u"большой"),\
             "exceptional":(2, 100, u"исключительный")}

cut_dict = {"polished":(50, 2, u"полированный"), "rough":(30, 1, u"необработанный"), "faceted":(20, 3, u"ограненный")}

"""Словарь , ключи - названия камней(для внутреннего пользования), значения - кортежи вида(шанс появления, ценность, название)"""
gem_types = {}
gem_types["amber"] = (5,3,u"янтарь")
gem_types["crystall"] = (5,3,u"горный хрусталь")
gem_types["beryll"] = (4,5,u"берилл")
gem_types["tigereye"] = (4,5,u"тигровый глаз")
gem_types["granate"] = (3,10, u"гранат")
gem_types["turmaline"] = (3,10,u"турмалин")
gem_types["aqua"] = (3,10,u"аквамарин")
gem_types["pearl"] = (3,10,u"жемчуг")
gem_types["black_pearl"] = (3,10,u"черный жемчуг")
gem_types["elven_beryll"] = (2,25,u"эльфийский берилл")
gem_types["topaz"] = (2,25,u"топаз")
gem_types["saphire"] = (2,25,u"сапфир")
gem_types["ruby"] = (2,25,u"рубин")
gem_types["emerald"] = (2,25,u"изумруд")
gem_types["goodruby"] = (1,100,u"яхонт")
gem_types["goodemerald"] = (1,100,u"смарагд")
gem_types["star"] = (1,100,u"звездный сапфир")
gem_types["diamond"] = (1,100,u"алмаз")
gem_types["black_diamond"] = (1,100,u"черный алмаз")
gem_types["rose_diamond"] = (1,100,u"розовый алмаз")

material_types = {"jasper":(5,1,u"яшма"), "turquoise":(5,1), "jade":(5,1),\
                  "malachite":(5,1), "corall":(4,2), "ivory":(4,2),\
                  "agate":(3,5), "shell":(3,5), "horn":(1,10)}
material_types["jasper"] = (5,1,u"яшма")
material_types["turquoise"] = (5,1,u"бирюза")
material_types["jade"] = (5,1,u"нефрит")
material_types["malachite"] = (5,1,u"малахит")
material_types["corall"] = (4,2,u"коралл")
material_types["ivory"] = (4,2,u"слоновая кость")
material_types["agate"] = (3,5,u"агат")
material_types["shell"] = (3,5,u"перламутр")
material_types["horn"] = (1,10,u"драконий рог")
"""словарь для типов металлов, ключ - металл, значение - ценность"""
metal_types = {"silver": (1,u"серебряный"), "gold":(10,u"золотой"), "mithril":(50,u"мифриловый"), "adamantine":(50,u"адамантиновый")}
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
    @property
    def desc(self):
        return 
    def __repr__(self):
        return "%s pound %s ingot"%(self.weight, self.metal_type)
class Coins(object):
    """
    Монеты.
    """
    def __init__(self,name, amount):
        self.amount = amount # количество монеток
        self.name = name
        self.value = coin_types[self.name][1]
    @property
    def cost(self):
        return self.amount*self.value

    def __repr__(self):
        return str(self.cost) +" " + "%s(s)" %(self.name)
class Gem(object):#класс для генерации драг.камней
    def __init__(self, g_type, size,cut):
        self.g_type = (g_type, gem_types[g_type][2])#Тип камня
        self.size = (size, size_dict[size][1], size_dict[size][2])
        """степень обработки"""
        self.cut_mod = (" ",1," ") if self.g_type == "pearl" or self.g_type == "black_pearl" else (cut, cut_dict[cut][1], cut_dict[cut][2])
        self.base = gem_types[self.g_type[0]][1]#базовая ценность, зависит от типа
        self.can_be_incrusted = False if self.size==100 else True #проверяем возможность инкрустации
        self.amount = 1 if self.size[1] >= 25 else 5 if self.size[1] == 5 else 20
    @property
    def cost(self):#цена камня, складывается из базы(зависит от типа), размера и степени обработки
        return self.base*self.size[1]*self.cut_mod[1]
    @property
    def desc(self):
        return "%s %s %s %s" %(self.amount, self.size[2], self.cut_mod[2], self.g_type[1])
    def __repr__(self):
        return "%s %s %s" %(self.size[0], self.cut_mod[0], self.g_type[0])
    def __eq__(self, other):
        return other and self.g_type == other.g_type and self.size == other.size\
        and self.cut_mod == other.cut_mod
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
def generate_gem(count, *args):
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
                        if size_dict.has_key(v) != False:
                            size[v] = size_dict[v]
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
                cut = cut_dict
            if len(size) == 0:
                size = size_dict
            if len(new_dict) == 0:
                new_dict = gem_types
            gems.append(Gem(weighted_select(new_dict), weighted_select(size),weighted_select(cut)))
            count -= 1
        return gems
    for i in xrange(count):
        cut = cut_dict
        gems.append(Gem(weighted_select(gem_types), weighted_select(size_dict),weighted_select(cut)))
    return gems
class Material(object):#класс для генерации материалов
    def __init__(self, m_type, size):
        self.m_type = (m_type, material_types[m_type][2])#кортеж (ключ для поиска в словаре, название)
        self.base = material_types[m_type][1]#базовая цена
        self.size = (size, size_dict[size][1], size_dict[size][2])#кортеж (ключ для поиска в словаре, числовой эквивалент размера, размер)
    @property
    def cost(self):#определяем цену материала(зависит от размера и типа)
        return self.size[1]*self.base
    @property
    def desc(self):#(описание)
        return "%s %s" %(self.size[2], self.m_type[1])
    def __repr__(self):
        return "%s %s" %(self.size[0], self.m_type[0])
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
        """дальше генерируем характеристики в зависимости от типа сокровища"""
        self.random_mod = random.randint(0, self.base_price*10)
        self.alignment = alignment
        self.spangled = generate_gem(1,{"size":("small",)})[0] if random.randint(1,100) <= 50 and self.incrustable != False else None
        self.inlaid = generate_gem(1,{"size":("common",)})[0] if random.randint(1,100)  <=15 and self.incrustable != False  else None
        self.huge = generate_gem(1,{"size":("large",)})[0] if random.randint(1,100) <= 5 and self.incrustable != False else None 
                
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
        self.material = material()#выбираем материал
        
        self.mat_price = material_types[self.material][1] if material_types.has_key(self.material) else metal_types[self.material][0]
        
        def decorate():
            if self.decorable != False:#todo: словарь, откуда будем брать варианты орнаментов
                rnd = random.randint(1,100)
                if rnd <= 15:
                    rnd = random.randint(1,100)
                    if rnd <=50:
                        if material_types.has_key(self.material):
                            return ("carving", "")
                        else:
                            return (weighted_select(Treasure.decorate_types), "")
                    else:
                        return
                else:
                    return
        self.decoration = decorate()#выбираем орнамент
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
    @property#цена вставленных камней
    def incrustation_cost(self):
        holder = 0
        if self.spangled != None:
            holder += self.spangled.cost
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
