#!/usr/bin/env python
# coding=utf-8

import collections


class Modifier(object):
    """
    Various modifiers class.
    Examples: mistress gifhts, knight's equipment, spells etc.
    """

    def __init__(self, attack=('base', (0, 0)), protection=('base', (0, 0)), magic=0, fear=0, energy=0):
        self.attack = attack
        self.protection = protection
        self.magic = magic
        self.fear = fear
        self.max_energy = energy

    def __contains__(self, item):
        return item in self.__dict__

    @staticmethod
    def attack_filter(attack):
        return attack


class Container(collections.defaultdict):
    """
    Storage class for various properties/modifiers
    TODO: реверсивный поиск
    """

    def __init__(self, container_id=None, data=None, *args, **kwargs):
        super(Container, self).__init__(*args, **kwargs)
        self.id = container_id
        if data is not None:

            for key, value in data.items():
                self.add(key, value)

    def add(self, container_id, data):
        """
        :param container_id: property/modifier identifier
        :param data: dict which contais properties of this property/modifier
        """
        if container_id not in self:
            if type(data) is dict:
                self[container_id] = Container(container_id, data)
            else:
                self[container_id] = data
        else:
            raise Exception("Already in container")

    def sum(self, parameter):
        """
        :param parameter: Value by which you should summarize attributes. Summing goes recursively.
        """
        total = 0
        if parameter in self:
            try:
                total += self[parameter]
            except ValueError:
                pass
        for i in self:
            if type(self[i]) == type(self):
                total += self[i].sum(parameter)
        return total

    def list(self, key):
        """
        Рекурсивно возвращает лист значений по ключу
        :param key: Ключ по которому производится поиск
        :return: Список значений
        """
        result = []
        if key in self:
            if type(self[key]) is list:
                result += self[key]
            else:
                result.append(self[key])
        for i in self:
            if type(self[i]) == type(self):
                result += self[i].list(key)
        return result

    def contains(self, key, value=None):
        """
        Returns a list of IDs that contain given key and and value if specified.
        :param key: Key which element should contain
        :return: list of elements that contain key, if there is no such elements, list is empty
        """
        result = []
        if key in self:
            if value is None:
                result += [self.id]
            else:
                if self[key] == value:
                    result += [self.id]
        for i in self:
            if type(self[i]) == type(self):
                result += self[i].contains(key, value)
        return result

    def select(self, query):
        """
        Return a list of IDs that fits conditions that set in query. Not recursively.
        :param query: tuples list (key, value) which object of serach must meet
        :return: list of satisfying elements
        """
        result = []
        for (key, value) in query:
            if key in self and self[key] == value:
                continue
            else:
                break
        else:
            result.append(self.id)
        for i in self:
            if type(self[i]) == type(self):
                result += self[i].select(query)
        return result

    def type(self):
        """
        For test uses
        """
        return type(self)

    def __getattr__(self, name):
        return self[name]

    def __missing__(self, key):
        return None


def get_description_by_count(description_list, count):
    """ 
    :param description_list: dictionary, key - minimum integer number,
    in which value is output with this key.
    Maximum number, in which value is output - minimum number of a next key minus one
    :param count: number for which we want to pick description
    :return: description for number count from dictionary description_list
    For example, if description_list = {0:'A', 10:'B'}, 
    than with count < 0 result is None, with count = 0..9 - 'A', and with count >= 10 - 'B'
    """
    count_list = reversed(sorted(description_list.keys()))
    for count_i in count_list:
        if count >= count_i:
            return description_list[count_i]

#
# Вор
#

thief_first_names = [
    u"Jack",
    u"Harry",
    u"Sem",
    u"Alex",
    u"Buddy",
    u"Buck",
    u"Chuck",
    u"Barry",
    u"Bart",
    u"Beaves",
    u"Bert",
    u"Billy",
    u"Beef",
    u"Butch",
    u"Brook",
    u"Bred",
    u"Willie",
    u"Woodie",
    u"Geib",
    u"Henry",
    u"Glen",
    u"Greg",
    u"Dacks",
    u"Dexter",
    u"Dean",
    u"Jet",
    u"Jessie",
    u"Jobe",
    u"Joy",
    u"Jonnie",
    u"Jhosh",
    u"Duaein",
    u"Duke",
    u"Zack",
    u"isie",
    u"Kennie",
    u"Kirk",
    u"Klaive",
    u"Kliff",
    u"Klod",
    u"Larrie",
    u"Meddison",
    u"Max",
    u"Marcus",
    u"Marvin",
    u"Martie",
    u"Mett",
    u"Nash",
    u"Nick",
    u"Ollie",
    u"Paul",
    u"Ray",
    u"Rickkie",
    u"Scott",
    u"Spaik",
    u"Stive",
    u"Tedd",
    u"Tonnie",
    u"Troy",
    u"Fill",
    u"Fox",
    u"Sean",
]

thief_last_names = [
    u"the Bald",
    u"Sliptoe",
    u"the Nimble",
    u"the Cunning",
    u"Fox",
    u"Jumper",
    u"Fastlegs",
    u"Joker",
    u"Rascal",
    u"Spliner",
    u"Smelly",
    u"Thorn",
    u"the Shadow",
    u"Stealthy",
    u"the Calm",
    u"Smugh",
    u"Agile Fingers",
    u"Snealing",
    u"cross-eyed",
    u"Shuher",
    u"Crazed",
    u"Con-artist",
    u"Pretender",
    u"Alpinist",
    u"the Crawler",
    u"Rimer",
    u"the Indescent",
    u"Unprincipled",
    u"Cock",
    u"Nervous",
    u"the Scretchy",
    u"the Stutterer",
    u"Pockmarked",
    u"Curva",
    u"the Throaty",
    u"Hungman",
    u"the Angry",
    u"Shycopant",
    u"Headoff",
    u"Frostbite",
    u"Immature",
    u"Snakethongue",
    u"the Venomous",
    u"Speedy",
    u"the Cautious",
    u"Blacktooth",
    u"Whitetooth",
    u"the Witehands",
    u"the Handsome",
    u"Cacksone",
    u"the Pussycat",
    u"Smutthy",
    u"the Hellspawn",
    u"the Greasy",
    u"Fastone",
    u"the Rasp",
    u"the Woomaniser",
    u"the Bull",
    u"the Cord",
    u"Masterkey",
    u"the Pig Nose",
    u"the Daredevil",
    u"the Sweet Talk",
]

thief_abilities = Container(
    "thief_abilities",
    {
        "climber": {
            "name": u"Alpinist",
            "description": u"can get high",
            "provide": ["alpinism"]
        },
        "diver": {
            "name": u"Diver",
            "description": u"holdes breath",
            "provide": ["swimming"]
        },
        "greedy": {
            "name": u"Greedy",
            "description": u"will get more treashues from you",
            "provide": []
        },
        "mechanic": {
            "name": u"Mechanist",
            "description": u"disarms mechanical traps",
            "avoids": ["mechanic_traps"],
            "provide": []
        },
        "magicproof": {
            "name": u"Arcane thief",
            "description": u"disarms magical traps",
            "avoids": ["magic_traps"],
            "provide": []
        },
        "poisoner": {
            "name": u"Poisoner",
            "description": u"ignores venomous guards",
            "avoids": ["poison_guards"],
            "provide": []
        },
        "assassin": {
            "name": u"Assasin",
            "description": u"ignores common guards",
            "avoids": ["regular_guards"],
            "provide": []
        },
        "night_shadow": {
            "name": u"Night Shadow",
            "description": u"ignores elite guards",
            "avoids": ["elite_guards"],
            # Это странно, что он может быть пойман обычными стражами
            "provide": []
        },
        "trickster": {
            "name": u"Trickster",
            "description": u"no chance to wake you up",
            "provide": []
        },
    })

thief_items = Container(
    "thief_items",
    {
        "plan": {
            "name": u"Great Plan",
            "level": 1,
            "description": u"more chances to suceed"
        },
        "scheme": {
            "name": u"Secret passage scheme",
            "description": u"ignors fortifications"
        },
        "sleep_dust": {
            "name": u"Sleepdust",
            "description": u"dragon can't wake up"
        },
        "bottomless_sac": {
            "name": u"Bag of holding",
            "dropable": True,
            "description": u"can get more treashures from you"
        },
        "antidot": {
            "name": u"Antidote",
            "description": u"ignores venomous guards",
            "avoids": ["poison_guards"]
        },
        "enchanted_dagger": {
            "name": u"Envenomed dagger",  # Applied
            "dropable": True,
            "description": u"ignores common guards",
            "avoids": ["regular_guards"]
        },
        "ring_of_invisibility": {
            "name": u"Ring of invisibility",  # Applied
            "dropable": True,
            "description": u"ignores elite guards",
            "avoids": ["elite_guards"]
        },
        "flying_boots": {
            "name": u"Boots of flying",  # Applied
            "dropable": True,
            "description": u"can fly",
            "provide": ["flight", "alpinism"]
        },
        "cooling_amulet": {
            "name": u"Cool amulet",  # Applied
            "dropable": True,
            "description": u"protection from fire",
            "provide": ["fireproof"]
        },
        "warming_amulet": {
            "name": u"Hot amulet",  # Applied
            "dropable": True,
            "description": u"protection from cold",
            "provide": ["coldproof"]
        }
    })

# Одинаковые айдишники вещей спасут от того, что у вора может оказаться норамльная.
# As I remember, we planned to use cursed items, but after all we didn't implemented them
thief_items_cursed = Container(
    "thief_items_cursed",
    {
        "plan": {
            "name": u"Плохой план",  # Applied
            "level": -1,
            "cursed": True,
            "description": u"-1 к уровню вора",
            "fails": []
        },
        "bottomless_sac": {
            "name": u"Дырявый мешок",  # Applied
            "cursed": True,
            "description": u"Вор не уносит никаких сокровищ",
            "fails": []
        },
        "enchanted_dagger": {
            "name": u"Проклятый кинжал",  # Applied
            "cursed": True,
            "description": u"Автоматический успех обычных стражей",
            "fails": ["regular_guards"]
        },
        "ring_of_invisibility": {
            "name": u"Кольцо мерцания",  # Applied
            "cursed": True,
            "description": u"Автоматический успех элитных стражей",
            "fails": ["elite_guards"]
        },
        "flying_boots": {
            "name": u"Ощипанные сандалии",  # Applied
            "cursed": True,
            "description": u"Вор автоматически разбивается насмерть, если идет в логово требующее полета",
            "fails": ["flight", "alpinism"],
            "provide": ["flight", "alpinism"]
        },
        "cooling_amulet": {
            "name": u"Морозильный амулет",  # Applied
            "cursed": True,
            "description": u"Вор замораживается насмерть, если идет в огненное логово",
            "fails": ["fireproof"],
            "provide": ["fireproof"]
        },
        "warming_amulet": {
            "name": u"Шашлычный амулет",  # Applied
            "cursed": True,
            "description": u"Вор зажаривается насмерть, если идет в ледяное логово",
            "fails": ["coldproof"],
            "provide": ["coldproof"]
        },
    })

thief_titles = [
    u"Marauder",
    u"Rogue",
    u"Burglar",
    u"Tomb Raider",
    u"Master-thief",
    u"Thief Prince"
]

