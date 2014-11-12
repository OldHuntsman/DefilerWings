#!/usr/bin/env python
# coding=utf-8
import math
import girls_data
from data import reputation_levels, reputation_gain
import renpy.store as store

class Mobilization(store.object):
    base=0 #Начальная мобилизация
    max=0 #Масимальная
    _lvl=0
    decrease=0 #Уменьшение мобилизации
    
    def __getinitargs__(self):
        return (self.level)
    
    def __init__(self, level = 0):
        '''
        level - уровень мобилизации
        '''
        self.level = level
    
    @property
    def level(self): #Текущая мобилизация
        return self._lvl
    @level.setter
    def level(self, value):
        value = int(value)
        if value >= 0:
            if value > self._lvl:
                self.max = value
            if value < self._lvl:
                self.decrease += self._lvl - value
            self._lvl = value
        
    def reset_base(self):
        self.gain = self._lvl
    def reset_max(self):
        self.max = self._lvl
    def reset_decrease(self):
        self.decrease = 0
    
    def reset(self)
        self.reset_base()
        self.reset_max()
        self.reset_decrease()
    
    @property
    def gain(self) #Изменение текущей мобилизации от базовой
        return self._lvl - self.base

class Reputation(store.object):
    '''
    Дурная слава дракона.
    '''
    _rp = 0
    _gain = 0
    _last_gain = 0
    
    @property
    def points(self):
        '''
        Количество очков дурной славы
        '''
        return self._rp
    @points.setter
    def points(self, value):
        if value >= 0:
            delta = int(value - self._rp)
            if delta in reputation_gain:
                self._last_gain = delta
                self._gain += delta
                self._rp = int(value)
            else:
                raise Exception("Cannot raise reputation. Invalid gain.")
    @property
    def gain_description(self):
        if self._last_gain in reputation_gain:
            return reputation_gain[self._last_gain]
            
    @property
    def points_gained(self):
        return self._gain
    
    def reset_gain(self):
        '''
        Обнуляет прибавку к очкам дурной славы. Используется когда, например, дракон спит.
        '''
        self._gain = 0
    
    @property
    def level(self):
        key = 0
        for i in sorted(reputation_levels.keys()):
            if self._rp >= int(i):
                key = int(i)
        return reputation_levels[key]

class Poverty (store.object):
    '''
    Счетчик разрухи. При попытке опустить разруху ниже нуля она примет нулевое значение.
    Использование:
    Poverty.value - возвращает текущий уровень разрухи
    Poverty.value += 1 - планирует увеличение разрухи на единицу
    Poverty.value -= 1 - планирует уменьшение разрухи на единицу
    Poverty.apply_value() - Применяет запланированное изменение разрухи
    '''
    _value = 0
    _planned = 0
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._planned += self._value - value
    
    def apply_planned(self):
        '''
        Применяем запланированные изменения в разрухе
        '''
        if self._value + self._planned >= 0: 
            self._value = self._value + self._planned
        else:
            self._value = 0
        self._planned = 0
        
class Army (store.object):
    '''
    Класс для армии Тьмы
    '''
    def __init__(self):
        self._grunts = {'goblin' : 1} # словарь для хранения рядовых войск
        self._elites = {} # словарь для хранения элитных войск
        self.money   = 0  # деньги в казне Владычицы
        self._force_residue = 100 # процент оставшейся силы армии - мощь армии
    
    def add_warrior(self, warrior_type):
        """
        Добавляет воина  в армию тьмы. warrior_type - название типа добавляемого воина из словаря girls_data.spawn_info
        """
        if 'elite' in girls_data.spawn_info[warrior_type]['modifier']:
            # воин элитный, добавляется в список элитных 
            warriors_list = self._elites
        else:
            # рядовой воин, добавляется в список рядовых 
            warriors_list = self._grunts
        if warrior_type in warriors_list:
            # такой тип воина уже в списке, просто увеличиваем их число
            warriors_list[warrior_type] += 1
        else:
            # такого типа воина нет в списке, добавляем
            warriors_list[warrior_type] = 1
        
    @property
    def grunts(self):
        """
        Возвращает число рядовых войск в армии тьмы
        """
        grunts_count = 0
        for grunts_i in self._grunts.values():
            grunts_count += grunts_i
        return grunts_count
        
    @property
    def grunts_list(self):
        """
        Возвращает список рядовых войск в армии тьмы
        """
        grunts_list = u""
        for grunt_name, grunt_count in self._grunts.iteritems():
            grunts_list += u"%s: %s. " % (girls_data.spawn_info[grunt_name]['name'], grunt_count)
        return grunts_list
    
    @property
    def elites(self):
        """
        Возвращает число элитных войск в армии тьмы
        """
        elites_count = 0
        for elites_i in self._elites.values():
            elites_count += elites_i
        return elites_count
        
    @property
    def elites_list(self):
        """
        Возвращает список элитных войск в армии тьмы
        """
        elites_list = u""
        for elite_name, elite_count in self._elites.iteritems():
            elites_list += u"%s: %s. " % (girls_data.spawn_info[elite_name]['name'], elite_count)
        return elites_list
        
    @property
    def diversity(self):
        """
        Возвращает разнообразие армии тьмы
        """
        diversity = len(self._elites)
        dominant_number = sorted(self._grunts.values())[-1] // 2
        for number_i in self._grunts.values():
            if dominant_number <= number_i:
                diversity += 1
        return diversity
        
    @property
    def equipment(self):
        """
        Возвращает уровень экипировки армии тьмы
        """
        equipment = 0
        AoD_money = self.money
        AoD_cost = (self.grunts + self.elites) * 1000
        while AoD_money >= AoD_cost:
            AoD_money //= 2
            equipment += 1
        return equipment
        
    @property
    def force(self):
        """
        Возвращает суммарную силу армии тьмы по формуле (force) = (grunts + 3 * elites) * diversity * equipment * текущий процент мощи 
        """
        return (self.grunts + 3 * self.elites) * self.diversity * self.equipment * self._force_residue // 100
        
    @property
    def power_percentage(self):
        """
        Возвращает текущий процент мощи армии тьмы
        """
        return self._force_residue
    @power_percentage.setter
    def power_percentage(self, value):
        """
        Устанавливает текущий процент мощи армии тьмы
        """
        self._force_residue = value