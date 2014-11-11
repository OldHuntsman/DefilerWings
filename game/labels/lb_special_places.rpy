label lb_special_places:
    nvl clear
    python:
        special_places_menu = []
        for special_place in game.dragon.special_places.keys():
            # добавляем в список исследованные достопримечательности
            special_stage = game.dragon.special_places[special_place]
            special_places_menu.append((data.special_places[special_stage][0], special_stage))
        special_places_menu.append(('Вернуться', 'back'))
        special_stage = renpy.display_menu(special_places_menu)
        
        if special_stage == 'back':
            pass
        else:
            renpy.call(data.special_places[special_stage][1])
    return
    
label lb_manor_found:
    show expression 'img/bg/special/castle1.png' as bg
    $ txt = random.choice(txt_place_manor[0])
    '[txt]'
    jump lb_manor
    
label lb_manor:
    show expression 'img/bg/special/castle1.png' as bg
    nvl clear
    $ txt = random.choice(txt_place_manor[1])
    '[txt]'    
    $ game.foe = core.Enemy('dog', gameRef=game, base_character=NVLCharacter)
    $ chance_win = battle.victory_chance(game.dragon, game.foe)
    $ chance_wound = battle.victory_chance(game.foe, game.dragon)
    "Шанс победы дракона: [chance_win] %%, шанс ранения дракона: [chance_wound] %%"
    nvl clear
    menu:
        'Вызвать рыцаря на бой':
            $ game.dragon.drain_energy()
            call lb_fight
            '[game.dragon.name] победил.'
            call lb_manor_rob
        'Запомнить место и уйти' if game.dragon.bloodiness < 5:
            $ game.dragon.add_special_place('manor', 'manor_full')
            $ game.dragon.gain_rage()
            
    return
    
label lb_manor_rob:
    python:
        count = random.randint(4,12)
        alignment = 'knight'
        min_cost = 10
        max_cost = 500
        obtained = "Это предмет из разграбленного рыцарского поместья."
        trs = treasures.gen_treas(count, data.loot['palace'], alignment, min_cost, max_cost, obtained)
        trs_list = game.lair.treasury.treasures_description(trs)
        trs_descrptn = '\n'.join(trs_list)
    menu:
        'Разграбить поместье':
            show expression 'img/bg/lair/ruins_inside.png' as bg
            $ txt = game.interpolate(random.choice(txt_place_manor[2]))
            '[txt]'    
            '[trs_descrptn]'
            nvl clear
            show expression 'img/bg/special/bedroom.png' as bg
            $ txt = random.choice(txt_place_manor[3]) % game.format_data
            '[txt]'    
            nvl clear
            $ description = game.girls_list.new_girl('princess')
            nvl clear
            game.girl.third "[description]"
            call lb_lair_sex     
            call lb_manor_empty
                                        
        'Запомнить место и уйти':
            $ game.dragon.add_special_place('manor', 'manor_empty')
            
    return
            
label lb_manor_empty:
    show expression 'img/bg/lair/ruins_inside.png' as bg
    $ txt = random.choice(txt_place_manor[4])
    '[txt]'   
    nvl clear
    menu:
        'Обустроить тут новое логово':
            $ game.create_lair('castle')
        
        'Покинуть заброшенную усадьбу':
            $ game.dragon.add_special_place('manor', 'manor_empty')
            
    return
            
label lb_wooden_fort_found:
    jump lb_manor_found            
            
label lb_abbey_found:
    jump lb_manor_found  

label lb_castle_found:
    jump lb_manor_found  
    
label lb_palace_found:
    jump lb_manor_found  
