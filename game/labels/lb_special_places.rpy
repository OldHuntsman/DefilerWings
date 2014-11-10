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
    'Рыцарский манор. Бинго!'
    jump lb_manor
    
label lb_manor:   
    nvl clear
    'Старый рыцарь живущий тут наверняка не сдастся без боя.'
    nvl clear
    $ game.foe = core.Enemy('dog', gameRef=game, base_character=NVLCharacter)
    $ chance_win = battle.victory_chance(game.dragon, game.foe)
    $ chance_wound = battle.victory_chance(game.foe, game.dragon)
    "Шанс победы дракона: [chance_win] %%, шанс ранения дракона: [chance_wound] %%"
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
            'Не обращая внимания на бегущую в ужасе челядь, [game.dragon.name] обшаривает поместье в поисках ценностей:'
            '[trs_descrptn]'
            nvl clear
            'В просторной и светлой комнате на самом последнем этаже дрожит спрятавшись под кроватью дочь убитого рыцаря. Но [game.dragon.name] способен учуять запах невинной плоти за много миль, от него не скрыться в маленькой комнате.'
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
    'Укрепления не спасли эту ныне уже безлюдную усадьбу от разграбления, однако крепкие стены могут послужить хорошей защитой для драконьих сокровищ. Не слишком крупный ящер мог бы устроить в винном погребе уютное логово, надо только протиснуться в узкие двери.'
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
