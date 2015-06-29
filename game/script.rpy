# coding=utf-8

init python hide:
    from pythoncode import shims
    
    shims.renpy_easy_monkey_patch()

init python:
    # Импортируем нужные библиотеки. Возможно это надо засунуть в какой-то отдельный файл инициализации.
    from pythoncode import data, treasures, focus_mask_ext, battle
    from pythoncode.game import Game
    from copy import deepcopy
    
    focus_mask_ext.load_focus_mask_data()
    
    # Заряжаем пасхалки. Их можно будет встретить в игре лишь однажды
    # Встреченную пасхалку следует добавить в persistent.seen_encounters
    # Проверить была ли встречена пасхалка: if <encounter> (not) in persistent.seen_encounters
    if not hasattr(persistent, 'seen_encounters'):
        persistent.seen_encounters = []
    freeplay = bool()
    save_blocked = False
    battle.army_battle = False
    if not persistent.achievements:
        persistent.achievements = {}
    if not persistent.easter_eggs:
        persistent.easter_eggs = []
# Начало игры
    
screen controls_overwrite():
    # Added by Alex on Hunters request, we overwrite default game menu leading to save screen:
    key "game_menu" action ShowMenu("preferences")

label start:
    $ renpy.block_rollback()
    python:
        # Инициализируем game в начале игры, а не при инициализации. Для того чтобы она сохранялась.
        game = Game(adv_character=ADVCharacter, nvl_character=NVLCharacter)
        narrator = game.narrator    # Ради совместимости с обычным синтаксисом RenPy
        # Alex: Zexy Images :)
        sex_imgs = DragonSexImagesDatabase()
    # Added by Alex on Hunters request, we overwrite default game menu leading to save screen:
    show screen controls_overwrite    
        
    # Alex: Чтобы смотреть на какой находишься локации кода в игре
    #if config.developer:
    #    show screen label_callback
        
    # Прокручиваем заставку.
    if not freeplay:
        $ persistent.isida_done = False
        $ persistent.lada_done = False
        $ persistent.kali_done = False        
        call screen sc_intro
    while not game.is_won or not game.is_lost:
        # Если дракона нет выбираем его
        show black as low
        if game.dragon is None or game.dragon.is_dead:
            if not freeplay:
                call lb_choose_dragon from _call_lb_choose_dragon_4
            else:
                call lb_dragon_creator from _call_lb_dragon_creator

        $ target_label = renpy.call_screen("main_map")
        if renpy.has_label(target_label):
            $ renpy.call(target_label)
        else:
            $ renpy.call("lb_location_missed")
    
    return
