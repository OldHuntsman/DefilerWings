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
        "Случайный энкаунтер":
            call lb_test_example_encounter
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
        "Создать логово":
            menu:
                "Пока логово только одно. Нужно больше логов."
                "Буреломный овраг":
                    $ game.lair = core.Lair()
    return
    
label lb_test_example_inaccessible_menu:
    nvl clear
    python:
        # Составляем список параметров для выбора.
        menu_options = [("Делать что-нибудь (Заблокировано:нужен остаток энергии меньше 2)", 1, game.dragon.energy()>=2, game.dragon.energy()<2),
                        ("Делать что-нибудь", 2, game.dragon.energy()<2, game.dragon.energy()<2),
                        ("Назад", 3, True, True)]
        # Для описания параметров см описание экрана "dw_choice", в данный момент он находится в screens.rpy
        result = renpy.call_screen("dw_choice", menu_options)
        if result == 1:
            pass
        elif result == 2:
            narrator("что-то сделано")
        elif result == 3:
            pass
    "Возвращаемся"
    return
