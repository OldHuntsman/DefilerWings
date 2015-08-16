# coding=utf-8
screen sc_disclaimer:
    frame:
        text "WARNING!!!":           # Отдельно так как нужно спозиционировать по центру.
            color "#f00"            # Текст красного цвета
            align(0.5, 0.15)      # Положение на экране
            size 40
        text("   This game contents multiple scenes of the extreme violence and strong sexual contents, and thus cannot be recomended to anyone. PG99.\n"
            "   By cliking “proceed” you confirm that you are adult and chose to play on your own risk. This game is NOT meant to be commertialy distributed. All grafical, audio and text elements used in the game are either freely aviable on internet or created by autors of the game, and used for the sake of parody.\n"
            "   Programm code of the game, created by our team, licensesd under BSD license (see LICENCE.txt for details)\n"
            "   Translation is parial, mostly inteface and menu choices. Intro, story, descriptions and dialogs are still in russian. Sorry, guys. Currently I have no resouces for the complete translation. But eventualy... maybe... if the game will be recepted..."):
            align(0.5, 0.4)
            color "#f00"            # Текст красного цвета
    
        textbutton "Proceed":       
            align(0.4, 0.8)        # Положение на экране
            action Return(True)     # Возвращаем True, что мы приняли дисклеймер
            
        textbutton "Stop":
            action Quit(False)      # Сразу выходим
            align(0.6, 0.8)        # Положение на экране
    
        background "#000"