label lb_location_gremlin_main:
    $ place = 'gremlins'
    show place
      
    if game.dragon.energy() == 0:
        'Даже драконам надо иногда спать. Особенно драконам!'
        return
        
    # Стоимость года работы гремлинов-слуг
    $ servant_cost = 100
        
    menu:
        'Нанять слуг' if 'servant' not in game.lair.upgrades:
            nvl clear
            "Гремлины будут служить в логове, приглядывать за пленницами и охранять их. Всего за [servant_cost] фартингов в год"
            if 'gremlin_servant' not in game.lair.upgrades:
                if servant_cost > game.lair.treasury.money:
                    "В сокровищнице не найдется денег на запросы этих алчных созданий. А без полной предоплаты они работать отказываются. Вот же гремлины."
                    return
                menu:
                    "Контракт на год" if servant_cost <= game.lair.treasury.money:
                        $ game.lair.upgrades.add('gremlin_servant', deepcopy(data.lair_upgrades['gremlin_servant']))
                        $ game.lair.upgrades['gremlin_servant']['recruitment_time'] += 1
                        $ game.lair.treasury.money -= servant_cost
                    "Контракт на 3 года" if 3 * servant_cost <= game.lair.treasury.money:
                        $ game.lair.upgrades.add('gremlin_servant', deepcopy(data.lair_upgrades['gremlin_servant']))
                        $ game.lair.upgrades['gremlin_servant']['recruitment_time'] += 3
                        $ game.lair.treasury.money -= 3 * servant_cost
                    "Контракт на 5 лет" if 5 * servant_cost <= game.lair.treasury.money:
                        $ game.lair.upgrades.add('gremlin_servant', deepcopy(data.lair_upgrades['gremlin_servant']))
                        $ game.lair.upgrades['gremlin_servant']['recruitment_time'] += 5
                        $ game.lair.treasury.money -= 5 * servant_cost
                    "Уйти":
                        pass
            else:
                $ remain_time = game.lair.upgrades['gremlin_servant']['recruitment_time']
                if servant_cost > game.lair.treasury.money:
                    $ remain_time_text = u"Прошлый контракт еще не истек. Последняя цифра в гремлинских расчетах - %s. Денег на продление не хватает." % remain_time
                else:
                    $ remain_time_text = u"Прошлый контракт еще не истек - на нем гремлинскими каракулями выведена цифра %s. Хотите его продлить?" % remain_time
                menu:
                    "[remain_time_text]"
                    "Продлить на год" if servant_cost <= game.lair.treasury.money:
                        $ game.lair.upgrades['gremlin_servant']['recruitment_time'] += 1
                        $ game.lair.treasury.money -= servant_cost
                    "Продлить на 3 года" if 3 * servant_cost <= game.lair.treasury.money:
                        $ game.lair.upgrades['gremlin_servant']['recruitment_time'] += 3
                        $ game.lair.treasury.money -= 3 * servant_cost
                    "Продлить на 5 лет" if 3 * servant_cost <= game.lair.treasury.money:
                        $ game.lair.upgrades['gremlin_servant']['recruitment_time'] += 5
                        $ game.lair.treasury.money -= 5 * servant_cost
                    "Уйти":
                        pass
            # TODO: платные гремлины
        'Ловушки для логова' if (not game.lair.type.provide or 'mechanic_traps' not in game.lair.type.provide) and 'mechanic_traps' not in game.lair.upgrades:
            $ game.lair.upgrades.add('mechanic_traps', deepcopy(data.lair_upgrades['mechanic_traps']))
            # TODO: платные ловушки
        'Укрепления для логова':
            $ pass
        'Уйти':
            $ pass
        
    return