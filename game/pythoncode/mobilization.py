import math
import renpy.store as store

class Mobilization(store.object):
    _points = 1
    
    def __getinitargs__(self):
        return (self.level, self.points)
    
    def __init__(self, level = 0, points = 1):
        '''
        level - уровень мобилизации
        points - количество очков мобилизации
        Оба параметра не являются обязательными. Но оба параметра по сути выражают отдно и то же.
        Поэтому, в случае если указаны оба параметра, то приоритет отдается тому, где получается 
        больше очков.
        '''
        points = max(self._lvl_to_points(level), points)
        if points >= 1:
            self.points = points
    
    @staticmethod
    def _points_to_lvl(points):
        return int(math.floor(math.log(points, 2)))
    @staticmethod
    def _lvl_to_points(lvl):
        return int(math.pow(2, lvl))
        
    def _check(self, lvl):
        '''
        lvl - уровень для проверки
        Проверяет правильно высчитывается количество очков для начала уровня
        '''
        return int(lvl) == self._points_to_lvl(self._lvl_to_points(int(lvl)))
    
    @property
    def points(self):
        return int(self._points)
    @points.setter
    def points(self, value):
        value = int(value)
        if value >= 1:
            self._points = value
        else:
            raise Exception("Invalid input")
    
    @property
    def level(self):
        return self._points_to_lvl(self.points)
    @level.setter
    def level(self, value):
        value = int(value)
        self.points = self._lvl_to_points(value)