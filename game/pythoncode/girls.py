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
from copy import deepcopy
from treasures import gen_treas

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
        self.game.girl.treasure = self.gen_tres()
        # создание аватарки
        relative_path = "img/avahuman/"+girls_data.girls_info[type]['avatar'] # Относительный путь для движка ренпи
        absolute_path = os.path.join(renpy_internal.config.basedir, "game", relative_path) # Cоставляем абсолютный путь где искать
        filename = random.choice(os.listdir(absolute_path)) # получаем название файла
        self.game.girl.avatar = relative_path + "/" + filename # Возвращаем правильно отформатированное значение
        # генерация имени
        if type + '_last' in girls_data.girls_names:
            self.game.girl.name = (u"%s %s") % (random.choice(girls_data.girls_names[type + '_first']), random.choice(girls_data.girls_names[type+ '_last']))
        else:
            if type + '_first' in girls_data.girls_names:
                self.game.girl.name = random.choice(girls_data.girls_names[type + '_first'])
            else:
                self.game.girl.name = 'Неизвестная Красавица'
        return self.description('new')

    def gen_tres(self):
        """
        Создание списка индивидуальных сокровищ для текущей девушки
        """
        type = self.game.girl.type # упрощение обращения к типу девушки
        girl_info = girls_data.girls_info[type] # упрощение обращения к информации для данного типа девушки
        count = random.randint(girl_info['t_count_min'], girl_info['t_count_max'])
        t_list = girl_info['t_list']
        alignment = girl_info['t_alignment']
        min_cost = girl_info['t_price_min']
        max_cost = girl_info['t_price_max']
        obtained = "Принадлежало красавице по имени %s" % self.game.girl.name
        return gen_treas(count, t_list, alignment, min_cost, max_cost, obtained)
        
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
        if self.game.girl.jailed:
            return self.description('free_prison')
        else:
            return self.description('free')
        
    def free_all_girls(self):
        """
        Выпустить на свободу всех девушек.
        """
        for girl_i in reversed(xrange(self.prisoners_count)):
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
        """
        Ограбить девушку.
        """
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
    
    @property
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
            # TODO: Ситуативные описания
            insert_list = [self.game.girl.name, self.game.dragon.name]
            if status == 'birth':
                insert_list.append(girls_data.spawn_info[self.spawn[-1]]['name'])
            text = text.format(*insert_list)
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
        for girl_i in reversed(xrange(self.prisoners_count)):
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
                        if self.game.girl.pregnant == 1:
                            self.spawn.append(girls_data.girls_info[self.game.girl.type]['regular_spawn'])
                        else:
                            self.spawn.append(girls_data.girls_info[self.game.girl.type]['advanced_spawn'])
                        self.description('birth', True)  #описание родов
                        self.game.girl.pregnant = 0
                else:
                    self.description('hunger', True)  #описание смерти от голода      
                    del self.prisoners[girl_i]
        #свободные, в том числе только что сбежавшие. Отслеживаются только беременные
        for girl_i in xrange(len(self.free_list)):
            self.game.girl = self.free_list[girl_i]
            if (random.randint(1,3) == 1) and not girls_data.girls_info[self.game.girl.type]['giantess']:
                self.description('kill', True) #убивают из-за беременности
            else:
                if self.game.girl.pregnant == 1:
                    spawn_type = girls_data.girls_info[self.game.girl.type]['regular_spawn']
                else:
                    spawn_type = girls_data.girls_info[self.game.girl.type]['advanced_spawn']
                spawn = girls_data.spawn_info[spawn_type] 
                self.description('free_birth', True) #рожает на свободе
                self.free_spawn(spawn['power'])
        self.free_list = [] #очистка списка - либо родила, либо убили - отслеживать дальше не имеет смысла
                               
    def before_sleep(self):
        """
        Все действия до начала сна - смерть с тоски, может быть что-то еще?
        """
        for girl_i in reversed(xrange(self.prisoners_count)):
            self.game.girl = self.prisoners[girl_i]
            if (not self.game.girl.virgin) and (not self.game.girl.pregnant):
                self.description('anguish', True) #умирает c тоски
                del self.prisoners[girl_i]
    
    def after_awakening(self):
        """
        Все действия после пробуждения - разбираемся с воспитанными отродьями.
        """
        for spawn_i in xrange(len(self.spawn)):
            spawn_type = self.spawn[spawn_i] #упрощение обращения к типу отродий
            spawn = girls_data.spawn_info[spawn_type] #упрощение обращения к данным отродий
            spawn_mod = spawn['modifier'] #упрощение обращения к списку модификаторов отродий
            marine_check = ('marine' not in spawn_mod) or (self.game.lair.type.require and 'swimming' in self.game.lair.type.require) #истина, если не морское отродье или морское в подводном логове
            spawn_menu = [] #меню отродий
            spawn_menu.append((u"К Вам приходит %s и просит назначения" % spawn['name'], None)) #заголовок меню
            #Возможные пункты меню
            if ('poisonous' in spawn_mod) and ('poison_guards' not in self.game.lair.modifiers) and marine_check:
                spawn_menu.append((u"Выпустить в логово", 'poison_guards')) 
            if ('servant' in spawn_mod) and ('servant' not in self.game.lair.modifiers) and marine_check:
                spawn_menu.append((u"Сделать слугой", 'servant'))
            if ('warrior' in spawn_mod) and ('regular_guards' not in self.game.lair.modifiers) and marine_check:
                spawn_menu.append((u"Сделать охранником", 'regular_guards'))
            if ('elite' in spawn_mod) and ('elite_guards' not in self.game.lair.modifiers) and marine_check:
                spawn_menu.append((u"Сделать элитным охранником", 'elite_guards'))
            spawn_menu.append((u"Выпустить в королевство", 'free'))
            if (('servant' in spawn_mod) or ('warrior' in spawn_mod) or ('elite' in spawn_mod)) and ('marine' not in spawn_mod):
                spawn_menu.append((u"Отправить в армию тьмы", 'army_of_darkness'))
                
            menu_action = renpy.display_menu(spawn_menu)
            
            if menu_action == 'free':
                renpy.say(self.game.narrator, u"%s отправляется бесчинствовать в королевстве" % spawn['name'])
                self.free_spawn(spawn['power'])
            elif menu_action == 'army_of_darkness':
                renpy.say(self.game.narrator, u"%s отправляется в армию тьмы" % spawn['name'])
                self.army_of_darkness()
            else:
                self.game.lair.modifiers.append(menu_action) #добавление в модификатор логова
                renpy.say(self.game.narrator, u"%s приступает к выполнению обязанностей" % spawn['name']) #выдача сообщения
                if menu_action <> 'servant':
                    self.game.lair.upgrades.add(menu_action, deepcopy(data.lair_upgrades[menu_action])) #добавление в улучшение логова
        self.spawn = []
        if 'gremlin' in self.game.lair.modifiers:
            self.game.lair.modifiers.remove('gremlin')
      
    def free_spawn(self, power):
        """
        Действия отродий на свободе
        """
        self.game.mobilization.points -= power
      
    def army_of_darkness(self):
        """
        Отправка в армию тьмы
        # TODO: реализовать отправку в армию тьмы, когда будет понятно что это такое
        """
        pass
        
    def inteructions(self):
        """
        Реализация меню для взаимодействий с девушками
        """
        while self.game.girl:
            girls_menu = [] #меню взаимодействий с девушками
            if self.game.girl.virgin and self.game.dragon.lust > 0:
                girls_menu.append((u"Надругаться", 'impregnate'))
            if self.game.dragon.hunger > 0:
                girls_menu.append((u"Сожрать", 'eat_girl'))
            girls_menu.append((u"Отпустить", 'free_prison'))
            girls_menu.append((u"Вернуть в клетку", 'jail_girl'))
            
            menu_action = renpy.display_menu(girls_menu)
            
            if menu_action == 'impregnate':
                girl_text = self.impregnate()
            elif menu_action == 'eat_girl':
                girl_text = self.eat_girl()
            elif menu_action == 'free_prison':
                girl_text = self.free_girl()
            else:
                girl_text = self.jail_girl()
            renpy.say(self.game.girl.third, girl_text)
            if not (menu_action == 'impregnate'): return
        
    def prison(self):
        """
        Реализация меню для девушек в заключении.
        """
        prison_index = 0
        cell_capacity = 10 # вместимость клетки - сколько будет отображается девушек в одном меню
        #пока кто-то есть в заключении, выполняем цикл
        while self.prisoners_count:
            girls_menu = [] #меню девушек
            if prison_index > 0: #мы находимся не в первой клетке, добавляем переход к предыдущей
                girls_menu.append((u"Предыдущая клетка", 'prev'))
            if self.prisoners_count - prison_index - cell_capacity <= 0: #количество девушек в меню
                menu_count = self.prisoners_count - prison_index
            else:
                menu_count = cell_capacity
            for girl_i in xrange(menu_count): #заполняем меню именами девушек
                girls_menu.append((self.prisoners[prison_index + girl_i].name, girl_i))
            if prison_index + cell_capacity < self.prisoners_count: #мы находимся не в последней клетке, добавляем переход к следующей
                girls_menu.append((u"Следующая клетка", 'next'))
            girls_menu.append((u"Покинуть темницу", 'return')) #выход
            
            menu_action = renpy.display_menu(girls_menu)
            
            if menu_action == 'prev':
                prison_index -= cell_capacity #отнимаем вместимость клетки
                if prison_index < 0: prison_index = 0 #если получилось меньше 0, ставим 0. Вообще такого не должно быть
            elif menu_action == 'next':
                prison_index += cell_capacity #прибавляем вместимость клетки
            elif menu_action == 'return':
                return
            else:
                self.set_active(prison_index + menu_action)
                self.description('prison', True)
                self.inteructions()
                if self.prisoners_count == prison_index: prison_index -= cell_capacity