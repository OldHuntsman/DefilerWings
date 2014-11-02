label lb_location_city_main:
        
    $ place = "city_gates"
    show place
    
    if game.dragon.energy() == 0:
        'Даже драконам надо иногда спать. Особенно драконам!'
        return      
        
    menu:
        'Тайный визит' if game.dragon.mana > 0:
            $ pass
        'Ворваться в город':
            $ pass
        'Отступить':
            return
            
    return