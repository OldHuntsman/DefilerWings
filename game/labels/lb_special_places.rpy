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
    $ game.foe = core.Enemy('old_knight', game_ref=game)
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
    $ game.foe = core.Enemy('footman', game_ref=game)
    $ chances = show_chances(game.foe)
    '[chances]'
    nvl clear
    menu:
        'Атаковать замок':
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

# Укреплённый монастырь
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
    $ game.foe = core.Enemy('templars', game_ref=game)
    $ chances = show_chances(game.foe)
    '[chances]'
    nvl clear
    menu:
        'Атаковать монастырь':
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
    $ game.foe = core.Enemy('castle_guard', game_ref=game)
    $ chances = show_chances(game.foe)
    '[chances]'
    nvl clear
    menu:
        'Атаковать крепость':
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
    $ game.foe = core.Enemy('palace_guards', game_ref=game)
    $ chances = show_chances(game.foe)
    '[chances]'
    nvl clear
    menu:
        'Атаковать замок':
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
    $ game.foe = core.Enemy('ogre', game_ref=game)
    $ narrator(show_chances(game.foe))
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
    'Жилище ледяного великана.'
    nvl clear
    jump lb_jotun
    
label lb_jotun:   
    show expression 'img/bg/lair/icecastle.png' as bg
    $ txt = game.interpolate(random.choice(txt_place_jotun[0]))
    '[txt]'
    $ game.foe = core.Enemy('jotun', game_ref=game)
    $ narrator(show_chances(game.foe))
    nvl clear
    menu:
        'Вызвать йотуна на бой':
            $ game.dragon.drain_energy()
            call lb_fight
            jump lb_jotun_rob
        'Запомнить место и уйти' if game.dragon.bloodiness < 5:
            $ game.dragon.add_special_place('jotun', 'jotun_full')
            $ game.dragon.gain_rage()
    return
    
label lb_jotun_rob:
    menu:
        'Обследовать ледяную цитадель':
            $ txt = game.interpolate(random.choice(txt_place_jotun[1]))
            '[txt]'
            $ description = game.girls_list.new_girl('ice')
            nvl clear
            game.girl.third "[description]"
            call lb_gigant_sex     
            jump lb_jotun_empty
                                        
        'Запомнить место и уйти':
            $ game.dragon.add_special_place('jotun', 'jotun_empty')
            return
 
label lb_jotun_empty:
    show expression 'img/bg/lair/icecastle.png' as bg
    $ txt = game.interpolate(random.choice(txt_place_jotun[2]))
    '[txt]'
    menu:
        'Переместить логово':
            $ game.create_lair('ice_citadel')
            $ game.dragon.del_special_place('jotun')
        'Покинуть ледяную цитадель':
            $ game.dragon.add_special_place('jotun', 'jotun_empty')
    return 
    
# Жильё огненного великана
    
label lb_ifrit_found:
    'Жилище огненного великана.'
    nvl clear
    jump lb_ifrit
    
label lb_ifrit:   
    show expression 'img/bg/lair/volcanoforge.png' as bg
    $ txt = game.interpolate(random.choice(txt_place_ifrit[0]))
    '[txt]'
    $ game.foe = core.Enemy('ifrit', game_ref=game)
    $ narrator(show_chances(game.foe))
    nvl clear
    menu:
        'Вызвать ифрита на бой':
            $ game.dragon.drain_energy()
            call lb_fight
            jump lb_ifrit_rob
        'Запомнить место и уйти' if game.dragon.bloodiness < 5:
            $ game.dragon.add_special_place('ifrit', 'ifrit_full')
            $ game.dragon.gain_rage()
    return
    
label lb_ifrit_rob:
    menu:
        'Обследовать вулканическую кузню':
            $ txt = game.interpolate(random.choice(txt_place_ifrit[1]))
            '[txt]'
            $ description = game.girls_list.new_girl('fire')
            nvl clear
            game.girl.third "[description]"
            call lb_gigant_sex     
            jump lb_ifrit_empty
                                        
        'Запомнить место и уйти':
            $ game.dragon.add_special_place('ifrit', 'ifrit_empty')
            return
 
label lb_ifrit_empty:
    show expression 'img/bg/lair/icecastle.png' as bg
    $ txt = game.interpolate(random.choice(txt_place_ifrit[2]))
    '[txt]'
    menu:
        'Переместить логово':
            $ game.create_lair('vulcanic_forge')
            $ game.dragon.del_special_place('ifrit')
        'Покинуть вулканическую кузню':
            $ game.dragon.add_special_place('ifrit', 'ifrit_empty')
    return 

    
# Жильё тритона
    
label lb_triton_found:
    'Дракон поднимается над облаками...'
    show expression 'img/bg/lair/underwater.png' as bg
    'И обнаруживает жилище огненного великана.'
    nvl clear
    jump lb_triton
    
