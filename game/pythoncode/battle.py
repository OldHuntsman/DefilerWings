#!/usr/bin/env python
# coding=utf-8
from core import Sayer
import random
import math
import data
import copy
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
        if (not r + p) or (key in immun):
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
        if (not r + p) or (key in immun):
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
    
class Fighter(Sayer):
    """
    Базовый класс для всего, что способно драться.
    Декоратор нужен чтобы реализовывать эффекты вроде иммунитета или ядовитого дыхания.
    То есть такие, которые воздействуют на модификаторы противника.
    """

    def __init__(self, *args, **kwargs):
        """
        :param gameRef: Game object
        """
        super(Fighter, self).__init__(*args, **kwargs)
        self._modifiers = []
        self.descriptions = [] #По умолчанию список описаний пуст
        self.avatar = None # По умолчанию аватарки нет, нужно выбрать в потомках.
        self.name = u""

    def protection(self):
        """
        :rtype : dict
        :return: Значение защиты данного бойца в виде котртежа (защита, верная защита).
        """
        result = dict()
        for type in data.protection_types:
            result[type] = tuples_sum(
                [get_modifier(mod).protection[1]
                 for mod in self.modifiers()
                 if get_modifier(mod).protection[0] == type]
            )
        return result

    def attack(self):
        """
        :rtype : dict
        :return: Словарик, ключами которого являются типы атаки(лед, огонь, яд...),
        а значениями кортежи вида (атака, верная атака)
        """
        result = dict()
        for type in data.attack_types:
            result[type] = tuples_sum(
                [get_modifier(mod).attack[1]
                 for mod in self.modifiers()
                 if get_modifier(mod).attack[0] == type]
            )
        return result
    
    def immunity(self):
        """
        :return: Список типов атаки(лед, огонь, яд...), к которым у данного бойца иммунитет
        """
        return []
        
    def battle_description (self, status, dragon):
        """
        :param status: список, описывающий состояние боя
        :param dragon: ссылка на дракона, выступающего противником
        :return: текстовое описание боя
        """
        desc_list = [] #список для возможных описаний момента боя
        curr_round = 100 #переменная для определения наимее использовавшегося описания
        #цикл по всем индексам списка self.descriptions
        for desc_i in range(len(self.descriptions)):
            #получаем список переменных для строки описания из списка
            (require, desc_str, insertion, round) = self.descriptions[desc_i]
            #определяем подходит ли описание для текущего статуса
            desc_need = round <= curr_round #предварительно проверяем на количество использований
            for req in require:
                desc_need = (req in status) and desc_need
            if desc_need:
                if round < curr_round:  
                    curr_round = round  #выбираем наименьшее число использований описания
                    desc_list = []      #все предыдущие описания использовались чаще, очищаем список
                #вставляем необходимые данные в описание 
                insert_list = []
                for ins in insertion:
                    if ins == 'foe_name':
                        insert_list.append(self.name)
                    elif ins == 'dragon_name':
                        insert_list.append(dragon.name)
                desc_str = desc_str.format(*insert_list)
                #добавляем в список для описаний            
                desc_list.append([desc_str, desc_i])
        if desc_list:
            #выбираем случайное описание
            dice = random.randint(0, len(desc_list) - 1)
            desc = desc_list[dice]
            self.descriptions[desc[1]][3] += 1 #увеличиваем число использований этого описания
            return desc[0]
        else:
            return status #список описаний пуст, возвращаем информацию для дебага
        
