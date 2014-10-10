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
    
    #Сокровища
    any_trs_list = ['farting', 'taller', 'dublon', 'dish', 'goblet', 'cup', 'casket', 'statue', 'tabernacle', 'icon', 'tome', 'mirror', 'comb', 'phallos', 'band', 'diadem', 'tiara', 'earring', 'necklace', 'pendant', 'ring', 'broch', 'gemring', 'seal', 'armbrace', 'legbrace', 'crown', 'scepter', 'chain', 'fibula', 'silver', 'gold', 'mithril', 'adamantine', 'jasper', 'turquoise', 'jade', 'malachite', 'corall', 'ivory', 'agate', 'shell', 'horn', 'amber', 'crystall', 'beryll', 'tigereye', 'granate', 'turmaline', 'aqua', 'pearl', 'elven_beryll', 'black_pearl', 'topaz', 'saphire', 'ruby', 'emerald', 'goodruby', 'goodemerald', 'star', 'diamond', 'black_diamond', 'rose_diamond']
    coins_list = ['farting', 'taller', 'dublon']
    klad_list = ['goblet', 'statue', 'band', 'diadem', 'tiara', 'earring', 'necklace', 'pendant', 'ring', 'broch', 'gemring', 'seal', 'armbrace', 'legbrace', 'crown', 'scepter', 'chain', 'fibula', 'silver', 'gold', 'mithril', 'adamantine', 'jasper', 'turquoise', 'jade', 'malachite', 'corall', 'ivory', 'agate', 'shell', 'horn', 'amber', 'crystall', 'beryll', 'tigereye', 'granate', 'turmaline', 'aqua', 'pearl', 'elven_beryll', 'black_pearl', 'topaz', 'saphire', 'ruby', 'emerald', 'goodruby', 'goodemerald', 'star', 'diamond', 'black_diamond', 'rose_diamond', 'taller', 'dublon']
    smuggler_list = ['silver', 'gold', 'mithril', 'adamantine', 'jasper', 'turquoise', 'jade', 'malachite', 'corall', 'ivory', 'agate', 'shell', 'horn', 'amber', 'crystall', 'beryll', 'tigereye', 'granate', 'turmaline', 'aqua', 'pearl', 'elven_beryll', 'black_pearl', 'topaz', 'saphire', 'ruby', 'emerald', 'goodruby', 'goodemerald', 'star', 'diamond', 'black_diamond', 'rose_diamond', 'taller', 'dublon', 'taller', 'dublon']
    knight_list = ['goblet', 'statue', 'tome', 'band', 'pendant', 'ring', 'gemring', 'seal', 'armbrace', 'chain', 'fibula', 'taller', 'dublon']
    jewler_list = ['casket', 'phallos', 'band', 'diadem', 'tiara', 'earring', 'necklace', 'pendant', 'ring', 'broch', 'gemring', 'armbrace', 'legbrace', 'chain', 'fibula']
    

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
        "place == 'prison'", "img/scene/prison.png",
        )
    define narrator = Character(None, kind=nvl)


# Начало игры
    
label start:
    
    python:
        #Инициализируем game в начале игры, а не при инициализации. Для того чтобы 
        game = core.Game(NVLCharacter)
        game.dragon.avatar = get_dragon_avatar(game.dragon.color_eng())
        narrator = game.narrator    # Ради совместимости с обычным синтаксисом RenPy
            
        bloodlust = game.dragon.bloodiness
        dragon = game.dragon
    
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
