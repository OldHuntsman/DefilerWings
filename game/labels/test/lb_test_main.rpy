# coding=utf-8
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
                    tmp += "\nУровень разрухи: [game.poverty.value]"
                    tmp += "\nОчки/уровень дурной славы: [game.dragon.reputation.points]/[game.dragon.reputation.level]"
                    tmp += "\nУровень дракона: [game.dragon.level]"
                    tmp += "\nМощь дракона:"
                    for type in data.attack_types:
                        tmp += "\n  %s: %s" % (str(type), str(game.dragon.attack()[type]))
                    tmp += "\nЗащита дракона:"
                    for type in data.protection_types:
                        tmp += "\n  %s: %s" % (str(type), str(game.dragon.protection()[type]))
                    tmp += "\nАрмия Тьмы:"
                    tmp += "\n  Рядовые войска: [game.army.grunts]. [game.army.grunts_list]"
                    tmp += "\n  Элитные войска: [game.army.elites]. [game.army.elites_list]"
                    tmp += "\n  Разнообразие войск: [game.army.diversity]. "
                    tmp += "\n  Денег в казне: [game.army.money]. Уровень экипировки: [game.army.equipment]"
                    tmp += "\n  Сила армии Тьмы: [game.army.force] (армия сильна на [game.army.power_percentage] %)."
                    narrator(tmp)
                return
            "Примеры":
                call lb_test_examples from _call_lb_test_examples
            "Отладка":
                call lb_test_debug from _call_lb_test_debug
            "Ачивки":
                call lb_achievements_list from _call_lb_achievements_list
            "Сбросить ачивки":
                python:
                    for a in persistent.achievements.keys():
                        persistent.achievements.__delitem__(a)
                "Список достижений очищен"
            "Назад":
                return
    return
    
label lb_test_examples:
    menu:
        "Примеры"
        "Цикл с возвратом":
            call lb_test_example_returnLoop from _call_lb_test_example_returnLoop
        "Схватка":
            call lb_test_example_fight from _call_lb_test_example_fight
        "Случайный энкаунтер":
            call lb_test_example_encounter from _call_lb_test_example_encounter
        "Меню с недоступными вариантами":
            call lb_test_example_inaccessible_menu from _call_lb_test_example_inaccessible_menu
        "Прямая и косвенная речь":
            game.dragon "Прямая речь"
            game.dragon.third "Косвенная речь"
        "Прокрутка при переполнении окна диалога":
            "Начал говорить"
            while True:
                "Продолжаю говорить"
        "Девушка":
            $ girl = core.Girl(game_ref = game)
            girl "Прямая речь"
            girl.third "Косвенная речь"
        "Назад":
            return
    return
    
