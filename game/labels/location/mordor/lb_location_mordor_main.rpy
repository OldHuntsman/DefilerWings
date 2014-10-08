label lb_location_mordor_main:
    $ place = 'mordor' 
    show place as bg
    
    if dragon.energy() == 0:
        'Даже драконам надо иногда спать. Особенно драконам!'
        return
        
    menu:
        'Армия Тьмы':
            $ pass
        'Аудиенция с владычицей':
            $ pass
        'Назад':
            $ pass
        
    return