# coding=utf-8

init python:
    from pythoncode.utils import weighted_random
    from pythoncode.characters import Enemy
    
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
    show expression 'img/bg/special/enchanted_forest.jpg' as bg
    'Даже зная путь в зачарованный лес, пройти через завесу магии альвов не просто. Нужно применить могучие чары.'
    menu:
        'Open the elvenpath (magic)' if game.dragon.mana > 0:
            $ game.dragon.drain_mana()
            '[game.dragon.fullname] применяет чёрную магию чтобы разорвать завесу иллюзий, морока и сна которыми скрыты владения альвов. Незамеченный и смертоносный [game.dragon.kind] входит под сень чародейсикх древ.'
            nvl clear
            call lb_enchanted_forest_enter from _call_lb_enchanted_forest_enter
        'Go away':
            return
        
    return
            

label lb_enchanted_forest_enter:        
    stop music fadeout 1.0
    play music "mus/forest.ogg"    
    menu:
        'Prowl around':
            $ choices = [
                ("lb_enchanted_forest_elfgirl", 10),
                ("lb_enchanted_forest_druid", 10),
                ]
            $ enc = weighted_random(choices)
            $ renpy.call(enc)
    
        'Defile the Three of Life':
            call lb_enchanted_forest_grove from _call_lb_enchanted_forest_grove
            
    return

label lb_enchanted_forest_elfgirl:
    '[game.dragon.name] слышит непередаваемый аромат сотканный из ноток невинности, красоты и колдовских чар. Это лесная ведьма, альва из народа богини Дану. Нет плоти более сладкой и желанной, но взять её будет непросто ведь на её стороне колдовство.'
    $ game.foe = Enemy('elf_witch', game_ref=game)
    $ narrator(show_chances(game.foe))
    nvl clear
    menu:
        'Fight the Fey':
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_25
            'Несмотря на жестокое сопротивление, чародейка не получила особых повреждений. Она теперь безащитна, но цела... пока что.'
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
            $ description = game.girls_list.new_girl('elf')
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex from _call_lb_nature_sex_14      
        
        'Flee' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()        
    return

