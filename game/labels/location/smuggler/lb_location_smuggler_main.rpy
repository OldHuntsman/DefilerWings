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
        'Финансировать террор':
            $ pass
        'Уйти':
            $ pass
            
    return