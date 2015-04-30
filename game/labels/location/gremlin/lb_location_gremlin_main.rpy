# coding=utf-8
label lb_location_gremlin_main:
    $ place = 'gremlins'
    show place as bg
        
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
                "Пообщеать им заплатить" if servant_cost <= game.lair.treasury.wealth:
                    $ game.lair.upgrades.add('gremlin_servant', deepcopy(data.lair_upgrades['gremlin_servant']))
                    "Гремлины идут {s}за сокровищами.{/s} заботиться о пленницах, не смыкая глаз."
                "Отказаться":
                    call lb_location_gremlin_main
        'Ловушки для логова' if (not game.lair.type.provide or 'mechanic_traps' not in game.lair.type.provide) and 'mechanic_traps' not in game.lair.upgrades:
            menu:
                "Стоимость установки ловушек: [mechanic_traps_cost] фартингов"
                "Установить ловушки" if mechanic_traps_cost <= game.lair.treasury.money:
                    $ game.lair.upgrades.add('mechanic_traps', deepcopy(data.lair_upgrades['mechanic_traps']))
                    $ game.lair.treasury.money -= mechanic_traps_cost
                    'Теперь вору не поздоровится. Но после того как вор попадётся, механическую ловушку надо будет переустановить.'
                "Уйти":
                    call lb_location_gremlin_main
        'Укрепления для логова' if 'gremlin_fortification' not in game.lair.upgrades:
            menu:
                "Стоимость возведения укреплений: [fortification_cost] фартингов"
                "Укрепить логово" if fortification_cost <= game.lair.treasury.money:
                    $ game.lair.upgrades.add('gremlin_fortification', deepcopy(data.lair_upgrades['gremlin_fortification']))
                    $ game.lair.treasury.money -= fortification_cost
                    'Гремлины устанавливают в логове дракона решётки и двери с хитрыми замками, укрепляют стены. Вор не пройдёт!'
                "Уйти":
                    call lb_location_gremlin_main
        'Смастерить вещь':
            $ new_item = game.lair.treasury.craft(**data.craft_options['gremlin'])
            if new_item:
                $ game.lair.treasury.receive_treasures([new_item])
                $ test_description = new_item.description()
                "Изготовлено: [test_description]."
                call lb_location_gremlin_main
        'Уйти':
            $ pass
        
    return