label lb_enchanted_forest_druid:
    '[game.dragon.name] не долго остаётся незамеченным. На пути дракона, словно материализовавшись из листьев возникает вооруженный корявым посохом друид. Он не выглядит особенно внушительным, однако это впечатление обманичво. На стороне жрец Дану сама сила леса.'
    $ game.foe = Enemy('druid', game_ref=game)
    $ narrator(show_chances(game.foe))
    menu:
        'Fight the Druid':
            $ game.dragon.drain_energy()
            $ game.foe = Enemy('druid', game_ref=game)
            call lb_fight from _call_lb_fight_26
            $ game.dragon.reputation.points += 3
            'Друид повержен. [game.dragon.reputation.gain_description]'
            '[game.dragon.name] находит на трупе кое-что ценное:'
            python:
                count = random.randint(1, 2)
                alignment = 'elf'
                min_cost = 25
                max_cost = 500
                obtained = "Это предмет принадлежал друиду - стражу зачарованого леса."
                trs = treasures.gen_treas(count, data.loot['knight'], alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
            '[trs_descrptn]'
        'Flee' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()   
    return

label lb_enchanted_forest_grove:
    show expression 'img/bg/special/enchanted_forest.jpg' as bg
    nvl clear
    $ txt = game.interpolate(random.choice(txt_place_enfr[1]))
    '[txt]'    
    $ game.foe = Enemy('treant', game_ref=game)
    $ chances = show_chances(game.foe)
    '[chances]'
    nvl clear
    menu:
        'Fight the Treant':
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_27
            $ txt = game.interpolate(random.choice(txt_place_enfr[5]))
            '[txt]' 
            $ game.dragon.reputation.points += 25
            '[game.dragon.reputation.gain_description]' 
            nvl clear
            call lb_enchanted_forest_grove_rob from _call_lb_enchanted_forest_grove_rob
        'Flee' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            
    return
    
label lb_enchanted_forest_grove_rob:
    $ game.dragon.add_event('ravage_sacred_grove')
    python:
        count = random.randint(5, 10)
        alignment = 'elf'
        min_cost = 500
        max_cost = 3000
        obtained = "Это предмет из королевской сокровищницы альвов зачарованного леса."
        trs = treasures.gen_treas(count, data.loot['palace'], alignment, min_cost, max_cost, obtained)
        trs_list = game.lair.treasury.treasures_description(trs)
        trs_descrptn = '\n'.join(trs_list)
    menu:
        'Defile the Sacred Grove':
            show expression 'img/bg/lair/elfruin.jpg' as bg
            $ txt = game.interpolate(random.choice(txt_place_enfr[2]))
            '[txt]'    
            '[trs_descrptn]'
            $ game.lair.treasury.receive_treasures(trs)
            nvl clear
            show expression 'img/bg/special/bedroom.jpg' as bg
            $ txt = game.interpolate(random.choice(txt_place_enfr[3]))
            '[txt]'    
            nvl clear
            $ description = game.girls_list.new_girl('elf')
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex from _call_lb_nature_sex_15    
            $ game.dragon.add_special_place('enchanted_forest', 'dead_grove')
                                        
        'Remember the place and go away':
            $ game.dragon.add_special_place('enchanted_forest', 'dead_grove')
            
    return
    
label lb_dead_grove:
    show expression 'img/bg/lair/ruins_inside.jpg' as bg
    $ txt = game.interpolate(random.choice(txt_place_enfr[4]))
    '[txt]'   
    nvl clear
    menu:
        'Make a lair here':
            $ game.create_lair('forest_heart')
            $ game.dragon.del_special_place('enchanted_forest')
        
        'Go away':
            $ game.dragon.add_special_place('enchanted_forest', 'dead_grove')
    
    return

# Рыцарская усадьба
label lb_manor_found:
    show expression 'img/bg/special/castle1.jpg' as bg
    $ txt = game.interpolate(random.choice(txt_place_manor[0]))
    '[txt]'
    jump lb_manor
    
label lb_manor:
    show expression 'img/bg/special/castle1.jpg' as bg
    nvl clear
    $ txt = game.interpolate(random.choice(txt_place_manor[1]))
    '[txt]'    
    $ game.foe = Enemy('old_knight', game_ref=game)
    $ chances = show_chances(game.foe)
    '[chances]'
    nvl clear
    menu:
        'Challenge the old knight':
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_28
            $ txt = game.interpolate(random.choice(txt_place_manor[5]))
            '[txt]' 
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
            nvl clear
            call lb_manor_rob from _call_lb_manor_rob
        'Remember and go' if game.dragon.bloodiness < 5:
            $ game.dragon.add_special_place('manor', 'manor_full')
            $ game.dragon.gain_rage()
            
    return
    
label lb_manor_rob:
    python:
        count = random.randint(1, 5)
        alignment = 'knight'
        min_cost = 10
        max_cost = 250
        obtained = "Это предмет из разграбленного рыцарского поместья."
        trs = treasures.gen_treas(count, data.loot['palace'], alignment, min_cost, max_cost, obtained)
        trs_list = game.lair.treasury.treasures_description(trs)
        trs_descrptn = '\n'.join(trs_list)
    menu:
        'Rob the manor':
            show expression 'img/bg/lair/ruins_inside.jpg' as bg
            $ txt = game.interpolate(random.choice(txt_place_manor[2]))
            '[txt]'    
            '[trs_descrptn]'
            $ game.lair.treasury.receive_treasures(trs)
            nvl clear
            show expression 'img/bg/special/bedroom.jpg' as bg
            $ txt = game.interpolate(random.choice(txt_place_manor[3]))
            '[txt]'    
            nvl clear
            $ description = game.girls_list.new_girl('princess')
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex from _call_lb_nature_sex_16     
            $ game.dragon.add_special_place('manor', 'manor_empty')
                                        
        'Remember and go':
            $ game.dragon.add_special_place('manor', 'manor_empty')
            
    return
            
label lb_manor_empty:
    show expression 'img/bg/lair/ruins_inside.jpg' as bg
    $ txt = game.interpolate(random.choice(txt_place_manor[4]))
    '[txt]'   
    nvl clear
    menu:
        'Make lair here':
            $ game.create_lair('castle')
            $ game.dragon.del_special_place('manor')
        
        'Go away':
            $ game.dragon.add_special_place('manor', 'manor_empty')
            
    return

# Деревянный замок
label lb_wooden_fort_found:
    show expression 'img/bg/special/castle2.jpg' as bg
    $ txt = game.interpolate(random.choice(txt_place_wooden_fort[0]))
    '[txt]'
    jump lb_wooden_fort
    
label lb_wooden_fort:
    show expression 'img/bg/special/castle2.jpg' as bg
    nvl clear
    $ txt = game.interpolate(random.choice(txt_place_wooden_fort[1]))
    '[txt]'    
    $ game.foe = Enemy('footman', game_ref=game)
    $ chances = show_chances(game.foe)
    '[chances]'
    nvl clear
    menu:
        'Siege the motte and bailey':
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_29
            $ txt = game.interpolate(random.choice(txt_place_wooden_fort[5]))
            '[txt]' 
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]'            
            nvl clear
            call lb_wooden_fort_rob from _call_lb_wooden_fort_rob
        'Remember and go away' if game.dragon.bloodiness < 5:
            $ game.dragon.add_special_place('wooden_fort', 'wooden_fort_full')
            $ game.dragon.gain_rage()
            
    return
    
