label lb_test_example_fight:
    #Позаимствовано из fight.rpy с небольшими изменениями
    scene black
    $ place = "city_gates"
    show place
    'А это уже локация самой битвы'
    $result = game.battle(game.dragon, enemy)
    "Результат боя: [result[1]]"
    #цикл, который заканчивается победой дракона, или отступлением
    #TODO: параметр здоровья дракона, механизм отрубания голов при низком здоровье
    #также завершение боя смертью дракона
    while result[0] == False:
        menu:
            "Вы можете продолжить бой, или отступить"
            'Продолжать бой':
                $ result = game.battle(game.dragon, game.knight)
                "Результат боя: [result[1]]"
            'Отступить':
                "Вы отступили"
                return
    return
