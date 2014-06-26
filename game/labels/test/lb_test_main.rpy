label lb_test_main:
    nvl clear
    while True:
        menu:
            "Примеры":
                call lb_test_examples
            "Отладка":
                call lb_test_debug
            "Назад":
                return
    return
    
label lb_test_examples:
    menu:
        "Примеры"
        "Цикл с возвратом":
            call lb_test_example_returnLoop
        "Назад":
            return
    return
    
label lb_test_debug:
    nvl clear
    menu:
        "Отладка"
        "Потратить одну энергию":
            $ res = game.dragon.drain_energy()
            if res:
                game.dragon "Силы покинули меня."
            else:
                game.dragon "Я и так истощен."
    return
