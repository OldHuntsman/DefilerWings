﻿init python:
    from pythoncode import data
    from pythoncode import core
    game = core.Game(NVLCharacter)
    dragon = game.dragon #TODO: Заменить везде использование дракона.
    narrator = game.narrator

init:
    transform bot_to_top:
        align(-2, -2)
        linear 100 yalign 3.0
        repeat
    image side dragon = "dragon ava"
    image bg main = "img/bg/main.jpg"  # заставка главного меню
    image place = ConditionSwitch(              
        "place == 'city_gates'", "img/bg/city/outside.png",    # определение фонов для разных мест (потребует доработки)  
        "place == 'lair'", "img/bg/lair/cave.png",
        "place == 'forest'", "img/bg/forest/1.png",
        "place == 'mountain'", "img/bg/mountain/1.png",
        "place == 'plain'", "img/bg/plain/3.png",
        "place == 'road'", "img/bg/road/1.png",
        "place == 'sea'", "img/bg/sea/1.png",
        "place == 'sky'", "img/bg/sky/1.png",
        "place == 'gremlins'", "img/bg/special/gremlins.png",
        "place == 'smuglers'", "img/bg/special/smuglers.png",
        "place == 'mordor'", "img/bg/special/mordor.png",
        )


# Начало игры
    
label start:
    # Прокручиваем заставку.
    call lb_intro
    nvl clear
    $ win = False
    while not win:
        $ target_location = renpy.call_screen("main_map")
        $ target_label = "lb_location_" + target_location + "_main"
        if renpy.has_label(target_label):
            $ renpy.call(target_label)
        else:
            $ renpy.call("lb_location_missed")
    
    return
