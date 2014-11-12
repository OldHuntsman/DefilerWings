init python:
    from pythoncode import battle

label lb_fight(foe = game.foe):
    show expression foe.bg as foeimg
    nvl clear
    $ battle_status = battle.check_fear(game.dragon, foe)
    $ narrator(foe.battle_description(battle_status, game.dragon))

    while 'foe_alive' in battle_status:
        $ battle_status = battle.battle_action(game.dragon, foe)
        $ description = foe.battle_description(battle_status, game.dragon)
        "[description]" 
        
        if 'dragon_dead' in battle_status:
            #TODO замена текущего дракона с возможностью выбора потомка
            "Дракон умер - да здравствует Дракон!"
            call lb_choose_dragon
            hide foeimg
            nvl clear
            $ renpy.pop_return()
            return
        elif 'foe_alive' in battle_status:
            $ chances = show_chances()
            '[chances]'
            nvl clear
            menu:
                'Продолжать бой':
                    pass
                    
                'Отступить':
                    "Вы бежали в логово"
                    hide foeimg
                    nvl clear
                    $ renpy.pop_return()
                    jump lb_location_lair_main
    hide foeimg
    nvl clear
    return

label lb_fight2(foe = game.foe):
    show expression foe.bg as foeimg
    $ battle_status = battle.check_fear(game.dragon, foe)
    $ narrator(foe.battle_description(battle_status, game.dragon))
    
    
    if 'foe_alive' in battle_status:
        $ narrator("Шанс победы дракона: %s %%, шанс ранения дракона: %s %%" % (battle.victory_chance(game.dragon, foe), battle.victory_chance(foe, game.dragon)))

    while 'foe_alive' in battle_status:
        $ battle_status = battle.battle_action(game.dragon, foe)
        $ description = foe.battle_description(battle_status, game.dragon)
        "[description]" 
        if 'dragon_dead' in battle_status:
            #TODO замена текущего дракона с возможностью выбора потомка
            "Дракон умер - да здравствует Дракон!"
            call lb_choose_dragon
            hide foeimg
            nvl clear
            $ renpy.pop_return()
            return
            
        if 'foe_alive' in battle_status:
            nvl clear
            menu:
                'Продолжать бой':
                    pass
                    
                'Отступить':
                    "Вы бежали в логово"
                    hide foeimg
                    nvl clear
                    $ renpy.pop_return()
                    jump lb_location_lair_main
    hide foeimg
    nvl clear
    return