class Dragon(Fighter):
    """
    Класс дракона.
    """

    def __init__(self, *args, **kwargs):
        super(Dragon, self).__init__(*args, **kwargs)
        # TODO: нужно дать игроку возможность называть своего дракона при первом выборе выборе и давать следующим драконом это имя как фамильное после рандомного личного
        self.name = u"Старый Охотник"
        self._tiredness = 0  # увеличивается при каждом действии
        self.bloodiness = 0  # range 0..5
        self.lust = 3  # range 0..3, ресурс восстанавливается до 3 после каждого отдыха
        self.hunger = 3  # range 0..3, ресурс восстанавливается до 3 после каждого отдыха
        self.health = 2 # range 0..2, ресурс восстанавливается до 2 после каждого отдыха
        self.reputation_points = 1 # при наборе определённого количества растёт уровень дурной славы

        self.anatomy = ['size', 'paws', 'size', 'wings', 'size', 'paws']
        self.heads = ['green']  # головы дракона
        self.dead_heads = [] #мертвые головы дракона
        self.spells = []  # заклинания наложенные на дракона(обнуляются после сна)
        self.avatar = "img/avadragon/green/1.jpg"

    def _debug_print(self):
        # self(u'Дракон по имени {0}'.format(self.name))
        # self(u'Список всех модификаторов {0}'.format(', '.join(self.modifiers())))
        # self(u'Вид дракона {0}'.format(self.kind()))
        # self(u'Размер {0}'.format(data.size_texts[self.size()]))
        # self(u'Анатомия дракона {0}'.format(', '.join(self.anatomy)))
        # self(u'Наложенная на дракона магия {0}'.format(' '.join(self.spells)))
        # self(u'Цвета голов дракона {0}'.format(', '.join(self.heads)))
        # self(u'Энергия {0} из {1}'.format(self.energy(), self.max_energy()))
        # self(u'Могущество {0}'.format(', '.join(['{0} {1}'.format(k, v) for k, v in self.attack().items()])))
        # self(u'Несокрушимость {0}'.format(', '.join(['{0} {1}'.format(k, v) for k, v in self.protection().items()])))
        # self(u'Коварство {0}'.format(self.magic()))
        # self(u'Чудовищиность {0}'.format(self.fear()))
        children = self.children()
        for child in children:
            self(u'Ребенок {0}'.format(', '.join(child.anatomy[-3:] + child.heads)))


    def modifiers(self):
        """
        :return: Список модификаторов дракона
        """
        return self.anatomy + \
               [mod for head_color in self.heads for mod in data.dragon_heads[head_color]] + \
               [mod for spell in self.spells for mod in data.spell_list[spell]]

    def max_energy(self):
        """
        :return: Максимальная энергия(целое число)
        """
        return sum([get_modifier(mod).max_energy for mod in self.modifiers()])

    def energy(self):
        """
        :return: Оставшаяся энергия(целое число)
        """
        return self.max_energy() - self._tiredness
        
    def drain_energy(self, drain=1):
        """
        :param drain: количество отнимаемой у дракона энергии.
        :return: True если успешно, иначе False.
        """
        if self.energy() - drain >= 0:
            self._tiredness = self._tiredness + drain
            return True
        return False
            
    def gain_rage(self, gain=1):
        """
        Увеличивает раздражение дракона на :gain:
        """
        if self.bloodiness < 5:
            self.bloodiness += gain
            return True
        return False
                
    def magic(self):
        """
        :return: Магическая сила(целое число)
        """
        return sum([get_modifier(mod).magic for mod in self.modifiers()])
            
    def reputation(self):
        """
        Видимые игроку очки дурной славы.
        Рассчитываются по хитрой формуле.
        """
        return math.floor(math.log(self.reputation_points))
        
    def fear(self):
        """
        :return: Значение чудовищности(целое число)
        """
        return sum([get_modifier(mod).fear for mod in self.modifiers()])

    def rest(self):
        self._tiredness = 0  # range 0..max_energy
        self.bloodiness = 0  # range 0..5
        self.lust = 3  # range 0..3
        self.hunger = 3  # range 0..3
        self.spells = []  # заклинания сбрасываются
        self.health = 2

    def color(self):
        """
        :return: Текстовое представление базового цвета дракона
        """
        if self.heads[0] == 'red':
            return u'красный'
        elif self.heads[0] == 'black':
            return u'черный'
        elif self.heads[0] == 'blue':
            return u'синий'
        elif self.heads[0] == 'gold':
            return u'золотой'
        elif self.heads[0] == 'silver':
            return u'серебряный'
        elif self.heads[0] == 'copper':
            return u'бронзовый'
        elif self.heads[0] == 'iron':
            return u'стальной'
        elif self.heads[0] == 'shadow':
            return u'фантомный'
        elif self.heads[0] == 'white':
            return u'белый'
        else:
            return u'зеленый'

    def kind(self):
        """
        :return: Текстовое представление 'вида' дракона
        """
        wings = self.wings()
        paws = self.paws()
        heads = len(self.heads)
        if wings == 0 and paws == 0:
            return u"ползучий гад"
        if wings > 0 and paws == 0:
            return u'летучий гад'
        if wings == 0 and paws >= 0:
            return u'линдвурм'
        if wings > 0 and paws == 1:
            return u'вирвен'
        if wings == 0 and heads > 1:
            if heads == 2:
                return u'двуглавый гидра'
            if heads == 3:
                return u'трехглавый гидра'
            if heads == 4:
                return u'четырёхглавый гидра'
            if heads == 5:
                return u'пятиглавый гидра'
            if heads == 6:
                return u'шестиглавый гидра'
            if heads == 7:
                return u'семиглавый гидрус'
        if wings == 1 and paws == 2 and heads == 1:
            return u'дракон'
        if wings > 0 and paws >= 1 and heads > 1:
            if heads == 2:
                return u'двуглавый дракон'
            if heads == 3:
                return u'трехглавый дракон'
            if heads == 4:
                return u'четырёхглавый дракон'
            if heads == 5:
                return u'пятиглавый дракон'
            if heads == 6:
                return u'шестиглавый дракон'
            if heads == 7:
                return u'семиглавый дракон'

    def size(self):
        """
        :return: Размер дракона(число от 1 до 6)
        """
        return self.modifiers().count('size')

    def wings(self):
        """
        :return: Количество пар крыльев
        """
        return self.modifiers().count('wings')

    def paws(self):
        """
        :return: Количество пар лап
        """
        return self.modifiers().count('paws')

    def children(self):
        """
        Сгенерировать список потомков.
        Вызывается при отставке дракона.
        :return: list of Dragons
        """
        # Обнуляем заклинания, они уже не понадобятся
        self.spells = []
        # копируем мертвые головы в список живых для наследования
        self.heads.extend(self.dead_heads)
        # Формируем список возможных улучшений
        dragon_leveling = ['head']
        if self.size() < 6:
            dragon_leveling += ['size']
        if self.paws() < 3:
            dragon_leveling += ['paws']
        if self.wings() < 3:
            dragon_leveling += ['wings']
        if 'tough_scale' not in self.modifiers():
            dragon_leveling += ['tough_scale']
        if 'clutches' not in self.modifiers():
            dragon_leveling += ['clutches']
        if 'fangs' not in self.modifiers() and self.paws() > 0:
            dragon_leveling += ['fangs']
        if 'horns' not in self.modifiers():
            dragon_leveling += ['horns']
        if 'ugly' not in self.modifiers():
            dragon_leveling += ['ugly']
        if 'poisoned_sting' not in self.modifiers():
            dragon_leveling += ['poisoned_sting']
        if self.modifiers().count('cunning') < 3:
            dragon_leveling += ['cunning']
        if self.heads.count('green') > 0:
            dragon_leveling += ['color']
        # Выбираем три случайных способности
        number_of_abilities = 3
        while len(dragon_leveling) < number_of_abilities:
            dragon_leveling += ['head']
        new_abilities = random.sample(dragon_leveling, number_of_abilities)
        children = [self.deepcopy() for i in range(0, number_of_abilities)]
        for i in range(0, number_of_abilities):
            if new_abilities[i] == 'color':
                # список всех цветов голов
                colors = data.dragon_heads.keys()
                # список возможных цветов 
                available_colors = []
                for head_color in colors:
                    # проходим список всех цветов, добавляем только отсутствующие цвета
                    if head_color not in self.heads:
                        available_colors += head_color
                # если список доступных цветов не пуст - добавляем случайный цвет из списка, иначе добавляем зеленую голову
                if available_colors:
                    children[i].heads[self.heads.index('green')] = random.choice(colors)
                else:
                    children[i].heads += ['green']
            elif new_abilities[i] == 'head':
                children[i].heads += ['green']
            else:
                children[i].anatomy += [new_abilities[i]]
        return children
        
    def struck(self):
        """
        вызывается при получении удара, наносит урон, отрубает головы и выдает описание произошедшего
        :return: описание результата удара
        """
        if self.health:
            #до удара self.health > 1 - дракон ранен, self.health = 1 - тяжело ранен
            self.health -= 1
            if self.health:
                return ['dragon_wounded']
            else:
                return ['dragon_wounded', 'dragon_heavily_wounded']
        else:
            # жизни закончились, рубим случайную голову
            lost_head = random.choice(self.heads)
            self.heads.remove(lost_head)
            self.dead_heads.append(lost_head)
            # потеря головы, если головы закончились - значит смертушка пришла
            if self.heads:
                return ['lost_head', 'lost_' + lost_head]
            else:
                return ['dragon_dead']
                
    def deepcopy(self):
        child = Dragon(gameRef=self._gameRef, base_character=self._base_character)
        child.heads = copy.deepcopy(self.heads)
        child.anatomy = copy.deepcopy(self.anatomy)
        return child
        
