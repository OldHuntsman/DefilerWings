label lb_test_main:
    nvl clear
    while True:
        menu:
            "Примеры":
                call lb_test_examples
            "Отладка":
                call lb_test_debug
            "Тестовый бой":
                $ place = "city_gates"           
                menu:
                    "Выберите уровень боя"
                    '1 уровень':
                        $foe = battle.Enemy('calf', gameRef=game, base_character=NVLCharacter)
                        $grdh = battle.test_dragon_gen(test_game=game, test_character=NVLCharacter, level=1)
                    '5 уровень':
                        $foe = battle.Enemy('bull', gameRef=game, base_character=NVLCharacter)
                        $grdh = battle.test_dragon_gen(test_game=game, test_character=NVLCharacter, level=5)
                    '10 уровень':
                        $foe = battle.Enemy('buffalo', gameRef=game, base_character=NVLCharacter)
                        $grdh = battle.test_dragon_gen(test_game=game, test_character=NVLCharacter, level=10)
                    '15 уровень':
                        $foe = battle.Enemy('minotaur', gameRef=game, base_character=NVLCharacter)
                        $grdh = battle.test_dragon_gen(test_game=game, test_character=NVLCharacter, level=15)
                    '20 уровень':
                        $foe = battle.Enemy('Jupiter', gameRef=game, base_character=NVLCharacter)
                        $grdh = battle.test_dragon_gen(test_game=game, test_character=NVLCharacter, level=20)
                nvl clear
                python:
                    ddescription = '  '
                    ddescription += size_texts[grdh.size()] + ' ' + grdh.color() + ' ' + grdh.kind()
                    i = -1
                    for head in grdh.heads:
                        i += 1 
                        if grdh.heads[i] != 'green': ddescription += '\n  Его %s голова ' % womennum[i] + head_texts[grdh.heads[i]]
                    if grdh.wings() == 0 and grdh.paws() == 0:
                        ddescription += wingstxt[0]
                    else:
                        if grdh.wings() > 0:
                            ddescription += '\n  ' + wingstxt[grdh.wings()]
                    
                        if grdh.paws() > 0:
                            ddescription += '\n  ' +pawstxt[grdh.paws()]
                "[ddescription]"
                call lb_fight
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
