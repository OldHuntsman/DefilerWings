init python:
    #Импортируем нужные библиотеки. Возможно это надо засунуть в какой-то отдельный файл инициализации.
    from pythoncode import data
    from pythoncode import core
    from pythoncode import treasures
    from copy import deepcopy
    
    #Заряжаем пасхалки. Их можно будет встретить в игре лишь однажды
    #Встреченную пасхалку следует добавить в persistent.seen_encounters
    #Проверить была ли встречена пасхалка: if <encounter> (not) in persistent.seen_encounters
    if not hasattr(persistent, 'seen_encounters'):
        persistent.seen_encounters = []

# Начало игры
    
label start:
    
    python:
        #Инициализируем game в начале игры, а не при инициализации. Для того чтобы 
        game = core.Game(adv_character=ADVCharacter, nvl_character=NVLCharacter)
        narrator = game.narrator    # Ради совместимости с обычным синтаксисом RenPy
    
    # Прокручиваем заставку.
    call screen sc_intro
    # Выбираем дракона
    call lb_choose_dragon
    $ win = False
    while not win:
        $ renpy.block_rollback()
        $ target_label = renpy.call_screen("main_map")
        if renpy.has_label(target_label):
            $ renpy.call(target_label)
        else:
            $ renpy.call("lb_location_missed")
    
    return
