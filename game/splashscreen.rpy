label splashscreen:
    python:
        if not persistent.disclaimer_accepted:                      # Проверяем был ли принят дисклеймер. Если нет, то:
            disclaimer_status = renpy.call_screen("sc_disclaimer")  # Показываем экран с дисклеймером.
            if disclaimer_status:                                   # И если дисклеймер приняли, то
                persistent.disclaimer_accepted = True               # Сохраняем этот факт на будущее
    
    scene black
    with Pause(1)

    show text "Old Huntsman present..." with dissolve   # интро
    with Pause(1)
    
    show text "Defiler Wings" with dissolve
    with Pause(2)

    hide text with dissolve
    with Pause(1)

    return