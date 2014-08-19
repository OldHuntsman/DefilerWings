import random
import math
import data
import core
import os
import renpy as renpy_internal
import renpy.exports as renpy
import renpy.store as store
import girls_data

class Girls_list(object):
    def __init__(self, gameRef, base_character):
        self.game = gameRef
        self.character = base_character
        self.prisoners = []
        self.free = []
    
    def new_girl (self, type = 'peasant'):
        """
        Генерация новой девушки указанного типа.
        """
        #TODO все типы девушек
        type = 'peasant'
        self.game.girl = core.Girl(gameRef=self.game, base_character=self.character)
        relative_path = "img/avahuman/"+type # Относительный путь для движка ренпи
        absolute_path = os.path.join(renpy_internal.config.basedir, "game", relative_path) # Cоставляем абсолютный путь где искать
        filename = random.choice(os.listdir(absolute_path)) # получаем название файла
        self.game.girl.avatar = relative_path + "/" + filename # Возвращаем правильно отформатированное значение
        self.game.girl.name = random.choice(girls_data.names[type])
        return u"Описание девушки"
        
    def impregnate(self):
        """
        Осеменение женщины.
        """
        self.game.girl.virgin = False
        if self.game.girl.quality < self.game.dragon.magic():
            self.game.girl.pregnant = 2
        else:
            self.game.girl.pregnant = 1
        self.game.dragon.lust -= 1
        return u"Подходящая сцена секса"
        
    def free_girl(self):
        """
        Выпустить текущую девушку на свободу.
        """
        #девушка отслеживается только если беременна
        if self.game.girl.pregnant:
            self.free.append(game.girl)
        return u"Описание процесса выпускания на свободу"
        
    def steal_girl(self):
        return u"%s относит пленницу в своё логово..." % (self.game.dragon.name)
        
    def jail_girl(self):
        """
        Посадить текущую девушку за решетку.
        """
        self.game.girl.jailed = True
        self.prisoners.append(self.game.girl)
        return u"...и сажает её под замок"
        
    def set_active(self, index):
        """
        Достать девушку с номером index из темницы
        """
        self.game.girl = self.prisoners[index]
        del self.prisoners[index]
        
    def eat_girl(self):
        """
        Скушать девушку.
        """
        self.game.dragon.hunger -= 1
        self.game.dragon.bloodiness = 0
        return u"Дракон кушает девушку"
        
    def rob_girl(self):
        return u"Дракон грабит девушку"
        
    def prisoners_list(self):
        """
        Возвращает список плененных девушек.
        """
        jail_list = []
        for girl_i in xrange(len(self.prisoners)):
            jail_list.append(self.prisoners[girl_i].name)
        return jail_list
    
    def prisoners_count(self):
        """
        Возвращает количество плененных девушек.
        """
        return len(self.prisoners)
        
    def new_year(self):
        """
        Все действия с девушками за год. Возвращает список сообщений.
        """
        self("Тестовое сообщение")
    