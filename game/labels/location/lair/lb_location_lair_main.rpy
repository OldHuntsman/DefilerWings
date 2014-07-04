label lb_location_lair_main:
    $ place = 'lair'
    show place
    
    menu:
        'Отладка дракона':
            game.dragon "I'm dragon"
            $ game.dragon._debug_print()
        'Сотворить заклинание':
            $ pass
        'Чахнуть над златом':
            $ pass
        'Проведать пленниц':
            $ pass
        'Лечь спать':
            python:
                # Делаем хитрую штуку.
                # Используем переменную game_loaded чтобы определить была ли игра загружена.
                # Но ставим ее перед самым сохранинием, используя renpy.retain_after_load() для того
                # чтобы она попала в сохранение.
                if 'game_loaded' in locals() and game_loaded:
                    del game_loaded
                    game.narrator("game loaded")
                    renpy.restart_interaction()
                else:
                    game_loaded = True
                    renpy.retain_after_load()
                    game.save()
                    game.next_year()
                    game.narrator("game saved")
                    del game_loaded
        'Покинуть логово':
            $ pass
        'Тестовый бой':
            menu:
                "Бой с рыцарем":
                    jump lb_fight
    return