label lb_test_debug:
    nvl clear
    menu:
        "Отладка"
        "Включить дебаговывод":
            $ config.debug = True
        "Королевство":
            menu:
                "Повысить мобилизацию":
                    $ game.mobilization.level += 1
                "Понизить мобилизацию":
                    $ game.mobilization.level -= 1
                "Повысить разруху":
                    $ game.poverty.value += 1
                "Понизить разруху":
                    $ game.poverty.value -= 1
                "Ослабить армию Тьмы":
                    $ game.army.power_percentage -= 10
        "Дракон":
            menu:
                "Потратить одно очко здоровья":
                    $ game.dragon.struck()
                "Добавить одно очко здоровья":
                    $ game.dragon.health += 1
                "Потратить одну энергию":
                    $ res = game.dragon.drain_energy()
                    if res:
                        game.dragon "Силы покинули меня."
                    else:
                        game.dragon "Я и так истощен."
                "Тип дракона":
                    python:
                        head_menu = []
                        for head_type in data.dragon_heads.iterkeys():
                            head_menu.append((data.heads_name_rus[head_type], head_type))
                        game.dragon.heads[0] = renpy.display_menu(head_menu)
                "Создать потомство":
                    call lb_choose_dragon from _call_lb_choose_dragon_3
        "Логово":
            menu:
                "Создать логово":
                    call lb_test_debug_create_lair from _call_lb_test_debug_create_lair
                "Описать логово":
                    nvl clear
                    python hide:
                        lair_description = u"Логово: %s.\n" % game.lair.type.name
                        if len(game.lair.upgrades) > 0: 
                            lair_description += u"Улучшения:\n"
                            for upgrade in game.lair.upgrades.values():   
                                lair_description += u" %s\n" % upgrade.name
                        else:
                            lair_description += u"Улучшений нет"
                        narrator(lair_description)
                "Добавить улучшение":
                    python hide:
                        upgrades_available = [(data.lair_upgrades[u].name, u) for u in data.lair_upgrades if u not in game.lair.upgrades]
                        upg = menu(upgrades_available)
                        game.lair.add_upgrade(upg)

                "Работа с сокровищницей":
                    call lb_test_debug_treasury from _call_lb_test_debug_treasury
                "Добавить девушку":
                    python hide:
                        from pythoncode import treasures
                        girls_menu = []
                        for girl_type in girls_data.girls_info.keys():
                            girl_type_name = girls_data.girls_info[girl_type]['description']
                            girls_menu.append((treasures.capitalizeFirst(girl_type_name), girl_type))
                        girl_type = renpy.display_menu(girls_menu)
                        game.girls_list.new_girl(girl_type)
                        game.girls_list.jail_girl()
                "Редактировать гемы в сокровищнице":
                    call screen sc_treasury_gems
                "Редактировать воровские предметы":
                    call screen sc_container_editor(game.lair.treasury.thief_items, [data.thief_items, data.thief_items_cursed])
                "Пустить вора на ограбление" if game.thief is not None and game.thief.is_alive():
                        $ game.thief.steal(game.lair)
        "Вор":
            menu:
                "(пере)Создать вора (через game)":
                    $ game._create_thief()
                "Cоздать вора (Определенного уровня)":
                    python hide:
                        lvls = []
                        for i in data.thief_titles:
                            lvls.append((i, data.thief_titles.index(i) + 1))
                        thief_lvl = menu(lvls)
                        game._create_thief(thief_level=1)
                "Описать вора" if game.thief is not None:
                    $ narrator(game.thief.description())
                "Редактировать умения" if game.thief is not None:
                    call screen sc_container_editor(game.thief.abilities, [data.thief_abilities])
                "Редактировать предметы" if game.thief is not None:
                    call screen sc_container_editor(game.thief.items, [data.thief_items, data.thief_items_cursed])
                "Пустить вора на ограбление" if game.thief is not None and game.thief.is_alive:
                    $ game.thief.steal(game.lair)
        "Рыцарь":
            menu:
                "(пере)Создать рыцаря (через game)":
                    $ game._create_knight()
                "Cоздать рыцаря (определенного уровня)":
                    python hide:
                        lvls = []
                        for i in data.knight_titles:
                            lvls.append((i, data.knight_titles.index(i) + 1))
                        knight_lvl = menu(lvls)
                        game._create_knight(knight_level=knight_lvl)
                "Описать рыцаря" if game.knight is not None:
                    $ narrator(game.knight.description())
                "Редактировать умения" if game.knight is not None:
                    call screen sc_container_editor(game.knight.abilities, [data.knight_abilities])
                "Редактировать предметы" if game.knight is not None:
                    call screen sc_equip_editor(game.knight, [data.knight_items])
                "Вызвать рыцарем дракона на бой" if game.knight is not None:
                    $ game.knight.go_challenge()
        "Удалить сохранения":
            menu:
                "Сохранение сюжетной игры":
                    $ renpy.unlink_save("1-1")
                    "Сохранение сюжетной игры удалено!"
                "Сохранение свободной игры":
                    $ renpy.unlink_save("1-3")
                    "Сохранение свободной игры удалено!"
                "Назад":
                    pass
    return
    
label lb_test_example_inaccessible_menu:
    nvl clear
    python:
        # Составляем список параметров для выбора.
        menu_options = [("Делать что-нибудь (Заблокировано:нужен остаток энергии меньше 2)", 1, game.dragon.energy() >= 2, game.dragon.energy() < 2),
                        ("Делать что-нибудь", 2, game.dragon.energy() < 2, game.dragon.energy() < 2),
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
            menu_options.append((data.lair_types[a].name, a, True, True))
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

label lb_mob_inc:
    "Оророро"
