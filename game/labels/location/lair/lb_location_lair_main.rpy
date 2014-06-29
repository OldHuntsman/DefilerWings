label lb_location_lair_main:
    $ place = 'lair'
    show place
    
    python:                
        dragon.avatar = get_dragon_avatar(dragon.heads[0])
        ddescription = '  '
        ddescription += size_texts[dragon.size()] + ' ' + dragon.color() + ' ' + dragon.kind()
        i = -1
        for head in dragon.heads:
            i += 1 
            if dragon.heads[i] != 'green': ddescription += '\n  Его %s голова ' % womennum[i] + head_texts[dragon.heads[i]]
        if dragon.wings() == 0 and dragon.paws() == 0:
            ddescription += wingstxt[0]
        else:
            if dragon.wings() > 0:
                ddescription += '\n  ' + wingstxt[dragon.wings()]
                
            if dragon.paws() > 0:
                ddescription += '\n  ' +pawstxt[dragon.paws()]
    
    menu:
        'Отладка дракона':
            #чтобы вывести сообщение от имени дракона можно использовать "game.dragon"
            game.dragon "[ddescription]"
            
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
