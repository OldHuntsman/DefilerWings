#!/usr/bin/env python
# coding=utf-8
import random


def calc_hit_def(hitdef):
    """
    вспомогательная функция для вычисления попадания
    :param hitdef: словарь с атакой либо защитой
    :return: значение атаки либо защиты
    """
    value = sum(hitdef[key][1] for key in hitdef)
    for attacks in range(1, sum(hitdef[key][0] for key in hitdef) + 1):
        dice = random.randint(1, 3)
        if dice == 1:
            value += 1
    return value


def battle_action(dragon, foe):
    """
    логика сражения.
    :param dragon: текущий дракон
    :param    foe: текущий противник
    :return: список, описывающий состояние боя
    """
    status = []
    # проверяем атаку дракона
    power = dragon.attack()
    immun = foe.immunity()
    # пробегаем все ключи словаря атаки дракона
    for key in power.keys():
        (r, p) = power[key]
        if (not (r + p)) or (key in immun):
            # удаляем нулевые атаки и те, к которым у противника иммунитет
            del power[key]
        else:
            # записываем чем дракон мог ударить в статус раунда боя
            status.append('dragon_' + key)
            # проверяем, если атака больше защиты - противника съели, иначе он еще жив
    dragon_hit = calc_hit_def(power)
    foe_defence = calc_hit_def(foe.protection())
    if dragon_hit > foe_defence:
        foe.die()
        status.append('foe_dead')
    else:
        status.append('foe_alive')
    # полностью зеркальная ситуация для атаки противника
    power = foe.attack()
    immun = dragon.immunity()
    # пробегаем все ключи словаря атаки противника
    for key in power.keys():
        (r, p) = power[key]
        if (not (r + p)) or (key in immun):
            # удаляем нулевые атаки и те, к которым у дракона иммунитет
            del power[key]
        else:
            # записываем чем противник мог ударить в статус раунда боя
            status.append('foe_' + key)
            # проверяем, если атака противника больше защиты дракона - дракон ранен
    foe_hit = calc_hit_def(power)
    dragon_defence = calc_hit_def(dragon.protection())
    if foe_hit > dragon_defence:
        status.extend(dragon.struck())
    else:
        status.append('dragon_undamaged')
    return status


def chance_list(size):
    """
    Построение честного списка выпадения значений.
    """
    if size < 0:
        return [1]  # защита, вообще такого быть не должно
    gen_list = [1L] + [0] * size
    for gen_i in xrange(size):
        sub_list = list(gen_list)
        for sub_i in xrange(gen_i + 1):
            gen_list[sub_i] += sub_list[sub_i]  # удвоение шанса для выпадения 0
            gen_list[sub_i + 1] += sub_list[sub_i]  # выпадение единицы
    return gen_list


def brute_chance(balance, attack, defence):
    """
    Честный расчет вероятности.
    """
    # расчет дополнения к функции распределения атаки
    attack_list = chance_list(attack)
    summ = sum(attack_list)
    residue = 0.0
    for attack_i in reversed(xrange(len(attack_list))):
        residue += attack_list[attack_i]
        attack_list[attack_i] = residue / summ
    # расчет плотности вероятности защиты
    defence_list = chance_list(defence)
    summ = float(sum(defence_list))
    defence_list = [a / summ for a in defence_list]
    # расчет шанса
    victory = 0.0
    for defence_i in xrange(len(defence_list)):
        attack_i = max(min(defence_i - balance + 1, len(attack_list)), 0)
        if attack_i < len(attack_list):
            victory += defence_list[defence_i] * attack_list[attack_i]
    return victory


def victory_chance(objective, foe):
    """
    Расчет вероятности победы.
    :param objective: для кого считается шанс победы
    :param    foe: текущий противник
    :return: вероятность победы в процентах
    """
    power = objective.attack()
    immun = foe.immunity()
    defence = foe.protection()
    # вычисляем атаку
    regular_attack = 0
    perfect_attack = 0
    for key in power.keys():
        if key not in immun:
            (r, p) = power[key]
            regular_attack += r
            perfect_attack += p
    # вычисляем защиту
    regular_defence = 0
    perfect_defence = 0
    for key in defence.keys():
        (r, p) = defence[key]
        regular_defence += r
        perfect_defence += p
    # вычисляем вероятность победы
    if perfect_attack + regular_attack < perfect_defence:
        return 0  # верную защиту невозможно пробить, победа невозможна
    elif perfect_attack > regular_defence + perfect_defence:
        return 100  # от верной атаки невозможно защититься, победа очевидна
    else:
        return int(brute_chance(perfect_attack - perfect_defence, regular_attack, regular_defence) * 100)


def practic_dragon_chance(dragon, foe):
    """
    Оценка вероятности победы на практике.
    ТОЛЬКО ДЛЯ ТЕСТА, слишком медленно
    """
    count = 100000
    drag_win = 0.0
    drag_wounded = float(count)
    for test_i in xrange(count):
        drag = dragon.deepcopy()
        rslt = battle_action(drag, foe)
        if 'foe_dead' in rslt:
            drag_win += 1
        if 'dragon_undamaged' in rslt:
            drag_wounded -= 1
    return "%d %% %d %%" % (int(100 * drag_win / count), int(100 * drag_wounded / count))


def check_fear(dragon, foe):
    """
    Проверяет не превышает ли страх дракона сумму защиты и атаки противника
    :param dragon: текущий дракон
    :param foe: текущий противник дракона
    :return: ['foe_intro', 'foe_alive'] если противник преодолел страх, если не смог - ['foe_fear', 'foe_dead']
    """
    fear = dragon.fear
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