label lb_wooden_fort_rob:
    python:
        count = random.randint(2, 6)
        alignment = 'knight'
        min_cost = 25
        max_cost = 500
        obtained = "Это предмет найден в деревянном рыцарском замке."
        trs = treasures.gen_treas(count, data.loot['palace'], alignment, min_cost, max_cost, obtained)
        trs_list = game.lair.treasury.treasures_description(trs)
        trs_descrptn = '\n'.join(trs_list)
    menu:
        'Raise the donjon':
            show expression 'img/bg/lair/ruins_inside.jpg' as bg
            $ txt = game.interpolate(random.choice(txt_place_wooden_fort[2]))
            '[txt]'    
            '[trs_descrptn]'
            $ game.lair.treasury.receive_treasures(trs)
            nvl clear
            show expression 'img/bg/special/bedroom.jpg' as bg
            $ txt = game.interpolate(random.choice(txt_place_wooden_fort[3]))
            '[txt]'    
            nvl clear
            $ description = game.girls_list.new_girl('princess')
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex from _call_lb_nature_sex_17 
            $ game.dragon.add_special_place('wooden_fort', 'wooden_fort_empty')
                                        
        'Remember and go away':
            $ game.dragon.add_special_place('wooden_fort', 'wooden_fort_empty')
            
    return
            
label lb_wooden_fort_empty:
    show expression 'img/bg/lair/ruins_inside.jpg' as bg
    $ txt = game.interpolate(random.choice(txt_place_wooden_fort[4]))
    '[txt]'   
    nvl clear
    menu:
        'Make a lair here':
            $ game.create_lair('castle')
            $ game.dragon.del_special_place('wooden_fort')
        
        'Go away':
            $ game.dragon.add_special_place('wooden_fort', 'wooden_fort_empty')
            
    return

# Укреплённый монастырь
label lb_abbey_found:
    show expression 'img/bg/special/castle3.jpg' as bg
    $ txt = game.interpolate(random.choice(txt_place_abbey[0]))
    '[txt]'
    jump lb_abbey
    
label lb_abbey:
    show expression 'img/bg/special/castle3.jpg' as bg
    nvl clear
    $ txt = game.interpolate(random.choice(txt_place_abbey[1]))
    '[txt]'    
    $ game.foe = Enemy('templars', game_ref=game)
    $ chances = show_chances(game.foe)
    '[chances]'
    nvl clear
    menu:
        'Storm the abbey':
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_30
            $ txt = game.interpolate(random.choice(txt_place_abbey[5]))
            '[txt]' 
            $ game.dragon.reputation.points += 10
            '[game.dragon.reputation.gain_description]'  
            nvl clear
            call lb_abbey_rob from _call_lb_abbey_rob
        'Remember and go away' if game.dragon.bloodiness < 5:
            $ game.dragon.add_special_place('abbey', 'abbey_full')
            $ game.dragon.gain_rage()
            
    return
    
label lb_abbey_rob:
    python:
        count = random.randint(4, 10)
        alignment = 'cleric'
        min_cost = 10
        max_cost = 500
        obtained = "Это предмет из разграбленного монастыря."
        trs = treasures.gen_treas(count, data.loot['palace'], alignment, min_cost, max_cost, obtained)
        trs_list = game.lair.treasury.treasures_description(trs)
        trs_descrptn = '\n'.join(trs_list)
    menu:
        'Rob the abbey':
            show expression 'img/bg/lair/ruins_inside.jpg' as bg
            $ txt = game.interpolate(random.choice(txt_place_abbey[2]))
            '[txt]'    
            '[trs_descrptn]'
            $ game.lair.treasury.receive_treasures(trs)
            nvl clear
            show expression 'img/bg/special/bedroom.jpg' as bg
            $ txt = game.interpolate(random.choice(txt_place_abbey[3]))
            '[txt]'    
            nvl clear
            $ description = game.girls_list.new_girl('princess')
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex from _call_lb_nature_sex_18 
            $ game.dragon.add_special_place('abbey', 'abbey_empty')
                                        
        'Remember and go away':
            $ game.dragon.add_special_place('abbey', 'abbey_empty')
            
    return
            
label lb_abbey_empty:
    show expression 'img/bg/lair/ruins_inside.jpg' as bg
    $ txt = game.interpolate(random.choice(txt_place_abbey[4]))
    '[txt]'   
    nvl clear
    menu:
        'Make a lair here':
            $ game.create_lair('castle')
            $ game.dragon.del_special_place('abbey')
        
        'Go away':
            $ game.dragon.add_special_place('abbey', 'abbey_empty')
            
    return