label lb_triton:   
    show expression 'img/bg/lair/underwater.png' as bg
    $ txt = game.interpolate(random.choice(txt_place_triton[0]))
    '[txt]'
    $ game.foe = core.Enemy('triton', game_ref=game)
    $ narrator(show_chances(game.foe))
    nvl clear
    menu:
        'Вызвать титана на бой':
            $ game.dragon.drain_energy()
            call lb_fight
            jump lb_triton_rob
        'Запомнить место и уйти' if game.dragon.bloodiness < 5:
            $ game.dragon.add_special_place('triton', 'triton_full')
            $ game.dragon.gain_rage()
    return
    
label lb_triton_rob:
    menu:
        'Обследовать облачный замок':
            $ txt = game.interpolate(random.choice(txt_place_triton[1]))
            '[txt]'
            $ description = game.girls_list.new_girl('siren')
            nvl clear
            game.girl.third "[description]"
            call lb_gigant_sex     
            jump lb_triton_empty
                                        
        'Запомнить место и уйти':
            $ game.dragon.add_special_place('triton', 'triton_empty')
            return
 
label lb_triton_empty:
    show expression 'img/bg/lair/underwater.png' as bg
    $ txt = game.interpolate(random.choice(txt_place_triton[2]))
    '[txt]'
    menu:
        'Переместить логово':
            $ game.create_lair('underwater_mansion')
            $ game.dragon.del_special_place('triton')
        'Покинуть облачный замок':
            $ game.dragon.add_special_place('triton', 'triton_empty')
    return 
    
# Жильё титана
    
label lb_titan_found:
    'Дракон поднимается над облаками...'
    show expression 'img/bg/special/cloud_castle.png' as bg
    'И обнаруживает жилище огненного великана.'
    nvl clear
    jump lb_titan
    
label lb_titan:   
    show expression 'img/bg/special/cloud_castle.png' as bg
    $ txt = game.interpolate(random.choice(txt_place_titan[0]))
    '[txt]'
    $ game.foe = core.Enemy('titan', game_ref=game)
    $ narrator(show_chances(game.foe))
    nvl clear
    menu:
        'Вызвать титана на бой':
            $ game.dragon.drain_energy()
            call lb_fight
            jump lb_titan_rob
        'Запомнить место и уйти' if game.dragon.bloodiness < 5:
            $ game.dragon.add_special_place('titan', 'titan_full')
            $ game.dragon.gain_rage()
    return
    
label lb_titan_rob:
    menu:
        'Обследовать облачный замок':
            $ txt = game.interpolate(random.choice(txt_place_titan[1]))
            '[txt]'
            $ description = game.girls_list.new_girl('titan')
            nvl clear
            game.girl.third "[description]"
            call lb_gigant_sex     
            jump lb_titan_empty
                                        
        'Запомнить место и уйти':
            $ game.dragon.add_special_place('titan', 'titan_empty')
            return
 
label lb_titan_empty:
    show expression 'img/bg/lair/cloud_castle.png' as bg
    $ txt = game.interpolate(random.choice(txt_place_titan[2]))
    '[txt]'
    menu:
        'Переместить логово':
            $ game.create_lair('cloud_castle')
            $ game.dragon.del_special_place('titan')
        'Покинуть облачный замок':
            $ game.dragon.add_special_place('titan', 'titan_empty')
    return 
    
# Подгорное царство цвергов

label lb_backdor:
    show expression 'img/bg/special/backdor.png' as bg
    'Эта потайная дверь в царство гномов обозначена на найденных в бастионе чертежах как "задний проход". В отличие от главных ворот тут нет своей линии обороны и любой кто знает секрет сможет пробраться внуть. Конечно внутри всё равно придётся столкнуться с армией цвергов, но пробраться тут всё же проще чем через центральные укрепления.'
    nvl clear
    menu:
        'Пора вороватъ и убиватъ!':
            stop music
            play music "mus/moria.ogg"
            show expression 'img/bg/special/moria.png' as bg
            'Нажав на неприметный камушек в правильном месте [game.dragon.name] открыл потайной проход в подгорное царство. Теперь отступать не стоит, если цвергов не добить, то они запечатают задний проход и укрепятся ещё основательнее.'
            $ game.dragon.add_special_place('backdor', 'backdor_sealed')
            jump lb_dwarf_army    
        'Для такого дела нужна подготовка...':
            return
            
    return


label lb_backdor_sealed:
    show expression 'img/bg/special/backdor.png' as bg
    'Когда то тут был тайный проход в подгорное царство, но во время нападения цверги обрушили тоннель завалив его камнями. Ох и любят же коротышки эти взрывы...'
    nvl clear
    return
    
