label lb_choose_dragon:
    #Хардкод на трех драконов.
    python:
        dragons = []
        for i in range(3):
            dragons.append(core.Dragon(parent=game.dragon, gameRef=game,base_character=game.base_character))
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