# Каменная крепость
label lb_castle_found:
    show expression 'img/bg/special/castle4.jpg' as bg
    $ txt = game.interpolate(random.choice(txt_place_castle[0]))
    '[txt]'
    jump lb_castle
    
label lb_castle:
    show expression 'img/bg/special/castle4.jpg' as bg
    nvl clear
    $ txt = game.interpolate(random.choice(txt_place_castle[1]))
    '[txt]'    
    $ game.foe = Enemy('castle_guard', game_ref=game)
    $ chances = show_chances(game.foe)
    '[chances]'
    nvl clear
    menu:
        'Siege the castle':
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_31
            $ txt = game.interpolate(random.choice(txt_place_castle[5]))
            '[txt]' 
            $ game.dragon.reputation.points += 10
            '[game.dragon.reputation.gain_description]'                
            nvl clear
            call lb_castle_rob from _call_lb_castle_rob
        'Remember and go away' if game.dragon.bloodiness < 5:
            $ game.dragon.add_special_place('castle', 'castle_full')
            $ game.dragon.gain_rage()
            
    return
    
label lb_castle_rob:
    python:
        count = random.randint(3, 8)
        alignment = 'knight'
        min_cost = 100
        max_cost = 1000
        obtained = "Это предмет из разграбленной крепости."
        trs = treasures.gen_treas(count, data.loot['palace'], alignment, min_cost, max_cost, obtained)
        trs_list = game.lair.treasury.treasures_description(trs)
        trs_descrptn = '\n'.join(trs_list)
    menu:
        'Rob the citadel':
            show expression 'img/bg/lair/ruins_inside.jpg' as bg
            $ txt = game.interpolate(random.choice(txt_place_castle[2]))
            '[txt]'    
            '[trs_descrptn]'
            $ game.lair.treasury.receive_treasures(trs)
            nvl clear
            show expression 'img/bg/special/bedroom.jpg' as bg
            $ txt = game.interpolate(random.choice(txt_place_castle[3]))
            '[txt]'    
            nvl clear
            $ description = game.girls_list.new_girl('princess')
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex from _call_lb_nature_sex_19     
            $ game.dragon.add_special_place('castle', 'castle_empty')
                                        
        'Remember and go away':
            $ game.dragon.add_special_place('castle', 'castle_empty')
            
    return
            
label lb_castle_empty:
    show expression 'img/bg/lair/ruins_inside.jpg' as bg
    $ txt = game.interpolate(random.choice(txt_place_castle[4]))
    '[txt]'   
    nvl clear
    menu:
        'Make a lair here':
            $ game.create_lair('castle')
            $ game.dragon.del_special_place('castle')
        
        'Go away':
            $ game.dragon.add_special_place('castle', 'castle_empty')
            
    return

# Королевский замок
    
label lb_palace_found:
    show expression 'img/bg/special/castle5.jpg' as bg
    $ txt = game.interpolate(random.choice(txt_place_palace[0]))
    '[txt]'
    jump lb_palace
    
label lb_palace:
    show expression 'img/bg/special/castle5.jpg' as bg
    nvl clear
    $ txt = game.interpolate(random.choice(txt_place_palace[1]))
    '[txt]'    
    $ game.foe = Enemy('palace_guards', game_ref=game)
    $ chances = show_chances(game.foe)
    '[chances]'
    nvl clear
    menu:
        'Attack the royal palace':
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_32
            $ txt = game.interpolate(random.choice(txt_place_palace[5]))
            '[txt]' 
            $ game.dragon.reputation.points += 25
            '[game.dragon.reputation.gain_description]'                 
            nvl clear
            call lb_palace_rob from _call_lb_palace_rob
        'Remember and go away' if game.dragon.bloodiness < 5:
            $ game.dragon.add_special_place('palace', 'palace_full')
            $ game.dragon.gain_rage()
            
    return
    
label lb_palace_rob:
    python:
        count = random.randint(5, 10)
        alignment = 'knight'
        min_cost = 250
        max_cost = 2500
        obtained = "Это предмет из королевской сокровищницы."
        trs = treasures.gen_treas(count, data.loot['palace'], alignment, min_cost, max_cost, obtained)
        trs_list = game.lair.treasury.treasures_description(trs)
        trs_descrptn = '\n'.join(trs_list)
    menu:
        'Rob the palace':
            show expression 'img/bg/lair/ruins_inside.jpg' as bg
            $ txt = game.interpolate(random.choice(txt_place_palace[2]))
            '[txt]'    
            '[trs_descrptn]'
            $ game.lair.treasury.receive_treasures(trs)
            nvl clear
            show expression 'img/bg/special/bedroom.jpg' as bg
            $ txt = game.interpolate(random.choice(txt_place_palace[3]))
            '[txt]'    
            nvl clear
            $ description = game.girls_list.new_girl('princess')
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex from _call_lb_nature_sex_20     
            $ game.dragon.add_special_place('palace', 'palace_empty')
                                        
        'Remember and go away':
            $ game.dragon.add_special_place('palace', 'palace_empty')
            
    return
            
