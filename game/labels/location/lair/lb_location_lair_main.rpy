label lb_location_lair_main:
    $ place = 'lair'
    show place
    
    python:
        ddescription = ''
        ddescription += size_texts[dragon.size()] + ' ' + dragon.color() + ' ' + dragon.kind()
        i = -1
        for head in dragon.heads:
            i += 1 
            if dragon.heads[i] != 'green': ddescription += '\nЕго %s голова ' % womennum[i] + head_texts[dragon.heads[i]]
    
    menu:
        'Отладка дракона':
            #чтобы вывести сообщение от имени дракона можно использовать "game.dragon"
             "[ddescription]"
            
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
                "Бой с рыцарем":
                    jump lb_fight
    return
