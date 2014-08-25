init python:
    #Импортируем нужные библиотеки. Возможно это надо засунуть в какой-то отдельный файл инициализации.
    from pythoncode import data
    from pythoncode import core
    from pythoncode import treasures
    from copy import deepcopy
    
    #Заряжаем пасхалки. Их можно будет встретить в игре лишь однажды
    one_time_encounters = ['enc_redcape']
    for encounter in one_time_encounters:
        if persistent.encounter == None:
            persistent.encounter = False
    
init:
    transform bot_to_top:
        align(-2, -2)
        linear 100 yalign 3.0
        repeat
    image side dragon = "dragon ava"
    image blur = "img/intro/blur.png"
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
    define narrator = Character(None, kind=nvl)


# Начало игры
    
label start:
    
    python:
        #Инициализируем game в начале игры, а не при инициализации. Для того чтобы 
        game = core.Game(NVLCharacter)
        game.dragon.avatar = get_dragon_avatar('green')
        narrator = game.narrator    # Ради совместимости с обычным синтаксисом RenPy
        
    # Прокручиваем заставку.
    call screen sc_intro
    show screen status_bar
    $ win = False
    while not win:
        $ renpy.block_rollback()
        $ target_label = renpy.call_screen("main_map")
        if renpy.has_label(target_label):
            $ renpy.call(target_label)
        else:
            $ renpy.call("lb_location_missed")
    
    return
