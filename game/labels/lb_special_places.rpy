# coding=utf-8
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
    
label lb_enchanted_forest:
    show expression 'img/bg/special/enchanted_forest.png' as bg
    'Дракон входит под сень колдовских древ.'
    menu:
        'Рыскать кругом':
            # TODO добавить энкаунтеры зачарованного леса
            $ pass
        'Напасть на Древо Жизни':
            'Дерево жизни разрушено.'
            $ game.dragon.add_event('ravage_sacred_grove')
            call lb_dead_grove
            # TODO сделать нормальный энкаунтер
    return

label lb_dead_grove:
    'Тут можно поселиться.'
    nvl clear
    menu:
        'Обустроить тут новое логово':
            $ game.create_lair('forest_heart')
            $ game.dragon.del_special_place('enchanted_forest')
        
        'Уйти прочь':
            $ game.dragon.add_special_place('enchanted_forest', 'dead_grove')
    
    return

# Рыцарская усадьба

label lb_manor_found:
    show expression 'img/bg/special/castle1.png' as bg
    $ txt = game.interpolate(random.choice(txt_place_manor[0]))
    '[txt]'
    jump lb_manor
    
label lb_manor:
    show expression 'img/bg/special/castle1.png' as bg
    nvl clear
    $ txt = game.interpolate(random.choice(txt_place_manor[1]))
    '[txt]'    
    $ game.foe = core.Enemy('old_knight', gameRef=game, base_character=NVLCharacter)
    $ chances = show_chances(game.foe)
    '[chances]'
    nvl clear
    menu:
        'Вызвать рыцаря на бой':
            $ game.dragon.drain_energy()
            call lb_fight
            $ txt = game.interpolate(random.choice(txt_place_manor[5]))
            '[txt]' 
            nvl clear
            call lb_manor_rob
        'Запомнить место и уйти' if game.dragon.bloodiness < 5:
            $ game.dragon.add_special_place('manor', 'manor_full')
            $ game.dragon.gain_rage()
            
    return
    
label lb_manor_rob:
    python:
        count = random.randint(4, 12)
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
            $ txt = game.interpolate(random.choice(txt_place_manor[3]))
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
    $ txt = game.interpolate(random.choice(txt_place_manor[4]))
    '[txt]'   
    nvl clear
    menu:
        'Обустроить тут новое логово':
            $ game.create_lair('castle')
            $ game.dragon.del_special_place('manor')
        
        'Покинуть заброшенную усадьбу':
            $ game.dragon.add_special_place('manor', 'manor_empty')
            
    return


# Деревянный замок

label lb_wooden_fort_found:
    show expression 'img/bg/special/castle2.png' as bg
    $ txt = game.interpolate(random.choice(txt_place_wooden_fort[0]))
    '[txt]'
    jump lb_wooden_fort
    
label lb_wooden_fort:
    show expression 'img/bg/special/castle2.png' as bg
    nvl clear
    $ txt = game.interpolate(random.choice(txt_place_wooden_fort[1]))
    '[txt]'    
    $ game.foe = core.Enemy('old_knight', gameRef=game, base_character=NVLCharacter)
    $ chances = show_chances(game.foe)
    '[chances]'
    nvl clear
    menu:
        'Вызвать рыцаря на бой':
            $ game.dragon.drain_energy()
            call lb_fight
            $ txt = game.interpolate(random.choice(txt_place_wooden_fort[5]))
            '[txt]' 
            nvl clear
            call lb_wooden_fort_rob
        'Запомнить место и уйти' if game.dragon.bloodiness < 5:
            $ game.dragon.add_special_place('wooden_fort', 'wooden_fort_full')
            $ game.dragon.gain_rage()
            
    return
    
label lb_wooden_fort_rob:
    python:
        count = random.randint(4, 12)
        alignment = 'knight'
        min_cost = 10
        max_cost = 500
        obtained = "Это предмет найден в деревянном рыцарском замке."
        trs = treasures.gen_treas(count, data.loot['palace'], alignment, min_cost, max_cost, obtained)
        trs_list = game.lair.treasury.treasures_description(trs)
        trs_descrptn = '\n'.join(trs_list)
    menu:
        'Разграбить центральную башню':
            show expression 'img/bg/lair/ruins_inside.png' as bg
            $ txt = game.interpolate(random.choice(txt_place_wooden_fort[2]))
            '[txt]'    
            '[trs_descrptn]'
            nvl clear
            show expression 'img/bg/special/bedroom.png' as bg
            $ txt = game.interpolate(random.choice(txt_place_wooden_fort[3]))
            '[txt]'    
            nvl clear
            $ description = game.girls_list.new_girl('princess')
            nvl clear
            game.girl.third "[description]"
            call lb_lair_sex     
            call lb_manor_empty
                                        
        'Запомнить место и уйти':
            $ game.dragon.add_special_place('wooden_fort', 'wooden_fort_empty')
            
    return
            
