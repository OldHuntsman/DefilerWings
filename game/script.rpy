﻿init python:
    #Импортируем нужные библиотеки. Возможно это надо засунуть в какой-то отдельный файл инициализации.
    from pythoncode import data
    from pythoncode import core
    
    #Заряжаем пасхалки. Их можно будет встретить в игре лишь однажды
    one_time_encounters = ['enc_redcape']
    for encounter in one_time_encounters:
        if persistent.encounter == None:
            persistent.encounter = False
    
    
    #Делаем нужные классы
    class Girl(object):
        """
        Базовый класс для всего, с чем можно заниматься сексом.
        """
            
        def __init__(self, gtype = 'peasant'):
            self.gtype = gtype
            self.avatar = "img/avahuman/peasant/1.jpg"
            self.name = u"Дуняша"            
    
    
init:
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
    python:
        #Инициализируем game в начале игры, а не при инициализации. Для того чтобы 
        game = core.Game(NVLCharacter)
        #dragon = game.dragon       #TODO: Заменить везде использование дракона на game.dragon
        game.dragon.avatar = get_dragon_avatar('green')
        narrator = game.narrator    # Ради совместимости с обычным синтаксисом RenPy
        
    # Прокручиваем заставку.
    call screen sc_intro
    nvl clear
    $ win = False
    while not win:
        $ target_label = renpy.call_screen("main_map")
        if renpy.has_label(target_label):
            $ renpy.call(target_label)
        else:
            $ renpy.call("lb_location_missed")
    
    return