label lb_palace_empty:
    show expression 'img/bg/lair/ruins_inside.jpg' as bg
    $ txt = game.interpolate(random.choice(txt_place_palace[4]))
    '[txt]'   
    nvl clear
    menu:
        'Make a lair here':
            $ game.create_lair('castle')
            $ game.dragon.del_special_place('palace')
        
        'Remember and go away':
            $ game.dragon.add_special_place('palace', 'palace_empty')
            
    return

# Жильё людоеда
    
label lb_enc_ogre:
    'Дракон некоторое время бродит по лесу...'
    show expression 'img/bg/special/cave_enter.jpg' as bg
    'И натыкается на вход в лесную пещеру, достаточно просторную, чтобы устроить внутри логово. Судя по запаху, логово себе там уже успел устроить великан-людоед.'
    jump lb_enc_fight_ogre
    
label lb_enc_fight_ogre:   
    $ game.foe = Enemy('ogre', game_ref=game)
    $ narrator(show_chances(game.foe))
    nvl clear
    menu:
        'Challenge the ogre':
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_33
            '[game.dragon.name] победил.'
            jump lb_enc_explore_ogre_den
        'Remember and go away' if game.dragon.bloodiness < 5:
            $ game.dragon.add_special_place('ogre', 'enc_ogre')
            $ game.dragon.gain_rage()
    return
    
label lb_enc_explore_ogre_den:
    menu:
        'Rob the den':
            'В пещере прячется испуганная великанша. То ли дочь, то ли жена того огра, труп которого валяется снаружи.'
            $ description = game.girls_list.new_girl('ogre')
            nvl clear
            game.girl.third "[description]"
            call lb_gigant_sex from _call_lb_gigant_sex     
            $ game.dragon.add_special_place('ogre', 'create_ogre_lair')
                                        
        'Remember and go away':
            $ game.dragon.add_special_place('ogre', 'create_ogre_lair')
            return
 
label lb_enc_create_ogre_lair:
    menu:
        'Пещера, в которой жил огр, теперь пуста. Но тут можно устроить своё логово, не слишком раскошное, однако всё же получше, чем открытый овраг в буреломной чащобе.'
        'Make a lair here':
            $ game.create_lair('ogre_den')
            $ game.dragon.del_special_place('ogre')
            return
        'Remember and go away':
            $ game.dragon.add_special_place('ogre', 'create_ogre_lair')
            return
            

# Жльё морозного великана    

label lb_jotun_found:
    'Высоко в горах, где всё покрыто льдом и снегом стоит гигантский ледяной дворец. Интересно...'
    nvl clear
    jump lb_jotun
    
label lb_jotun:   
    show expression 'img/bg/lair/icecastle.jpg' as bg
    $ txt = game.interpolate(random.choice(txt_place_jotun[0]))
    '[txt]'
    $ game.foe = Enemy('jotun', game_ref=game)
    $ narrator(show_chances(game.foe))
    nvl clear
    menu:
        'Challenge the Jotun':
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_34
            jump lb_jotun_rob
        'Remember and go away' if game.dragon.bloodiness < 5:
            $ game.dragon.add_special_place('jotun', 'jotun_full')
            $ game.dragon.gain_rage()
    return
    
label lb_jotun_rob:
    menu:
        'Rob the Icy Citadel':
            $ txt = game.interpolate(random.choice(txt_place_jotun[1]))
            '[txt]'
            $ description = game.girls_list.new_girl('ice')
            nvl clear
            game.girl.third "[description]"
            call lb_gigant_sex from _call_lb_gigant_sex_1     
            $ game.dragon.add_special_place('jotun', 'jotun_empty')
                                        
        'Remember and go away':
            $ game.dragon.add_special_place('jotun', 'jotun_empty')
            return
 
label lb_jotun_empty:
    show expression 'img/bg/lair/icecastle.jpg' as bg
    $ txt = game.interpolate(random.choice(txt_place_jotun[2]))
    '[txt]'
    menu:
        'Make a lair here':
            $ game.create_lair('ice_citadel')
            $ game.dragon.del_special_place('jotun')
        'Remember and go away':
            $ game.dragon.add_special_place('jotun', 'jotun_empty')
    return 
    