label lb_wooden_fort_empty:
    show expression 'img/bg/lair/ruins_inside.png' as bg
    $ txt = game.interpolate(random.choice(txt_place_wooden_fort[4]))
    '[txt]'   
    nvl clear
    menu:
        'Обустроить тут новое логово':
            $ game.create_lair('castle')
            $ game.dragon.del_special_place('wooden_fort')
        
        'Покинуть деревянный форт':
            $ game.dragon.add_special_place('wooden_fort', 'wooden_fort_empty')
            
    return


#Укреполённый морнастырь

label lb_abbey_found:
    show expression 'img/bg/special/castle3.png' as bg
    $ txt = game.interpolate(random.choice(txt_place_abbey[0]))
    '[txt]'
    jump lb_abbey
    
label lb_abbey:
    show expression 'img/bg/special/castle3.png' as bg
    nvl clear
    $ txt = game.interpolate(random.choice(txt_place_abbey[1]))
    '[txt]'    
    $ game.foe = core.Enemy('old_knight', gameRef=game, base_character=NVLCharacter)
    $ chances = show_chances(game.foe)
    '[chances]'
    nvl clear
    menu:
        'Вызвать рыцаря на бой':
            $ game.dragon.drain_energy()
            call lb_fight
            $ txt = game.interpolate(random.choice(txt_place_abbey[5]))
            '[txt]' 
            nvl clear
            call lb_abbey_rob
        'Запомнить место и уйти' if game.dragon.bloodiness < 5:
            $ game.dragon.add_special_place('abbey', 'abbey_full')
            $ game.dragon.gain_rage()
            
    return
    
label lb_abbey_rob:
    python:
        count = random.randint(4, 12)
        alignment = 'cleric'
        min_cost = 10
        max_cost = 500
        obtained = "Это предмет из разграбленного монастыря."
        trs = treasures.gen_treas(count, data.loot['palace'], alignment, min_cost, max_cost, obtained)
        trs_list = game.lair.treasury.treasures_description(trs)
        trs_descrptn = '\n'.join(trs_list)
    menu:
        'Разграбить монастырь':
            show expression 'img/bg/lair/ruins_inside.png' as bg
            $ txt = game.interpolate(random.choice(txt_place_abbey[2]))
            '[txt]'    
            '[trs_descrptn]'
            nvl clear
            show expression 'img/bg/special/bedroom.png' as bg
            $ txt = game.interpolate(random.choice(txt_place_abbey[3]))
            '[txt]'    
            nvl clear
            $ description = game.girls_list.new_girl('princess')
            nvl clear
            game.girl.third "[description]"
            call lb_lair_sex     
            call lb_manor_empty
                                        
        'Запомнить место и уйти':
            $ game.dragon.add_special_place('abbey', 'abbey_empty')
            
    return
            
label lb_abbey_empty:
    show expression 'img/bg/lair/ruins_inside.png' as bg
    $ txt = game.interpolate(random.choice(txt_place_abbey[4]))
    '[txt]'   
    nvl clear
    menu:
        'Обустроить тут новое логово':
            $ game.create_lair('castle')
            $ game.dragon.del_special_place('abbey')
        
        'Покинуть заброшенную усадьбу':
            $ game.dragon.add_special_place('abbey', 'abbey_empty')
            
    return


# Каменная крепость

label lb_castle_found:
    show expression 'img/bg/special/castle4.png' as bg
    $ txt = game.interpolate(random.choice(txt_place_castle[0]))
    '[txt]'
    jump lb_castle
    
