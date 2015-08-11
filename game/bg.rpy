# coding=utf-8
init python:
    import random

    def get_place_bg(type):
        relative_path = "img/bg/" + type  # relative path for renpy engine
        files = [f for f in renpy.list_files() if f.startswith(relative_path)]        
        return random.choice(files)  # get file name

init:
    image bg main = "img/bg/main.jpg"  # main menu background
    image place = ConditionSwitch(
        "place == 'city_gates'", "img/bg/city/outside.jpg",    # background defenition for various places (need update?)
        "place == 'impassable_coomb'", "img/bg/lair/ravine.jpg",
        "place == 'impregnable_peak'", "img/bg/lair/cavelarge.jpg",
        "place == 'solitude_citadel'", "img/bg/lair/icecave.jpg",
        "place == 'vulcano_chasm'", "img/bg/lair/volcanocave.jpg",
        "place == 'underwater_grot'", "img/bg/lair/grotto.jpg",
        "place == 'underground_burrow'", "img/bg/lair/burrow.jpg",
        "place == 'dragon_castle'", "img/bg/lair/dragon_castle.jpg",
        "place == 'castle'", "img/bg/lair/castle_lair.jpg",
        "place == 'ogre_den'", "img/bg/lair/cave.jpg",
        "place == 'broad_cave'", "img/bg/lair/cavelarge.jpg",
        "place == 'forest_heart'", "img/bg/lair/elfruin.jpg",
        "place == 'tower_ruin'", "img/bg/lair/tower_lair.jpg",
        "place == 'monastery_ruin'", "img/bg/lair/crypt_lair.jpg",
        "place == 'fortress_ruin'", "img/bg/lair/fortress_lair.jpg",
        "place == 'castle_ruin'", "img/bg/lair/palace_lair.jpg",
        "place == 'ice_citadel'", "img/bg/lair/icecastle.jpg",
        "place == 'vulcanic_forge'", "img/bg/lair/volcanoforge.jpg",
        "place == 'cloud_castle'", "img/bg/lair/cloud_castle.jpg",
        "place == 'underwater_mansion'", "img/bg/lair/underwater.jpg",
        "place == 'underground_palaces'", "img/bg/lair/dwarfruin.jpg",
        "place == 'forest'", "img/bg/forest/1.jpg",
        "place == 'mountain'", "img/bg/mountain/1.jpg",
        "place == 'plain'", "img/bg/plain/3.jpg",
        "place == 'road'", "img/bg/road/1.jpg",
        "place == 'sea'", "img/bg/sea/1.jpg",
        "place == 'sky'", "img/bg/sky/1.jpg",
        "place == 'gremlins'", "img/bg/special/gremlins.jpg",
        "place == 'smugglers'", "img/bg/special/smugglers.jpg",
        "place == 'mordor'", "img/bg/special/mordor.jpg",
        "place == 'prison'", "img/scene/prison.jpg",
    )