# Жильё огненного великана
    
label lb_ifrit_found:
    'Над жерлом вулкана возвышается башня из чёрного обсидиана. Интересно кто там живет...'
    nvl clear
    jump lb_ifrit
    
label lb_ifrit:   
    show expression 'img/bg/lair/volcanoforge.jpg' as bg
    $ txt = game.interpolate(random.choice(txt_place_ifrit[0]))
    '[txt]'
    $ game.foe = Enemy('ifrit', game_ref=game)
    $ narrator(show_chances(game.foe))
    nvl clear
    menu:
        'Challenge the Ifrit':
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_35
            jump lb_ifrit_rob
        'Remember and go away' if game.dragon.bloodiness < 5:
            $ game.dragon.add_special_place('ifrit', 'ifrit_full')
            $ game.dragon.gain_rage()
    return
    
label lb_ifrit_rob:
    menu:
        'Rob the volcanic forge':
            $ txt = game.interpolate(random.choice(txt_place_ifrit[1]))
            '[txt]'
            $ description = game.girls_list.new_girl('fire')
            nvl clear
            game.girl.third "[description]"
            call lb_gigant_sex from _call_lb_gigant_sex_2     
            $ game.dragon.add_special_place('ifrit', 'ifrit_empty')
                                        
        'Remember and go away':
            $ game.dragon.add_special_place('ifrit', 'ifrit_empty')
            return
 
label lb_ifrit_empty:
    show expression 'img/bg/lair/volcanoforge.jpg' as bg
    $ txt = game.interpolate(random.choice(txt_place_ifrit[2]))
    '[txt]'
    menu:
        'Make a lair here':
            $ game.create_lair('vulcanic_forge')
            $ game.dragon.del_special_place('ifrit')
        'Remember and go away':
            $ game.dragon.add_special_place('ifrit', 'ifrit_empty')
    return 

    
# Жильё тритона
    
label lb_triton_found:
    'Дракон проплывает вдоль прибрежной зоны...'
    show expression 'img/bg/lair/underwater.jpg' as bg
    'И обнаруживает подводную арку, украшенную кораллами и ракушками. Проём достаточно велик чтобы внутрь мог заплыть даже кашалот.'
    nvl clear
    jump lb_triton
    
label lb_triton:   
    show expression 'img/bg/lair/underwater.jpg' as bg
    $ txt = game.interpolate(random.choice(txt_place_triton[0]))
    '[txt]'
    $ game.foe = Enemy('triton', game_ref=game)
    $ narrator(show_chances(game.foe))
    nvl clear
    menu:
        'Challenge the Triton':
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_36
            jump lb_triton_rob
        'Remember and go away' if game.dragon.bloodiness < 5:
            $ game.dragon.add_special_place('triton', 'triton_full')
            $ game.dragon.gain_rage()
    return
    
label lb_triton_rob:
    menu:
        'Rob the underwater mansion':
            $ txt = game.interpolate(random.choice(txt_place_triton[1]))
            '[txt]'
            $ description = game.girls_list.new_girl('siren')
            nvl clear
            game.girl.third "[description]"
            call lb_gigant_sex from _call_lb_gigant_sex_3    
            $ game.dragon.add_special_place('triton', 'triton_empty')
                                        
        'Remember and go away':
            $ game.dragon.add_special_place('triton', 'triton_empty')
            return
 
label lb_triton_empty:
    show expression 'img/bg/lair/underwater.jpg' as bg
    $ txt = game.interpolate(random.choice(txt_place_triton[2]))
    '[txt]'
    menu:
        'Make a lair here':
            $ game.create_lair('underwater_mansion')
            $ game.dragon.del_special_place('triton')
        'Go away':
            $ game.dragon.add_special_place('triton', 'triton_empty')
    return 
    
# Жильё титана
    
label lb_titan_found:
    'Дракон поднимается над облаками...'
    show expression 'img/bg/special/cloud_castle.jpg' as bg
    'И обнаруживает летающий остров с прекрасным замком. Интересно кто его построил...'
    nvl clear
    jump lb_titan
    
label lb_titan:   
    show expression 'img/bg/special/cloud_castle.jpg' as bg
    $ txt = game.interpolate(random.choice(txt_place_titan[0]))
    '[txt]'
    $ game.foe = Enemy('titan', game_ref=game)
    $ narrator(show_chances(game.foe))
    nvl clear
    menu:
        'Challenge the Titan':
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_37
            $ game.dragon.reputation.points += 10
            '[game.dragon.reputation.gain_description]'   
            jump lb_titan_rob
        'Remember and go away' if game.dragon.bloodiness < 5:
            $ game.dragon.add_special_place('titan', 'titan_full')
            $ game.dragon.gain_rage()
    return
    
