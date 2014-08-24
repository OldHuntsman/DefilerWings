init python:
    from pythoncode import core

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
        "Прямая и косвенная речь":
            game.dragon "Прямая речь"
            game.dragon.third "Косвенная речь"
        "Прокрутка при переполнении окна диалога":
            "Начал говорить"
            while True:
                "Продолжаю говорить"
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
        "Логово":
            menu:
                "Создать логово":
                    call lb_test_debug_create_lair
                "Редактировать воровские предметы":
                    call screen sc_container_editor(game.lair.treasury.thief_items, [data.thief_items, data.thief_items_cursed])
                "Пустить вора на ограбление":
                    if game.thief is not None and game.thief.is_alive():
                        $ game.thief.steal(game.lair)
                    else:
                        "Вора нет или он мертв."
        "Вор":
            menu:
                "(пере)Создать вора":
                    $ game._create_thief()
                "Cоздать вора 1-го уровня":
                    $ game._create_thief(thief_level=1)
                "Изменить уровнень вора":
                    #TODO: implement change of thief level
                    pass
                "Описать вора":
                    if game.thief is not None:
                        $ narrator(game.thief.description())
                    else:
                        "Вора нет"
                "Редактировать умения":
                    if game.thief is not None:
                        $ value = "ololo" #Хз зачем эта строчка
                        call screen sc_container_editor(game.thief.abilities, [data.thief_abilities])
                    else:
                        "Вора нет"
                "Редактировать предметы":
                    if game.thief is not None:
                        call screen sc_container_editor(game.thief.items, [data.thief_items, data.thief_items_cursed])
                    else:
                        "Вора нет"
                "Пустить вора на ограбление":
                    if game.thief is not None and game.thief.is_alive():
                        $ game.thief.steal(game.lair)
                    else:
                        "Вора нет или он мертв."
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

label lb_test_debug_create_lair:
    python:
        menu_options = []
        for a in data.lair_types:
            menu_options.append((data.lair_types[a].name,a, True, True))
        type = renpy.call_screen("dw_choice", menu_options)
        game.create_lair(type)
    return
        
