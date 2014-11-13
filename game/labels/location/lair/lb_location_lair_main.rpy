label lb_location_lair_main:
    $ place = game.lair.type_name
    show place as bg
    
    menu:
        'Осмотреть дракона':
            #чтобы вывести сообщение от имени дракона можно использовать "game.dragon"
            game.dragon.third "[game.dragon.description]"
        'Сотворить заклинание'  if game.dragon.energy() > 0 and game.dragon.mana > 0:
            python:
                spells_menu = []
                for spell in data.spell_list.keys():
                    # добавляем в список только актуальные заклинания
                    if spell not in game.dragon.spells and (spell is not 'spellbound_trap' or 'magic_traps' not in game.lair.upgrades):
                        spells_menu.append((data.spell_list_rus[spell], spell))
                spells_menu.append(('Вернуться в логово', 'back'))
                spell_name = renpy.display_menu(spells_menu)
                
            if spell_name == 'back':
                jump lb_location_lair_main
            else:
                python: 
                    game.dragon.add_effect(spell_name)
                    game.dragon.drain_mana()
                    game.dragon.gain_rage()
                if spell_name == 'spellbound_trap':
                    $ game.lair.upgrades.add('magic_traps', deepcopy(data.lair_upgrades['magic_traps']))

        'Чахнуть над златом' if game.lair.treasury.wealth > 0:
            #TODO: заменить на адекватный вариант
            python:
                def get_bg():
                    import random
                    import os
                    rel_path = "img/bg/hoard"
                    abs_path = os.path.join(renpy.config.basedir, "game", rel_path)
                    if game.dragon.color_eng in os.listdir(abs_path):
                        color_filename = random.choice(os.listdir(os.path.join(abs_path, game.dragon.color_eng)))
                        return rel_path + "/" + game.dragon.color_eng + "/" + color_filename
                    else:
                        return "img/bg/hoard/base.png"
                renpy.treasurybg = ui.image(get_bg())
                    
            show image renpy.treasurybg as bg
            $ description = u"%s собрал кучу сокровищ общей стоимостью %s" % (game.dragon.name, treasures.number_conjugation_rus(game.lair.treasury.wealth, u"фартинг"))
            nvl clear
            "[description]"
            menu:
                '[game.lair.treasury.gems_mass_description]' if game.lair.treasury.gem_mass > 0:
                    nvl clear
                    "[game.lair.treasury.gems_list]"
                '[game.lair.treasury.materials_mass_description]' if game.lair.treasury.metal_mass + game.lair.treasury.material_mass > 0:
                    nvl clear
                    "[game.lair.treasury.materials_list]"
                '[game.lair.treasury.coin_mass_description]' if game.lair.treasury.coin_mass > 0:
                    nvl clear
                    $ description = u"В сокровищнице:\n"
                    $ description += u"%s\n" % treasures.number_conjugation_rus(game.lair.treasury.farting, u"фартинг")
                    $ description += u"%s\n" % treasures.number_conjugation_rus(game.lair.treasury.taller, u"талер")
                    $ description += u"%s" %treasures.number_conjugation_rus(game.lair.treasury.dublon, u"дублон")
                    "[description]"
                '[game.lair.treasury.jewelry_mass_description]' if game.lair.treasury.jewelry_mass > 0:
                    menu:
                        'Самая дорогая в сокровищнице':
                            nvl clear
                            "[game.lair.treasury.most_expensive_jewelry]"
                        'Самая дешёвая в сокровищнице':
                            nvl clear
                            "[game.lair.treasury.cheapest_jewelry]"
                        'Случайная':
                            nvl clear
                            "[game.lair.treasury.random_jewelry]"
                        'Вернуться в логово':
                            jump lb_location_lair_main   
                'Вернуться в логово':
                    jump lb_location_lair_main        
            call lb_location_lair_main

        'Проведать пленниц' if game.girls_list.prisoners_count:
            call screen girls_menu
        'Лечь спать':
            nvl clear
            python:
                # Делаем хитрую штуку.
                # Используем переменную game_loaded чтобы определить была ли игра загружена.
                # Но ставим ее перед самым сохранинием, используя renpy.retain_after_load() для того
                # чтобы она попала в сохранение.
                if 'game_loaded' in locals() and game_loaded:
                    del game_loaded
                    game.narrator("game loaded")
                    renpy.restart_interaction()
                else:
                    game_loaded = True
                    renpy.retain_after_load()
                    game.save()
                    game.narrator("game saved")
                    del game_loaded
                    game.sleep()
        'Покинуть логово':
            $ pass
            
    return