label lb_titan_rob:
    menu:
        'Rob the Cloudcastle':
            $ txt = game.interpolate(random.choice(txt_place_titan[1]))
            '[txt]'
            $ description = game.girls_list.new_girl('titan')
            nvl clear
            game.girl.third "[description]"
            call lb_gigant_sex from _call_lb_gigant_sex_4  
            $ game.dragon.add_special_place('titan', 'titan_empty')
                                        
        'Remember and go away':
            $ game.dragon.add_special_place('titan', 'titan_empty')
            return
 
label lb_titan_empty:
    show expression 'img/bg/lair/cloud_castle.jpg' as bg
    $ txt = game.interpolate(random.choice(txt_place_titan[2]))
    '[txt]'
    menu:
        'Make a lair here':
            $ game.create_lair('cloud_castle')
            $ game.dragon.del_special_place('titan')
        'Go away':
            $ game.dragon.add_special_place('titan', 'titan_empty')
    return 
    
# Подгорное царство цвергов

label lb_backdor:
    show expression 'img/bg/special/backdor.jpg' as bg
    'Эта потайная дверь в царство гномов обозначена на найденных в бастионе чертежах как "задний проход". В отличие от главных ворот тут нет своей линии обороны и любой кто знает секрет сможет пробраться внуть. Конечно внутри всё равно придётся столкнуться с армией цвергов, но пробраться тут всё же проще чем через центральные укрепления.'
    nvl clear
    menu:
        'Go thru the backdor!':
            stop music fadeout 1.0
            play music "mus/moria.ogg"
            $ renpy.music.queue(get_random_files('mus/ambient'))           
            show expression 'img/bg/special/moria.jpg' as bg
            'Нажав на неприметный камушек в правильном месте [game.dragon.name] открыл потайной проход в подгорное царство. Теперь отступать не стоит, если цвергов не добить, то они запечатают задний проход и укрепятся ещё основательнее.'
            $ game.dragon.add_special_place('backdor', 'backdor_sealed')
            jump lb_dwarf_army    
        'Some preparations needed...':
            return
            
    return


label lb_backdor_sealed:
    show expression 'img/bg/special/backdor.jpg' as bg
    'Когда то тут был тайный проход в подгорное царство, но во время нападения цверги обрушили тоннель завалив его камнями. Ох и любят же коротышки эти взрывы...'
    nvl clear
    return
    
label lb_frontgates:
    'Укреплённые неприступыми бастионами эти внушительные металлические врата надёжно закрывают единственный(?) вход в подгорное царство. Там в глубине таятся невероятные сокровища, равных которым нету ни у кого из наземных королей, но пробраться внутрь под силу только кому то очень-очень могучему.'
    show expression 'img/bg/special/gates_dwarf.jpg' as bg
    nvl clear
    menu:
        'Crush the Mountain Gates' if game.dragon.size > 3:
            'Жалкие укрепления коротышек не смогут устоять перед яростным отродьем Госпожи. [game.dragon.fullname] достаточно огромен и могуч чтобы проломиться сквозь ворота и ворваться в подгорное царство. Однако теперь отступать нельзя - если цвергов не прогнать, они укрепятся заново.'
            $ game.dragon.add_special_place('backdor', 'backdor_sealed')
            $ game.dragon.drain_energy()
            call lb_golem_guard from _call_lb_golem_guard
        'Flee':
            'Шататься перед главными воротами цвергов без дела будет не лучшей идеей, они ведь могут и пальнуть чем нибудь...'
            $ game.dragon.gain_rage()
        
    return
    
label lb_golem_guard:
    stop music fadeout 1.0
    play music "mus/moria.ogg"
    $ renpy.music.queue(get_random_files('mus/ambient')) 
    show expression 'img/bg/special/moria.jpg' as bg
    'Даже после того как врата обрушились, пыль и мелкие камушки продолжают сыпаться с потолка. По центральной галерее гулко раздаются шаги стража ворот - выкованного целиком из закалённого адамантия механического гиганта. На свете не много противников равных ему по силе...'
    $ game.foe = Enemy('golem', game_ref=game)
    $ narrator(show_chances(game.foe))
    nvl clear
    menu:
        'Fight the Iron Golem':
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_38
            jump lb_dwarf_army
        'Flee' if game.dragon.bloodiness < 5:
            'Сегодня коротыкам повезло, но даже если они восстановят ворота, не долго им осталось пребывать в покое...'
            $ game.dragon.gain_rage()
    
    return
    