label lb_castle:
    show expression 'img/bg/special/castle4.png' as bg
    nvl clear
    $ txt = game.interpolate(random.choice(txt_place_castle[1]))
    '[txt]'    
    $ game.foe = core.Enemy('old_knight', gameRef=game, base_character=NVLCharacter)
    $ chances = show_chances(game.foe)
    '[chances]'
    nvl clear
    menu:
        'Вызвать рыцаря на бой':
            $ game.dragon.drain_energy()
            call lb_fight
            $ txt = game.interpolate(random.choice(txt_place_castle[5]))
            '[txt]' 
            nvl clear
            call lb_castle_rob
        'Запомнить место и уйти' if game.dragon.bloodiness < 5:
            $ game.dragon.add_special_place('castle', 'castle_full')
            $ game.dragon.gain_rage()
            
    return
    
label lb_castle_rob:
    python:
        count = random.randint(4, 12)
        alignment = 'knight'
        min_cost = 10
        max_cost = 500
        obtained = "Это предмет из разграбленного рыцарского поместья."
        trs = treasures.gen_treas(count, data.loot['palace'], alignment, min_cost, max_cost, obtained)
        trs_list = game.lair.treasury.treasures_description(trs)
        trs_descrptn = '\n'.join(trs_list)
    menu:
        'Разграбить цитадель':
            show expression 'img/bg/lair/ruins_inside.png' as bg
            $ txt = game.interpolate(random.choice(txt_place_castle[2]))
            '[txt]'    
            '[trs_descrptn]'
            nvl clear
            show expression 'img/bg/special/bedroom.png' as bg
            $ txt = game.interpolate(random.choice(txt_place_castle[3]))
            '[txt]'    
            nvl clear
            $ description = game.girls_list.new_girl('princess')
            nvl clear
            game.girl.third "[description]"
            call lb_lair_sex     
            call lb_castle_empty
                                        
        'Запомнить место и уйти':
            $ game.dragon.add_special_place('castle', 'castle_empty')
            
    return
            
label lb_castle_empty:
    show expression 'img/bg/lair/ruins_inside.png' as bg
    $ txt = game.interpolate(random.choice(txt_place_castle[4]))
    '[txt]'   
    nvl clear
    menu:
        'Обустроить тут новое логово':
            $ game.create_lair('castle')
            $ game.dragon.del_special_place('castle')
        
        'Покинуть заброшенную усадьбу':
            $ game.dragon.add_special_place('castle', 'castle_empty')
            
    return

# Королевский замок
    
label lb_palace_found:
    show expression 'img/bg/special/castle5.png' as bg
    $ txt = game.interpolate(random.choice(txt_place_palace[0]))
    '[txt]'
    jump lb_palace
    
label lb_palace:
    show expression 'img/bg/special/castle5.png' as bg
    nvl clear
    $ txt = game.interpolate(random.choice(txt_place_palace[1]))
    '[txt]'    
    $ game.foe = core.Enemy('old_knight', gameRef=game, base_character=NVLCharacter)
    $ chances = show_chances(game.foe)
    '[chances]'
    nvl clear
    menu:
        'Вызвать рыцаря на бой':
            $ game.dragon.drain_energy()
            call lb_fight
            $ txt = game.interpolate(random.choice(txt_place_palace[5]))
            '[txt]' 
            nvl clear
            call lb_palace_rob
        'Запомнить место и уйти' if game.dragon.bloodiness < 5:
            $ game.dragon.add_special_place('palace', 'palace_full')
            $ game.dragon.gain_rage()
            
    return
    
label lb_palace_rob:
    python:
        count = random.randint(4, 12)
        alignment = 'knight'
        min_cost = 10
        max_cost = 500
        obtained = "Это предмет из разграбленного рыцарского поместья."
        trs = treasures.gen_treas(count, data.loot['palace'], alignment, min_cost, max_cost, obtained)
        trs_list = game.lair.treasury.treasures_description(trs)
        trs_descrptn = '\n'.join(trs_list)
    menu:
        'Разграбить королевский дворец':
            show expression 'img/bg/lair/ruins_inside.png' as bg
            $ txt = game.interpolate(random.choice(txt_place_palace[2]))
            '[txt]'    
            '[trs_descrptn]'
            nvl clear
            show expression 'img/bg/special/bedroom.png' as bg
            $ txt = game.interpolate(random.choice(txt_place_palace[3]))
            '[txt]'    
            nvl clear
            $ description = game.girls_list.new_girl('princess')
            nvl clear
            game.girl.third "[description]"
            call lb_lair_sex     
            call lb_palace_empty
                                        
        'Запомнить место и уйти':
            $ game.dragon.add_special_place('palace', 'palace_empty')
            
    return
            
