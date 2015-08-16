# coding=utf-8
init python:
    from pythoncode import treasures
    
label lb_location_smuggler_main:
    nvl clear
    python:
        if not renpy.music.is_playing():
            renpy.music.play(get_random_files('mus/ambient'))    
    $ place = 'smugglers'
    show expression 'img/bg/special/smugglers.jpg' as bg
    
    if game.dragon.energy() == 0:
        '[game.dragon.name] need some sleep!'
        return

    # Стоимость года работы охранников
    $ guards_cost = data.lair_upgrades['smuggler_guards']['cost']
    
    menu:
        'Hire mercenaries' if 'smuggler_guards' not in game.lair.upgrades and 'regular_guards' not in game.lair.upgrades:
            "Наёмные головорезы не дадут наглым ворам растащить драконье достояние. Всего за [guards_cost] фартингов в год."
            menu:
                "Заключить контракт" if guards_cost <= game.lair.treasury.wealth:
                    $ game.lair.upgrades.add('smuggler_guards', deepcopy(data.lair_upgrades['smuggler_guards']))
                    "Наемные головорезы будут сторожить логово, пока дракон спит."
                    call lb_location_smuggler_main from _call_lb_location_smuggler_main_2 
                "Отказаться":
                    call lb_location_smuggler_main from _call_lb_location_smuggler_main_3 
        'Sell trinkets' if len(game.lair.treasury.jewelry) > 0:
            nvl clear
            menu:
                'Most valuable':
                    $ item_index = game.lair.treasury.most_expensive_jewelry_index
                'Cheapest' if len(game.lair.treasury.jewelry) > 0:
                    $ item_index = game.lair.treasury.cheapest_jewelry_index
                'Random' if len(game.lair.treasury.jewelry) > 0:
                    $ item_index = random.randint(0, len(game.lair.treasury.jewelry) - 1)
                'Sell all' if len(game.lair.treasury.jewelry) > 0:
                    $ item_index = None
                'Cancel':
                    jump lb_location_smuggler_main 
            python:
                if (item_index is None):
                    description = u"Продать все украшения за %s?" % (
                        treasures.number_conjugation_rus(game.lair.treasury.all_jewelries * 75 // 100, u"фартинг"))
                else:
                    description = u"%s.\nПродать украшение за %s?" % (
                        game.lair.treasury.jewelry[item_index].description().capitalize(),
                        treasures.number_conjugation_rus(game.lair.treasury.jewelry[item_index].cost * 75 // 100, u"фартинг"))
            menu:
                "[description]"
                'Sell':
                    python:
                        if (item_index is None):
                            description = u"Все украшения проданы за %s?" % (
                                treasures.number_conjugation_rus(game.lair.treasury.all_jewelries  * 75 // 100, u"фартинг"))
                            game.lair.treasury.money += game.lair.treasury.all_jewelries  * 75 // 100
                            game.lair.treasury.jewelry = []
                        else:
                            description = u"%s.\nПродано за %s" % (
                                game.lair.treasury.jewelry[item_index].description().capitalize(),
                                treasures.number_conjugation_rus(game.lair.treasury.jewelry[item_index].cost * 75 // 100, u"фартинг"))
                            game.lair.treasury.money += game.lair.treasury.jewelry[item_index].cost * 75 // 100
                            game.lair.treasury.jewelry.pop(item_index)
                    call lb_location_smuggler_main from _call_lb_location_smuggler_main_5 
                'Keep':
                    call lb_location_smuggler_main from _call_lb_location_smuggler_main_6 
        'Finance the terrorists' if game.mobilization.level > 0:
            show expression 'img/scene/thief.jpg' as bg
            $ terror_cost = game.mobilization.level * 100
            'Войска королевства мобилизуются и безнаказанно творить зло становится всё сложнее. Но если обеспечить местных бандитов деньгами на оружие, снаряжение и снабжение они могут стать угрозой которая отвлечёт солдат от патрулирования. [terror_cost] фартингов будет достаточно, чтобы обстановка в тылах накалилась и армейские конвои снабжения начали пропадать в пути.'
            menu:
                'Pay [terror_cost] to terrorists' if terror_cost <= game.lair.treasury.money:
                    $ game.lair.treasury.money -= terror_cost
                    $ game.mobilization.level -= 1
                    'По приказанию дракона, разбойники будут поджигать продовольственные склады, отравлять колодцы и перехватывать армейские обозы. Мобилизационный потенциал королевства снижается.'
                    call lb_location_smuggler_main from _call_lb_location_smuggler_main
                'Do not worth it':
                    call lb_location_smuggler_main from _call_lb_location_smuggler_main_1
        'Information on thief' if game.thief is not None:
            "Тут много знающих людей и слухи ходят разные. Только наливай и языки сами развяжутся, никто не посмотрит что болтает с ящерицей."
            nvl clear
            menu:
                "Beer for all (10 rf.)" if game.lair.treasury.money >= 10:
                    python:
                        game.lair.treasury.money -= 10
                        if game.thief is not None:
                            game.thief.third('[game.thief.name] \n\n' + game.thief.description())
                        else:
                            narrator("Не появился пока вор на твое злато.")
                "Decline" if game.lair.treasury.money < 10:
                    call lb_location_smuggler_main from _call_lb_location_smuggler_main_7 
                "Go away." if game.lair.treasury.money >= 10:
                    call lb_location_smuggler_main from _call_lb_location_smuggler_main_8 
        'Thief info' if game.thief is not None:
            $ price = game.dragon.reputation.level * 50
            $ game.thief.third("За %d фартингов мы с ребятами объясним этому корешу что он не с той ящерицей связался, босс!" % price)
            menu:
                "Pay [price] fr." if game.lair.treasury.money >= price:
                    $ game.lair.treasury.money -= price
                    $ game.thief.retire()
                    call lb_location_smuggler_main from _call_lb_location_smuggler_main_9 
                "Decline" if game.lair.treasury.money < price:
                    call lb_location_smuggler_main from _call_lb_location_smuggler_main_10 
                "Go away." if game.lair.treasury.money >= price:
                    call lb_location_smuggler_main from _call_lb_location_smuggler_main_11 
        'Knight info' if game.knight is not None:
            "Тут много знающих людей и слухи ходят разные. Только наливай и языки сами развяжутся, никто не посмотрит что болтает с ящерицей."
            nvl clear
            menu:
                "Beer for all (10 rf.)" if game.lair.treasury.money >= 10:
                    python:
                        game.lair.treasury.money -= 10
                        if game.knight is not None:
                            game.knight.third('[game.knight.name] \n\n' + game.knight.description())
                        else:
                            narrator("Не появился пока рыцарь желающий убить тебя.")
                    call lb_location_smuggler_main from _call_lb_location_smuggler_main_12 
                "Decline" if game.lair.treasury.money < 10:
                    call lb_location_smuggler_main from _call_lb_location_smuggler_main_13 
                "go away." if game.lair.treasury.money >= 10:
                    call lb_location_smuggler_main from _call_lb_location_smuggler_main_14 
        'Hire robbers' if game.knight is not None:
            $ price = game.knight.enchanted_equip_count * 100
            $ narrator("Ограбить славного рыцаря дело не простое, даже опасное. А если ещё и спутников его надо порешить... Всё стит денег. %d фартингов на бочку и он будет гол как сокол!" % price)
            nvl clear
            menu:
                "Pay [price] fr." if game.lair.treasury.money >= price:
                    $ game.lair.treasury.money -= price
                    $ game.knight.equip_basic()
                    call lb_location_smuggler_main from _call_lb_location_smuggler_main_15 
                "Decline" if game.lair.treasury.money < price:
                    call lb_location_smuggler_main from _call_lb_location_smuggler_main_16 
                "Go away." if game.lair.treasury.money >= price:
                    call lb_location_smuggler_main from _call_lb_location_smuggler_main_17 
        'Go away':
            return
            
    return
    