'''
Calls label shown in value of dictionary. If list is shown, calls all labels shown at list in specified order.
Crucial parameters are:
thief - thief which triggered an event
Additionally for: "start_trap", "die_trap", "pass_trap", "pass_trap_by_luck", "pass_trap_no_influence", "end_trap":
trap - upgrade which triggered an event
Additionally for "pass_trap_by_luck":
drain_luck - amount of luck, removed from thief who passed this trap.
Additionally for "die_item", "receive_item":
item - item that thief get
'''
thief_events = {
    "spawn": "lb_event_thief_spawn",
    "lair_unreachable": "lb_event_thief_lair_unreachable",
    "prepare": "lb_event_thief_prepare",
    "prepare_usefull": "lb_event_thief_prepare_usefull",
    "prepare_useless": "lb_event_thief_prepare_useless",
    "lair_enter": "lb_event_thief_lair_enter",
    "die_inaccessability": "lb_event_thief_die_inaccessability",
    "start_trap": None,
    "die_trap": "lb_event_thief_die_trap",
    "pass_trap": "lb_event_thief_pass_trap",
    "end_trap": None,
    "receive_no_item": "lb_event_thief_receive_no_item",
    "receive_item": "lb_event_thief_receive_item",
    "steal_items": "lb_event_thief_steal_items",
    "retire": None,
    # @Review: Alex: Added new event:label k/v to fill in the gaps:
    "checking_accessability": "lb_event_thief_checking_accessability",
    "checking_accessability_success": "lb_event_thief_checking_accessability_success",
    "trying_to_avoid_traps_and_guards": "lb_event_thief_trying_to_avoid_traps_and_guards",
    "retreat_and_try_next_year": "lb_event_thief_retreat_and_try_next_year",
    "starting_to_rob_the_lair": "lb_event_thief_starting_to_rob_the_lair",
    "took_an_item": "lb_event_thief_took_an_item",
    "lair_empty": "lb_event_thief_lair_empty",
    "awakened_the_dragon": "lb_event_thief_awakened_dragon"
}

#
# Knight
#

knight_first_names = [
    u"Havein",
    u"Lancelott",
    u"Gallahad",
    u"Parcivail",
    u"Boris",
    u"Kay",
    u"Mordredd",
    u"Harret",
    u"Urience",
    u"Yveyn",
    u"Ouen",
    u"Bediver",
    u"Gaheris",
    u"Argavein",
    u"Alan",
    u"Alistair",
    u"Alven",
    u"Alen",
    u"Anakin",
    u"Ardeen",
    u"Arman",
    u"Anrie",
    u"Archibald",
    u"Bardrick",
    u"Bardolf",
    u"Barklai",
    u"Barnabas",
    u"Benvan",
    u"Bartolomeus",
    u"Benjamine",
    u"Bedivir",
    u"Benneth",
    u"Benedict",
    u"Bertran",
    u"Blaine",
    u"Blaze",
    u"Bolduin",
    u"Valentain",
    u"Virgile",
    u"Willford",
    u"Wayland",
    u"Gabriel",
    u"Hammilton",
    u"Garfild",
    u"Hilbert",
    u"Gordon",
    u"Taiven",
    u"Darnell",
    u"Dastin",
    u"Daireel",
    u"Dilbert",
    u"Denzel",
    u"Jarred",
    u"Geralt",
    u"Jaison",
    u"Diggory",
    u"Douglass",
    u"Daiton",
    u"Igglebert",
    u"Ingramm",
    u"Inescent",
    u"Irvain",
    u"Carlail",
    u"Cventine",
    u"Curtis",
    u"Kingsley",
    u"Clarence",
    u"Clivlend",
    u"Connor",
    u"Cristofer",
    u"Kaspian",
    u"Lionnel",
    u"Leopold",
    u"Lindsey",
    u"Listar",
    u"Lorence",
    u"Maximillian",
    u"Melburn",
    u"Milford",
    u"Montgommery",
    u"Mordicain",
    u"Naijell",
    u"Nicolas",
    u"Nordbert",
    u"Nimbus",
    u"Norton",
    u"Norris",
    u"Oberon",
    u"Oldredd",
    u"Orson",
    u"Osbert",
    u"Percie",
    u"Rassel",
    u"Redcliff",
    u"Redmoond",
    u"Reginald",
    u"Rainold",
    u"Rondile",
    u"Ronald",
    u"Rendall",
    u"Sebastian",
    u"Silvester",
    u"Stenlie",
    u"Theiobald",
    u"Timoty",
    u"Thobias",
    u"Trevice",
    u"Willbert",
    u"Willfred",
    u"Warren",
    u"Fabian",
    u"Fredderick",
]

knight_last_names = [
    u"of the Lake",
    u"the Glorious",
    u"of the Meadows",
    u"the Proud",
    u"the Kind",
    u"the Courageous",
    u"the Brave",
    u"the Faithfull",
    u"the Gallant",
    u"the Glorious",
    u"the Handsome",
    u"the Great",
    u"the Radiant",
    u"the Whiteshield",
    u"the Strong",
    u"the Kin Eye",
    u"the Lionehart",
    u"Oakenshield",
    u"the Patient",
    u"the Timid",
    u"the Seeker",
    u"the Adherent",
    u"the Deffender",
    u"the Savior",
    u"the Benevolent",
    u"the Exemplar",
    u"the Sagacious",
    u"the Farseer",
    u"the Wise",
    u"the Marvellous",
    u"the Daydreamer",
    u"a Choosen One",
    u"the Honorable",
    u"the Blessed One",
    u"the Fine",
    u"the Virgin",
    u"the Modest",
    u"the Humble",
    u"the Generous",
    u"the Thrifty",
    u"the Merciful",
    u"the Benignant",
    u"the Sweet Woice",
    u"the Witty",
    u"the Landless",
    u"the White Face",
    u"the Honest",
]

knight_abilities = Container(
    "knight_abilities",
    {
        "brave": {
            "name": u"Braveheart",
            "description": u"no fear of dragons",
            "modifiers": ["fearless"]
        },
        "charmed": {
            "name": u"Charmed",
            "description": u"can get to any lair",
            "modifiers": ["swimming", "flight", "alpinism"]
        },
        "liberator": {
            # Implemented at Knight._ability_modifiers
            "name": u"Liverator",
            "description": u"goes stronger if you hold a captives",
            "modifiers": []
        },
        "fiery": {
            "name": u"Fiery",
            "description": u"stronger attack",
            "modifiers": ['atk_up', 'atk_up']
        },
        "cautious": {
            "name": u"Cautious",
            "description": u"more armor",
            "modifiers": ['def_up', 'def_up']
        }
    }
)

knight_items = Container(
    "knight_items",
    {
        # Breastplates
        "basic_vest": {
            "id": "basic_vest",
            "name": u"Chainmail",
            "description": u"standart armor",
            "type": "vest",
            "basic": True,
            "modifiers": []
        },
        "glittering_vest": {
            "id": "glittering_vest",
            "name": u"Shining platemail",
            "description": u"strong armor",
            "type": "vest",
            "basic": False,
            "modifiers": ['def_up', 'def_up']
        },
        "gold_vest": {
            "id": "gold_vest",
            "name": u"Golden platemail",
            "description": u"great armor",
            "type": "vest",
            "basic": False,
            "modifiers": ['sdef_up']
        },
        "magic_vest": {
            # Implemented at Knight.enchant_equip
            "id": "magic_vest",
            "name": u"Enchanted platemail",
            "description": u"protection from elements",
            "type": "vest",
            "basic": False,
            "modifiers": []
        },
        # Spears
        "basic_spear": {
            "id": "basic_spear",
            "name": u"Steel lance",
            "description": u"standart weapon",
            "type": "spear",
            "basic": True,
            "modifiers": []
        },
        "blued_spear": {
            "id": "blued_spear",
            "name": u"Burhished lance",
            "description": u"strong weapon",
            "type": "spear",
            "basic": False,
            "modifiers": ['atk_up', 'atk_up']
        },
        "spear_with_scarf": {
            "id": "spear_with_scarf",
            "name": u"Lance with scarf",
            "description": u"great weapon",
            "type": "spear",
            "basic": False,
            "modifiers": ['satk_up']
        },
        "dragonslayer_spear": {
            # implemented at Knight._item_modifiers and battle_action
            "id": "dragonslayer_spear",
            "name": u"Dragonslayer lance",  # TODO: implement
            "description": u"kills you outright",
            "type": "spear",
            "basic": False,
            "modifiers": []
        },
        # Swords
        "basic_sword": {
            "id": "basic_sword",
            "name": u"Longsword",
            "description": u"standart weapon",
            "type": "sword",
            "basic": True,
            "modifiers": []
        },
        "glittering_sword": {
            "id": "glittering_sword",
            "name": u"Shiny longsword",
            "description": u"strong weapon",
            "type": "sword",
            "basic": False,
            "modifiers": ['atk_up', 'atk_up']
        },
        "lake_woman_sword": {
            "id": "lake_woman_sword",
            "name": u"Lady of the Lake Sword",
            "description": u"irresistible attack",
            "type": "sword",
            "basic": False,
            "modifiers": ['satk_up']
        },
        "flameberg_sword": {
            "id": "flameberg_sword",
            "name": u"Flamberge",
            "description": u"fiery weapon",
            "type": "sword",
            "basic": False,
            "modifiers": ['sfatk_up', 'sfatk_up']
        },
        "icecracker_sword": {
            "id": "icecracker_sword",
            "name": u"Icecracker sword",
            "description": u"frost weapon",
            "type": "sword",
            "basic": False,
            "modifiers": ['siatk_up', 'siatk_up']
        },
        "thunderer_sword": {
            "id": "thunderer_sword",
            "name": u"The Thunderrer",
            "description": u"thunder weapon",
            "type": "sword",
            "basic": False,
            "modifiers": ['slatk_up', 'slatk_up']
        },
        # Shields
        "basic_shield": {
            "id": "basic_shield",
            "name": u"Heraldic shield",
            "description": u"standart",
            "type": "shield",
            "basic": True,
            "modifiers": []
        },
        "polished_shield": {
            "id": "polished_shield",
            "name": u"Polished shield",
            "description": u"strong",
            "type": "shield",
            "basic": False,
            "modifiers": ['def_up', 'def_up']
        },
        "mirror_shield": {
            # Implemented at Knight._item_modifiers
            "id": "mirror_shield",
            "name": u"Mirror shild",
            "description": u"reflects your breath weapon",
            "type": "shield",
            "basic": False,
            "modifiers": []
        },
        # Horses
        "basic_horse": {
            "id": "basic_horse",
            "name": u"Horse",
            "description": u"standart mount",
            "type": "horse",
            "basic": True,
            "modifiers": []
        },
        "white_horse": {
            "id": "white_horse",
            "name": u"White stallion",
            "description": u"stronger atk and def",
            "type": "horse",
            "basic": False,
            "modifiers": ['atk_up', 'def_up']
        },
        "pegasus": {
            "id": "pegasus",
            "name": u"Pegassus",
            "description": u"can fly",
            "type": "horse",
            "basic": False,
            "modifiers": ['flight']
        },
        "firehorse": {
            "id": "firehorse",
            "name": u"Firehorse",
            "description": u"alpinism, protection from fire",
            "type": "horse",
            "basic": False,
            "modifiers": ['alpinism', 'fire_immunity']
        },
        "sivka": {
            "id": "sivka",
            "name": u"Sivka-Burka",
            "description": u"alpinism, protection from cold",
            "type": "horse",
            "basic": False,
            "modifiers": []
        },
        "kelpie": {
            "id": "kelpie",
            "name": u"Kelpie",
            "description": u"swims underwater",
            "type": "horse",
            "basic": False,
            "modifiers": ['swimming']
        },
        "griffon": {
            "id": "griffon",
            "name": u"Griffin",
            "description": u"can fly, strong mount",
            "type": "horse",
            "basic": False,
            "modifiers": ['atk_up', 'def_up', 'flight']
        },
        # Followers
        "basic_follower": {
            "id": "basic_follower",
            "name": u"Squire",
            "description": u"no use",
            "type": "follower",
            "basic": True,
            "modifiers": []
        },
        "squire": {
            "id": "squire",
            "name": u"Agile squire",
            "description": u"can climb",
            "type": "follower",
            "basic": False,
            "modifiers": ['alpinism']
        },
        "veteran": {
            "id": "veteran",
            "name": u"Veteran squire",
            "description": u"stronger deffence",
            "type": "follower",
            "basic": False,
            "modifiers": ['sdef_up']
        },
        "pythoness": {
            "id": "pythoness",
            "name": u"Farseer",
            "description": u"stronger attack",
            "type": "follower",
            "basic": False,
            "modifiers": ['satk_up']
        },
        "thaumaturge": {
            "id": "thaumaturge",
            "name": u"Wisard",
            "description": u"more atk and def",
            "type": "follower",
            "basic": False,
            "modifiers": ['satk_up', 'sdef_up']
        },
    }
)

