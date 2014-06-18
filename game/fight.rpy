label lb_fight:
    $ place = "city_gates"
    show place
    'А это уже локация самой битвы'
    $result = game.battle(game.dragon, game.knight)
    result "Результат боя"
    #цикл, который заканчивается победой дракона, или отступлением
    #TODO: параметр здоровья дракона, механизм отрубания голов при низком здоровье
    #также завершение боя смертью дракона
    while result[0:len(game.dragon.name)+13] == "%s не побеждает"%(game.dragon.name):
        menu:
            "Вы можете продолжить бой, или отступить"
            'Продолжать бой':
                $ result = game.battle(game.dragon, game.knight)
                result "Результат боя"
            'Отступить':
                "Вы отступили"
                jump lb_location_lair_main
    jump lb_location_lair_main
