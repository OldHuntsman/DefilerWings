#!/usr/bin/env python
# coding=utf-8
import random
"""Словари , ключи - типы камней, значения - кортежи типа(ценность, шанс появления"""
gem_types = {"amber":(3,5), "crystall":(3,5), "beryll":(5,4),\
             "tigerye":(5,4), "granate":(10,3), "turmaline":(10,3),\
             "aqua":(10,3), "pearl":(10,3),"black_pearl":(10,3),\
             "elven_beryll":(25,2), "topaz":(25,2), "saphire":(25,2),\
             "ruby":(25,2), "emerald":(25,2), "goodruby":(100,1),\
             "goodemerald":(100,1), "star":(100,1), "diamond":(100,1),\
             "black_diamond":(100,1), "rose_diamond":(100,1)}
material_types = {"jasper":(1,5), "turquoise":(1,5), "jade":(1,5),\
                  "malachite":(1,5), "corall":(2,4), "ivory":(2,4),\
                  "agate":(5,3), "shell":(5,3), "horn":(10,1)}
def size_chose():#прокидывает шансы для размера, возвращает кортеж вида(число, текст)
    rnd = random.randint(1,100)
    if rnd <=10:
        if rnd >2:
            return (25, "large")
        else:
            return (100, "exceptional")
    elif rnd >10:
        if rnd < 50:
            return (5,"common")
        else:
            return (1, "small")
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
    weight = random.random()*sum(v[1] for k, v in d.items())
    for k, v in d.items():
        if weight < v[1]:
            return k
        weight -= v[1]
    return d.keys()[random.randint(0,len(d.keys()))]
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
class Gem(object):
    def __init__(self, g_type, size,cut_chose ):
        self.g_type = g_type#Тип камня
        self.size = size#размер
        """степень обработки"""
        self.cut_mod = (1,"") if self.g_type == "pearl" or self.g_type == "black_pearl" else cut_chose
        self.base = gem_types[self.g_type][0]#базовая ценность, зависит от типа
        self.can_be_incrusted = False if self.size==100 else True #проверяем возможность инкрустации
    @property
    def cost(self):#цена камня, складывается из базы(зависит от типа), размера и степени обработки
        return self.base*self.size[0]*self.cut_mod[0]
    def __str__(self):
        return "%s %s %s" %(self.size[1], self.cut_mod[1], self.g_type)
    def __repr__(self):
        return "%s %s %s" %(self.size[1], self.cut_mod[1], self.g_type)
"""функция для генерации камней, 1 обязательный аргумент - количество камней
которое нужно сгенерировать, чтобы задать размер и/или качество обработки
вызываем с аргументом {"size или cut":("имя_размера или качества",num)}
где num любое число, которое будет использоваться для определения ценности
камня, чтобы задать типы камней, вызываем с аргументом "тип камня" или
["тип камня", "тип камня", ...]
на пример generate_gem(5, {"size":("unusual", 33)}, ["ruby", "star", "aqua"],
                       "diamond")
создаст 5 разных камней размера unusual случайного качества огранки, 
тип каждого будет выбран из заданных, шансы появления которых относительно
друг друга указанны в словаре gem_types"""
def generate_gem(count, *args):
    cut = None
    size = None
    gems = []
    if len(args) != 0:
        size = size_chose()
        new_dict = {}
        args_holder = [i for i in args]
        for i in args_holder:
            if type(i) == dict:
                if i.keys()[0] == "size":
                    size = i.values()[0]
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
            elif size == None:
                size = size_chose()
            elif len(new_dict) == 0:
                new_dict = gem_types
            gems.append(Gem(weighted_select(new_dict), size, cut))
            count -= 1
        return gems
    for i in xrange(count):
        cut = cut_chose()
        size = size_chose()
        gems.append(Gem(weighted_select(gem_types), size, cut))
    return gems
class Material(object):
    def __init__(self, m_type, size):
        self.m_type = m_type
        self.base = material_types[self.m_type][0]
        self.size = size
    @property
    def cost(self):
        return self.size[0]*self.base
    def __repr__(self):
        return "%s %s, which cost %s" %(self.size[1], self.m_type, self.cost)
"""принцип работы такойже как для драг.камней"""
def generate_mat(count, *args):
    mats = []
    size = None
    if len(args) != 0:
        new_dict = {}
        args_holder = [i for i in args]
        for i in args_holder:
            if type(i) == dict:
                if i.keys()[0] == "size":
                    size = i.values()[0]
            elif type(i) == list:
                for item in i:
                    if material_types.has_key(item) != False:
                        new_dict[item] = material_types[item]
            elif type(i) == str:
                if material_types.has_key(i) != False:
                    new_dict[i] = material_types[i]
        while count != 0:
            if size == None:
                size = size_chose()
            elif len(new_dict) == 0:
                new_dict = material_types
            mats.append(Material(weighted_select(new_dict), size))
            count -= 1
    while count != 0:
        size = size_chose()
        mats.append(Material(weighted_select(material_types), size))
        count -= 1
    return mats       
class Treasure(object):
    materials_cost = {'Copper': 20,
                      'Silver': 50,
                      'Gold': 75,
                      'Platinum': 100,
                      'Diamond': 150}
    forms_cost = {'Ring': 20,
                  'Amulet': 40,
                  'Scepter': 70,
                  'Crown': 100}

    def __init__(self, material, form, base_price):
        self.material = material
        self.form = form
        self.base_price = base_price
        self.random_mod = random.randint(0, base_price*10)

    @property
    def cost(self):
        return int(self.materials_cost[self.material] * self.forms_cost[self.form] * self.random_mod)

    def __str__(self):
        return '%s %s (%s)' % (self.material.capitalize(), self.form.lower(), self.cost)


def generate_treasures(count):
    def gen():
        rnd = random.randint(0, 100)
        if rnd > 50:
            return Treasure(random.choice(Treasure.materials_cost.keys()),
                            random.choice(Treasure.forms_cost.keys()))
        else:
            return Coins(random.randint(10, 1000))

    gold = Coins(0)
    treasures = []
    for i in xrange(count):
        treasure = gen()
        if isinstance(treasure, Coins):
            gold.amount += treasure.amount
        else:
            treasures.append(treasure)

    treasures.append(gold)

    return treasures
