# coding=utf-8

import random

from data import achieve_target
        
army_battle = False

def calc_hit_def(hitdef):
    """
    secondary function for hit chance calculations
    :param hitdef: dictionary with attack of defense
    :return: attack or defense value
    """
    value = sum(hitdef[key][1] for key in hitdef)
    for attacks in range(1, sum(hitdef[key][0] for key in hitdef) + 1):
        dice = random.randint(1, 3)
        if dice == 1:
            value += 1
    return value


def battle_action(dragon, foe):
    """
    combat logic.
    :type dragon: Dragon
    :param dragon: current dragon
    :type foe: Enemy
    :param foe: current enemy
    :return: list which describes battle status
    """
    status = []
    # check dragon's attack
    power = dragon.attack()
    immun = foe.immunity()
    # check each key of the dragon's attack dictionary
    for key in power.keys():
        (r, p) = power[key]
        if (not (r + p)) or (key in immun):
            # removing null attacks and attacks enemy is immune to
            del power[key]
        else:
            # record things that dragon could attack with to a battle status
            status.append('dragon_' + key)
            # check if dragon's attack is over foe's protection, if yes foe has been eaten by dragon
    dragon_hit = calc_hit_def(power)
    foe_defence = calc_hit_def(foe.protection())
    if dragon_hit > foe_defence:
        achieve_target(foe.name, "kill")    # achievement event
        foe.die()
        status.append('foe_dead')
    else:
        status.append('foe_alive')
    # now same as before, but for foe's attack
    power = foe.attack()
    immun = dragon.immunity()
    # check each key of the foe's attack dictionary
    for key in power.keys():
        (r, p) = power[key]
        if (not (r + p)) or (key in immun):
            # removing null attacks and attacks dragon is immune to
            del power[key]
        else:
            # record things that foe could attack with to a battle status
            status.append('foe_' + key)
            # check if foe's attack if over dragon's protection, if yes dragon is wounded
    foe_hit = calc_hit_def(power)
    dragon_defence = calc_hit_def(dragon.protection())
    if foe_hit > dragon_defence:
        # If enemy decapitates dragon without wounds.
        if 'decapitator' in foe.modifiers():
            status.extend(dragon.decapitate())
        # Else just wounds.
        else:
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
    Straight probability calculation.
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
    Chance of victory calculation.
    :param objective: для кого считается шанс победы
    :param    foe: текущий противник
    :return: вероятность победы в процентах
    """
    # вычисляем атаку
    immun = foe.immunity()
    power = objective.attack_strength(immun)
    regular_attack = power[0]
    perfect_attack = power[1]
    # вычисляем защиту
    defence = foe.defence_power()
    regular_defence = defence[0]
    perfect_defence = defence[1]
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
    Too slow, just for tests
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
    Check if dragon's fear is more than foe's attack+protection
    :param dragon: current dragon
    :param foe: current foe
    :return: ['foe_intro', 'foe_alive'] if foe overcomes fear, else - ['foe_fear', 'foe_dead']
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
        foe.die()
        return ['foe_fear', 'foe_dead']
    else:
        return ['foe_intro', 'foe_alive']
