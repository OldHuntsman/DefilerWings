#!/usr/bin/env python
# coding=utf-8
import random
import math
import data
import battle
import mob_data
import girls
from data import get_modifier
from copy import deepcopy
import renpy.exports as renpy
import renpy as renpy_internal
import renpy.store as store

def tuples_sum(tuple_list):
    return sum([first for first, _ in tuple_list]), sum([second for _, second in tuple_list])


class Game(store.object):
    def __init__(self, base_character=None):
        """
        :param base_character: Базовый класс для персонажа. Скорее всего NVLCharacter.
        """
        from thief import Thief
        self.base_character = base_character
        self.reputation_points = 0  # Дурная слава дракона
        self.mobilization = 0  # мобилизация королевства
        self._year = 0  # текущий год
        self.currentCharacter = None # Последний говоривший персонаж. Используется для поиска аватарки.
        
                
        self.lair = Lair()
        self.dragon = Dragon(gameRef=self, base_character=base_character)
        self.knight = Knight(gameRef=self, base_character=base_character)
        self.thief = None #Вора не создаем, потому что его по умолчанию нет. Он возможно появится в первый сон.
        
        self.narrator = Sayer(gameRef=self, base_character=base_character)
        self.girls_list = girls.Girls_list(gameRef=self, base_character=base_character)
        self.foe = None
        self.girl = None

    @property
    def year(self):
        return self._year
    @year.setter
    def year(self, value):
        if value >= self._year:
            self._year = value
        else:
            raise Exception ("Время не может течь назад")
        
    def save(self):
        '''
        Логика сохранения игры.
        '''
        renpy.rename_save("1-1", "1-2") #Переименовываем старый сейв
        renpy.take_screenshot() # Делаем скриншот для отображения в сейве
        renpy.save("1-1")               # Сохраняем игру
        return True

    def next_year(self):
        '''
        Логика смены года.
        Проверки на появление/левелап/рейд рыцаря/вора.
        Изменение дурной славы.
        Что-то ещё?
        '''
        self.year += 1
        # Если вора нет, то пробуем создать его
        if self.thief is None or self.thief.is_dead():
            if renpy.config.debug: self.narrator(u"Вора не было или он был мертв, попробуем его создать.")
            self._create_thief()
            if self.thief is None:
                if renpy.config.debug: self.narrator(u"Вор не появился.")
            else:
                if renpy.config.debug: self.narrator(u"Вор появился.")
                self.thief.event("spawn")
        else: # Иначе пробуем его пустить на дело
            if random.choice(range(6)) in range(1+len(self.thief.items)): # Шанс 1 + количество шмота на воре, что он пойдет на дело
                # Идем на дело
                if renpy.config.debug: self.narrator(u"Вор идет на дело")
                self.thief.steal(self.lair)
            else:
                if renpy.config.debug: self.thief(u"Что-то ссыкотно, надо бы подготовиться.")
                self.thief.event("prepare")
                if random.choice(range(2)) == 0:    # C 50% шансом получаем шмотку
                    self.thief.event("prepare_usefull")
                    self.thief.receive_item()
                else:
                    if renpy.config.debug: self.narrator(u"Но вместо этого вор весь год бухает.")
                    self.thief.event("prepare_usefull")

    def sleep(self):
        """
        Рассчитывается количество лет которое дракон проспит.
        Попытки бегства женщин.
        Сброс характеристик дракона.
        """
        time_to_sleep = self.dragon.injuries + 1
        # Сбрасываем характеристики дракона
        self.dragon.rest()
        # Спим
        for i in xrange(time_to_sleep):
            self.year += 1
            self.next_year()
            if self.knight:
                if 1 == random.randint(1, 3):
                    self.knight.upgrade()
            else:
                self._create_knight()
            if self.thief:
                if 1 == random.randint(1, 3):
                    self.thief.upgrade()
            else:
                self._create_knight()

    def _create_knight(self):
        """
        Проверка на появление рыцаря.
        """
        raise NotImplementedError

    def _create_thief(self, thief_level=None):
        """
        Проверка на появление вора.
        """
        from thief import Thief
        if thief_level is None:
            thief_level = Thief.start_level(self.reputation())
        if thief_level > 0:
            self.thief = Thief(level=thief_level,
                               treasury=self.lair.treasury,
                               gameRef=self, 
                               base_character=self.base_character)
        else:
            self.thief = None

    def reputation(self):
        """
        Видимые игроку очки дурной славы.
        Рассчитываются по хитрой формуле.
        """
        #т.к. логарифма нуля не существует, а меньше 1 логарифм будет отрицательным
        if self.reputation_points < 1:
            return 0
        return math.floor(math.log(self.reputation_points))
        
    @staticmethod
    def weighted_random(data):
        """
        :param data: list of tuples (option, weight), где option - возвращаемый вариант, а
                     weight - вес варианта. Чем больше, тем вероятнее что он выпадет.
        :return: option, или None, если сделать выбор не удалось.
        Пример использования:
        coin_flip = weighted_random([("орёл", 1), ("решка",1)])
        """
        if len(data)>0:
            import bisect
            #Складываем вес всех доступных энкаунтеров
            accumulated = []
            total = 0
            for option, weight in data:
                assert weight >= 0
                accumulated.append(weight + total)
                total += weight
            #Проверяем, что суммарный вес не равен нулю.
            if total == 0:
                return None
            r = random.random() * accumulated[-1]
            return data[bisect.bisect(accumulated, r)][0]
        return None
    


