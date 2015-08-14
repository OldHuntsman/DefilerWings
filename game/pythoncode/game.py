# coding=utf-8

import random
import data
import girls_data
import mob_data
import girls
import treasures
from data import get_modifier
from copy import deepcopy
import renpy.exports as renpy
import renpy.store as store
from characters import Fighter, Mortal, Talker, Thief, Knight, Enemy
from utils import call, tuples_sum, get_random_image
from points import Mobilization, Poverty, Army
from lair import Lair

class Game(store.object):
    _win = False
    _defeat = False
    _dragons_used = 0  # Amount of dragons used in current game 
    lair = None
    _quest = None
    _quest_threshold = None
    _quest_text = None

    def __init__(self, adv_character=None, nvl_character=None):
        """
        :param adv_character: Base class for ADV-mode
        :param nvl_character: Base class for NVL-mode
        """
        self.adv_character = adv_character
        self.nvl_character = nvl_character
        self.mobilization = Mobilization()  # Set mobilization before first dragon appearance
        self.poverty = Poverty()
        self.army = Army()
        self._year = 0  # current year
        self._quest_time = 0  # quest expiration year
        self.currentCharacter = None  # Character who spoke last. Used to search avatar.
        self.unique = []  # list of unique actions for quests

        self._dragon = None

        self.narrator = Talker(game_ref=self, kind='nvl')
        self.foe = None
        self.girl = None

        self.dragon_parent = None
        
    @property
    def dragon(self):
        return self._dragon

    @dragon.setter
    def dragon(self, new_dragon):
        self.mobilization.reset()
        new_dragon._gift = None
        self._dragon = new_dragon
        if self._dragons_used > 0:  # If it's not first dragon,
            self.year += 10  # add 10 years(for hatching, growing, etc)
        self._dragons_used += 1
        if not store.freeplay:
            self.set_quest()
        self.thief = None  # Don't create thief, because we have no thief by default. He may appear at first sleep.
        self.knight = None  # Don't create knight, because we have no knight by default. He may appear at first sleep.
        self.girls_list = girls.GirlsList(game_ref=self, base_character=self.adv_character)
        self.create_lair()

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        if value >= self._year:
            self._year = value
        else:
            raise Exception("Time can't flow back")

    @staticmethod
    def save():
        """
        Save logic.
        """
        renpy.rename_save("1-1", "1-2")  # rename old save
        renpy.take_screenshot()  # Create screenshot to display it on save
        renpy.save("1-1")  # Save game
        return True

    @staticmethod
    def save_freegame():
        renpy.rename_save("1-3", "1-4")
        renpy.take_screenshot()
        renpy.save("1-3")

    def next_year(self):
        """
        Year changing logic.
        Checks for appearance/level increase/raid of knight/thief.
        Reputation changes.
        Girls attempts to escape.
        Something else?
        """
        call(data.game_events["sleep_new_year"])
        self.year += 1
        self.dragon.age += 1
        # Fee for service, checked at begining of year
        for upgrade in self.lair.upgrades.keys():
            if type(self.lair.upgrades) == type(self.lair.upgrades[upgrade]) and \
                    'cost' in self.lair.upgrades[upgrade].keys():
                salary = self.lair.treasury.get_salary(self.lair.upgrades[upgrade]['cost'])
                if salary:
                    if renpy.config.debug:
                        summ = 0
                        for salary_i in salary:
                            summ += salary_i.cost
                        salary_tuple = (self.lair.upgrades[upgrade]['name'], summ - self.lair.upgrades[upgrade]['cost'])
                        self.narrator(u"%s в качестве платы за год воруют: %s ф." % salary_tuple)
                    salary = self.lair.treasury.treasures_description(salary)
                    salary_tuple = (self.lair.upgrades[upgrade]['name'], ' '.join(salary))
                    self.narrator(u"%s в качестве платы за год получают:\n %s" % salary_tuple)
                else:
                    self.narrator(u"%s не получили обещанной платы и уходят." % self.lair.upgrades[upgrade]['name'])
                    del self.lair.upgrades[upgrade]
        # Applies stored for year devastation, considering new builds
        self.poverty.value -= 1
        self.poverty.apply_planned()
        # Actions with girls every year
        self.girls_list.next_year()

        # Change mobilization level
        # At first counts desired mobilization level
        desired_mobilization = self.dragon.reputation.level - self.poverty.value
        # Затем
        # Then count if there is a diffirence with current mobilization level
        mobilization_delta = desired_mobilization - self.mobilization.level
        if mobilization_delta != 0:  # if there is a diffirence
            # Increase or reduce by one 
            if mobilization_delta > 0:
                self.mobilization.level += 1
            else:
                self.mobilization.level -= 1

        # If there is not thief, try to create him
        if self.thief is None or self.thief.is_dead:
            if renpy.config.debug:
                self.narrator(u"Вора не было или он был мертв, попробуем его создать.")
            self._create_thief()
            if self.thief is None:
                if renpy.config.debug:
                    self.narrator(u"Вор не появился.")
                call(data.game_events["no_thief"])
            else:
                if renpy.config.debug:
                    self.narrator(u"Вор появился.")
                self.thief.event("spawn")
        else:  # Esle try to send him to theft
            if self.thief.forced_to_rob or \
               random.choice(range(6)) in range(
                    1 + len(self.thief.items)):  # Chance is  1 + amount of items on thief, that he'll go to theft
                # Going on theft
                if renpy.config.debug:
                    self.narrator(u"Вор идет на дело")
                self.thief.steal(lair=self.lair, dragon=self.dragon)
            else:
                if renpy.config.debug:
                    self.narrator(u"Вору ссыкотно, надо бы подготовиться.")
                self.thief.event("prepare")
                if random.choice(range(3)) == 0:  # 33% chance to get item
                    self.thief.event("prepare_usefull")
                    self.thief.receive_item()
                    if renpy.config.debug:
                        self.narrator(u"Вор получил %s" % self.thief.last_received_item.name)
                else:
                    if renpy.config.debug:
                        self.narrator(u"Но вместо этого вор весь год бухает.")
                    self.thief.event("prepare_useless")
        # If there is no knight, then try to create him
        if self.knight is None or self.knight.is_dead:
            if renpy.config.debug:
                self.narrator(u"Рыцаря не было или он был мертв, попробуем его создать.")
            self._create_knight()
            if self.knight is None:
                if renpy.config.debug:
                    self.narrator(u"Рыцарь не появился.")
                call(data.game_events["no_knight"])
            else:
                if renpy.config.debug:
                    self.narrator(u"Рыцарь появился.")
                self.knight.event("spawn")
        else:  # Else try to send him on fight
            # Chance is  1 + amount of not basic item on knight of 7, that he'll go to fight
            if self.knight.forced_to_challenge or \
               random.choice(range(7)) in range(
                    1 + self.knight.enchanted_equip_count):
                # Going to fight
                self.knight.go_challenge()
            # If knight is not going to fight, he'll try to prepare better.
            else:
                if renpy.config.debug:
                    self.narrator(u"Рыцарю ссыкотно, надо бы подготовиться.")
                self.knight.event("prepare")
                if random.choice(range(3)) == 0:  # 33% chance to get item
                    self.knight.event("prepare_usefull")
                    self.knight.enchant_equip()
                    if renpy.config.debug:
                        self.narrator(u"Рыцарь получил %s" % self.knight.last_received_item.name)
                else:
                    if renpy.config.debug:
                        self.narrator(u"Но вместо этого рыцарь весь год бухает.")
                    self.knight.event("prepare_useless")
        return

    def sleep(self):
        """
        Calculate amount of years that dragon sleep.
        Reset dragon's characteristics.
        """
        call(data.game_events["sleep_start"])
        time_to_sleep = self.dragon.injuries + 1
        # Reset dragon's characteristics
        self.dragon.rest()
        # Actions with girls before sleep
        self.girls_list.before_sleep()
        # Sleep
        i = 0
        while self.dragon.is_alive and i < time_to_sleep:
            i += 1
            self.next_year()
            # in theory we should end sleep here
            # if self.dragon.is_dead:
            #    return
        # Reset mobilization points accumulated while awake
        self.dragon.reputation.reset_gain()
        # Actions with girls after sleep ends    
        self.girls_list.after_awakening()
        # Check quest deadline
        if (self.quest_time <= 0) and not store.freeplay:
            call('lb_location_mordor_questtime')
        call(data.game_events["sleep_end"])

    def create_foe(self, foe_type):
        """ Create enemy with specified type

        :param foe_type: Type of created foe
        :return:
        """
        self.foe = Enemy(foe_type)

    def _create_thief(self, thief_level=None):
        """
        Check for thief appearance.
        :param thief_level: Starting level of thief. If not specified, then determined from reputation level.
        """
        # If thief's level is not specified, then it is a standart test on thief appearance.
        if thief_level is None and random.choice(range(1, 5 + (self.dragon.reputation.level + 1), 1)) in \
                    range(self.dragon.reputation.level + 1):
            thief_level = Thief.start_level(self.dragon.reputation.level)
        if thief_level > 0:
            self.thief = Thief(level=thief_level, treasury=self.lair.treasury, game_ref=self)
        else:
            self.thief = None

    def _create_knight(self, knight_level=None):
        """
        Create knight.
        """
        # If knight's level is not specified, then it is a standart test on knight appearance.
        if knight_level is None and random.choice(range(1, 5 + (self.dragon.reputation.level + 1), 1)) in \
                    range(self.dragon.reputation.level + 1):
            knight_level = Knight.start_level(self.dragon.reputation.level)
        if knight_level > 0:
            self.knight = Knight(level=knight_level, game_ref=self)
        else:
            self.knight = None

    def create_lair(self, lair_type=None):
        """
        Create new lair.
        """
        # Frees all girls from old lair. 
        self.girls_list.free_all_girls()

        if lair_type is not None:
            # If lair changed for better one - save treasury
            save_treas = self.lair.treasury
            # Create new lair
            self.lair = Lair(lair_type)
            data.achieve_target(self.lair.type_name, "lair")#событие для ачивок
            # Copy treasury from old lair
            self.lair.treasury = save_treas
        else:
            # define default lair
            lair_list = []
            mods = self.dragon.modifiers()
            for lair in data.lair_types.iterkeys():
                # review lairs which are given away automatically if requirements done
                if 'prerequisite' in data.lair_types[lair]:
                    prerequisite_list = data.lair_types[lair]['prerequisite']  # get list of requirements for dragon
                    prerequisite_exists = True  # temporary variable for requirements
                    for prerequisite in prerequisite_list:  # look through requirements list
                        # Make sure that list of requirements is done
                        prerequisite_exists = prerequisite_exists and prerequisite in mods
                    if prerequisite_exists:
                        # if list of requirements is done, adding lair to a list
                        lair_list.append((data.lair_types[lair].name, lair))
            if len(lair_list) == 0:
                lair_type = 'impassable_coomb'  # list of lairs is empty, choose default
            elif len(lair_list) == 1:
                lair_type = lair_list[0][1]  # one lair in a list, choose it automatically
            else:
                lair_list.insert(0, (u"Выберите логово:", None))
                lair_type = renpy.display_menu(lair_list)  # more than one lair in list, give a list to choose from
            self.lair = Lair(lair_type)
            data.achieve_target(self.lair.type_name, "lair")# achievements event

    def set_quest(self):
        lvl = self.dragon.level
        # Go through entire list of quests
        quests = []
        for quest_i in xrange(len(data.quest_list)):
            quest = data.quest_list[quest_i]
            # find quest which suits our level, is not unique and still is not done in current game
            is_applicable = ('prerequisite' not in quest or quest['prerequisite'] in self.unique)
            is_applicable = is_applicable and ('unique' not in quest or quest['unique'] not in self.unique)
            is_applicable = is_applicable and quest['min_lvl'] <= lvl <= quest['max_lvl']
            if 'anatomy_required' in quest:
                any_applicable = False
                for require in quest['anatomy_required']:
                    curr_applicable = True
                    for subrequire in require.keys():
                        curr_applicable = curr_applicable and \
                            self.dragon.modifiers().count(subrequire) >= require[subrequire]
                    any_applicable = any_applicable or curr_applicable
                is_applicable = is_applicable and any_applicable
            if is_applicable:
                quests.append(quest)
        self._quest = random.choice(quests)
        # Sets quest deadline
        self._quest_time = self._year
        if 'fixed_time' in self._quest:
            self._quest_time += self._quest['fixed_time']
        if 'lvlscale_time' in self._quest:
            self._quest_time += lvl * self._quest['lvlscale_time']
        # Set threshold value, if necessary
        self._quest_threshold = 0
        if 'fixed_threshold' in self._quest:
            self._quest_threshold += self._quest['fixed_threshold']
        if 'lvlscale_threshold' in self._quest:
            self._quest_threshold += lvl * self._quest['lvlscale_threshold']
        self._quest_text = self._quest['text'].format(*[self._quest_threshold])

    @property
    def is_quest_complete(self):
        """
        Check if quest completed
        TODO: проверки на выполнение квестов. Сразу после добавления квестов.
        """
        task_name = self._quest['task']
        current_level = 0
        reached_list = []
        if task_name == 'autocomplete':  # task is always completed
            return True
        elif task_name == 'reputation':  # reputation level check
            current_level = self.dragon.reputation.level
        elif task_name == 'wealth':  # treasures cost check
            current_level = self.lair.treasury.wealth
        elif task_name == 'gift':  # the most expensive treasure check
            current_level = self.lair.treasury.most_expensive_jewelry_cost
        elif task_name == 'poverty':  # mobilization level decrease check
            current_level = self.mobilization.decrease
        elif task_name == 'offspring':  # offspring birth check
            reached_list.extend(self.girls_list.offspring)
        elif task_name == 'lair':  # lair type and it's improvements check
            reached_list.extend(self.lair.upgrades.keys())
            reached_list.append(self.lair.type_name)
        elif task_name == 'event':  # events check
            reached_list.extend(self.dragon.events)
        # requirements check
        if 'task_requirements' in self._quest and type(self._quest['task_requirements']) is str:
            quest_complete = self._quest['task_requirements'] in reached_list
        elif 'task_requirements' in self._quest:
            quest_complete = True
            for require in self._quest['task_requirements']:
                # have to complete full list of requirements
                if type(require) is str:
                    reached_requirements = require in reached_list
                else:
                    reached_requirements = False
                    for sub_require in require:
                        if type(sub_require) is str:
                            variant_reached = sub_require in reached_list
                        else:
                            # It is enought to complete one option for this requirement
                            variant_reached = True
                            for var_sub_require in sub_require:
                                variant_reached = variant_reached and var_sub_require in reached_list
                        reached_requirements = reached_requirements or variant_reached
                quest_complete = quest_complete and reached_requirements
        else:
            quest_complete = True
        # obstacles to quest check
        if 'task_obstruction' in self._quest:
            for obstruction in self._quest['task_obstruction']:
                quest_complete = quest_complete and obstruction not in reached_list
        quest_complete = quest_complete and current_level >= self._quest_threshold
        return quest_complete

    def complete_quest(self):
        """
        Consider current quest as completed
        """
        # adds our treasures to mistress treasury
        self.army.money += self.lair.treasury.wealth
        # Specifies unique quest as already performed
        if 'unique' in self._quest:
            self.unique.append(self._quest['unique'])

    @property
    def quest_task(self):
        return self._quest['task']

    @property
    def quest_text(self):
        return self._quest_text

    @property
    def quest_time(self):
        """
        Years to quest deadline
        """
        return self._quest_time - self._year

    @quest_time.setter
    def quest_time(self, value):
        self._quest_time = self._year + value

    @property
    def quest_time_text(self):
        number = self.quest_time
        if number == 1:
            return u"Последний год на выполнение задания!"
        elif 1 < number < 5:
            return u"Тебе нужно выполнить задание за %s года!" % str(number)
        elif (number % 100 > 20) and (number % 10 == 1):
            return u"Задание нужно выполнить за %s год." % str(number)
        elif (number % 100 > 20) and (1 < number % 10 < 5):
            return u"Задание нужно выполнить за %s года." % str(number)
        else:
            return u"Задание нужно выполнить за %s лет." % str(number)

    def choose_spell(self, back_message=u"Вернуться"):
        """
        Implements spell choose menu
        :param back_message: name for item with choose refusion in menu.
        :return: When spell choosed, uses it and return True,
                 return False on refuse.
        """
        spells_menu = []
        for spell in data.spell_list.keys():
            # Добавляем в список только актуальные заклинания.
            if spell not in self.dragon.spells and (spell is not 'spellbound_trap' or 'magic_traps' not in self.lair.upgrades):
                spells_menu.append((data.spell_list_rus[spell], spell))
        spells_menu = sorted(spells_menu, key=lambda spell: spell[0])
        spells_menu.append((back_message, 'back'))
        spell_name = renpy.display_menu(spells_menu)
        if spell_name == 'back':
            return False
        else:
            if spell_name == 'spellbound_trap':
                self.lair.add_upgrade('magic_traps')
            else:
                self.dragon.add_effect(spell_name)
            return True

    def interpolate(self, text):
        """
        Function which replace variables in string to actual game data
        """
        return text % self.format_data

    @property
    def format_data(self):
        substitutes = {
            "dragon_name": self.dragon.name,
            "dragon_name_full": self.dragon.fullname,
            "dragon_type": self.dragon.kind,
        }
        if self.foe is not None:
            substitutes["foe_name"] = self.foe.name
        return substitutes

    @property
    def is_won(self):
        # Check if game is won
        if not self._win:
            # Check if we win
            pass
        return self._win

    def win(self):
        """
        Forced win game
        """
        self._win = True

    @property
    def is_lost(self):
        # Check if game is lost
        if not self._defeat:
            # Check if we loose
            pass
        return self._defeat

    def defeat(self):
        """
        Forced loose game
        """
        self._defeat = True