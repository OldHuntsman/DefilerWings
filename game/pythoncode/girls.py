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
        self.active = 0 # номер текущей девушки
        self.offspring = [] # типы потомков для выполнения квеста
    
    def new_girl (self, type = 'peasant'):
        """
        Генерация новой девушки указанного типа.
        """
        self.game.girl = core.Girl(gameRef=self.game, base_character=self.character)
        self.game.girl.type = type
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
        self.game.girl.treasure = self.gen_tres()
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
        obtained = u"Принадлежало красавице по имени %s" % self.game.girl.name
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
            self.prisoners.insert(self.active, self.game.girl)
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
        self.active = index
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
        rob_description = self.description('rob')
        self.game.lair.treasury.receive_treasures(self.game.girl.treasure)
        self.game.girl.treasure = []
        return rob_description
        
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
            elif status == 'rob':
                treas_description = self.game.lair.treasury.treasures_description(self.game.girl.treasure)
                treas_description = '\n'.join(treas_description)
                insert_list.append(treas_description)
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
               'regular_guards' not in self.game.lair.upgrades and \
               'elite_guards' not in self.game.lair.upgrades:
                #девушка сбежала из камеры
                del self.prisoners[girl_i]
                if 'mechanic_traps' in self.game.lair.upgrades or \
                   'magic_traps' in self.game.lair.upgrades:
                    self.description('traps', True) #описание гибели в ловушке
                else:
                    self.description('escape', True)#описание чудесного спасения
                    if self.game.girl.pregnant: self.free_list.append(self.game.girl)
            else:
                #девушка не убежала
                if ('servant' in self.game.lair.upgrades) or ('gremlin_servant' in self.game.lair.upgrades):
                    if self.game.girl.pregnant:
                        girl_type = girls_data.girls_info[self.game.girl.type]
                        
                        spawn_class = 'regular_spawn' if self.game.girl.pregnant == 1 else 'advanced_spawn' 
                        if 'educated_spawn' not in self.offspring: self.offspring.append('educated_spawn')
                        girl_size = 'giantess' if girl_type['giantess'] else 'usual_size'
                        if girl_size not in self.offspring: self.offspring.append(girl_size)
                        
                        self.spawn.append(girl_type[spawn_class])
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
                girl_type = girls_data.girls_info[self.game.girl.type]
                
                spawn_class = 'regular_spawn' if self.game.girl.pregnant == 1 else 'advanced_spawn' 
                if 'free_spawn' not in self.offspring: self.offspring.append('free_spawn')
                girl_size = 'giantess' if girl_type['giantess'] else 'usual_size'
                if girl_size not in self.offspring: self.offspring.append(girl_size) 
                
                spawn_type = girls_data.girls_info[self.game.girl.type][spawn_class]
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
            if ('poisonous' in spawn_mod) and ('poison_guards' not in self.game.lair.upgrades) and marine_check:
                spawn_menu.append((u"Выпустить в логово", 'poison_guards')) 
            if ('servant' in spawn_mod) and ('servant' not in self.game.lair.upgrades) and marine_check:
                spawn_menu.append((u"Сделать слугой", 'servant'))
            if ('warrior' in spawn_mod) and ('regular_guards' not in self.game.lair.upgrades) and marine_check:
                spawn_menu.append((u"Сделать охранником", 'regular_guards'))
            if ('elite' in spawn_mod) and ('elite_guards' not in self.game.lair.upgrades) and marine_check:
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
                self.army_of_darkness(spawn_type)
            else:
                renpy.say(self.game.narrator, u"%s приступает к выполнению обязанностей" % spawn['name']) #выдача сообщения
                self.game.lair.upgrades.add(menu_action, deepcopy(data.lair_upgrades[menu_action])) #добавление в улучшение логова
        self.spawn = []
      
    def free_spawn(self, power):
        """
        Действия отродий на свободе
        """
        #TODO: Что тут вообще имелось ввиду? Очков мобилизации теперь нет. Зато есть разруха.
        #self.game.mobilization.points -= power
        pass
      
    def army_of_darkness(self, warrior_type):
        """
        Отправка в армию тьмы
        """
        self.game.army.add_warrior(warrior_type)
    
    @property
    def is_mating_possible(self):
        """
        Возвращает возможность совокупления - истину или ложь.
        # TODO: проверка на превращение в человека
        """
        assert self.game.girl, "Girl not found"
        mating_possible = self.game.girl.virgin and self.game.dragon.lust > 0
        if girls_data.girls_info[self.game.girl.type]['giantess']:
            mating_possible = self.game.dragon.size() > 3 and mating_possible
        else:
            mating_possible = self.game.dragon.size() < 5 and mating_possible
        return mating_possible