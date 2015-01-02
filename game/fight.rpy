# coding=utf-8
init python:
    from pythoncode import battle

label lb_fight(foe=game.foe):
    show expression foe.bg as foeimg
    nvl clear
    $ battle_status = battle.check_fear(game.dragon, foe)
    $ narrator(foe.battle_description(battle_status, game.dragon))

    while 'foe_alive' in battle_status:
        $ battle_status = battle.battle_action(game.dragon, foe)
        $ description = foe.battle_description(battle_status, game.dragon)
        "[description]"

        if 'dragon_dead' in battle_status:
            # TODO замена текущего дракона с возможностью выбора потомка
            "Дракон умер - да здравствует Дракон!"
            if freeplay:
                $ renpy.unlink_save("1-3")
                $ renpy.full_restart()
            call lb_choose_dragon
            # Не вызываем дракона, потому что он вызвовется перед тем как нас выкинет на карту
            hide foeimg
            nvl clear
            if foe.kind != 'knight':
                $ renpy.pop_return()
            return "defeat"
        elif 'foe_alive' in battle_status:
            $ chances = show_chances(foe=foe)
            '[chances]'
            nvl clear
            menu:
                'Продолжать бой':
                    pass
                'Отступить':
                    if foe.kind == 'knight':
                        # Отступаем в новое логово
                        "Позорно бежав дракон укрылся в буреломном овраге"
                        $ game.create_lair()
                    else:
                        "Вы бежали в логово"
                    hide foeimg
                    nvl clear
                    if foe.kind != 'knight':
                        $ renpy.pop_return()
                        jump lb_location_lair_main
                    return "retreat"
    hide foeimg
    nvl clear
    return "win"
