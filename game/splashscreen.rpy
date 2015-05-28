# coding=utf-8
label splashscreen:
    python:
        if not persistent.disclaimer_accepted:                      # Проверяем был ли принят дисклеймер. Если нет, то:
            disclaimer_status = renpy.call_screen("sc_disclaimer")  # Показываем экран с дисклеймером.
            if disclaimer_status:                                   # И если дисклеймер приняли, то
                persistent.disclaimer_accepted = True               # Сохраняем этот факт на будущее
    
    image white = Solid("#fff")
    scene white
    with Pause(0.4)
    
    show expression 'img/logo.png'  at truecenter with zoomin
    show text "{font=fonts/PFMonumentaPro-Regular.ttf}{size=+15}{color=#000}И{vspace=20} КОМПАНИЯ{/color}{/size}{vspace=60}{/font}" at center with zoomin
    with Pause(3)
    hide text with dissolve
    hide expression 'img/logo.png' with dissolve
    
    show text "{font=fonts/PFMonumentaPro-Regular.ttf}{size=+15}{color=#000}ДОСТАВЛЯЮТ...{/color}{/size}{/font}" at truecenter with dissolve
    with Pause(3)

    hide text with dissolve

    return
    