label lb_palace_empty:
    show expression 'img/bg/lair/ruins_inside.png' as bg
    $ txt = game.interpolate(random.choice(txt_place_palace[4]))
    '[txt]'   
    nvl clear
    menu:
        'Обустроить тут новое логово':
            $ game.create_lair('castle')
            $ game.dragon.del_special_place('palace')
        
        'Покинуть заброшенную усадьбу':
            $ game.dragon.add_special_place('palace', 'palace_empty')
            
    return

# Жильё людоеда
    
label lb_enc_ogre:
    'Дракон некоторое время бродит по лесу...'
    show expression 'img/bg/special/cave_enter.png' as bg
    'И натыкается на вход в лесную пещеру, достаточно просторную, чтобы устроить внутри логово. Судя по запаху, логово себе там уже успел устроить великан-людоед.'
    jump lb_enc_fight_ogre
    
label lb_enc_fight_ogre:   
    $ game.foe = core.Enemy('ogre', gameRef=game, base_character=NVLCharacter)
    $ narrator(show_chances())
    nvl clear
    menu:
        'Вызвать великана на бой':
            $ game.dragon.drain_energy()
            call lb_fight
            '[game.dragon.name] победил.'
            jump lb_enc_explore_ogre_den
        'Запомнить место и уйти' if game.dragon.bloodiness < 5:
            $ game.dragon.add_special_place('ogre', 'enc_ogre')
            $ game.dragon.gain_rage()
    return
    
label lb_enc_explore_ogre_den:
    menu:
        'Обследовать пещеру':
            'В пещере прячется испуганная великанша. То ли дочь, то ли жена того огра, труп которого валяется снаружи.'
            $ description = game.girls_list.new_girl('ogre')
            nvl clear
            game.girl.third "[description]"
            call lb_gigant_sex     
            jump lb_enc_create_ogre_lair
                                        
        'Запомнить место и уйти':
            $ game.dragon.add_special_place('ogre', 'create_ogre_lair')
            return
 
label lb_enc_create_ogre_lair:
    menu:
        'Пещера, в которой жил огр, теперь пуста. Но тут можно устроить своё логово, не слишком раскошное, однако всё же получше, чем открытый овраг в буреломной чащобе.'
        'Переместить логово':
            $ game.create_lair('ogre_den')
            $ game.dragon.del_special_place('ogre')
            return
        'Покинуть пещеру':
            $ game.dragon.add_special_place('ogre', 'create_ogre_lair')
            return
            

# Жльё морозного великана    

label lb_jotun_found:
    'Дракон некоторое время обследует горные склоны...'
    show expression 'img/bg/special/cave_enter.png' as bg
    $ txt = game.interpolate(random.choice(txt_place_jotun[0]))
    '[txt]'
    jump lb_jotun
    
label lb_jotun:   
    $ game.foe = core.Enemy('jotun', gameRef=game, base_character=NVLCharacter)
    $ narrator(show_chances())
    nvl clear
    menu:
        'Вызвать йотуна на бой':
            $ game.dragon.drain_energy()
            call lb_fight
            $ txt = game.interpolate(random.choice(txt_place_jotun[1]))
            '[txt]'
            jump lb_jotun_rob
        'Запомнить место и уйти' if game.dragon.bloodiness < 5:
            $ game.dragon.add_special_place('jotun', 'enc_jotun_full')
            $ game.dragon.gain_rage()
    return
    
label lb_jotun_rob:
    menu:
        'Обследовать ледяную цитадель':
            'В пещере прячется испуганная великанша. То ли дочь, то ли жена того огра, труп которого валяется снаружи.'
            $ description = game.girls_list.new_girl('jotun')
            nvl clear
            game.girl.third "[description]"
            call lb_gigant_sex     
            jump lb_jotun_empty
                                        
        'Запомнить место и уйти':
            $ game.dragon.add_special_place('jotun', 'enc_jotun_empty')
            return
 
label lb_jotun_empty:
    menu:
        'Пещера, в которой жил огр, теперь пуста. Но тут можно устроить своё логово, не слишком раскошное, однако всё же получше, чем открытый овраг в буреломной чащобе.'
        'Переместить логово':
            $ game.create_lair('ice_citadel')
            $ game.dragon.del_special_place('jotun')
            return
        'Покинуть ледяную цитадель':
            $ game.dragon.add_special_place('jotun', 'enc_jotun_empty')
            return
    
# Жильё огненного великана
    
label lb_ifrit_found:
    'Ифрит. Плейсхолдер.'
    
    return
    