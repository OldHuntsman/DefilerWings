label lb_location_mordor_main:
    $ place = 'mordor' 
    show place as bg
    
    if game.dragon.energy() == 0:
        'Даже драконам надо иногда спать. Особенно драконам!'
        return
        
    menu:
        'Армия Тьмы':
            $ pass
        'Аудиенция с владычицей':
            menu:
                "Продолжить род?"
                "Да":
                    call lb_choose_dragon
                "Нет":
                    pass
        'Назад':
            $ pass
        
    return