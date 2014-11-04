init python:
    from pythoncode import core
    from pythoncode import girls_data

label lb_test_main:
    nvl clear
    while True:
        menu:
            "Краткая сводка":
                python hide:
                    tmp = "Уровень мобилизации: [game.mobilization.level]"
                    tmp+= "\nУровень разрухи: [game.poverty.value]"
                    tmp+= "\nОчки/уровень дурной славы: [game.dragon.reputation.points]/[game.dragon.reputation.level]"
                    tmp+= "\nУровень дракона: [game.dragon.level]"
                    tmp+= "\nМощь дракона:"
                    for type in data.attack_types:
                        tmp+= "\n  %s: %s" % (str(type), str(game.dragon.attack()[type]))
                    tmp+= "\nЗащита дракона:"
                    for type in data.protection_types:
                        tmp+= "\n  %s: %s" % (str(type), str(game.dragon.protection()[type]))
                    tmp+= "\nАрмия Тьмы:"
                    tmp+= "\n  Рядовые войска: [game.army.grunts]. [game.army.grunts_list]"
                    tmp+= "\n  Элитные войска: [game.army.elites]. [game.army.elites_list]"
                    tmp+= "\n  Разнообразие войск: [game.army.diversity]. "
                    tmp+= "\n  Денег в казне: [game.army.money]. Уровень экипировки: [game.army.equipment]"
                    tmp+= "\n  Сила армии Тьмы: [game.army.force] (армия сильна на [game.army.power_percentage] %)."
                    narrator(tmp)
                return
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
        "Ослабить армию Тьмы":
            $ game.army.power_percentage -= 10
        "Работа с сокровищницей":
            call lb_test_debug_treasury
        "Добавить девушку":
            python:
                from pythoncode import treasures
                girls_menu = []
                for girl_type in girls_data.girls_info.keys():
                    girls_menu.append((treasures.capitalizeFirst(girl_type), girl_type))
                girl_type = renpy.display_menu(girls_menu)
                game.girls_list.new_girl(girl_type)
                game.girls_list.jail_girl()
        "Потратить одну энергию":
            $ res = game.dragon.drain_energy()
            if res:
                game.dragon "Силы покинули меня."
            else:
                game.dragon "Я и так истощен."
        "Создать потомство":
            call lb_choose_dragon
        "Логово":
            menu:
                "Создать логово":
                    call lb_test_debug_create_lair
                "Редактировать гемы в сокровищнице":
                    call screen sc_treasury_gems
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
    
    
label lb_test_debug_treasury:  
    while True: 
        menu:
            "Добавление денег":
                "Стоимость сокровищ до добавления: [game.lair.treasury.wealth]"
                $ treasure_list = treasures.gen_treas(10, ['farting', 'farting', 'dublon'], 'elf', 1, 1000, "")
                $ game.lair.treasury.receive_treasures(treasure_list)
                $ treasure_list = game.lair.treasury.treasures_description(treasure_list)
                $ treasure_list = '\n'.join(treasure_list)
                "Список добавленных монет:\n[treasure_list]"
                "Стоимость сокровищ после добавления: [game.lair.treasury.wealth]"
            "Добавление слитков":
                "Стоимость сокровищ до добавления: [game.lair.treasury.wealth]"
                $ test_list = treasures.gen_treas(10, ["silver", "gold", "mithril", "adamantine"], 'elf', 1, 1000000, "")
                $ treasure_list = game.lair.treasury.treasures_description(test_list)
                $ treasure_list = '\n'.join(treasure_list)
                "Список добавленных слитков:\n[treasure_list]"
                $ game.lair.treasury.receive_treasures(test_list)
                "Стоимость сокровищ после добавления: [game.lair.treasury.wealth]"
            "Добавление материалов":
                "Стоимость сокровищ до добавления: [game.lair.treasury.wealth]"
                $ test_list = treasures.gen_treas(10, treasures.material_types.keys(), 'elf', 1, 1000000, "")
                $ treasure_list = game.lair.treasury.treasures_description(test_list)
                $ treasure_list = '\n'.join(treasure_list)
                "Список добавленных материалов:\n[treasure_list]"
                $ game.lair.treasury.receive_treasures(test_list)
                "Стоимость сокровищ после добавления: [game.lair.treasury.wealth]"
            "Добавление камней":
                "Стоимость сокровищ до добавления: [game.lair.treasury.wealth]"
                $ test_list = treasures.gen_treas(10, treasures.gem_types.keys(), 'elf', 1, 1000000, "")
                $ treasure_list = game.lair.treasury.treasures_description(test_list)
                $ treasure_list = '\n'.join(treasure_list)
                "Список добавленных камней:\n[treasure_list]"
                $ game.lair.treasury.receive_treasures(test_list)
                "Стоимость сокровищ после добавления: [game.lair.treasury.wealth]"
            "Добавление сокровищ":
                "Стоимость сокровищ до добавления: [game.lair.treasury.wealth]"
                $ test_list = treasures.gen_treas(10, treasures.treasure_types.keys(), 'elf', 1, 1000000, "")
                $ treasure_list = game.lair.treasury.treasures_description(test_list)
                $ treasure_list = '\n'.join(treasure_list)
                "Список добавленных сокровищ:\n[treasure_list]"
                $ game.lair.treasury.receive_treasures(test_list)
                "Стоимость сокровищ после добавления: [game.lair.treasury.wealth]"
            "Ограбление":
                "Стоимость сокровищ до ограбления: [game.lair.treasury.wealth]"
                $ abducted_list = game.lair.treasury.rob_treasury(10)
                $ abducted_list = game.lair.treasury.treasures_description(abducted_list)
                $ abducted_list = '\n'.join(abducted_list)
                "Список украденного: [abducted_list]"
                "Стоимость сокровищ после ограбления: [game.lair.treasury.wealth]"
            "Назад":
                return
    return
        