knight_titles = [
    u"Poor knight",
    u"Questing knight",
    u"Knight of the Mark",
    u"Noble knight",
    u"Palladin",
    u"Prince"]

knight_events = {
    "spawn": "lb_event_knight_spawn",
    "prepare": None,
    "prepare_usefull": None,
    "prepare_useless": None,
    "receive_item": "lb_event_knight_receive_item",
    "challenge_start": "lb_event_knight_challenge_start",   # Должен возвращать True или False
                                                            # True - бой с рыцарем начинается
                                                            # False - нет
    "challenge_end": "lb_event_knight_challenge_end",       # В ивент передается параметр result, содержащий
                                                            # теги исхода битвы дракона с рыцарем
}

#
# Lair
#

lair_types = Container(
    "lair_types",
    {
        "impassable_coomb": {
            "name": u"impassable comb",
            "inaccessability": 0
        },
        "impregnable_peak": {
            "name": u"impregnable peak",
            "inaccessability": 0,
            "require": ["alpinism"],
            'prerequisite': ['wings']
        },
        "solitude_citadel": {
            "name": u"Solitude citadel",
            "inaccessability": 0,
            "require": ["alpinism", "coldproof"],
            'prerequisite': ['wings', 'ice_immunity']
        },
        "vulcano_chasm": {
            "name": u"Voolcano chasm",
            "inaccessability": 0,
            "require": ["alpinism", "fireproof"],
            'prerequisite': ['wings', 'fire_immunity']
        },
        "underwater_grot": {
            "name": u"Underwater grotto",
            "inaccessability": 0,
            "require": ["swimming"],
            'prerequisite': ['swimming']
        },
        "underground_burrow": {
            "name": u"Underground burrow",
            "inaccessability": 1,
            "require": [],
            'prerequisite': ['can_dig']
        },
        "dragon_castle": {
            "name": u"Dragon castle",
            "inaccessability": 1,
            "require": []
        },
        "castle": {
            "name": u"Old ruins",
            "inaccessability": 1,
            "require": []
        },
        "ogre_den": {
            "name": u"Ogre Den",
            "inaccessability": 1,
            "require": []
        },
        "broad_cave": {
            "name": u"Broad Cave",
            "inaccessability": 1,
            "require": []
        },
        "tower_ruin": {
            "name": u"Tower Ruin",
            "inaccessability": 1,
            "provide": ["magic_traps"]
        },
        "monastery_ruin": {
            "name": u"Monastery Ruin",
            "inaccessability": 1,
            "require": []
        },
        "fortress_ruin": {
            "name": u"Fortress ruin",
            "inaccessability": 2,
            "require": []
        },
        "castle_ruin": {
            "name": u"Castle ruins",
            "inaccessability": 2,
            "require": []
        },
        "ice_citadel": {
            "name": u"Ice citadel",
            "inaccessability": 1,
            "require": ["alpinism", "coldproof"]
        },
        "vulcanic_forge": {
            "name": u"Volcanic Forge",
            "inaccessability": 1,
            "require": ["alpinism", "fireproof"]
        },
        "forest_heart": {
            "name": u"Forest Heart",
            "inaccessability": 2,
            "provide": ["magic_traps"]
        },
        "cloud_castle": {
            "name": u"Cloud Castle",
            "inaccessability": 2,
            "require": ["flight"]
        },
        "underwater_mansion": {
            "name": u"Underwater mansion",
            "inaccessability": 1,
            "require": ["swimming"]
        },
        "underground_palaces": {
            "name": u"Underground Palace",
            "inaccessability": 2,
            "require": ["alpinism"],
            "provide": ["mechanic_traps"]
        },
    }
)

lair_upgrades = Container(
    "lair_upgrades",
    {
        "mechanic_traps": {
            "name": u"Mechanical traps",
            "protection": 1,
            "success": [
                u'Thef bypasses the traps.',
            ],
            "fail": [
                u'Unlucky therf steps on a shiftplate and activates'
                u'deadly blade trap.',
            ]
        },
        "magic_traps": {
            "name": u"Magic trap",
            "protection": 1,
            "success": [
                u'Cunning thief spots a glimer and avoids a magical trap.',
            ],
            "fail": [
                u'Magical trap desintegtates the tresspasser.',
            ]
        },
        "poison_guards": {
            "name": u"Venomous guards",
            "protection": 1,
            "success": [
                u"Venomous beasts can't stop the tresspasser.",
            ],
            "fail": [
                u'Sneaky venomous beast bites the unlucky thief. '
                u'He dies in a great pain...',
            ]
        },
        "regular_guards": {
            "name": u"Common guards",
            "replaces": "smuggler_guards",  # какое улучшение автоматически заменяет
            "protection": 2,
            "success": [
                u'Burglar stealthily stabs guards with dagger, one by one.',
            ],
            "fail": [
                u'Guard spots the thief and raises the alarm. '
                u'After a short but brutal fight thef is defeated and murdered.',
            ]
        },
        "smuggler_guards": {
            "name": u"Mercenary guards",
            "cost": 100,
            "protection": 2,
            "success": [
                u'Burglar stealthily stabs guards with dagger, one by one.',
            ],
            "fail": [
                u'Guard spots the thief and raises the alarm. '
                u'After a short but brutal fight thef is defeated and murdered.',
            ]
        },
        "elite_guards": {
            "name": u"Elite guard",
            "protection": 3,
            "success": [
                u'Under the cower of darkness, thief slips behind '
                u'the elite guard into the treashure chamber.',
            ],
            "fail": [
                u'Thef tried to sneak on an guard of treashure chamber but fails.'
                u'Bloodthirsty beast rips him apart.',

            ]
        },
        "gremlin_fortification": {
            "name": u"Fortifications",
            "inaccessability": 1,
            "protection": 0
        },
        "gremlin_servant": {
            "name": u"Gremlin-servants",
            "cost": 100,
            "protection": 0
        },
        "servant": {
            "name": u"Servants",
            "replaces": "gremlin_servant",  # какое улучшение автоматически заменяет
            "protection": 0
        }
    }
)

attack_types = ['base', 'fire', 'ice', 'poison', 'sound', 'lightning']
protection_types = ['base', 'scale', 'shield', 'armor']

#
# Reputation
#

reputation_levels = {
    0: 0,
    3: 1,
    6: 2,
    10: 3,
    15: 4,
    21: 5,
    28: 6,
    36: 7,
    45: 8,
    55: 9,
    66: 10,
    78: 11,
    91: 12,
    105: 13,
    120: 14,
    136: 15,
    153: 16,
    171: 17,
    190: 18,
    210: 19,
    231: 20
}

reputation_gain = {
    1: u"Common folk will notice this mischief.",
    3: u"Ill fame of dragon rises in Free Kingdoms.",
    5: u"Defiler ill fame rised considerably.",
    10: u"This dread deed will be remembered far and wide.",
    25: u"The legend of this dread deed will persist in ages."
}

#
# Dragon
#

# Names
dragon_names = [
    u'Azogh',
    u'Auring',
    u'Alaphis',
    u'Braghnir',
    u'Bellywyrg',
    u'Bloodwing',
    u'Beorgis',
    u'Buran',
    u'Wicerin',
    u'Wazgor',
    u'Balerion',
    u'Meraxes',
    u'Wxagar',
    u'Syraxis',
    u'Tyraxes',
    u'Wermax',
    u'Arrax',
    u'Kharaxes',
    u'Thadnros',
    u'Moonhide',
    u'Silverwing',
    u'Vermitor',
    u'Shiptif',
    u'Shrikos',
    u'Morgul',
    u'Urraks',
    u'Drogo',
    u'Reyerghal',
    u'Wizerion',
    u'Essovius',
    u'Gicksar',
    u'Wermitrax',
    u'Archoney',
    u'Desterion',
    u'Alhafton',
    u'Torogrim',
    u'Korinstraz',
    u'Ironicus',
    u'Charris',
    u'Itarius',
    u'Izondir',
    u'Lithurgahn',
    u'Taeradh',
    u'Morphals',
    u'Nepharian',
    u'Searnox',
    u'Pyonix',
    u'Ldorynx',
    u'Scipionax',
    u'Erihthon',
    u'Ghoronis',
    u'Gorgatrox',
    u'Artaxerks',
    u'Aitvaras',
    u'Balaur',
    u'Orlangoor',
    u'Shadizar',
]

dragon_surnames = [
    u'teh Furious',
    u'teh Mighty',
    u'teh Sinister',
    u'teh Shtormborn',
    u'teh Omnious',
    u'teh Dark',
    u'teh Baleful',
    u'teh Arrogant',
    u'teh Greedy',
    u'teh Covetous',
    u'teh Mercyless',
    u'teh Ruthless',
    u'teh Proud',
    u'teh Glutton',
    u'teh Loudroar',
    u'teh Horrendous',
    u'teh Deadly',
    u'teh Quarellsome',
    u'teh Awesome',
    u'teh Envious',
    u'teh Vicious',
    u'teh Snakeeyed',
    u'teh Longtail',
    u'teh Ugly',
    u'teh Spikescale',
    u'teh Isidious',
    u'teh Defiller',
    u'teh Devourer',
    u'teh Vivisector',
    u'teh Doomuide',
    u'teh Deathstalker',
    u'teh Shaded',
    u'teh Bloody',
    u'teh Saberthooth',
    u'teh Temper',
    u'teh Shameless',
    u'teh Foul',
    u'teh Crazed',
    u'teh Impaler',
    u'teh Voloptous',
    u'teh Angersome',
    u'teh Gutspiller',
    u'teh Flayer',
    u'teh Vorewhole',
    u'teh Indolent',
    u'teh Slimy',
    u'teh Destroer',
    u'teh Snakeeater',
    u'teh Cursed',
    u'teh Bloodthirsty',
    u'teh Molester',
    u'teh Godless',
    u'teh Powerfull',
    u'teh Lier',
    u'teh Thunderbird',
    u'teh Sneaky',
    u'teh Duplitious',
    u'teh Wise',
    u'teh Kineyed',
    u'teh Impetuous',
    u'teh Unholy',
]

