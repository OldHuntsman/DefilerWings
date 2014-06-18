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
            $ pass
        'Покинуть логово':
            $ pass
        'Тестовый бой':
            menu:
                "Бой с рыцарем"
                jump lb_fight
    return
