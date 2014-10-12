label lb_location_smugler_main:
    $ place = 'smuglers'
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