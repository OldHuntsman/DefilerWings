#!/usr/bin/env python
# coding=utf-8
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
        self.prisoners = [] # список заключенных девушек
        self.free_list = [] # список свободных девушек
        self.spawn = []     # список отродий, приходящих после пробуждения 
    
    def new_girl (self, type = 'peasant'):
        """
        Генерация новой девушки указанного типа.
        """
        self.game.girl = core.Girl(gameRef=self.game, base_character=self.character)
        self.game.girl.type = type
        relative_path = "img/avahuman/"+girls_data.girls_info[type]['avatar'] # Относительный путь для движка ренпи
        absolute_path = os.path.join(renpy_internal.config.basedir, "game", relative_path) # Cоставляем абсолютный путь где искать
        filename = random.choice(os.listdir(absolute_path)) # получаем название файла
        self.game.girl.avatar = relative_path + "/" + filename # Возвращаем правильно отформатированное значение
        self.game.girl.name = random.choice(girls_data.girls_names[type])
        return self.description('new')
        
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
        return self.description('sex')
        
    def free_girl(self):
        """
        Выпустить текущую девушку на свободу.
        """
        #девушка отслеживается только если беременна
        if self.game.girl.pregnant:
            self.free_list.append(self.game.girl)
        return self.description('free')
        
    def free_all_girls(self):
        """
        Выпустить на свободу всех девушек.
        """
        for girl_i in reversed(xrange(self.prisoners_count())):
            self.game.girl = self.prisoners[girl_i]
            if self.game.girl.pregnant:
                self.free_list.append(self.game.girl)
        self.prisoners = []
        
    def steal_girl(self):
        return self.description('steal')
        
    def jail_girl(self):
        """
        Посадить текущую девушку за решетку.
        """
        if self.game.girl.jailed:
            text = self.description('jailed')
        else:
            text = self.description('jail')
            self.game.girl.jailed = True
        self.prisoners.append(self.game.girl)
        return text
        
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
        if self.game.dragon.lust < 3: self.game.dragon.lust += 1
        self.game.dragon.bloodiness = 0
        return self.description('eat')
        
    def rob_girl(self):
        #TODO реальное ограбление с описанием награбленного
        return self.description('rob')
        
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
        
    def description(self, status, say=False):
        """
        Генерация описания ситуации для текущей девушки (self.game.girl).
        status - кодовое описание ситуации
        say - если истина - описание выводится сразу на экран, возвращается None, если ложь - возвращается текст описания
        """
        girl_type = self.game.girl.type
        if girl_type not in girls_data.girls_texts or \
           status not in girls_data.girls_texts[girl_type]:
            girl_type = 'girl'
        if girls_data.girls_texts[girl_type][status]:
            text = random.choice(girls_data.girls_texts[girl_type][status]) 
            text = text.format(*[self.game.girl.name, self.game.dragon.name])
        else: 
            text = "Описание для действия '%s' девушки типа '%s' отсутствует" % (status, self.game.girl.type)
        if say:
            store.nvl_list = [ ] #вариант nvl clear на питоне
            renpy.say(self.game.girl.third, text) #выдача сообщения
        else:
            return text
        
    def next_year(self):
        """
        Все действия с девушками за год.
        """        
        #плененные девушки
        for girl_i in reversed(xrange(self.prisoners_count())):
            self.game.girl = self.prisoners[girl_i]
            #попытка побега
            if (random.randint(1,2) == 1) and self.game.lair.reachable([]) and \
               'regular_guards' not in self.game.lair.modifiers and \
               'elite_guards' not in self.game.lair.modifiers:
                #девушка сбежала из камеры
                del self.prisoners[girl_i]
                if 'mechanic_traps' in self.game.lair.modifiers or \
                   'magic_traps' in self.game.lair.modifiers:
                    self.description('traps', True) #описание гибели в ловушке
                else:
                    self.description('escape', True)#описание чудесного спасения
                    if self.game.girl.pregnant: self.free_list.append(self.game.girl)
            else:
                #девушка не убежала
                if ('servant' in self.game.lair.modifiers) or ('gremlin' in self.game.lair.modifiers):
                    if self.game.girl.pregnant:
                        self.description('birth', True)  #описание родов
                        if self.game.girl.pregnant == 1:
                            self.spawn.append(girls_data.girls_info[self.game.girl.type]['regular_spawn'])
                        else:
                            self.spawn.append(girls_data.girls_info[self.game.girl.type]['advanced_spawn'])
                        self.game.girl.pregnant = 0
                else:
                    self.description('hunger', True)  #описание смерти от голода      
                    del self.prisoners[girl_i]
        #свободные, в том числе только что сбежавшие
        for girl_i in xrange(len(self.free_list)):
            self.game.girl = self.free_list[girl_i]
            if (random.randint(1,3) == 1) and not girls_data.girls_info[self.game.girl.type]['giantess']:
                self.description('kill', True) #убивают из-за беременности
            else:
                self.description('free_birth', True) #рожает на свободе
                self.free_spawn()
        self.free_list = [] #очистка списка - либо родила, либо убили - отслеживать дальше не имеет смысла
            
                    
    def before_sleep(self):
        """
        Все действия до начала сна - смерть с тоски, может быть что-то еще?
        """
        for girl_i in reversed(xrange(self.prisoners_count())):
            self.game.girl = self.prisoners[girl_i]
            if (not self.game.girl.virgin) and (not self.game.girl.pregnant):
                self.description('anguish', True) #умирает c тоски
                del self.prisoners[girl_i]
    
    def after_awakening(self):
        """
        Все действия после пробуждения - разбираемся с воспитанными отродьями.
        """
        for spawn_i in xrange(len(self.spawn)):
            spawn_mod = girls_data.spawn_info[self.spawn[spawn_i]]['modifier']
            spawn_menu = []
            spawn_menu.append((u"К Вам приходит %s и просит назначения" % girls_data.spawn_info[self.spawn[spawn_i]]['name'], None))
            if ('poisonous' in spawn_mod) and ('poison_guards' not in self.game.lair.modifiers):
                spawn_menu.append((u"Выпустить в логово", 'poison_guards')) 
            if ('servant' in spawn_mod) and ('servant' not in self.game.lair.modifiers):
                spawn_menu.append((u"Сделать слугой", 'servant'))
            if ('warrior' in spawn_mod) and ('regular_guards' not in self.game.lair.modifiers):
                spawn_menu.append((u"Сделать охранником", 'regular_guards'))
            if ('elite' in spawn_mod) and ('elite_guards' not in self.game.lair.modifiers):
                spawn_menu.append((u"Сделать элитным охранником", 'elite_guards'))
            spawn_menu.append((u"Выпустить в королевство", 'free'))
            if (('servant' in spawn_mod) or ('warrior' in spawn_mod) or ('elite' in spawn_mod)) and ('marine' not in spawn_mod):
                spawn_menu.append((u"Отправить в армию тьмы", 'army_of_darkness'))
            menu_action = renpy.display_menu(spawn_menu)
            if menu_action == 'free':
                renpy.say(self.game.narrator, u"%s отправляется бесчинствовать в королевстве" % girls_data.spawn_info[self.spawn[spawn_i]]['name'])
                self.free_spawn()
            elif menu_action == 'army_of_darkness':
                renpy.say(self.game.narrator, u"%s отправляется в армию тьмы" % girls_data.spawn_info[self.spawn[spawn_i]]['name'])
                self.army_of_darkness()
            else:
                self.game.lair.modifiers.append(menu_action)
                renpy.say(self.game.narrator, u"%s приступает к выполнению обязанностей" % girls_data.spawn_info[self.spawn[spawn_i]]['name']) #выдача сообщения
                # TODO: добавление не только в список модификаторов, но и в список апргрейда логова
      
    def free_spawn(self):
        """
        Действия отродий на свободе
        # TODO: реализовать снижение мобилизации королевства
        """
        pass
      
    def army_of_darkness(self):
        """
        Отправка в армию тьмы
        # TODO: реализовать отправку в армию тьмы, когда будет понятно что это такое
        """
        pass