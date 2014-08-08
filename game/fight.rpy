init python:
    from pythoncode import battle

#TODO: заменить grdh на game.dragon
label lb_fight:
    show place
    $ battle_status = battle.check_fear(grdh, foe)
    $ description = foe.battle_description(battle_status, grdh)
    "[description]"
    #цикл, который заканчивается победой дракона, или отступлением
    #TODO: параметр здоровья дракона, механизм отрубания голов при низком здоровье
    #также завершение боя смертью дракона
    while 'foe_alive' in battle_status:
        menu:
            "Вы можете продолжить бой, или отступить"
            'Продолжать бой':
                $ battle_status = battle.battle_action(grdh, foe)
                $ description = foe.battle_description(battle_status, grdh)
                "[description]" 
                if 'dragon_dead' in battle_status:
                    #TODO замена текущего дракона на потомка
                    "Дракон умер - да здравствует Дракон!"
                    jump lb_location_lair_main
                
            'Отступить':
                if type(foe) == core.Knight:
                    #TODO потеря логова, магнитофона импортного, куртки замшевой. Двух!
                    jump lb_location_lair_main
                else:
                    "Вы бежали в логово"
                    jump lb_location_lair_main
    return
