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
    $ data.achieve_target("conquer", "win")
    $ data.achieve_win(game.dragon)
    call lb_achievement_acquired
    hide all
    play music 'mus/outro.ogg'
    show black
    show expression 'img/scene/ge1.jpg' at right
    show text "      НАД ПРОЕКТОМ РАБОТАЛИ: \n\n\n Anonimous №13 \n\n Denkun \n\n ImG \n\n Graylor \n\n OldHuntsman \n\n HikkeKun \n\n Titlish \n\n Vladimir Sudalov \n\n Xela00 \n\n\n и другие..." at topleft
    pause (30.0)
    hide expression 'img/scene/ge1.jpg'
    show expression 'img/scene/ge2.jpg' at left
    show text '\n\n      Эта игра всего лишь попытка \n освоить новый движок. \n У нас огромные планы на будущие игры, \n но воплотить их в жизнь \n будет очень не просто. \n Если хочешь помочь, \n нам всегда пригодятся \n толковые программисты и дизайнеры. \n И разумеется мы не отказываемся \n от добровольных пожертвований ;) \n Новости ищи на \n\n  http://oldhuntergames.blogspot.com/. ' at topright    
    pause
    $ persistent.allow_freeplay = True
    $ renpy.unlink_save("1-1")
    $ game.win()
    $ renpy.full_restart()