# Sizes
dragon_size = [
    u'Small',
    u'Modestsized',
    u'Large',
    u'Huge',
    u'Gigantic',
    u'Gargantious',
]

dragon_size_description = [
    u'Его размеры вряд ли кого-то впечатлят. '
    u'Хотя и сильно вытянутый в длинну, змей весит не больше чем крупная крестьянская собака.',

    u'Он весит примерно столько же сколько и взрослый, здоровый мужчина. Ничего поразительного.',

    u'Достаточно велик чтобы поконкурировать размерами с небольшой лошадью или откормленным годовалым бычком.',

    u'В местных лесах вряд ли найдётся зверь способный потягаться с ним в размерах. '
    u'Разве что самые откормленные быки или пещерные медведи смогут с ним сравниться.',

    u'Пожалуй по своему весу и размеру он заткнёт за пояс даже африканского слона. '
    u'Не говоря уже об обитателях лесов и полей этого королевства. Тут ему равных нет.',

    u'На его фоне даже титаны смотрятся бледно, разве что кашалот или кракен весит примерно столько же. '
    u'Но могут ли они быть столь же ловкими и смертносными на суше и в воздухе?',
]

head_description = {
    'green': u'have no special abilities',
    'red': u'spews fire',
    'white': u'chilling breath',
    'blue': u'have gills',
    'black': u'spews poisonous gas',
    'iron': u'covered in tough steel-like scales',
    'bronze': u'can dig the earth',
    'silver': u'spews lightning bolts',
    'gold': u'can see the unseen',
    'shadow': u'commands sininster necromantic powers'
}

wings_description = [
    u'He crawls like a big snake.',
    u'He has a mighty wings to fly in the sky.',
    u'he has two pairs of mighty wings',
    u'Он оснащён тремя парами разноразмерных крыльев, обеспечиваюих невероятную маневренность.'
]

paws_description = [
    u'He crawls like a big snake.',
    u'He walks with a pair of mighty legs',
    u'He has two pairs of paws with claws.',
    u'He has three pairs of legs.'
]

special_features = ('tough_scale', 'poisoned_sting', 'clutches', 'horns', 'fangs', 'ugly')

special_description = [
    u'He has an inpenetrable scales.',

    u'He has a deadly poison sting in the tip of the tail.',

    u'His claws are razor shatp.',

    u'The mighty horns are topping his head, providing protection and scary look.',

    u'He has a saber-claws.',

    u'He is so ugly and scary, that no one can look at him straight, '
    u'and weeklings are simply flee in terror.',
]

special_features_rus = {
    "tough_scale": u"Tough scales",
    "poisoned_sting": u"Venomous sting",
    "clutches": u"Razor claws",
    "horns": u"Magnificent horns",
    "fangs": u"Saberthoos fangs",
    "ugly": u"Ugliness",
}

cunning_description = [
    u'The magical spark are flickering in his eyes.',

    u'The flame of magic fires in his eyes. '
    u'His maggical power is great.',

    u'He comands the immense magical powers.',
]

# TODO: Text module with numerals
head_num = [
    u'main',
    u'second',
    u'third',
    u'forth',
    u'fifth',
    u'sixth',
    u'seventh',
    u'eighth',
    u'nineth',
    u'tenth'
]

# heads amount description
head_count = {
    2: u"twoheaded",
    3: u"threheaded",
    4: u"forheaded",
    5: u"fiveheaded",
    6: u"sixheaded",
    7: u"sevenheaded",
    8: u"eightheaded",
    9: u"manyheaded",
    10: u"manyheaded",
    11: u"manyheaded",
}

# Head types(colors)
dragon_heads = {
    'green': [],
    'red': ['fire_breath', 'fire_immunity'],
    'white': ['ice_breath', 'ice_immunity'],
    'blue': ['swimming'],
    'black': ['black_power', 'poison_breath'],  # black_power -- +1 атака
    'iron': ['iron_scale', 'sound_breath'],  # iron_scale -- +1 защита
    'bronze': ['bronze_scale', 'can_dig'],  # bronze_scale -- +1 защита
    'silver': ['silver_magic', 'lightning_immunity'],
    'gold': ['gold_magic', 'greedy'],  # greedy -- -2 к шансам вора
    'shadow': ['shadow_magic', 'fear_of_dark'],  # fear_of_dark -- +2 к страху
}

heads_name_rus = {
    'red': u"red",
    'black': u"black",
    'blue': u"blue",
    'gold': u"golden",
    'silver': u"silver",
    'bronze': u"bronze",
    'iron': u"steel",
    'shadow': u"phantom",
    'white': u"white",
    'green': u"green"
}

dragon_gifts = dict()

# Spells
spell_list = {
    # заговоры -- дают иммунитет к атаке выбранного типа
    'fire_protection': ['fire_immunity'],
    'ice_protection': ['ice_immunity'],
    #'poison_protection': ['poison_immunity'],
    'lightning_protection': ['lightning_immunity'],
    #'sound_protection': ['sound_immunity'],
    # сердца -- дают дыхание нужного типа
    'fire_heart': ['fire_breath'],
    'ice_heart': ['ice_breath'],
    'poison_heart': ['poison_breath'],
    'thunder_heart': ['sound_breath'],
    'lightning_heart': ['lightning_breath'],
    # прочие
    'wings_of_wind': ['wings_of_wind'],
    'aura_of_horror': ['aura_of_horror'],
    'unbreakable_scale': ['virtual_head'],
    'spellbound_trap': ['spellbound_trap'],
    'swimmer_spell': ['swimming'],
    'impregnator': ['impregnator'],
}

# Русское название для отображения заклинания
spell_list_rus = {
    # заговоры -- дают иммунитет к атаке выбранного типа
    'fire_protection': u"Protection from fire",
    'ice_protection': u"Protection from cold",
    #'poison_protection': u"Защита от яда",
    'lightning_protection': u"Protection from lightning",
    #'sound_protection': u"Защита от грома",
    # сердца -- дают дыхание нужного типа
    'fire_heart': u"Fire breather",
    'ice_heart': u"Ice breather",
    'poison_heart': u"Toxic breather",
    'thunder_heart': u"Thunder roar",
    'lightning_heart': u"Lightning thrower",
    # прочие
    'wings_of_wind': u"Wing of Wind",
    'aura_of_horror': u"Sinister Aura",
    'unbreakable_scale': u"Phantom head",
    'spellbound_trap': u"Magic trap",
    'swimmer_spell': u"Gills",
    'impregnator': u"Impregnator",
}

effects_list = {
    # effects from food and other sourcesспецеффекты от еды и других прокачек дракона помимо собственных заклинаний
    'boar_meat': ['atk_up'],
    'bear_meat': ['def_up'],
    'griffin_meat': ['mg_up'],
    'shark_meat': ['mg_up'],
}

modifiers = {
    # global
    'fire_immunity': Modifier(),
    'community': Modifier(),
    'poison_immunity': Modifier(),
    'lightning_immunity': Modifier(),
    'ice_immunity': Modifier(),
    'sound_immunity': Modifier(),
    'magic_immunity': Modifier(),

    'flight': Modifier(),
    'alpinism': Modifier(),
    'swimming': Modifier(),

    'atk_up': Modifier(attack=('base', (1, 0))),  # 1 простая атака
    'satk_up': Modifier(attack=('base', (0, 1))),  # 1 верная атака
    'sfatk_up': Modifier(attack=('fire', (0, 1))),  # 1 верная атака огнем
    'sfatk_2up': Modifier(attack=('fire', (0, 2))), # 2 верных атаки огнём
    'siatk_up': Modifier(attack=('ice', (0, 1))),  # 1 верная атака льдом
    'siatk_2up': Modifier(attack=('ice', (0, 2))),  # 2 верных атаки льдом
    'slatk_up': Modifier(attack=('lightning', (0, 1))),  # 1 верная атака молнией  
    'slatk_2up': Modifier(attack=('lightning', (0, 2))),  # 2 верных атаки молнией    
    'def_up': Modifier(protection=('base', (1, 0))),  # 1 защита
    'sdef_up': Modifier(protection=('base', (0, 1))),  # 1 верная защита
    'decapitator': Modifier(),  # Обезглавливатель, при наличии этого модификатора у врага дракон вместо получения урона
                                # сразу теряет одну голову
    # Knight-specific
    'fearless': Modifier(),
    # Dragon-specific
    'can_dig': Modifier(),
    'greedy': Modifier(),
    'virtual_head': Modifier(),
    'spellbound_trap': Modifier(),
    'impregnator': Modifier(),
    # Заклинания
    'fire_breath': Modifier(attack=('fire', (0, 1))),
    'ice_breath': Modifier(attack=('ice', (0, 1))),
    'poison_breath': Modifier(attack=('poison', (0, 1))),
    'sound_breath': Modifier(attack=('sound', (0, 1))),
    'lightning_breath': Modifier(attack=('lightning', (0, 1))),
    'black_power': Modifier(attack=('base', (1, 0))),
    'iron_scale': Modifier(protection=('scale', (1, 0))),
    'bronze_scale': Modifier(protection=('scale', (1, 0))),
    'silver_magic': Modifier(magic=1),
    'gold_magic': Modifier(magic=1),
    'shadow_magic': Modifier(magic=1),
    'fear_of_dark': Modifier(fear=2),
    'aura_of_horror': Modifier(fear=1),
    'wings_of_wind': Modifier(energy=1),
    #
    'size': Modifier(attack=('base', (1, 0)), protection=('base', (1, 0)), fear=1),
    'paws': Modifier(attack=('base', (1, 0)), energy=1),
    'wings': Modifier(protection=('base', (1, 0)), energy=1),
    'tough_scale': Modifier(protection=('scale', (0, 1))),
    'clutches': Modifier(attack=('base', (0, 1))),
    'fangs': Modifier(attack=('base', (2, 0)), fear=1),
    'horns': Modifier(protection=('base', (2, 0)), fear=1),
    'ugly': Modifier(fear=2),
    'poisoned_sting': Modifier(attack=('poison', (1, 1))),
    'cunning': Modifier(magic=1),
    #
    'mg_up': Modifier(magic=1),
}


def get_modifier(name):
    if name in modifiers:
        return modifiers[name]
    raise NotImplementedError(name)

# lairs, images
lair_image = {
    'ravine': 'ravine'
}

