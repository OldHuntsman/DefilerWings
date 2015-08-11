# coding=utf-8

init python hide:
    from pythoncode import shims
    
    shims.renpy_easy_monkey_patch()
    shims.screen_displayable_monkey_patch()

init python:
    # Importing libraries. Maybe we need separat init file?.
    from pythoncode import data, treasures, focus_mask_ext, battle
    from pythoncode.game import Game
    from copy import deepcopy
    
    focus_mask_ext.load_focus_mask_data()
    
    # Easter eggs. Can be seen once per game
    # Seen egg should be added to persistent.seen_encounters
    # To check if egg was seen: if <encounter> (not) in persistent.seen_encounters
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
        # initialize <game> at begining of the game, but no at init. So game could be saved.
        game = Game(adv_character=ADVCharacter, nvl_character=NVLCharacter)
        narrator = game.narrator    # For compability with common Renpy syntax
        # Alex: Zexy Images :)
        sex_imgs = DragonSexImagesDatabase()
    # Added by Alex on Hunters request, we overwrite default game menu leading to save screen:
    show screen controls_overwrite    
        
    # Alex: To see on which location you are in game
    #if config.developer:
    #    show screen label_callback
        
    # Прокручиваем заставку.
    if not freeplay:
        $ persistent.isida_done = False
        $ persistent.lada_done = False
        $ persistent.kali_done = False        
        call screen sc_intro
    while not game.is_won or not game.is_lost:
        # Choose dragon if we have no one
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
