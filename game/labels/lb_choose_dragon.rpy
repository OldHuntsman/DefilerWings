label lb_choose_dragon:
    #Хардкод на трех драконов.
    $ dragons = []
    python hide:
        used_gifts = []
        used_avatars = []
        if game.dragon is not None:
            used_avatars.append(game.dragon.avatar)
        
        while len(dragons) < 3:
            child = core.Dragon(parent=game.dragon, gameRef=game,base_character=game.base_character)
            if child._gift not in used_gifts and child.avatar not in used_avatars:
                dragons.append(child)
                used_gifts.append(child._gift)
                used_avatars.append(child.avatar)
    
    while True:
        nvl clear
        menu:
            "Выберите дракона"
            "[dragons[0].name]":
                "[dragons[0].description]"
                menu:
                    " " #Костыль чтобы не скрывалось описание дракона
                    "Выбрать этого":
                        $ game.dragon = dragons[0]
                        return
                    "Вернуться":
                        pass
            "[dragons[1].name]":
                "[dragons[1].description]"
                menu:
                    " "
                    "Выбрать этого":
                        $ game.dragon = dragons[1]
                        return
                    "Вернуться":
                        pass
            "[dragons[2].name]":
                "[dragons[2].description]"
                menu:
                    " "
                    "Выбрать этого":
                        $ game.dragon = dragons[2]
                        return
                    "Вернуться":
                        pass
            
    return