class Enemy(Fighter):
    """
    Класс одноразового противника для энкаунтера.
    """

    def __init__(self, kind = 'generic',  *args, **kwargs):
        """
        Здесь должна быть генерация нового рыцаря.
        """
        super(Enemy, self).__init__(*args, **kwargs)
        self.name = mob[kind]['name']
        self.power = mob[kind]['power']
        self.defence = mob[kind]['defence']
        self.descriptions = mob[kind]['descriptions']
        self.abilities = []
        self.equipment = []

    def modifiers(self):
        return []

    def attack(self):
        return self.power

    def protection(self):
        return self.defence
        
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
    test_dragon = Dragon(gameRef=test_game, base_character=test_character)
    for lvl_i in range(1, level - 1):
        test_dragon = test_dragon.children()[0]
    return test_dragon
        
mob = {
        'calf' : {
            'name' : u"Теленок",
            'power': {'base' : (2, 0)},
            'defence' : {'base' : (2, 0)},
            'descriptions' : [
                    [['foe_intro'], u"{0} бросается на {1}", ['foe_name', 'dragon_name'], 0],
                    [['foe_intro'], u"{0} роет копытами землю, готовясь напасть", ['foe_name'], 0],
                    [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
                    [['foe_fear'], u"{0} бежит в страхе от {1}", ['foe_name', 'dragon_name'], 0],
                    [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
                    [['foe_dead', 'dragon_wounded'], u"{0} наносит сильный удар, {1} яростным контрударом убивает его", ['foe_name', 'dragon_name'], 0],
                    [['foe_alive', 'dragon_wounded'], u"{0} наносит сильный удар и уворачивается от ответного удара", ['foe_name'], 0],
                    [['foe_alive', 'dragon_undamaged'], u"Противники маневрируют, готовясь к удару", [], 0],
                    [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову", ['foe_name'], 0],
                    [['foe_dead', 'lost_head'], u"{0} ценой головы убивает супостата", ['dragon_name'], 0]
                ]
            },
        
        'bull' : {
            'name' : u"Бык",
            'power': {'base' : (6, 0)},
            'defence' : {'base' : (6, 0)},
            'descriptions' : [
                    [['foe_intro'], u"{0} бросается на {1}", ['foe_name', 'dragon_name'], 0],
                    [['foe_intro'], u"{0} роет копытами землю, готовясь напасть", ['foe_name'], 0],
                    [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
                    [['foe_fear'], u"{0} бежит в страхе от {1}", ['foe_name', 'dragon_name'], 0],
                    [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
                    [['foe_dead', 'dragon_wounded'], u"{0} наносит сильный удар, {1} яростным контрударом убивает его", ['foe_name', 'dragon_name'], 0],
                    [['foe_alive', 'dragon_wounded'], u"{0} наносит сильный удар и уворачивается от ответного удара", ['foe_name'], 0],
                    [['foe_alive', 'dragon_undamaged'], u"Противники маневрируют, готовясь к удару", [], 0],
                    [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову", ['foe_name'], 0],
                    [['foe_dead', 'lost_head'], u"{0} ценой головы убивает супостата", ['dragon_name'], 0]
                ]
            },
        
        'buffalo' : {
            'name' : u"Бизон",
            'power': {'base' : (10, 0)},
            'defence' : {'base' : (10, 0)},
            'descriptions' : [
                    [['foe_intro'], u"{0} бросается на {1}", ['foe_name', 'dragon_name'], 0],
                    [['foe_intro'], u"{0} роет копытами землю, готовясь напасть", ['foe_name'], 0],
                    [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
                    [['foe_fear'], u"{0} бежит в страхе от {1}", ['foe_name', 'dragon_name'], 0],
                    [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
                    [['foe_dead', 'dragon_wounded'], u"{0} наносит сильный удар, {1} яростным контрударом убивает его", ['foe_name', 'dragon_name'], 0],
                    [['foe_alive', 'dragon_wounded'], u"{0} наносит сильный удар и уворачивается от ответного удара", ['foe_name'], 0],
                    [['foe_alive', 'dragon_undamaged'], u"Противники маневрируют, готовясь к удару", [], 0],
                    [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову", ['foe_name'], 0],
                    [['foe_dead', 'lost_head'], u"{0} ценой головы убивает супостата", ['dragon_name'], 0]
                ]
            },
        
        'minotaur' : {
            'name' : u"Минотавр",
            'power': {'base' : (15, 0)},
            'defence' : {'base' : (15, 0)},
            'descriptions' : [
                    [['foe_intro'], u"{0} бросается на {1}", ['foe_name', 'dragon_name'], 0],
                    [['foe_intro'], u"{0} роет копытами землю, готовясь напасть", ['foe_name'], 0],
                    [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
                    [['foe_fear'], u"{0} бежит в страхе от {1}", ['foe_name', 'dragon_name'], 0],
                    [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
                    [['foe_dead', 'dragon_wounded'], u"{0} наносит сильный удар, {1} яростным контрударом убивает его", ['foe_name', 'dragon_name'], 0],
                    [['foe_alive', 'dragon_wounded'], u"{0} наносит сильный удар и уворачивается от ответного удара", ['foe_name'], 0],
                    [['foe_alive', 'dragon_undamaged'], u"Противники маневрируют, готовясь к удару", [], 0],
                    [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову", ['foe_name'], 0],
                    [['foe_dead', 'lost_head'], u"{0} ценой головы убивает супостата", ['dragon_name'], 0]
                ]
            },
            
        'Jupiter' : {
            'name' : u"Юпитер",
            'power': {'base' : (20, 0)},
            'defence' : {'base' : (20, 0)},
            'descriptions' : [
                    [['foe_intro'], u"{0} бросается на {1}", ['foe_name', 'dragon_name'], 0],
                    [['foe_intro'], u"{0} роет копытами землю, готовясь напасть", ['foe_name'], 0],
                    [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
                    [['foe_fear'], u"{0} бежит в страхе от {1}", ['foe_name', 'dragon_name'], 0],
                    [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
                    [['foe_dead', 'dragon_wounded'], u"{0} наносит сильный удар, {1} яростным контрударом убивает его", ['foe_name', 'dragon_name'], 0],
                    [['foe_alive', 'dragon_wounded'], u"{0} наносит сильный удар и уворачивается от ответного удара", ['foe_name'], 0],
                    [['foe_alive', 'dragon_undamaged'], u"Противники маневрируют, готовясь к удару", [], 0],
                    [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову", ['foe_name'], 0],
                    [['foe_dead', 'lost_head'], u"{0} ценой головы убивает супостата", ['dragon_name'], 0]
                ]
            },
       }