#Окончание игры

label lb_game_over:
    if freeplay:
        $ renpy.unlink_save("1-3")
    else:
        $ renpy.unlink_save("1-1")
    show expression 'img/scene/game_over.png' as bg
    show text "GAME OVER"
    pause (500.0)
    $ renpy.full_restart()
    
label lb_you_win:
    hide all
    show black
    show text "нам нужен экран с титрами..."
    pause (500.0)    
    $ renpy.unlink_save("1-1")
    $ game.win()
    $ renpy.full_restart()