class Treasury(store.object):
    def __init__(self):
        self.copper_coins = 0
        self.silver_coins = 0
        self.gold_coins = 0
        # списки строк
        self.materials = []
        self.jewelry = []
        self.equipment = []
        #TODO: multiple same equipment
        self.thief_items = data.Container(id="equipment")

    def money(self):
        """
        :return: Суммарная стоимость всего, что есть в сокровищнице(Золотое ложе).
        """
        raise NotImplementedError


class Lair(object):
    def __init__(self, type = "impassable_coomb"):
        self.type = data.Container(type, data.lair_types[type])
        self.upgrades = data.Container('lair_upgrades')
        # Сокровищиница
        self.treasury = Treasury()
        # Список модификаций(ловушки, стражи и.т.п.)
        self.modifiers = []
        # Список женщин в логове
        self.women = []
        
    def reachable(self, abilities):
        '''
        Функция для проверки доступности логова
        :param abilities: - список способностей у того, кто пытается достичь, например, для вора: [ 'alpinism', 'swimming' ]
        :return: Возращает True ,если до логова можно добраться и False если нет
        '''
        for r in self.requirements():
            if r not in abilities:
                return False
        return True
    
    def requirements(self):
        '''
        :return: Возвращает список способностей которые нужны чтобы достичь логова.
        '''
        r = []
        if self.type.require: # Если тип логова что-то требует добавляем что оно требует
            r += self.type.require
        for u in self.upgrades: # Тоже самое для каждого апгрейда
            if u.require:
                r += u.require
        return r
    
    @property
    def inaccessability(self):
        return self.type.inaccessability + self.upgrades.sum("inaccessability")
        
class Sayer(store.object):
    '''
    Базовый класс для всего что умеет говорить
    '''
    def __init__(self,gameRef=None, base_character=None, *args, **kwargs):
        """
        :param gameRef: Game object
        :param base_character: base_character базовый класс персонажа от которого будет вестись вещание
        """
        self.avatar = None      # По умолчанию аватарки нет
        self._gameRef = gameRef # Проставляем ссылку на игру
        self._base_character = base_character # На всякий случай если захотим пересоздать (но зачем?)
        self._real_character = base_character() # Создаем объект от которого будет вестись вещание
    
    @property   #Задаем имя через свойство, чтобы при изменении его передавать в персонажа.
    def name(self):
        return self._real_character.name
    
    @name.setter
    def name(self, value):
        self._real_character.name = value
        
    def __call__(self, *args, **kwargs):
        """
        Этот метод используется при попытке сказать что-то персонажем.
        Переопределяем, чтобы сообщить игре, что сейчас говорит этот персонаж.
        """
        self._gameRef.currentCharacter = self # Прописываем кто говорит в настоящий момент
        self._real_character(*args, **kwargs) # На самом деле говорим
        
    def third(self, *args, **kwargs):
        '''
        Говорим от третьего лица. Принимаются предложения на более удачное название.
        Например прямая речь:
        $ game.person ("Что-нибудь")
        game.person "Где-нибудь"
        Рассказ о том что делает этот персонаж:
        $ game.person.third("Делая что-нибудь")
        game.person.third "Делая где-нибудь"
        '''
        self._gameRef.currentCharacter = self # Делаем вид, что сказали сами
        self._gameRef.narrator._real_character(*args, **kwargs) # Говорим о лица нарратора. Грязный хак.
        

