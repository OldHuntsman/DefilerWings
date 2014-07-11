label lb_fight:
    show place
    '[enemy.fight_intro]'
    $result = game.battle(game.dragon, game.knight)
    result[1] "Результат боя"
    #цикл, который заканчивается победой дракона, или отступлением
    #TODO: параметр здоровья дракона, механизм отрубания голов при низком здоровье
    #также завершение боя смертью дракона
    while result[0] == False:
        menu:
            "Вы можете продолжить бой, или отступить"
            'Продолжать бой':
                $ result = game.battle(game.dragon, game.knight)
                result[1] "Результат боя"
            'Отступить':
                "Вы отступили"
                jump lb_location_lair_main
    jump lb_location_lair_main
