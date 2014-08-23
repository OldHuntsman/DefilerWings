label lb_location_gremlin_main:
    $ place = 'gremlins'
    show place
      
    menu:
        'Нанять слуг':
            $ game.lair.modifiers.append('gremlin')
            # TODO: платные гремлины
        'Ловушки для логова':
            $ pass
        'Укрепления для логова':
            $ pass
        'Уйти':
            $ pass
        
    return