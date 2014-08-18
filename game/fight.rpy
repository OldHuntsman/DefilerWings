init python:
    from pythoncode import battle

label lb_fight:
    show expression foe.img
    $ battle_status = battle.check_fear(game.dragon, foe)
    $ description = foe.battle_description(battle_status, game.dragon)
    "[description]"
    #цикл, который заканчивается победой дракона, или отступлением
    while 'foe_alive' in battle_status:
        $ battle_status = battle.battle_action(game.dragon, foe)
        $ description = foe.battle_description(battle_status, game.dragon)
        "[description]" 
        if 'dragon_dead' in battle_status:
            #TODO замена текущего дракона с возможностью выбора потомка
            "Дракон умер - да здравствует Дракон!"
            $ game.dragon = game.dragon.children()[0]
            $ game.dragon.avatar = get_dragon_avatar(game.dragon.heads[0])
            jump lb_location_lair_main
            
        if 'foe_alive' in battle_status:
            menu:
                "Вы можете продолжить бой, или отступить"
                'Продолжать бой':
                    pass
                    
                'Отступить':
                    if type(foe) == core.Knight:
                        #TODO потеря логова, магнитофона импортного, куртки замшевой. Двух!
                        jump lb_location_lair_main
                    else:
                        "Вы бежали в логово"
                        jump lb_location_lair_main
    return
