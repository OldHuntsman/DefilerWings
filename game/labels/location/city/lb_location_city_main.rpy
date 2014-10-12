label lb_location_city_main:
        
    $ place = "city_gates"
    show place
    
    if game.dragon.energy() == 0:
        'Даже драконам надо иногда спать. Особенно драконам!'
        return      
        
    menu:
        'Тайный визит':
            $ pass
        'Ворваться в город':
            $ pass
        'Осадить город':
            $ pass
        'Отступить':
            $ pass
            
    return