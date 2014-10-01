label lb_location_lair_main:
    $ place = 'lair'
    show place as bg
    
    python:                
        ddescription = '  '
        ddescription += size_texts[game.dragon.size()] + ' ' + game.dragon.color() + ' ' + game.dragon.kind()
        i = -1
        for head in game.dragon.heads:
            i += 1 
            if game.dragon.heads[i] != 'green': ddescription += '\n  Его %s голова ' % womennum[i] + head_texts[game.dragon.heads[i]]
        if game.dragon.wings() == 0 and game.dragon.paws() == 0:
            ddescription += wingstxt[0]
        else:
            if game.dragon.wings() > 0:
                ddescription += '\n  ' + wingstxt[game.dragon.wings()]
                
            if game.dragon.paws() > 0:
                ddescription += '\n  ' +pawstxt[game.dragon.paws()]
    
    menu:
        'Отладка дракона':
            #чтобы вывести сообщение от имени дракона можно использовать "game.dragon"
            game.dragon "[ddescription]"
        'Осмотреть сокровищницу':
            python hide:
                for i in game.lair.treasury.thief_items:
                    item_name = game.lair.treasury.thief_items[i].name
                    game.dragon("Я вижу %s" % item_name)
        'Сотворить заклинание':
            $ pass
        'Чахнуть над златом':
            $ pass
        'Проведать пленниц' if game.girls_list.prisoners_count:
            $ game.girls_list.prison()
        'Лечь спать':
            nvl clear
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
                    game.sleep()
                    game.narrator("game saved")
                    del game_loaded
        'Покинуть логово':
            $ pass
    return