# Dictionary with "showplaces",
# key - stage name,
# value - tuple of stage name for menu and mark you should jump to
special_places = {
    # лесная пещера с огром
    'enc_ogre': (u"Ogre den", 'lb_enc_fight_ogre'),
    'explore_ogre_den': (u"Explore ogre den", 'lb_enc_explore_ogre_den'),
    'create_ogre_lair': (u"Make lair in ogre den", 'lb_enc_create_ogre_lair'),
    # йотун
    'jotun_full': (u"Ice citadel", 'lb_jotun'),
    'jotun_empty': (u"Abandoned ice citadel", 'lb_jotun_empty'),
    # Ифрит
    'ifrit_full': (u"Volcanic cave", 'lb_ifrit'),
    'ifrit_empty': (u"Abandoned volcanic cave", 'lb_ifrit_empty'),
    # Тритон
    'triton_full': (u"Underwater mansion", 'lb_triton'),
    'triton_empty': (u"Abandoned underwater mansion", 'lb_triton_empty'),
    # Титан
    'titan_full': (u"Cloud castle", 'lb_titan'),
    'titan_empty': (u"Abandoned cloud castle", 'lb_titan_empty'),
    # рыцарский манор
    'manor_full': (u"Manor", 'lb_manor'),
    'manor_empty': (u"Abandoned manor", 'lb_manor_empty'),
    # деревянный замок
    'wooden_fort_full': (u"Motte and bailey", 'lb_wooden_fort'),
    'wooden_fort_empty': (u"Abandoned fort", 'lb_wooden_fort_empty'),
    # монастрыь
    'abbey_full': (u"Monasty", 'lb_abbey'),
    'abbey_empty': (u"Abandoned monasty", 'lb_abbey_empty'),
    # каменный замок
    'castle_full': (u"Castle", 'lb_castle'),
    'castle_empty': (u"Abandoned castle", 'lb_castle_empty'),
    # королевский замок
    'palace_full': (u"Palace", 'lb_palace'),
    'palace_empty': (u"Abandoned palace", 'lb_palace_empty'),
    # зачарованный лес
    'enter_ef': (u"Enchanted wood", 'lb_enchanted_forest'),
    'dead_grove': (u"Defiled wood", 'lb_dead_grove'),
    # задний проход в морию
    'backdor_open': (u"Back door", 'lb_backdor'),
    'backdor_sealed': (u"Back door", 'lb_backdor_sealed'),
    # мория
    'frontgates_guarded': (u"Mountain Gate", 'lb_frontgates'),
    'frontgates_open': (u"Brocken Gates", 'lb_dwarf_ruins'),
}

