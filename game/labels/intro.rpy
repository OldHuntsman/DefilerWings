# TODO: Нужно чтобы текст одним куском прокручивался снизу вверх на фоне меняющихся картинок. И чтобы текст нормально читался нужно либо обвести буквы, либо сделать подложку.
label lb_intro:
    scene black
    play music "mus/intro.ogg"
    show intro 1 with dissolve
    show text intro_text at bot_to_top
    with Pause(10)
    show intro 2 with dissolve
    with Pause(10)
    show intro 3 with dissolve
    with Pause(10)
    show intro 4 with dissolve
    with Pause(10)
    show intro 5 with dissolve
    with Pause(10)
    show intro 6 with dissolve
    with Pause(10)
    show intro 7 with dissolve
    with Pause(10)
    show intro 8 with dissolve
    with Pause(10)

    stop music
    show intro blank
    hide text
    
    return
