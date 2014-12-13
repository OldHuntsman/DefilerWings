# coding=utf-8
label lb_location_gremlin_main:
    $ place = 'gremlins'
    show place
      
    if game.dragon.energy() == 0:
        'Даже драконам надо иногда спать. Особенно драконам!'
        return
        
    # Стоимость года работы гремлинов-слуг
    $ servant_cost = data.lair_upgrades['gremlin_servant']['cost']
    # Стоимость установки механических ловушек
    $ mechanic_traps_cost = 100
    # Стоимость строительства укреплений
    $ fortification_cost = 100
    nvl clear
        
    menu:
        'Нанять слуг' if 'servant' not in game.lair.upgrades and 'gremlin_servant' not in game.lair.upgrades:
            "Гремлины будут служить в логове, приглядывать за пленницами и охранять их. Всего за [servant_cost] фартингов в год"
            menu:
                "Нанять слуг" if servant_cost <= game.lair.treasury.wealth:
                    $ game.lair.upgrades.add('gremlin_servant', deepcopy(data.lair_upgrades['gremlin_servant']))
                    "Гремлины идут {s}за сокровищами.{/s} заботиться о пленницах, не смыкая глаз."
                "Уйти":
                    pass
        'Ловушки для логова' if (not game.lair.type.provide or 'mechanic_traps' not in game.lair.type.provide) and 'mechanic_traps' not in game.lair.upgrades:
            menu:
                "Стоимость установки ловушек: [mechanic_traps_cost] фартингов"
                "Установить ловушки" if mechanic_traps_cost <= game.lair.treasury.money:
                    $ game.lair.upgrades.add('mechanic_traps', deepcopy(data.lair_upgrades['mechanic_traps']))
                    $ game.lair.treasury.money -= mechanic_traps_cost
                "Уйти":
                    pass
        'Укрепления для логова' if 'gremlin_fortification' not in game.lair.upgrades:
            menu:
                "Стоимость возведения укреплений: [fortification_cost] фартингов"
                "Укрепить логово" if fortification_cost <= game.lair.treasury.money:
                    $ game.lair.upgrades.add('gremlin_fortification', deepcopy(data.lair_upgrades['gremlin_fortification']))
                    $ game.lair.treasury.money -= fortification_cost
                "Уйти":
                    pass
        'Уйти':
            $ pass
        
    return