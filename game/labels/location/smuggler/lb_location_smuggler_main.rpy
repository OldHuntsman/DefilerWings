# coding=utf-8
label lb_location_smuggler_main:
    $ place = 'smugglers'
    show place
    
    if game.dragon.energy() == 0:
        'Даже драконам надо иногда спать. Особенно драконам!'
        return
        
    # Стоимость года работы охранников
    $ guards_cost = data.lair_upgrades['smuggler_guards']['cost']
        
    menu:
        'Нанять охрану' if 'smuggler_guards' not in game.lair.upgrades and 'regular_guards' not in game.lair.upgrades:
            "Охранники не дадут наглым ворам растащить драконье достояние. Всего за [guards_cost] фартингов в год"
            menu:
                "Нанять охрану" if guards_cost <= game.lair.treasury.wealth:
                    $ game.lair.upgrades.add('smuggler_guards', deepcopy(data.lair_upgrades['smuggler_guards']))
                    "Ох рано встаёт охрана..."
                "Уйти":
                    pass
        'Продать драгоценности':
            menu:
                'Самую дорогую' if len(game.lair.treasury.jewelry) > 0:
                    $ item_index = game.lair.treasury.most_expensive_jewelry_index
                'Самую дешёвую' if len(game.lair.treasury.jewelry) > 0:
                    $ item_index = game.lair.treasury.cheapest_jewelry_index
                'Случайную' if len(game.lair.treasury.jewelry) > 0:
                    $ item_index = random.randint(0, len(game.lair.treasury.jewelry))
                'Отмена':
                    return
            python:
                from pythoncode import treasures
                description = u"%s.\nПродать украшение за %s?" % (
                    game.lair.treasury.jewelry[item_index].description().capitalize(),
                    treasures.number_conjugation_rus(game.lair.treasury.jewelry[item_index].cost * 75 // 100, u"фартинг"))
            menu:
                "[description]"
                'Продать':
                    python:
                        description = u"%s.\nПродано за %s" % (
                            game.lair.treasury.jewelry[item_index].description().capitalize(),
                            treasures.number_conjugation_rus(game.lair.treasury.jewelry[item_index].cost * 75 // 100, u"фартинг"))
                        game.lair.treasury.money += game.lair.treasury.jewelry[item_index].cost * 75 // 100
                        game.lair.treasury.jewelry.pop(item_index)
                'Оставить':
                    pass
        'Финансировать террор':
            $ pass
        'Уйти':
            $ pass
            
    return