init python:
    from pythoncode import battle

# Тестовая локация для боя
label lb_test_fight:
    show place
    $ battle_status = battle.check_fear(grdh, foe)
    $ description = foe.battle_description(battle_status, grdh)
    "[description]"
    # цикл, который заканчивается победой дракона, или отступлением
    # TODO: параметр здоровья дракона, механизм отрубания голов при низком здоровье
    # также завершение боя смертью дракона
    while 'foe_alive' in battle_status:
        $ battle_status = battle.battle_action(grdh, foe)
        $ description = foe.battle_description(battle_status, grdh)
        "[description]" 
        
        if 'dragon_dead' in battle_status:
            "Дракон умер - да здравствует Дракон!"
            jump lb_location_lair_main
         
        if 'foe_alive' in battle_status:
            menu:      
                "Вы можете продолжить бой, или отступить"
                'Продолжать бой':
                    pass
                    
                'Отступить':
                    jump lb_location_lair_main
    return
