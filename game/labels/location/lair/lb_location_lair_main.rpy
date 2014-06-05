label lb_location_lair_main:
    $ place = 'lair'
    show place
    
    menu:
        'Сотворить заклинание':
            dragon "I'm dragon"
            $ dragon._debug_print()
        'Чахнуть над златом':
            $ pass
        'Проведать пленниц':
            $ pass
        'Лечь спать':
            $ pass
        'Покинуть логово':
            $ pass
            
    return