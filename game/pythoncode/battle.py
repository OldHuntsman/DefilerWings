#!/usr/bin/env python
# coding=utf-8
from core import Sayer
import random
import math
import data
import copy
import core
from data import get_modifier
from core import tuples_sum

def calc_hit_def(hitdef):
    """
    вспомогательная функция для вычисления попадания
    :param hitdef: словарь с атакой либо защитой
    :return: значение атаки либо защиты
    """
    value = sum(hitdef[key][1] for key in hitdef)
    for attacks in range(1,sum(hitdef[key][0] for key in hitdef) +1):
        dice = random.randint(1,3)
        if dice ==1:
            value +=1
    return value

def battle_action(dragon, foe):
    """
    логика сражения.
    :param dragon: текущий дракон
    :param    foe: текущий противник
    :return: список, описывающий состояние боя
    """
    status = []
    #проверяем атаку дракона
    power = dragon.attack()
    immun = foe.immunity()
    #пробегаем все ключи словаря атаки дракона
    for key in power.keys():
        (r, p) = power[key]
        if (not (r + p)) or (key in immun):
            #удаляем нулевые атаки и те, к которым у противника иммунитет
            del power[key]
        else:
            #записываем чем дракон мог ударить в статус раунда боя
            status.append('dragon_' + key) 
    #проверяем, если атака больше защиты - противника съели, иначе он еще жив
    dragon_hit = calc_hit_def(power)
    foe_defence = calc_hit_def(foe.protection())
    if dragon_hit > foe_defence:
        status.append('foe_dead')
    else:
        status.append('foe_alive')
    #полностью зеркальная ситуация для атаки противника
    power = foe.attack()
    immun = dragon.immunity()
    #пробегаем все ключи словаря атаки противника
    for key in power.keys():
        (r, p) = power[key]
        if (not (r + p)) or (key in immun):
            #удаляем нулевые атаки и те, к которым у дракона иммунитет
            del power[key]
        else:
            #записываем чем противник мог ударить в статус раунда боя
            status.append('foe_' + key) 
    #проверяем, если атака противника больше защиты дракона - дракон ранен
    foe_hit = calc_hit_def(power)
    dragon_defence = calc_hit_def(dragon.protection())
    if foe_hit > dragon_defence:
        status.extend(dragon.struck())
    else:
        status.append('dragon_undamaged')
    return status          
    
        
def check_fear(dragon, foe):
    """
    Проверяет не превышает ли страх дракона сумму защиты и атаки противника
    :param dragon: текущий дракон
    :param foe: текущий противник дракона
    :return: ['foe_intro', 'foe_alive'] если противник преодолел страх, если не смог - ['foe_fear', 'foe_dead']
    """
    fear = dragon.fear()
    power = foe.attack()
    total = 0
    for key in power:
        (r, p) = power[key]
        total += r + p 
    protect = foe.protection()
    for key in protect:
        (r, p) = protect[key]
        total += r + p 
    if fear > total:
        return ['foe_fear', 'foe_dead']
    else:
        return ['foe_intro', 'foe_alive']

def test_dragon_gen(test_game, test_character, level):  
    """
    Тестовая функция для генерации случайного дракона с уровнем level 
    """
    test_dragon = core.Dragon(gameRef=test_game, base_character=test_character)
    for lvl_i in range(1, level - 1):
        test_dragon = test_dragon.children()[0]
    return test_dragon