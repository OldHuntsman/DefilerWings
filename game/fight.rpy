# coding=utf-8
init python:
    from pythoncode import battle

label lb_fight(foe=game.foe, skip_fear=False):
    show expression foe.bg as foeimg
    nvl clear
    if not skip_fear:
        $ battle_status = battle.check_fear(game.dragon, foe)
    else:
        $ battle_status = ['foe_intro', 'foe_alive']
    $ narrator(foe.battle_description(battle_status, game.dragon))

    while 'foe_alive' in battle_status:
        $ battle_status = battle.battle_action(game.dragon, foe)
        $ description = foe.battle_description(battle_status, game.dragon)
        "[description]"

        if 'dragon_dead' in battle_status:
            game.dragon "Oh, Mother..."
            if freeplay or battle.army_battle:
                jump lb_game_over
            hide foeimg
            nvl clear
            if foe.kind != 'knight':
                $ renpy.pop_return()
            return "defeat"
        elif 'foe_alive' in battle_status:
            $ chances = show_chances(foe)
            '[chances]'
            nvl clear
            menu:
                'Продолжать бой':
                    pass
                'Отступить' if not battle.army_battle:
                    if foe.kind == 'knight':
                        # Отступаем в новое логово
                        "[game.dragon.name] retreats in disgrace and covers in a makeshift lair"
                        $ game.create_lair()
                    else:
                        "[game.dragon.name] retreats to his lair, to recuperate and make up a new strategy."
                    hide foeimg
                    nvl clear
                    if foe.kind != 'knight':
                        $ renpy.pop_return()
                        jump lb_location_lair_main
                    return "retreat"
    hide foeimg
    nvl clear
    return "win"
