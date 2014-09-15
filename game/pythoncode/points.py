#!/usr/bin/env python
# coding=utf-8
import math
from data import reputation_levels, reputation_gain
import renpy.store as store

class Mobilization(store.object):
    
    def __getinitargs__(self):
        return (self.level)
    
    def __init__(self, level = 0):
        '''
        level - уровень мобилизации
        '''
        self.level = level
    
    @property
    def level(self):
        return self._lvl
    @level.setter
    def level(self, value):
        self._lvl = int(value)

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