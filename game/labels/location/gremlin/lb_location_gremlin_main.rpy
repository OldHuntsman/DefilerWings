label lb_location_gremlin_main:
    $ place = 'gremlins'
    show place
      
    menu:
        'Нанять слуг' if 'gremlin' not in game.lair.modifiers:
            $ game.lair.modifiers.append('gremlin')
            # TODO: платные гремлины
        'Ловушки для логова' if (not game.lair.type.provide or 'mechanic_traps' not in game.lair.type.provide) and 'mechanic_traps' not in game.lair.upgrades:
            $ game.lair.upgrades.add('mechanic_traps', deepcopy(data.lair_upgrades['mechanic_traps']))
            # TODO: платные ловушки
        'Укрепления для логова':
            $ pass
        'Уйти':
            $ pass
        
    return