label lb_intro:
    scene black
    play music "mus/intro.ogg"
    show intro 1 with dissolve
    image bg blur = "img/bg/blur.png"
    show bg blur
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
    hide text
    
    return