label lb_dwarf_army:
    'Подобно несущему смерть урагану [game.dragon.fullname] ворвался во внутренние палаты подгорного царства. Однако цверги всё ещё не беззащитны, дорогу дракону заступает в спешке собранный ударный отряд...'
    $ game.foe = Enemy('dwarf_guards', game_ref=game)
    $ narrator(show_chances(game.foe))
    menu:
        'Massacre':
            call lb_fight from _call_lb_fight_39
            'Теперь, когда основные силы цвергов разбиты и деморализованы, надо выбрать направление финального удара. Ремесленные кварталы почти беззащиты и там цвергов можно будет перебить во множестве, пока они не успели сбежать. С другой стороны, самые главные ценности должны храниться ниже, в главной сокровищнице. Если не наведаться туда прямо сейчас, хитрые цверги вынесут всё до последней монетки.'
            menu:
                'Down to the treashury!':
                    call lb_dwarf_treashury from _call_lb_dwarf_treashury
                    
                'Rob the halls':
                    call lb_dwarf_houses from _call_lb_dwarf_houses
                    
                'Flee':
                    'Обидно отступать, когда победа была так близка, но загнанные в угол цверги могут быть крайне опасными противниками. Иногда лучше не рисковать!'
                    $ game.dragon.gain_rage()
                    
        'Бежать поджав хвост':
            'Сегодня коротышкам повезло, но даже если они восстановят ворота, не долго им осталось пребывать в покое...'
            $ game.dragon.gain_rage()
    return
    
label lb_dwarf_houses:
    'Хотя большинство цвергов бегают в панике и пытаются спасти себя и свои пожитки, при виде дракона многие хватаются за ломы, кирки и тпоры чтобы дать отпор супостату...'
    $ game.foe = Enemy('dwarf_citizen', game_ref=game)
    $ narrator(show_chances(game.foe))
    nvl clear
    menu:
        'Fight the dwarfs':
            call lb_fight from _call_lb_fight_40
            call lb_dwarf_ruins from _call_lb_dwarf_ruins
        'Flee':
            'Обидно отутпать когда победа была так близка, но загнанные в угол цверги могут быть крайне опасными противниками. Иногда лучше не рисковать!'
            $ game.dragon.gain_rage()        
    return
    
label lb_dwarf_treashury:
    'Понимая что их королевство стоит на грани катастрофы, цверги пытаются спасти две самые большие ценности - короля и сокровища. Бойцов у них осталось не много, однако среди них есть один равный по силе целой армии - закованный в доспехи до самых глаз чемпион цвергов выступает вперёд потрясая массивным но острым топором.'
    $ game.foe = Enemy('dwarf_champion', game_ref=game)
    $ narrator(show_chances(game.foe))
    nvl clear
    menu:
        'Fight the champon':
            call lb_fight from _call_lb_fight_41
            $ game.dragon.reputation.points += 25
            '[game.dragon.reputation.gain_description]'     
            call lb_dwarf_rob from _call_lb_dwarf_rob
        'Flee':
            'Обидно отутпать когда победа была так близка, но загнанные в угол цверги могут быть крайне опасными противниками. Иногда лучше не рисковать!'
            $ game.dragon.gain_rage()      
    return

label lb_dwarf_rob:
    python:
        count = random.randint(12,15)
        alignment = 'dwarf'
        min_cost = 500
        max_cost = 5000
        obtained = "Это предмет из сокровищницы короля-под-горой."
        trs = treasures.gen_treas(count, data.loot['palace'], alignment, min_cost, max_cost, obtained)
        trs_list = game.lair.treasury.treasures_description(trs)
        trs_descrptn = '\n'.join(trs_list)
    menu:
        'Rob the Great Treashury':
            show expression 'img/bg/hoard/base.jpg' as bg
            'Подлые цверги многое успели растащить, но даже от того что осталось разбегаются глаза. Нигде больше не найти столь богатой добычи!'    
            '[trs_descrptn]'
            $ game.lair.treasury.receive_treasures(trs)
            nvl clear
            call lb_dwarf_ruins from _call_lb_dwarf_ruins_1
                                        
        'Remember and go away':
            $ game.dragon.add_special_place('palace', 'palace_empty')
    return
            
label lb_dwarf_ruins:
    show expression 'img/bg/special/moria.jpg' as bg
    'Когда-то тут жили цверги, но теперь это место опустошено и заброшено. Внутри можно устроить просторное и отлично защищённое логово.'
    menu:
        'Make a lair here':
            $ game.create_lair('underground_palaces')
            $ game.dragon.del_special_place('frontgates')
            $ game.dragon.del_special_place('backdor')
        'Go away':
            $ game.dragon.add_special_place('frontgates', 'frontgates_open')
    return 
