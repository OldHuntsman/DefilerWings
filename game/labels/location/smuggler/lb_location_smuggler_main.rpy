# coding=utf-8
label lb_location_smuggler_main:
    nvl clear
    python:
        if not renpy.music.is_playing():
            renpy.music.play(get_random_files('mus/ambient'))    
    $ place = 'smugglers'
    show expression 'img/bg/special/smugglers.png' as bg
    
    if game.dragon.energy() == 0:
        'Даже драконам надо иногда спать. Особенно драконам!'
        return
        
    # Стоимость года работы охранников
    $ guards_cost = data.lair_upgrades['smuggler_guards']['cost']
        
    menu:
        'Нанять охрану' if 'smuggler_guards' not in game.lair.upgrades and 'regular_guards' not in game.lair.upgrades:
            "Наёмные головорезы не дадут наглым ворам растащить драконье достояние. Всего за [guards_cost] фартингов в год."
            menu:
                "Заключить контракт" if guards_cost <= game.lair.treasury.wealth:
                    $ game.lair.upgrades.add('smuggler_guards', deepcopy(data.lair_upgrades['smuggler_guards']))
                    "Наемные головорезы будут сторожить логово, пока дракон спит."
                "Уйти":
                    pass
        'Продать драгоценности':
            nvl clear
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
        'Финансировать террор' if game.mobilization.level > 0:
            show expression 'img/scene/thief.png' as bg
            $ terror_cost = game.mobilization.level * 100
            'Войска королевства мобилизуются и безнаказанно творить зло становится всё сложнее. Но если обеспечить местных бандитов деньгами на оружие, снаряжение и снабжение они могут стать угрозой которая отвлечёт солдат от патрулирования. [terror_cost] фартингов будет достаточно, чтобы обстановка в тылах накалилась и армейские конвои снабжения начали пропадать в пути.'
            menu:
                'Отдать [terror_cost] фартингов разбойникам' if terror_cost <= game.lair.treasury.money:
                    $ game.lair.treasury.money -= terror_cost
                    $ game.mobilization.level -= 1
                    'По приказанию дракона, разбойники будут поджигать продовольственные склады, отравлять колодцы и перехватывать армейские обозы. Мобилизационный потенциал королевства снижается.'
                    call lb_location_smuggler_main from _call_lb_location_smuggler_main
                'Это того не стоит':
                    call lb_location_smuggler_main from _call_lb_location_smuggler_main_1
        'Уйти':
            $ pass
            
    return