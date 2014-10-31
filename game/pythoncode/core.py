#!/usr/bin/env python
# coding=utf-8
import random
import math
import data
import battle
import mob_data
import girls
import girls_data
import treasures
from points import Mobilization, Reputation, Poverty
from data import get_modifier
from copy import deepcopy
import renpy.exports as renpy
import renpy as renpy_internal
import renpy.store as store

def tuples_sum(tuple_list):
    return sum([first for first, _ in tuple_list]), sum([second for _, second in tuple_list])


class Game(store.object):
    def __init__(self, adv_character=None, nvl_character=None):
        """
        :param base_character: Базовый класс для персонажа. Скорее всего NVLCharacter.
        """
        from thief import Thief
        from knight import Knight
        self.adv_character = adv_character
        self.nvl_character = nvl_character
        self.mobilization = Mobilization()
        self.poverty = Poverty()
        self._year = 0  # текущий год
        self.currentCharacter = None # Последний говоривший персонаж. Используется для поиска аватарки.
          
        self.dragon = None
        self.knight = Knight(gameRef=self, base_character=adv_character)
        self.thief = None #Вора не создаем, потому что его по умолчанию нет. Он возможно появится в первый сон.
        
        self.narrator = Sayer(gameRef=self, base_character=nvl_character)
        self.girls_list = girls.Girls_list(gameRef=self, base_character=adv_character)
        self.create_lair() # TODO: первоначальное создание логова
        self.foe = None
        self.girl = None
        
        # переменные для армии Тьмы
        self._grunts = {'goblin' : 1} # словарь для хранения рядовых войск
        self._elites = {} # словарь для хранения элитных войск
        self.money   = 0  # деньги в казне Владычицы
        self._force_residue = 100 # процент оставшейся силы армии - мощь армии

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
        Попытки бегства женщин.
        Что-то ещё?
        '''
        self.year += 1
        self.dragon.age += 1
        # Применяем разруху накопленную за год с учетом отстройки
        self.poverty.value -= 1
        self.poverty.apply_planned()
        # Действия с девушками каждый год
        self.girls_list.next_year()
        # Уменьшаем срок всех наймов
        for upgrade in self.lair.upgrades.keys():
            if type(self.lair.upgrades) == type(self.lair.upgrades[upgrade]) and \
               'recruitment_time' in self.lair.upgrades[upgrade].keys():
                self.lair.upgrades[upgrade]['recruitment_time'] -= 1
                if self.lair.upgrades[upgrade]['recruitment_time'] == 0:
                    del self.lair.upgrades[upgrade]
        # Изменяем уровень мобилизации
        desired_mobilization = self.dragon.reputation.level - self.poverty.value # Желаемый уровень мобилизации
        mobilization_delta = self.mobilization.level - desired_mobilization # Считаем есть ли разница с текущим уровнем мобилизации
        if mobilization_delta != 0: # И если есть разница
            # Увеличиваем  или  уменьшаем на единицу 
            if mobilization_delta > 0:
                self.mobilization.level += 1
            else:
                self.mobilization.level -= 1
        
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
                #self.thief.steal(self.lair)
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
        Сброс характеристик дракона.
        """
        time_to_sleep = self.dragon.injuries + 1
        # Сбрасываем характеристики дракона
        self.dragon.rest()
        # Действия с девушками до начала сна
        self.girls_list.before_sleep()
        # Спим
        for i in xrange(time_to_sleep):
            self.next_year()
	# Обнуляем накопленные за бодрствование очки мобилизации
        self.dragon.reputation.reset_gain()
        # Действия с девушками после конца сна    
        self.girls_list.after_awakening()

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
            thief_level = Thief.start_level(self.dragon.reputation.level)
        if thief_level > 0:
            self.thief = Thief(level=thief_level,
                               treasury=self.lair.treasury,
                               gameRef=self, 
                               base_character=self.adv_character)
        else:
            self.thief = None
            
    def create_lair(self, lair_type = "impassable_coomb"):
        """
        Создание нового логова.
        """
        # Выпускаем всех женщин в прошлом логове на свободу. 
        self.girls_list.free_all_girls()
        # Создаем новое логово
        self.lair = Lair(lair_type)
        
    def add_warrior_to_army(self, warrior_type):
        """
        Добавляет воина  в армию тьмы. warrior_type - название типа добавляемого воина из словаря girls_data.spawn_info
        """
        if 'elite' in girls_data.spawn_info[warrior_type]['modifier']:
            # воин элитный, добавляется в список элитных 
            warriors_list = self._elites
        else:
            # рядовой воин, добавляется в список рядовых 
            warriors_list = self._grunts
        if warrior_type in warriors_list:
            # такой тип воина уже в списке, просто увеличиваем их число
            warriors_list[warrior_type] += 1
        else:
            # такого типа воина нет в списке, добавляем
            warriors_list[warrior_type] = 1
        
    @property
    def army_grunts(self):
        """
        Возвращает число рядовых войск в армии тьмы
        """
        grunts_count = 0
        for grunts_i in self._grunts.values():
            grunts_count += grunts_i
        return grunts_count
        
    @property
    def army_grunts_list(self):
        """
        Возвращает список рядовых войск в армии тьмы
        """
        grunts_list = u""
        for grunt_name, grunt_count in self._grunts.iteritems():
            grunts_list += u"%s: %s. " % (girls_data.spawn_info[grunt_name]['name'], grunt_count)
        return grunts_list
    
    @property
    def army_elites(self):
        """
        Возвращает число элитных войск в армии тьмы
        """
        elites_count = 0
        for elites_i in self._elites.values():
            elites_count += elites_i
        return elites_count
        
    @property
    def army_elites_list(self):
        """
        Возвращает список элитных войск в армии тьмы
        """
        elites_list = u""
        for elite_name, elite_count in self._elites.iteritems():
            elites_list += u"%s: %s. " % (girls_data.spawn_info[elite_name]['name'], elite_count)
        return elites_list
        
    @property
    def army_diversity(self):
        """
        Возвращает разнообразие армии тьмы
        """
        diversity = len(self._elites)
        dominant_number = sorted(self._grunts.values())[-1] // 2
        for number_i in self._grunts.values():
            if dominant_number <= number_i:
                diversity += 1
        return diversity
        
    @property
    def army_equipment(self):
        """
        Возвращает уровень экипировки армии тьмы
        """
        equipment = 0
        AoD_money = self.money
        AoD_cost = (self.army_grunts + self.army_elites) * 1000
        while AoD_money >= AoD_cost:
            AoD_money //= 2
            equipment += 1
        return equipment
        
    @property
    def army_force(self):
        """
        Возвращает суммарную силу армии тьмы по формуле (force) = (grunts + 3 * elites) * diversity * equipment * текущий процент мощи 
        """
        return (self.army_grunts + 3 * self.army_elites) * self.army_diversity * self.army_equipment * self._force_residue // 100
        
    @property
    def army_power_percentage(self):
        """
        Возвращает текущий процент мощи армии тьмы
        """
        return self._force_residue
    @army_power_percentage.setter
    def army_power_percentage(self, value):
        """
        Устанавливает текущий процент мощи армии тьмы
        """
        self._force_residue = value

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
    

class Lair(object):
    def __init__(self, type = "impassable_coomb"):
        self.type_name = type
        self.type = data.Container(type, data.lair_types[type])
        # Список модификаций(ловушки, стражи и.т.п.)
        self.upgrades = data.Container('lair_upgrades')
        if 'provide' in self.type:
            for upgrade in self.type['provide']:
                self.upgrades.add(upgrade, deepcopy(data.lair_upgrades[upgrade]))
        # Сокровищиница
        self.treasury = treasures.Treasury()
        
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
            if self.upgrades[u].require:
                r += self.upgrades[u].require
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

    def __init__(self, parent=None, *args, **kwargs):
        '''
        parent - родитель дракона, если есть.
        '''
        super(Dragon, self).__init__(*args, **kwargs)
        # TODO: pretty screen for name input
        #self._first_name = u"Старый"
        #self._last_name = u"Охотник"
        self.name = random.choice(data.dragon_names)
        self.age = 0
        self.reputation = Reputation()
        self._tiredness = 0  # увеличивается при каждом действии
        self.bloodiness = 0  # range 0..5
        self.lust = 3  # range 0..3, ресурс восстанавливается до 3 после каждого отдыха
        self.hunger = 3  # range 0..3, ресурс восстанавливается до 3 после каждого отдыха
        self.health = 2 # range 0..2, ресурс восстанавливается до 2 после каждого отдыха
        self._mana_used = 0 # количество использованной маны
        self.spells = [] # заклинания наложенные на дракона(обнуляются после сна)
        self._base_energy = 3 #Базовая энергия дракона, не зависящая от модификторов
        self.special_places = {} # Список разведанных "достопримечательностей"
        self._gift = None # Дар Владычицы
        
        # Головы
        if parent is not None:
            self.heads = deepcopy(parent.heads) #Копируем живые головы родителя
            self.heads.extend(parent.dead_heads) #И прибавляем к ним мертвые
        else:
            self.heads = ['green']  # головы дракона
        self.dead_heads = [] #мертвые головы дракона
        
        #Анатомия
        if parent is None:
            self.anatomy = ['size']
        else:
            self.anatomy = deepcopy(parent.anatomy)
        self._gift = self._get_ability()
        if self._gift == 'head':
            self.heads.append('green')
        elif self._gift == 'color':
            self._colorize_head()
        else:
            self.anatomy.append(self._gift)
        
        self.avatar = self._get_dragon_avatar(self.color_eng()) #Назначаем аватарку
        #self(self._gift)
    
    @property
    def description(self):
        ddescription = '  '
        ddescription += data.dragon_size[self.size()-1] + u' ' + self.color() + u' ' + self.kind() + u'. ' + data.dragon_size_description[self.size()-1] 
        i = -1
        for head in self.heads:
            i += 1 
            ddescription += u'\n  Его %s голова ' % data.head_num[i] + data.head_description[self.heads[i]]
        if self.wings() == 0 and self.paws() == 0:
            ddescription += '\n  ' + data.wings_description[0]
        else:
            if self.wings() > 0:
                ddescription += '\n  ' + data.wings_description[self.wings()]
                
            if self.paws() > 0:
                ddescription += '\n  ' + data.paws_description[self.paws()]
                
        if 'tough_scale' in self.modifiers():
            ddescription += '\n  ' + data.special_description[0]
        if 'poisoned_sting' in self.modifiers():
            ddescription += '\n  ' + data.special_description[1]
        if 'clutches' in self.modifiers():
            ddescription += '\n  ' + data.special_description[2]
        if 'horns' in self.modifiers():
            ddescription += '\n  ' + data.special_description[3]
        if 'fangs' in self.modifiers():
            ddescription += '\n  ' + data.special_description[4]
        if 'ugly' in self.modifiers():
            ddescription += '\n  ' + data.special_description[5]
        if self.modifiers().count('cunning') == 1:
            ddescription += '\n  ' + data.special_description[6]
        elif self.modifiers().count('cunning') == 2:
            ddescription += '\n  ' + data.special_description[7]
        elif self.modifiers().count('cunning') == 3:
            ddescription += '\n  ' + data.special_description[8]
            
        return ddescription
    
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
    
    def _get_dragon_avatar(self, type):
        import os
        # config.basedir - директория где у нас лежит сама игра.
        # "game" - директория относительно config.basedir где лежат собственно файлы игры и 
        # относительно которой высчитываются все пути
        relative_path = "img/avadragon/"+type # Относительный путь для движка ренпи
        absolute_path = os.path.join(renpy.config.basedir, "game", relative_path) # Cоставляем абсолютный путь где искать
        filename = random.choice(os.listdir(absolute_path)) # получаем название файла
        return relative_path + "/" + filename # Возвращаем правильно отформатированно значение

    def modifiers(self):
        """
        :return: Список модификаторов дракона
        """
        return self.anatomy + \
               [mod for head_color in self.heads for mod in data.dragon_heads[head_color]] + \
               [mod for spell in self.spells if spell in data.spell_list for mod in data.spell_list[spell]] + \
               [mod for effect in self.spells if spell in data.effects_list for mod in data.effects_list[spell]] 

    def max_energy(self):
        """
        :return: Максимальная энергия(целое число)
        """
        return self._base_energy + sum([get_modifier(mod).max_energy for mod in self.modifiers()])

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
        if self.bloodiness + gain <= 5:
            self.bloodiness += gain
            return True
        return False
                
    def magic(self):
        """
        :return: Магическая сила(целое число)
        """
        return sum([get_modifier(mod).magic for mod in self.modifiers()])
        
    @property
    def mana(self):
        """
        :return: Количество текущей маны (магическая сила - использованная мана, целое число)
        """
        return self.magic() - self._mana_used
        
    def drain_mana(self, drain=1):
        """
        :param drain: количество отнимаемой у дракона маны.
        :return: True если успешно, иначе False.
        """
        if self.mana - drain >= 0:
            self._mana_used += drain
            return True
        return False    
        
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
        self._mana_used = 0 # использованная мана сбрасывается
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
        
    def color_eng(self):
        """
        :return: Текстовое представление базового цвета дракона
        """
        if self.heads[0] == 'red':
            return u'red'
        elif self.heads[0] == 'black':
            return u'black'
        elif self.heads[0] == 'blue':
            return u'blue'
        elif self.heads[0] == 'gold':
            return u'gold'
        elif self.heads[0] == 'silver':
            return u'silver'
        elif self.heads[0] == 'bronze':
            return u'bronze'
        elif self.heads[0] == 'iron':
            return u'iron'
        elif self.heads[0] == 'shadow':
            return u'shadow'
        elif self.heads[0] == 'white':
            return u'white'
        else:
            return u'green'

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
        
    def _get_ability(self):
        '''
        Возвращает способность, которую может получить дракон при рождении
        '''
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
        new_ability = random.choice(dragon_leveling)
        return new_ability
    
    def _colorize_head(self):
        #На всякий случай проверяем есть ли зеленые головы.
        assert self.heads.count('green') > 0
        #Считаем достпуные цвета
        available_colors = [ color for color in data.dragon_heads if color not in self.heads ] 
        #Заменяем зеленую голову на один из доступных цветов
        self.heads[self.heads.index('green')] = random.choice(available_colors)
    
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
            if 'unbreakable_scale' in self.spells:
                # потеря заклинания защиты головы
                self.spells.remove('unbreakable_scale')
                return ['lost_head', 'lost_virtual']
            else:
                # жизни закончились, рубим голову (последнюю в списке)
                lost_head = self.heads.pop()
                self.dead_heads.insert(0, lost_head) # ставим на первое место, чтобы после объединения списков порядок голов не изменился
                # потеря головы, если головы закончились - значит смертушка пришла
                if self.heads:
                    return ['lost_head', 'lost_' + lost_head]
                else:
                    return ['dragon_dead']
                
    def deepcopy(self):#TODO: Выпилить deepcopy
        child = Dragon(gameRef=self._gameRef, base_character=self._base_character)
        child.heads = deepcopy(self.heads)
        child.anatomy = deepcopy(self.anatomy)
        return child
    
    @property
    def injuries(self):
        return 2 - self.health
    
    @property
    def age(self):
        """
        Возраст дракона. integer
        """
        return self._age
    @age.setter
    def age(self, value):
        assert value >= 0
        if hasattr(self, '_age'):
            if int(value) >= self._age:
                self._age = int(value)
        self._age = int(value)
        
    def add_effect(self, effect_name):
        if effect_name not in self.spells:
            if effect_name in data.spell_list or effect_name in data.effects_list:
                self.spells.append(effect_name)
            else:
                raise Exception("Unknown effect: %s" % effect_name)
                
    @property
    def can_fly(self):
        return 'wings' in self.modifiers() or 'wings_of_wind' in self.modifiers()
        
    @property
    def can_swim(self):
        return 'can_swim' in self.modifiers()
    
    @property
    def special_places_count(self):
        return len (self.special_places)
        
    def add_special_place(self, place_name, stage):
        """
        :param place_name: название достопримечательности для добавления - ключ для словаря.
        :param      stage: на каком этапе достопримечательность, ключ для словаря data.special_places, из которого берется надпись в списке и название локации для перехода.
        """
        assert stage in data.special_places, "Unknown stage: %s" % stage
        self.special_places[place_name] = stage
        
        

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

def call(label, *args, **kwargs):
    if renpy.has_label(label):
        renpy.call_in_new_context(label, *args, **kwargs)
    else:
        renpy.call_in_new_context("lb_missed", label=label)
    return