quest_list = (
    {   # только для дебага, не используется
        'min_lvl': 25,  # минимальный уровень дракона для получения квеста
        'max_lvl': 25,  # максимальный уровень дракона для получения квеста
        'text': u"Проживи 5 лет.",  # текст квеста
        'fixed_time': 25,  # количество лет на выполнение квеста, не зависящее от уровня дракона
        # ключевое слово для описания задачи, 'autocomplete' - задача выполняется автоматически
        'task': 'autocomplete',
    },
    {   # Набрать дурной славы (уровень 2)
        'min_lvl': 1,  # минимальный уровень дракона для получения квеста
        'max_lvl': 1,  # максимальный уровень дракона для получения квеста
        # текст квеста, {0} будет заменён на требуемый уровень
        'text': u"(Gain 1 infamity) \n Ты уже вырос, пора заняться настоящим делом, сыночек. Там за пределами моих владений, лежат земли Вольных Народов, это они унизили меня и изгнали в эти бесплодные пустоши. Ты станешь началом Рода несущего вольным погибель. \n Давай-ка проверим на что ты способен родной. Отправляйся в земли Вольных Народов и стяжай себе дурную славу - пусть о тебе говорят, пусть тебя боятся. Только не лезь на рожон, мы же не хотим чтобы ты умер не оставив сыновей, верно? Если видишь что враг силён - убегай. Бей исподтишка. Рыскай по лесам и полям, убивай одиноких женщин, разоряй стада. Мы увидим как растёт твоя дурная слава. Когда люди начнут шептаться возвращайся ко мне и я подарю тебе сына, который станет сильнее тебя и сможет сделать больше. \n Мой совет - не оставайся спать в Землях Вольных. Когда ты устанешь то захочешь вздремнуть. И сон твой продлится год, а может быть и дольше если надо будет залечивать раны. А пока ты спишь, люди будут охотиться за тобой и твоими сокровищами. Чем больше твоя дурная слава, тем больше внимания ты привлечёшь, а пока что тебе это не нужно. Если успеешь достаточно набедокурить до того как совсем устанешь и захочешь спать, иди лучше сразу сюда. В крайнем случае переночуй в овражке. \n Но если пропадёшь больше чем на пять лет, я сделаю продолжателем рода другого. ",
        'fixed_time': 5,  # количество лет на выполнение квеста, не зависящее от уровня дракона
        # ключевое слово для описания задачи, 'reputation' - проверяется уровень дурной славы
        'task': 'reputation',
        'fixed_threshold': 1,  # 'fixed_'+ ключевое слово для задания фиксированного требуемого значения
    },
    {   # Породить любое потомство.
        'min_lvl': 2,  # минимальный уровень дракона для получения квеста
        'max_lvl': 2,  # максимальный уровень дракона для получения квеста
        'text': u"(make any offspring) \n Ну вот ты и подрос, родной. Ты сильнее совего папы, но всё же ещё не так могуч чтобы отомстить за меня - это дело для твоих потомков. А знаешь что нужно делать чтобы завести детей? Нет-нет, не со мной, глупыш. Пока что не со мной. Надо проверить на что ты способен, для продолжения Рода я выберу самого лучшего из выводка. \n   У тебя очень сильное семя, ты сможешь оплодотворить кого захочешь. Но принять и выносить твоего ребёнка смогут не все. Чем больше сил будет у женщины, тем лучше выйдет потомство. Обязательно бери дев, которые ещё не знали мужского прикосновения. Разве что для великанш это не имеет значения, одно отродье они смогут тебе подарить даже если уже рожали обычных детей до того. Ищи для себя лучшую кровь. Горожанка лучше крестьянки. Благородная дама лучше горожанки. У эльфийских дев в крови магия - а значит они дадут отличное потомство. \n   Ты первый в роду и поэтому тебе рано гоняться за волшебными девами, хватит на первой и крестьянок. Поймай где-нибудь у деревни одну, а лучше нескольких. Оплодотвори их и отпусти на волю, ведь в логове за ними некому будет смотреть пока ты спишь. Если их не убьют свои же, то через год, когда проснёшься, они породят тварей. Не драконов конечно, драконов могу породить лишь Я, но всё же это будут монстры которые попортят людям кровушку. Когда что-нибудь вылупится возвращайся ко мне и получишь особую награду!  \n   На всё про всё сроку тебе пять лет. Если не справишься за это время, то назад можешь не возвращаться.",  # текст квеста
        'fixed_time': 5,  # количество лет на выполнение квеста, не зависящее от уровня дракона
        'task': 'offspring',  # ключевое слово для описания задачи, 'offspring' - породить потомство
        # кортеж с требованиями, для выполнения задания нужно выполнить любое из них,
        # 'free_spawn' - потомство, рождённое на воле, 'educated_spawn' - воспитанное потомство
        'task_requirements': (('free_spawn', 'educated_spawn'),)
    },
    {   # Снизить боеспособность королевства.
        'min_lvl': 3,  # минимальный уровень дракона для получения квеста
        'max_lvl': 3,  # максимальный уровень дракона для получения квеста
        'text': u"(rise kingdom mobilization, then drop it down) \n Сегодня день твоего совершеннолетия. Это значит, что пришла пора и тебе как до того твоим предкам, отправляться в Земли Вольных народов. Среди всех, люди самые мерзкие. Они многочисленны и организованы. Их королевство огромно. И они уже знают о появлении драконов, а значит будут защищаться. \n   Когда твоя дурная слава растёт, вслед за ней растёт мобилизация королевства. Они будут увеличивать свою армию, вышлют на дороги патрули. Чем выше мобилизация, тем лучше защищено королевство. Но мы можем помешать людям собраться с силами. Для этого подойдут любые способы: можно разорять деревни, жечь амбары и мельницы. Тогда в стране начнётся разруха и мобилизация упадёт. Можно наводнить королевство отродьями, которые отвлекут войска на себя. А можно просто заплатить разбойникам с одинокого острова, чтобы они начали саботаж. Так или иначе, но ты должен уметь справляться с угрозой. Вот что ты должен сделать: \n   Сначала стяжай дурную славу и ложись спать. Как проснёшься, люди уже будут суетиться. Тогда то и надо будет сделать что-нибудь, чтобы умерить их пыл. Когда мобилизация упадёт, считай что сделал всё что нужно. Можешь возвращаться ко мне за наградой! \n   Сроку дам тебе десять лет. Этого должно быть более чем достаточно для такой простой задачи. ",  # текст квеста
        'fixed_time': 10,  # количество лет на выполнение квеста, не зависящее от уровня дракона
        # ключевое слово для описания задачи, 'poverty' - проверяется уровень понижения мобилизации из-за разрухи
        'task': 'poverty',
        'fixed_threshold': 1,  # 'fixed_'+ ключевое слово для задания фиксированного требуемого значения
    },
    {   # Переселиться в приличное логово, сделать там любое улучшение, завести слуг и охрану.
        # минимальный уровень дракона для получения квеста
        'min_lvl': 4,
        # максимальный уровень дракона для получения квеста
        'max_lvl': 4,
        # текст квеста
        'text': u"(Get good lair, with guards, servants, fortifications and traps) \n Ты уже совсем взрослый, сынок. И ты намного сильнее чем были первые в твоём Роде, настало время драконам вести себя по королевски. Я хочу чтобы ты хорошенько обосновался на Землях Вольных. Тебе понадобится настоящее драконье логово, не какой-нибудь сырой овраг или дыра в земле. Лучше найди хорошую пещеру или отбей у какого-нибудь рыцаря поместье или небольшой замок. Тебе потребуются слуги и охрана. Лучше всего если тебя будут охранять твои же отродья, но для начала сойдут и наёмники с разбойничьего острова. В качестве слуг можно нанять гремлинов, они будут присматривать за пленницами пока ты спишь. Тварям рождённым в твоём логове ты сможешь приказывать что делать. Если хочешь насолить людям - отпусти их резвиться на волю. Если нужна охрана или слуги которые не возьмут с тебя денег, оставь их в логове - там найдётся место для слуг, цепных ядовитых тварей, обычной охраны и элитного защитника сокровищ. Если же твоё логово уже под защитой, отправляй разумных отродий ко мне - они станут дополнением к войску гоблинов и размножатся под моей рукой. \n   Гремлины искусные мастера - обязательно закажи у них ловушки и укрепления для своего нового логова, чтобы ворам было сложнее добраться до сокровищницы. Отнесись к обустройству логова со всем возможным вниманием, ведь менять его дело хлопотное - переселяясь ты потеряешь всё что нажил до того, кроме разве что сокровищ. \n   Когда у тебя будет достойное жильё со слугами, охраной, ловушками и укреплениями, позови меня посмотреть. Сроку даю тебе десять лет, если справишься то станешь продолжателем Рода.",
        # количество лет на выполнение квеста, не зависящее от уровня дракона
        'fixed_time': 10,
        # ключевое слово для описания задачи, 'lair' - проверяется тип логова и его улучшений
        'task': 'lair',
        # кортеж с описанием препятствий для выполнения квеста,
        # 'impassable_coomb' - буреломный овраг, квест не выполнится с этим типом логова
        'task_obstruction': ('impassable_coomb',),
        # кортеж с требованиями, для выполнения задания нужно выполнить любое из них,
        # чтобы потребовать список требований - нужно использовать кортеж внутри кортежа
        # а для вариантов среди списка требований - нужно использовать котреж,
        # который будет внутри кортежа для списка, который уже внутри кортежа
        'task_requirements': (
            ('mechanic_traps', 'magic_traps', 'gremlin_fortification'),
            ('gremlin_servant', 'servant'),
            ('poison_guards', 'regular_guards', 'elite_guards', 'smuggler_guards'),
        )
    },
    {   # Поймать вора или одолеть рыцаря в собственном логове.
        'min_lvl': 5,  # минимальный уровень дракона для получения квеста
        'max_lvl': 5,  # максимальный уровень дракона для получения квеста
        'text': u"(Kill the thief or knight in your lair) \n В твоём возрасте, твой отец отправился в Земли Вольных и устроил там отличное логово. Правда в деле он его толком так и не проверил. Логово нужно дракону не просто так. Там ты хранишь сокровища и держишь пленниц вынашивающих твоё потомство. Чем больше твоя дурная слава, тем больше злодеев захочет тебя обидеть. \n   Рыцари будут приезжать пока ты спишь, будить тебя громкими звуками боевого рога и вызывать на бой. Ну как их за это ну убивать? Если же рыцарь тебя одолевает, то можно убежать, но тогда все сокровища и пленницы достанутся ему а логово будет потеряно навсегда! \n   Воры не так опасны, но они очень раздражают. Слетаются на золото, словно мухи на мёд. Вор будет пытаться проникнуть в сокровищницу пока ты спишь и стянуть самые ценные вещи прямо у тебя из под носа! Тут то и пригодятся охранники, укрепления и ловушки. \n Обустрой себе неприступное логово и проверь его в деле - поймай вора или одолей рыцаря. Тогда я смогу спать спокойно, зная что мои детки способны сами о себе позаботиться и прожить долгую жизнь в землях наших врагов. \n Четверти века должно хватить, но если справишься быстрее - приходи раньше.",  # текст квеста
        'fixed_time': 25,  # количество лет на выполнение квеста, не зависящее от уровня дракона
        'task': 'event',  # ключевое слово для описания задачи, 'event' - должно произойти какое-то событие
        # кортеж с требованиями, нужно либо 'thief_killer' - поймать вора, либо 'knight_killer' - убить рыцаря
        'task_requirements': (('thief_killer', 'knight_killer'),),
    },
    {   # Набрать дурной славы (уровни 6-11)
        'min_lvl': 6,  # минимальный уровень дракона для получения квеста
        'max_lvl': 11,  # максимальный уровень дракона для получения квеста
        # текст квеста, {0} будет заменён на требуемый уровень
        'text': u"(Gain {0} infamity) \n Садись и слушай, дитя моё. Твои беззаботные дни окончены, теперь ты взрослый и будешь сам по себе, один в мире людей. Ты сможешь позаботиться о себе, как и все те твои предки. Если же хочешь стать продолжателем рода, то покажи себя в деле - стяжай дурную славу (не менее {0}) и возвращайся ко мне за наградой. \n   Впрочем не торопись особо. Времени у нас много, но надо думать о будущем. Золото которое ты соберёшь и отродья которых ты отправишь в мою армию очень пригодятся нам когда придёт час войны. \n   И да будет имя твоё ночным кошмаром для всех Вольных Народов!",
        'lvlscale_time': 5,  # на что нужно умножить уровень дракона, чтобы получить число лет на выполнение
        # ключевое слово для описания задачи, 'reputation' - проверяется уровень дурной славы
        'task': 'reputation',
        'fixed_threshold': 5,  # задаёт фиксированное значения для задачи
        # число, на которое нужно умножить уровень дракона, чтобы получить необходимый уровень
        'lvlscale_threshold': 1,
    },
    {   # Набрать сокровищ
        'min_lvl': 6,  # минимальный уровень дракона для получения квеста
        'max_lvl': 10,  # максимальный уровень дракона для получения квеста
        # текст квеста, {0} будет заменён на требуемый уровень
        'text': u"(Gain {0} wealth) \n Вижу как горят твои глаза при виде золота и женских форм. Ты стал совсем взрослым и в тебе окрепли драконьи страсти. Это отлично. Но здесь всё золото принадлежит мне, как и все женские прелести. Если хочешь что-то для себя, милый, отправляйся в земли Вольных Народов. Там достаточно металла и плоти иди и возьми! \n   Наша армия растёт, им нужно снаряжение, оружие, продовольствие. Нужно золото. Собери для меня сокровища которые стоили бы не меньше  {0} фартингов. Если твоё золотое ложе будет достаточно дорогим, я позволю тебе продолжить твой Род и твои потомки прославят тебя!",
        'lvlscale_time': 5,  # на что нужно умножить уровень дракона, чтобы получить число лет на выполнение
        'task': 'wealth',  # ключевое слово для описания задачи, 'wealth' - проверяется стоимость сокровищ
        'fixed_threshold': 10000,  # задаёт фиксированное значения для задачи
        # число, на которое нужно умножить уровень дракона, чтобы получить необходимый уровень
        'lvlscale_threshold': 5000,
    },
    {   # Подарок владычице
        'min_lvl': 6,  # минимальный уровень дракона для получения квеста
        'max_lvl': 12,  # максимальный уровень дракона для получения квеста
        # текст квеста, {0} будет заменён на требуемый уровень
        'text': u"(Give me a gift, item {0} worth or more) \n Хочешь меня? Я знаю, знаю. Чем старше ты становишься, тем больше хочешь. Тебя снедает желание продолжить свой род, но это право надо заслужить, сын мой. Женщин знаешь ли не всегда похищают и насилуют, со мной этот трюк не пройдёт. Но я буду благосклонна, если ты подаришь мне что-нибудь красивое. И дорогое. Не меньше {0} фартингов, а лучше больше! Уверена ты сможешь отыскать что-нибудь подходящее в сокровищницах Вольных Народов или даже соберёшь нужные материалы и сделаешь что-то уникальное специально для меня. Ведь ты хочешь меня… но пройдут годы прежде чем сможешь получить. Пусть эта страсть питает тебя, дитя моё. Пусть перерастает в злобу. Я хочу чтобы Вольные почувствовали твою ярость! Иди и принеси мне подарок, я буду терпелива, я дождусь тебя. ",
        'lvlscale_time': 5,  # на что нужно умножить уровень дракона, чтобы получить число лет на выполнение
        'task': 'gift',  # ключевое слово для описания задачи, 'wealth' - проверяется стоимость сокровищ
        'fixed_threshold': 1500,
        # число, на которое нужно умножить уровень дракона, чтобы получить необходимый уровень
        'lvlscale_threshold': 100,
    },
    {   # Породить потомка от великанши.
        'min_lvl': 7,  # минимальный уровень дракона для получения квеста
        'max_lvl': 11,  # максимальный уровень дракона для получения квеста
        'text': u"(Make offspring wih giantess) \n Поздравляю с совершеннолетием. Ты уже вырос и готов, я вижу как ты на меня глядишь. Всему своё время. Сначала докажи что ты настоящий мужчина. Обрюхатить крестьянку много ума не надо, с этим и гоблин справится. Но если ты заведёшь потомство от великанши, это уже достижение. Тогда и я соглашусь что ты достоин стать продолжателем Рода. \n   Только не забывай пожалуйста, что кроме пушечного мяса нашей армии нужно и золото, чем больше ты соберёшь, тем лучше мы будем готовы к войне. \n   Теперь ступай, сей ужас в землях Вольных Народов!",  # текст квеста
        'fixed_time': 50,  # количество лет на выполнение квеста, не зависящее от уровня дракона
        'task': 'offspring',  # ключевое слово для описания задачи, 'offspring' - породить потомство
        # кортеж с требованиями, для выполнения задания нужно выполнить любое из них, 'giantess' - потомок от великанши
        'task_requirements': 'giantess',
        # требования для анатомии дракона - список из вариантов, достаточных для выполнения задания
        # каждый вариант - словарь, в котором значение - необходимый модификатор анатомии дракона,
        # а значение - пороговое значение, достаточное для выполнения требования
        'anatomy_required': ({'size': 4}, {'cunning': 1}),
        # наличие этого ключа - задание выполняется только один раз в течение игры,
        # значение - ключ для game.unique, который добавится после выполнения
        'unique': 'giantess'
    },
    {   # Разорить рощу альвов
        'min_lvl': 8,  # минимальный уровень дракона для получения квеста
        'max_lvl': 12,  # максимальный уровень дракона для получения квеста
        'text': u"(Raze elven forest) \n Ты вырос. Стал таким могучим и большим. Сильнее любого из твоих предков, я ведь помню каждого в твоём роду. Ещё немного и драконы будут готовы исполнить своё предназначение. Но не ты. Однако для тебя у меня есть испытание достойное твоего могущества и великолепия. До сих пор мы больше досаждали людям, а они и правда самые мерзкие среди всех. Но есть ещё и другие. В лесах прячутся трусливые альвы, дети богини Дану. Покажи им на что способны драконы. Найди и уничтожь их священное древо, убей их владык, оскверни их волшебные рощи. Там тебя ждут несметные богатства и прекрасные вечно-юные девы. Но помни, что ни одна из них не сравнится со мной. А меня ты сможешь получить только тогда, когда одолеешь лесной народ. \n   Ступай!",  # текст квеста
        'fixed_time': 75,  # количество лет на выполнение квеста, не зависящее от уровня дракона
        'prerequisite': 'giantess',  # ключ для game.unique, который необходим для получения этой задачи
        'task': 'event',  # ключевое слово для описания задачи, 'event' - должно произойти какое-то событие
        # кортеж с требованиями, для выполнения задания нужно выполнить любое из них,
        # 'ravage_sacred_grove' - разорить рощу альвов
        'task_requirements': 'ravage_sacred_grove',
        # наличие этого ключа - задание выполняется только один раз в течение игры,
        # значение - ключ для game.unique, который добавится после выполнения
        'unique': 'ravage_sacred_grove'
    },
    {   # Устроить логово в подгорном царстве цвергов
        'min_lvl': 9,  # минимальный уровень дракона для получения квеста
        'max_lvl': 12,  # максимальный уровень дракона для получения квеста
        'text': u"(Make lair in Dwarves Kingdom) \n Ох, какой же ты большой стал. Сильнее всех прочих, я уверена что именно ты станешь продолжателем Рода, мой милый. Но как и всем твоим предкам, сначала тебе придётся доказать что ты этого достоин. Люди для тебя не угроза. Даже альвы не устоят. Но в Вольных Землях нет большего богатства чем таят в себе подгорные чертоги цвергов. Наложить на них лапу будет очень и очень не просто, задача как раз для такого могучего змея как ты. Одолей цевргов и устрой своё логово в сокровщнице их короля и тогда я стану твоей. \n    Ступай. Близок час когда все Вольные Народы склонятся перед могуществом моих детей.",  # текст квеста
        'fixed_time': 75,  # количество лет на выполнение квеста, не зависящее от уровня дракона
        'prerequisite': 'ravage_sacred_grove',  # ключ для game.unique, который необходим для получения этой задачи
        'task': 'lair',  # ключевое слово для описания задачи, 'lair' - проверяется тип логова и его улучшений
        # кортеж с требованиями, для выполнения задания нужно выполнить любое из них,
        # 'ravage_sacred_grove' - разорить рощу альвов
        'task_requirements': 'underground_palaces',
        # наличие этого ключа - задание выполняется только один раз в течение игры,
        # значение - ключ для game.unique, который добавится после выполнения
        'unique': 'underground_palaces'
    },
    {   # Захватить столицу
        'min_lvl': 13,  # минимальный уровень дракона для получения квеста
        'max_lvl': 20,  # максимальный уровень дракона для получения квеста
        'text': u"(Lead the Army of Darkness and raze the Capital) \n Подойди ко мне, сын мой. Каким же большим и сильным ты вырос. Нам нет нужды больше ждать, ты будешь тем кто отомстит за меня. Ты положишь к моим ногам короны владык Вольных Народов. Исполнишь предназначение ради которого был создан твой Род. \n   Не торопись, я дам тебе достаточно времени на подготовку. Позаботься о том, чтобы наша армия была в полной готовности, нам нужно много бойцов и чем разнообразнее они будут тем лучше. Когда настанет время выступать, помни что тебе придётся пройти несколько битв и времени на отдых не будет. В каждой битве у нас будут потери. Большие если ты останешься в стороне, меньшие если встанешь на остриё атаки. Если понадобится, один раз я сражусь сама. Когда столица людей падёт, остальные сдадутся сами...",  # текст квеста
        'fixed_time': 1000,  # количество лет на выполнение квеста, не зависящее от уровня дракона
        'task': 'event',  # ключевое слово для описания задачи, 'event' - должно произойти какое-то событие
        # кортеж с требованиями, для выполнения задания нужно выполнить любое из них,
        # 'victory' - заглушка для победы
        'task_requirements': 'victory',
    },
)

