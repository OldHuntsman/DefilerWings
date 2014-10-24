label lb_location_smuggler_main:
    $ place = 'smugglers'
    show place
    
    if game.dragon.energy() == 0:
        'Даже драконам надо иногда спать. Особенно драконам!'
        return
        
    menu:
        'Нанять охрану':
            $ pass
        'Финансировать террор':
            $ pass
        'Уйти':
            $ pass
            
    return