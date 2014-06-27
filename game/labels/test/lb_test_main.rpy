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
        "Схватка":
            call lb_test_example_fight
        "Меню с недоступными вариантами":
            call lb_test_example_inaccessible_menu
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
    
label lb_test_example_inaccessible_menu:
    nvl clear
    python:
        menu_options = [("Делать что-нибудь (Заблокировано:нужен остаток энергии меньше 2)", 1, game.dragon.energy()>=2, game.dragon.energy()<2),
                        ("Делать что-нибудь", 2, game.dragon.energy()<2, game.dragon.energy()<2),
                        ("Назад", 3, True, True)]
        result = renpy.call_screen("dw_choice", menu_options)
        if result == 1:
            pass
        elif result == 2:
            narrator("что-то сделано")
        elif result == 3:
            pass
    "Возвращаемся"
    return