# Список всех доступных для дракона событий
dragon_events = (
    'ravage_sacred_grove',  # Добавляется при уничтожении священной рощи альвов
    'thief_killer',  # Убил вора
    'knight_killer',  # Убил рыцаря
)

# Словарь с набором параметров создания/покупки вещей для упрощения вызова
craft_options = {
    'jeweler_buy': {
        'is_crafting': False, 
        'quality': ['rough', 'common', 'skillfully', 'mastery'], 
        'alignment': ['human'], 
        'base_cost': 0, 
        'price_multiplier': 200,
    },
    'jeweler_craft': {
        'is_crafting': True, 
        'quality': ['skillfully'], 
        'alignment': ['human'], 
        'base_cost': 200, 
        'price_multiplier': 0,
    },
    'gremlin': {
        'is_crafting': True, 
        'quality': ['random'], 
        'alignment': ['random'], 
        'base_cost': 100, 
        'price_multiplier': 0,
    },
    'servant': {
        'is_crafting': True, 
        'quality': ['common'], 
        'alignment': [], 
        'base_cost': 0, 
        'price_multiplier': 0,
    },
}

# Различный лут
loot = {
    'palace': [
        'taller',
        'taller',
        'taller',
        'taller',
        'dublon',
        'dublon',
        'dublon',
        'dish',
        'dish',
        'goblet',
        'goblet',
        'cup',
        'cup',
        'casket',
        'statue',
        'tabernacle',
        'icon',
        'tome',
        'mirror',
        'band',
        'pendant',
        'broch',
        'gemring',
        'seal',
        'crown',
        'scepter',
        'chain',
        'fibula',
        'silver',
        'gold',
        'ivory',
        'agate',
        'shell',
        'horn',
        'amber',
        'granate',
        'turmaline',
        'aqua',
        'black_pearl',
        'topaz',
        'saphire',
        'ruby',
        'emerald',
    ],

    'knight': [
        'goblet',
        'statue',
        'tome',
        'band',
        'pendant',
        'ring',
        'gemring',
        'seal',
        'armbrace',
        'chain',
        'fibula',
        'taller',
        'taller',
        'taller',
        'dublon',
        'dublon',
    ],
    
    'jeweler': [
        'taller',
        'taller',
        'dublon',
        'dublon',
        'casket',
        'phallos',
        'band',
        'diadem',
        'tiara',
        'earring',
        'necklace',
        'pendant',
        'ring',
        'broch',
        'gemring',
        'armbrace',
        'legbrace',
        'chain',
        'fibula'
    ],
    
    'smuggler': [
        'silver',
        'gold',
        'mithril',
        'adamantine',
        'jasper',
        'turquoise',
        'jade',
        'malachite',
        'corall',
        'ivory',
        'agate',
        'shell',
        'horn',
        'amber',
        'crystall',
        'beryll',
        'tigereye',
        'granate',
        'turmaline',
        'aqua',
        'pearl',
        'elven_beryll',
        'black_pearl',
        'topaz',
        'saphire',
        'ruby',
        'emerald',
        'goodruby',
        'goodemerald',
        'star',
        'diamond',
        'black_diamond',
        'rose_diamond',
        'taller',
        'dublon',
        'taller',
        'dublon'
    ],
    
    'klad': [
        'goblet',
        'statue',
        'band',
        'diadem',
        'tiara',
        'earring',
        'necklace',
        'pendant',
        'ring',
        'broch',
        'gemring',
        'seal',
        'armbrace',
        'legbrace',
        'crown',
        'scepter',
        'chain',
        'fibula',
        'silver',
        'gold',
        'mithril',
        'adamantine',
        'jasper',
        'turquoise',
        'jade',
        'malachite',
        'corall',
        'ivory',
        'agate',
        'shell',
        'horn',
        'amber',
        'crystall',
        'beryll',
        'tigereye',
        'granate',
        'turmaline',
        'aqua',
        'pearl',
        'elven_beryll',
        'black_pearl',
        'topaz',
        'saphire',
        'ruby',
        'emerald',
        'goodruby',
        'goodemerald',
        'star',
        'diamond',
        'black_diamond',
        'rose_diamond',
        'taller',
        'dublon',
        'taller',
        'dublon',
        'taller',
        'dublon',
        'taller',
        'dublon',
        'taller',
        'dublon',
    ],
    
    'coins': [
        'farting',
        'taller',
        'dublon'
    ],

    'church': [
        'goblet',
        'cup',
        'casket',
        'statue',
        'tabernacle',
        'icon',
        'tome',
        'seal',
    ],
    
    'raw_material': [
        'silver',
        'silver',
        'silver',
        'silver',
        'silver',
        'silver',
        'silver',        
        'gold',
        'gold',
        'gold',
        'gold',
        'gold',
        'mithril',
        'adamantine',
        'jasper',
        'turquoise',
        'jade',
        'malachite',
        'corall',
        'ivory',
        'agate',
        'shell',
        'horn',
        'amber',
        'crystall',
        'beryll',
        'tigereye',
        'granate',
        'turmaline',
        'aqua',
        'pearl',
        'elven_beryll',
        'black_pearl',
        'topaz',
        'saphire',
        'ruby',
        'emerald',
        'goodruby',
        'goodemerald',
        'star',
        'diamond',
        'black_diamond',
        'rose_diamond'
    ],

    'any': [
        'farting',
        'taller',
        'dublon',
        'dish',
        'goblet',
        'cup',
        'casket',
        'statue',
        'tabernacle',
        'icon',
        'tome',
        'mirror',
        'comb',
        'phallos',
        'band',
        'diadem',
        'tiara',
        'earring',
        'necklace',
        'pendant',
        'ring',
        'broch',
        'gemring',
        'seal',
        'armbrace',
        'legbrace',
        'crown',
        'scepter',
        'chain',
        'fibula',
        'silver',
        'gold',
        'mithril',
        'adamantine',
        'jasper',
        'turquoise',
        'jade',
        'malachite',
        'corall',
        'ivory',
        'agate',
        'shell',
        'horn',
        'amber',
        'crystall',
        'beryll',
        'tigereye',
        'granate',
        'turmaline',
        'aqua',
        'pearl',
        'elven_beryll',
        'black_pearl',
        'topaz',
        'saphire',
        'ruby',
        'emerald',
        'goodruby',
        'goodemerald',
        'star',
        'diamond',
        'black_diamond',
        'rose_diamond'
    ],
}

# список специальных мест людей
human_special_places = [
    'lb_manor_found',
    'lb_wooden_fort_found',
    'lb_abbey_found',
    'lb_castle_found',
    'lb_palace_found',
]

game_events = {
    "mobilization_increased": "lb_event_mobilization_increase",
    "poverty_increased": "lb_event_poverty_increase",
    "no_thief": "lb_event_no_thief",    # Не было активного вора и новый не нашелся
    "no_knight": "lb_event_no_knight",  # Не было активного рыцаря и новый не нашелся
    "sleep_start": "lb_event_sleep_start",
    "sleep_new_year": "lb_event_sleep_new_year",
    "sleep_end": "lb_event_sleep_end",
}