label lb_frontgates:
    'Укреплённые неприступыми бастионами эти внушительные металлические врата надёжно закрывают единственный(?) вход в подгорное царство. Там в глубине таятся невероятные сокровища, равных которым нету ни у кого из наземных королей, но пробраться внутрь под силу только кому то очень-очень могучему.'
    show expression 'img/bg/special/gates_dwarf.png' as bg
    nvl clear
    menu:
        'Проломить ворота' if game.dragon.size > 3:
            'Жалкие укрепления коротышек не смогут устоять перед яростным отродьем Госпожи. [game.dragon.fullname] достаточно огромен и могуч чтобы проломиться сквозь ворота и ворваться в подгорное царство. Однако теперь отступать нельзя - если цвергов не прогнать, они укрепятся заново.'
            $ game.dragon.add_special_place('backdor', 'backdor_sealed')
            $ game.dragon.drain_energy()
            call lb_golem_guard
        'Убраться пока они не зарядили пушки...':
            'Шататься перед главными воротами цвергов без дела будет не лучшей идеей, они ведь могут и пальнуть чем нибудь...'
            $ game.dragon.gain_rage()
        
    return
    
label lb_golem_guard:
    stop music
    play music "mus/moria.ogg"
    show expression 'img/bg/special/moria.png' as bg
    'Даже после того как врата обрушились, пыль и мелкие камушки продолжают сыпаться с потолка. По центральной галерее гулко раздаются шаги стража ворот - выкованного целиком из закалённого адамантия механического гиганта. На свете не много противников равных ему по силе...'
    $ game.foe = core.Enemy('golem', game_ref=game)
    $ narrator(show_chances(game.foe))
    nvl clear
    menu:
        'Сразиться с механическим стражем':
            $ game.dragon.drain_energy()
            call lb_fight
            jump lb_dwarf_army
        'Бежать поджав хвост' if game.dragon.bloodiness < 5:
            'Сегодня коротыкам повезло, но даже если они восстановят ворота, не долго им осталось пребывать в покое...'
            $ game.dragon.gain_rage()
    
    return
    
label lb_dwarf_army:
    'Подобно несущему смерть урагану [game.dragon.fullname] ворвался во внутренние палаты подгорного царства. Однако цверги всё ещё не беззащитны, дорогу дракону заступает в спешке собранный ударный отряд...'
    $ game.foe = core.Enemy('dwarf_guards', game_ref=game)
    $ narrator(show_chances(game.foe))
    menu:
        'Атаковать без жалости':
            call lb_fight
            'Теперь, когда основные силы цвергов разбиты и деморализованы, надо выбрать направление финального удара. Ремесленные кварталы почти беззащиты и там цвергов можно будет перебить во множестве, пока они не успели сбежать. С другой стороны, самые главные ценности должны храниться ниже, в главной сокровищнице. Если не наведаться туда прямо сейчас, хитрые цверги вынесут всё до последней монетки.'
            menu:
                'Вниз - за сокровищами!':
                    call lb_dwarf_treashury
                    
                'Разорить ремесленные цеха':
                    call lb_dwarf_houses
                    
                'Отступить':
                    'Обидно отступать, когда победа была так близка, но загнанные в угол цверги могут быть крайне опасными противниками. Иногда лучше не рисковать!'
                    $ game.dragon.gain_rage()
                    
        'Бежать поджав хвост':
            'Сегодня коротышкам повезло, но даже если они восстановят ворота, не долго им осталось пребывать в покое...'
            $ game.dragon.gain_rage()
    return
    
label lb_dwarf_houses:
    'Хотя большинство цвергов бегают в панике и пытаются спасти себя и свои пожитки, при виде дракона многие хватаются за ломы, кирки и тпоры чтобы дать отпор супостату...'
    $ game.foe = core.Enemy('dwarf_citizen', game_ref=game)
    $ narrator(show_chances(game.foe))
    nvl clear
    menu:
        'Наброситься на цвергов':
            call lb_fight
            call lb_dwarf_ruins
        'Отступить':
            'Обидно отутпать когда победа была так близка, но загнанные в угол цверги могут быть крайне опасными противниками. Иногда лучше не рисковать!'
            $ game.dragon.gain_rage()        
    return
    
label lb_dwarf_treashury:
    'Понимая что их королевство стоит на грани катастрофы, цверги пытаются спасти две самые большие ценности - короля и сокровища. Бойцов у них осталось не много, однако среди них есть один равный по силе целой армии - закованный в доспехи до самых глаз чемпион цвергов выступает вперёд потрясая массивным но острым топором.'
    $ game.foe = core.Enemy('dwarf_champion', game_ref=game)
    $ narrator(show_chances(game.foe))
    nvl clear
    menu:
        'Сразиться с чемпионом':
            call lb_fight
            call lb_dwarf_ruins
        'Бежать поджав хвост':
            'Обидно отутпать когда победа была так близка, но загнанные в угол цверги могут быть крайне опасными противниками. Иногда лучше не рисковать!'
            $ game.dragon.gain_rage()      
    return
    
label lb_dwarf_ruins:
    show expression 'img/bg/special/moria.png' as bg
    'Когда-то тут жили цверги, но теперь это место опустошено и заброшено. Внутри можно устроить просторное и отлично защищённое логово.'
    menu:
        'Переместить сюда логово':
            $ game.create_lair('underground_palaces')
            $ game.dragon.del_special_place('frontgates')
            $ game.dragon.del_special_place('backdor')
        'Покинуть подгорные чертоги':
            $ game.dragon.add_special_place('frontgates', 'frontgates_open')
    return 