class Girl(Sayer):
    """
    Базовый класс для всего, с чем можно заниматься сексом.
    """
            
    def __init__(self, *args, **kwargs):
        super(Girl, self).__init__(*args, **kwargs) # Инициализируем родителя
        self.virgin = True # девственность = пригодность для оплодотворения драконом
        self.pregnant = 0 # 0 - не беременна, 1 - беременна базовым отродьем, 2 - беременна продвинутым отродьем
        self.quality = 0 # Репродуктивное качество женщины. Если коварство дракона превышает её репродуктивное качество, то отродье будет продвинутым. Иначе базовым 
        self.name = ''
        self.jailed = False # была ли уже в тюрьме, пригодится для описания
        self.treasure = []
            
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
        immun = []
        for type in data.attack_types:
                if type + '_immunity' in self._modifiers:
                    immun.append(type)
        return immun
        
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
        elif self.heads[0] == 'bronze':
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
        child.heads = deepcopy(self.heads)
        child.anatomy = deepcopy(self.anatomy)
        return child
        
class Enemy(Fighter):
    """
    Класс одноразового противника для энкаунтера.
    """

    def __init__(self, kind = 'generic',  *args, **kwargs):
        """
        Создание врага.
        """
        super(Enemy, self).__init__(*args, **kwargs)
        self.name = mob_data.mob[kind]['name']
        self.power = mob_data.mob[kind]['power']
        self.defence = mob_data.mob[kind]['defence']
        self.descriptions = mob_data.mob[kind]['descriptions']
        self._modifiers = mob_data.mob[kind]['modifiers']
        self.abilities = []
        self.equipment = []
        self.img = '' "img/scene/fight/%s.png" % mob_data.mob[kind]['image']

    def modifiers(self):
        return self._modifiers

    def attack(self):
        return self.power

    def protection(self):
        return self.defence

class Knight(Fighter):
    """
    Класс рыцаря.
    Набросок для тестирования боя.
    Спутников, особенности и снаряжение предпологается засовывать в переменную _modifiers
    """

    def __init__(self, *args, **kwargs):
        """
        Здесь должна быть генерация нового рыцаря.
        """
        super(Knight, self).__init__(*args, **kwargs)
        self.name = u"Сер Ланселот Озёрный"
        self.power = 1
        self.abilities = []
        self.equipment = [u"щит", u"меч", u"броня", u"копьё", u"скакун", u"спутник"]

    def modifiers(self):
        return self._modifiers + self.abilities + self.equipment

    def attack(self):
        a = super(Knight, self).attack()
        if "liberator" in self.modifiers():
            # TODO: подумать как получаем ссылку на логово
            # Увеличиваем атаку в соответствии со списком женщин в логове
            raise NotImplementedError
        a['base'][0] + self.power
        return a

    def protection(self):
        p = super(Knight, self).protection()
        if "liberator" in self.modifiers():
            # Увеличиваем защиту в соответствии со списком женщин в логове
            raise NotImplementedError
        p['base'][0] + self.power
        return p

    def title(self):
        """
        :return: Текстовое представление 'звания' рыцаря.
        """
        if self.power == 1:
            return u"Бедный рыцарь"
        elif self.power == 2:
            return u"Странствующий рыцарь"
        elif self.power == 3:
            return u"Межевой рыцарь"
        elif self.power == 4:
            return u"Благородный рыцарь"
        elif self.power == 5:
            return u"Паладин рыцарь"
        elif self.power == 6:
            return u"Прекрасный принц"
        else:
            assert False, u"Недопустимое значение поля power"

    def upgrade(self):
        """
        Метод вызвается если рыцать не пошел драться с драконом.
        Добавляет новое снаряжение.
        """
        raise NotImplementedError


def call(label, *args, **kwargs):
    if renpy.has_label(label):
        renpy.call_in_new_context(label, *args, **kwargs)
    else:
        renpy.call_in_new_context("lb_missed", label=label)
    return