dark_army = {
    "grunts": {
        0: u"После поражения Госпожи в Битве Шести Воинств от её армии остались жалкие ошмётки. "
           u"Немногие выжившие гоблины прячутся по своим пещерам и "
           u"размножаются словно кролики в попытке пополнить ряды войск. ",
        10: u"Хорошая новость: на бесплодных равнинах собралось достаточно агрессивных тварей, "
           u"чтобы из них можно было собрать настоящее войско. "
           u"Плохая: это войско будет уступать по численности тому что могут собрать Вольные Народы.",
        25: u"Пещер и дыр уже не хватает чтобы дать укрытие всем уродливым воинам живущим под рукой Госпожи. "
            u"Бесплодные равнины стали местом огромной стройки - тут и там возникают целые городки из шатров, "
            u"трудолюбиво окружаемые рвами, насыпями и частоколами. "
            u"На первый взгляд бойцов тут не меньше чем может выставить на поле коалиция Вольных Народов.",
        50: u"Взглянув на бесплодные равнины в ночи трудно понять где кончается усыпанное звёздами небо и "
            u"начинается выгоревшая земля с мириадами костров дающих свет и тепло воинам Госпожи. "
            u"Днём можно увидеть многие тысячи шатров покрывающие долину словно заросли ядовитых грибов. "
            u"Тут и там снуют вестовые и дозорные. "
            u"Эта огромная Орда захлестнёт малочисленные войска Вольных Народов словно морской прибой."
    },
    "elites": {
        0: u"Но каково бы не было количество этих войск их главной слабостью является отсутствие элитных бойцов. "
           u"Столкнувшись на поле боя с великанами, эльфийскими магами и боевыми машинами цвергов, "
           u"Госпожа поняла что противостоять им смогут лишь существа "
           u"многократно превосходящие по силе людей или гоблинов. Именно таких должны породить драконы. "
           u"Именно в них отчаянно нуждается войско Госпожи.",
        1: u"Тут и там можно заметить огромные силуэты элитных бойцов. "
           u"Их тут не много, однако в ключевой момент они встанут на острие атаки. ",
        5: u"На каждый отряд мелких тварей вроде гоблинов тут приходится хотя бы один элитный боец, "
           u"порождённый драконом от самой сильной крови Вольных Народов. "
           u"Каждый их этих могучих гигантов сам стоит в бою целой армии.",
        10: u"В этом войске столько элитных бойцов, "
           u"что обычная мелочь вроде гоблинов служит лишь для разведки и поддержки их действий. "
           u"Ударную мощь обеспечивают уродливые гиганты порождённые драконами от самой могучей крови Вольных Народов."
    },
    "diversity": {
        0: u"Армия тьмы не отличается разнообразием, "
           u"подавляющее большинство бойцов относится к одному единственному виду. "
           u"Воины Вольных Народов уже отлично умеют сражаться с такими тварями и "
           u"обладают отработанной тактикой против них.",
        2: u"Разнообразие войск не слишком велико, "
           u"хотя порождения драконов будут выгодно дополнять обычных гоблинов на поле боя. "
           u"Тем не менее Вольным Народам не составит труда выработать тактику противодействия и "
           u"изучить сильные и слабые места всех бойцов Госпожи.",
        4: u"Порождения драконов собравшиеся под знамёна Госпожи очень разнообразны. "
           u"Здесь есть дылды и коротышки, стремительные лазутчики и массивные штурмовики, всех цветов, размеров и форм. "
           u"Кого-то украшает чеушая, кого-то рога. "
           u"Выгодно дополняя друг друга на поле боя "
           u"вся эта пёстрая компания не позволит Вольным Народам использовать простую и привычную тактику боя.",
        7: u"Тут столько разнообразных тварей что наверное даже сама Госпожа не сможет различить их всех. "
           u"Бесконтрольно смешиваясь между собой "
           u"отродья драконов порождают новые мутатнтные гибриды с невероятными свойствами. "
           u"Когда начнётся война, Вольные Народы не будут знать как бороться с ними."
    },
    "equipment": {
        1: u"Денег на снаряжение армии катастрофически не хватает. Воины Госпожи ходят в одних набедренных повязках, "
           u"вооружаются кривыми дубинами и заострёнными палками вместо копий. "
           u"Только некоторые могут позволить себе грубую броню из плохо обработанных шкур.",
        2: u"Армия снаряжена по минимуму. Рядовые воины могут надеяться получить железное копьё, "
           u"плетёный щит и простой стёганный доспех. Элита вооружается чуть лучше, но всё же картина далека от желаемой.",
        3: u"Сокровища драконов позволили неплохо снарядить бойцов Госпожи. "
           u"Даже у рядовых воинов есть полный комплект вооружения и брони, "
           u"а элита закована в воронёную сталь с ног до головы. "
           u"Ряды чёрных пик и щитов на поле боя будут смотреться очень внушительно.",
        4: u"За долгие годы драконы скопили для Госпожи такую кучу сокровищ, "
           u"что её с лихвой хватает для вооружения всей армии по самому высшему разряду. "
           u"Тяжёлая пехота и кавалерия вооружена до зубов, а элитные бойцы щеголяют волшебным оружием и доспехами. "
    },
    "force": {
        0: u"Выступать с такими силами против Вольных Народов будет просто самоубийством. Разве что дракон сам выиграет все битвы.",
        500: u"Хотя армия тьмы и окрепла за последние годы, к битве с Вольными Народами она пока не готова. Дракону прийдётся брать основной удар на себя в каждом бою, чтобы иметь хоть какие-то шансы.",
        1000: u"В общем и целом Армия Тьмы достаточно боеспособна, чтобы иметь шансы в битвах с войском Вольных Народов. "
              u"Однако полной уверенности в победе быть не может. Дракон должен будет поддержать свои войска личным примером.",
        1800: u"За долгие годы подготовки Армия Тьмы не просто воспаряла, но и стала могущественнее чем когда-либо. "
              u"Войско Вольных Народов будет смято и растоптано этой неодолимой силой. Даже не учитывая помощи которую могут лично оказать Дракон и сама Владычица."
    }
}
#Achievements
def achieve_target(target, tag=None):
    for achievement in achievements_list:
        if tag == "wealth" or tag == "treasure" or tag == "reputation":
            if achievement.goal == tag:
                    achievement.progress(target)
        elif achievement.goal == tag and target in achievement.targets:
            achievement.progress(target)
def achieve_restart(reason):
    for achievement in achievements_list:
        if achievement.restartif == reason:
            achievement.restart()
def achieve_fail(reason):
    for achievement in achievements_list:
        if achievement.failif == reason:
            achievement.fail()
def achieve_win(dragon):
    achieve_target("win", "win")
    if dragon.size > 1:
        achieve_fail("too_big")
    if dragon.magic > 0:
        achieve_fail("dragon_magic")
    for n in xrange(dragon.size):
        achieve_target("size", "win")
    for head in dragon.heads:
        if head != "green":
            achieve_target("colored_head", "win")
        achieve_target("head", "win")
    if dragon.wings == 1 and dragon.paws == 2 and len(dragon.heads) == 1:
        achieve_target("archetype", "win")
    else:
        achieve_target(dragon.kind, "win")
    achieve_target(dragon.color_eng, "win")
def store_achievements(storage_dict):
    temporary_storage = {}
    for achievement in achievements_list:
        if achievement.unlocked and achievement.name not in storage_dict.keys():
            storage_dict[achievement.name] = achievement.description
            temporary_storage[achievement.name] = achievement.description
    return temporary_storage
class Achievement(object):
    def __init__(self, name="", description="", goal=None, targets=None, restartif=None, failif=None, *args, **kwagrs):
        self.name = name
        self.description = description
        self.unlocked = False
        self.failed = False
        self.restartif = restartif
        self.failif = failif
        self.goal = goal
        self.targets = targets
        self.targets_completed = []
    def progress(self, target):
        if self.failed:
            return
        if self.targets:
            if self.goal == "wealth" or self.goal == "treasure" or self.goal == "reputation":
                for i in self.targets:
                    if target >= i:
                        self.targets.remove(i)
                        self.targets_completed.append(i)
                
            else:
                self.targets_completed.append(target)
                self.targets.remove(target)
                    
        if not self.targets and not self.unlocked:
            self.unlock()
    def unlock(self):
        if not self.failed:
            self.unlocked = True
    def fail(self):
        self.failed = True
    def restart(self):
        if not self.unlocked and self.targets_completed:
            self.targets.extend(self.targets_completed)
            self.targets_completed = []

achievements_list = [Achievement(name = u"Великий змей",
                                 description = u"Достиг победы в сюжетном режиме",
                                 goal = "win",
                                 targets = ["win"]),
                     Achievement(name = u"Осквернитель",
                                 description=u"Сделал логово в эльфийском лесу",
                                 goal = "lair",
                                 targets = ["forest_heart"]),
                     Achievement(name = u"Смауг Великолепный",
                                 description = u"Сделал логово в подгорных чертогах",
                                 goal = "lair",
                                 targets = ["underground_palaces"]),
                     Achievement(name = u"Великолепное ложе",
                                 description = u"Достиг суммарной стоимости сокровищ 100.000 фартингов",
                                 goal = "wealth",
                                 targets = [100000]),
                     Achievement(name = u"Венец коллекции",
                                 description = u"Иметь в сокровищнице предмет стоимостью больше 3000 фартингов",
                                 goal = "treasure",
                                 targets = [9000]),
                     Achievement(name = u"Легендарный тиран",
                                 description = u"Достичь уровня дурной славы больше 19",
                                 goal = "reputation",
                                 targets = [19]),
                     Achievement(name = u"Осеменитель",
                                 description = u"Спарился со всеми видами не-великанш играя за одного дракона",
                                 goal = "impregnate",
                                 targets = ["peasant", "citizen", "princess", "elf", "mermaid"], #вернуть когда появятся  "thief", "knight",
                                 restartif = "new_dragon"),
                     Achievement(name = u"Отец титанов",
                                 description = u"Спарился со всеми видами великанш играя за одного дракона",
                                 goal = "impregnate",
                                 targets = ["ice", "fire", "titan", "ogre", "siren"],
                                 restartif = "new_dragon"),
                     Achievement(name = u"Неуязвимый",
                                 description = u"Достиг победы в сюжетном режиме не потеряв ни одной головы",
                                 goal = "win",
                                 targets = ["win"],
                                 failif = "lost_head"),
                     Achievement(name = u"Абсолютный хищник",
                                 description = u"Победить ангела, титана, и железного голема одним и тем же драконом",
                                 goal = "kill",
                                 targets = ["golem", "angel", "titan"],
                                 restartif = "new_dragon"),
                     Achievement(name = u"Дитя предназначения",
                                 description = u"Выйграть игру захватом земель вольных народов",
                                 goal = "win",
                                 targets = ["conquer"]),
                     Achievement(name = u"Иуда",
                                 description = u"Выйграть игру победой над владычицей",
                                 goal = "win",
                                 targets = ["betray"]),
                     Achievement(name = u"Архетип",
                                 description = u"Достиг победы в сюжетном режиме с подтипом: дракон",
                                 goal = "win",
                                 targets = ["archetype"]),
                     Achievement(name = u"Йормунгард",
                                 description = u"Достиг победы в сюжетном режиме драконом не имеющем крыльев и конечностей",
                                 goal = "win",
                                 targets = [u"ползучий гад"]),
                     Achievement(name = u"Змей горыныч",
                                 description = u"Достиг победы в сюжетном режиме с подтипом: многоглавый дракон",
                                 goal = "win",
                                 targets = [u"многоглавый дракон"]),
                     Achievement(name = u"Наследие Тиамат",
                                 description = u"Достиг победы драконом с 3+ разными цветами",
                                 goal = "win",
                                 targets = ["colored_head", "colored_head", "colored_head"]),
                     Achievement(name = u"Лернейская гидра",
                                 description = u"Достиг победы с 4+ головами",
                                 goal = "win",
                                 targets = ["head", "head", "head", "head"]),
                     Achievement(name = u"Левиафан",
                                 description = u"Достиг победы драконом максимального размера",
                                 goal = "win",
                                 targets = ["size", "size", "size", "size", "size", "size"]),
                     Achievement(name = "T-Rex",
                                 description = u"Достиг победы зеленым линдвурмом без магии, с одной головой и размером больше 4",
                                 goal = "win",
                                 targets = ["size", "size", "size", "size", u"линдвурм", "green"],
                                 failif = "dragon_magic"),
                     Achievement(name = u"Годзила",
                                 description = u"Достиг победы красным линдвурмом с размером больше 4",
                                 goal = "win",
                                 targets = ["size", "size", "size", "size", u"линдвурм", "red"]),
                     Achievement(name = u"Фейский дракончик",
                                 description = u"Достиг победы драконом самого маленького размера",
                                 goal = "win",
                                 targets = ["size"],
                                 failif = "too_big"),
                     Achievement(name = u"Недрёмное око",
                                 description = u"Достиг победы не потеряв ни одного сокровища из-за воров или рыцарей",
                                 goal = "win",
                                 targets = ["win"],
                                 failif = "lost_treasure"),
                     Achievement(name = u"Пасхальный кролик",
                                 description = u"Собрать все пасхалки",
                                 goal = "easter_eggs",
                                 targets = ["domiki_done", "redhood_done"])
                    ]
