label lb_location_plains_main:
    $ place = 'plain'
    show expression get_place_bg(place) as bg
    nvl clear
    
    if game.dragon.energy() == 0:
        'Даже драконам надо иногда спать. Особенно драконам!'
        return
        
    menu:
        'Рыскать за околицей':
            call lb_encounter_plains
            return
        'Одинокий хутор':
            $ village_size = 1
            call lb_village
        'Маленький посёлок':
            $ village_size = 2
            call lb_village
        'Деревня':
            $ village_size = 3
            call lb_village
        'Село':
            $ village_size = 4
            call lb_village
        'Городок':
            $ village_size = 5
            call lb_village
        'Прочь отсюда':
            return
        
    return
    
label lb_encounter_plains:
    $ nochance = game.poverty.value*3
    $ choices = [("lb_enc_fair", 10),
                ("lb_enc_berries", 10),
                ("lb_enc_shrooms", 10),
                ("lb_enc_laundry", 10),
                ("lb_enc_bath", 10),   
                ("lb_enc_militia", 10),
                ("lb_enc_mill", 10),
                ("lb_enc_granary", 10),
                ("lb_enc_sheepherd", 10),
                ("lb_enc_pigs", 10),
                ("lb_enc_cattle", 10),
                ("lb_enc_gooze", 10),
                ("lb_patrool_plains", 3*game.mobilization.level),                   
                ("lb_enc_noting", nochance),]
    $ enc = core.Game.weighted_random(choices)
    $ renpy.call(enc)
    return
    
    
label lb_enc_fair:
    $ txt = game.interpolate(random.choice(txt_enc_fair[0]))
    '[txt]'
    nvl clear
    menu:
        'Первая красавица':
            $ game.dragon.drain_energy()
            $ description = game.girls_list.new_girl('peasant')
            $ txt = game.interpolate(random.choice(txt_enc_fair[1]))
            '[txt]'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex      
            return

        'Призовой бык':
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('bull_champion', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            menu:
                'Сожрать призового быка' if game.dragon.hunger > 0:
                    'Бык съеден. -1 к голоду, +1 к похоти. Ярость обнуляется.'
                    $ game.dragon.reputation.points += 1
                    '[game.dragon.reputation.gain_description]'
                    $ game.dragon.bloodiness = 0
                    $ if game.dragon.lust < 3: game.dragon.lust += 1
                    $ game.dragon.hunger -= 1
                'Уйти':
                    return
            return
            
        'Оставить их в покое' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            return
    
    return
    
    
label lb_enc_berries:
    'Девушки на опушке собирают ягоды. При появлении дракона поднимается дикий визг, девушки разбегаются. Одна не бросает корзину с ягодами. Ещё одна по запаху кажется невинной.'
    nvl clear
    $ description = game.girls_list.new_girl('peasant')
    nvl clear
    menu:
        'Невинная девица':
            $ game.dragon.drain_energy()
            'Сцена погони. Дракон ловит невинную девушку.'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex      
            return
            
        'Девица с ягодами':
            $ game.dragon.drain_energy()
            'Сцена погони. Дракон ловит девушку с корзинкой ягод.'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            game.girl 'Ой только не ешьте меня пожалуйста.'
            menu:
                'Ограбить девицу' if game.girl.treasure != []:
                    $ description = game.girls_list.rob_girl()
                    game.girl.third "Дракон раздевает девушку догола и забирает всё ценное."
                    game.girl 'Можно я теперь пойду?'
                    menu:
                        'Поиграть с девицей' if game.dragon.lust > 0:
                            'Дракон заставляет девушку обмазаться ягодами из лукошка, а затем сделать ему минет.'
                            $ game.dragon.lust -= 1
                            menu:
                                'Сожрать девицу' if game.dragon.hunger > 0:
                                    'Дракон пожирает девицу'
                                    $ if game.dragon.bloodiness > 0: game.dragon.bloodiness = 0
                                    $ game.dragon.hunger -= 1
                                'Отпустить':
                                    'Голая крестьянка убегает пытаясь прикрыть срам руками.'
                            return
                        'Сожрать девицу' if game.dragon.hunger > 0:
                            'Дракон обмазывает девушку ягодами из лукошка и съедает.'
                            $ if game.dragon.bloodiness > 0: game.dragon.bloodiness = 0
                            $ if game.dragon.lust < 3: game.dragon.lust += 1
                            $ game.dragon.hunger -= 1
                            return
                        'Отпустить':
                            'Голая крестьянка убегает пытаясь прикрыть срам руками.'
                            return
                'Поиграть с девицей' if game.dragon.lust > 0:
                    'Дракон заставляет девушку раздеться и обмазаться ягодами из лукошка, а затем сделать ему минет.'
                    $ game.dragon.lust -= 1
                    menu:
                        'Сожрать девицу' if game.dragon.hunger > 0:
                            'Дракон пожирает девицу'
                            $ if game.dragon.bloodiness > 0: game.dragon.bloodiness = 0
                            $ game.dragon.hunger -= 1
                        'Отпустить':
                            'Голая крестьянка убегает пытаясь прикрыть срам руками.'
                    return
                'Сожрать девицу' if game.dragon.hunger > 0:
                    'Дракон срывает с девушки одежду, обмазывает её ягодами из лукошка и съедает.'
                    $ if game.dragon.bloodiness > 0: game.dragon.bloodiness = 0
                    $ if game.dragon.lust < 3: game.dragon.lust += 1
                    $ game.dragon.hunger -= 1
                'Отнять ягоды и отпустить':
                    'Дракон закусывает сладкими ягодками и уходит.'
                    $ if game.dragon.lust < 3: game.dragon.lust += 1
                    return
                    
        'Оставить их в покое': 
            '[game.dragon.name] берет одну из брошенных корзинок с ягодами себе на дессерт и уходит.'
            $ game.dragon.gain_rage()
            return
    
    return
    
label lb_enc_shrooms:
    'Девушки на опушке собирают грибы. При появлении дракона поднимается дикий визг, девушки разбегаются. Одна не бросает корзину с грибами. Ещё одна по запаху кажется невинной.'
    $ description = game.girls_list.new_girl('peasant')
    nvl clear
    menu:
        'Невинная девица':
            $ game.dragon.drain_energy()
            'Сцена погони. Дракон ловит невинную девушку.'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex      
            return
            
        'Девица с грибным лукошком':
            $ game.dragon.drain_energy()
            'Сцена погони. Дракон ловит девушку с корзинкой грибов.'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            game.girl 'Ой только не ешьте меня пожалуйста.'
            menu:
                'Ограбить девицу' if game.girl.treasure != []:
                    $ description = game.girls_list.rob_girl()
                    game.girl.third "Дракон раздевает девушку догола и забирает всё ценное."
                    game.girl 'Можно я теперь пойду?'
                    nvl clear
                    menu:
                        'Поиграть с девицей' if game.dragon.lust > 0:
                            'Дракон заставляет девушку сделать ему минет.'
                            $ game.dragon.lust -= 1
                            nvl clear
                            menu:
                                'Сожрать девицу' if game.dragon.hunger > 0:
                                    'Дракон заставляет крестьянку нажарить грибов, затем потрошит её, фарширует грибами и пожирает.'
                                    $ if game.dragon.bloodiness > 0: game.dragon.bloodiness = 0
                                    $ if game.dragon.lust < 3: game.dragon.lust += 1
                                    $ game.dragon.hunger -= 1
                                'Отпустить':
                                    'Голая крестьянка убегает пытаясь прикрыть срам руками.'
                            return
                        'Сожрать девицу' if game.dragon.hunger > 0:
                            'Дракон заставляет крестьянку нажарить грибов, затем потрошит её, фарширует грибами и пожирает.'
                            $ if game.dragon.bloodiness > 0: game.dragon.bloodiness = 0
                            $ if game.dragon.lust < 3: game.dragon.lust += 1
                            $ game.dragon.hunger -= 1
                            return
                        'Отпустить':
                            'Голая крестьянка убегает пытаясь прикрыть срам руками.'
                            return
                'Поиграть с девицей' if game.dragon.lust > 0:
                    'Дракон заставляет девушку раздеться и сделать ему минет.'
                    $ game.dragon.lust -= 1
                    nvl clear
                    menu:
                        'Сожрать девицу' if game.dragon.hunger > 0:
                            'Дракон заставляет крестьянку нажарить грибов, затем потрошит её, фарширует грибами и пожирает.'
                            $ if game.dragon.bloodiness > 0: game.dragon.bloodiness = 0
                            $ game.dragon.hunger -= 1
                        'Отпустить':
                            'Голая крестьянка убегает пытаясь прикрыть срам руками.'
                    return
                'Сожрать девицу' if game.dragon.hunger > 0:
                    'Дракон срывает с крестьянки одежду, потрошит и фарширует грибами а затем пожирает.'
                    $ if game.dragon.bloodiness > 0: game.dragon.bloodiness = 0
                    $ if game.dragon.lust < 3: game.dragon.lust += 1
                    $ game.dragon.hunger -= 1
                'Отнять ягоды и отпустить':
                    'Дракон закусывает свежими грибами и уходит.'
                    $ if game.dragon.lust < 3: game.dragon.lust += 1
                    return
                    
        'Оставить их в покое': 
            '[game.dragon.name] берет одну из брошенных корзинок с грибами себе на закуску и уходит.'
            $ game.dragon.gain_rage()
            return
    
    return

    
label lb_enc_laundry:
    'Прачки. Одна из них по запаху кажется невинной девушкой.'
    nvl clear
    menu:
        'Схватить невинную девицу':
            $ game.dragon.drain_energy()
            $ description = game.girls_list.new_girl('peasant')
            'Сцена погони. Все разбегаются, дракон остаётся с пойманной девушкой.'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex      
            return        
        'Оставить их в покое' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            return    
    return
    
label lb_enc_bath:
    'Купальщицы. Одна из них по запаху кажется невинной девушкой.'
    nvl clear
    menu:
        'Схватить невинную девицу':
            $ game.dragon.drain_energy()
            $ description = game.girls_list.new_girl('peasant')
            'Сцена погони. Все разбегаются, дракон остаётся с пойманной девушкой.'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex      
        'Оставить их в покое' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    return
    
label lb_enc_militia:
    $ if game.mobilization.level <= 0: renpy.jump('lb_encounter_plains')
    show expression 'img/scene/fight/militia.png' as bg
    'На поле тренируются ополченцы-новобранцы.'
    nvl clear
    menu:
        'Напасть':
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('militia', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            '  Отряд ополченцев готовившийся пополнить армию больше не существует. Немногие выжившие новобранцы разбежались в ужасе. Теперь королю будет сложнее собирать свои патрульные отряды.'
            $game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
            $ game.mobilization.level -= 1
                        
        'Убраться прочь' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    
    return
    
    
label lb_enc_mill:
    show expression 'img/bg/special/windmill.png' as bg
    'Ветряная мельница.'
    nvl clear
    menu:
        'Расшатать мельницу' if game.dragon.size() > 3:
            $ game.dragon.drain_energy()
            "Я твой мельница щаталь!"
            $ game.poverty.value += 1
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
        'Заклятье гнили' if game.dragon.mana > 0:
            $ game.dragon.drain_energy()
            "Амбар сгорает синим пламенем."
            $ game.poverty.value += 1
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
        'Обследовать здание' if game.dragon.size() <= 3 and game.dragon.mana == 0:
            $ game.dragon.drain_energy()
            "[game.dragon.name] тщательно обследует необычное строение на предмет важности и уязвимых мест. Эту четырёхкрылую башню с каменным основанием люди используют чтобы делать из зерна муку. Очень хочется её разрушить, но стоит она прочно. Нужно либо размер иметь побольше чтобы расшатать её собственным телом, либо наслать гнилостное заклятье на внутренние деревянные механизмы."
            'Только время зря потерял. Придётся уйти несолоно хлебавши.'
        'Пройти мимо' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    
    return
    
label lb_enc_granary:
    show expression 'img/bg/plain/9.png' as bg    
    'Амбар полный зерна.'
    nvl clear
    python:
        doit = False
        if 'fire_breath' in game.dragon.modifiers(): 
            doit = True
    menu:
        'Дыхнуть огнём' if doit:
            $ game.dragon.drain_energy()
            "Амбар сгорает оставив людей без запасов зерна."
            $ game.poverty.value += 1
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]'
        'Наколдовать синее пламя' if game.dragon.mana > 0:
            $ game.dragon.drain_energy()
            "Амбар сгорает синим пламенем."
            $ game.poverty.value += 1
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]'
        'Обследовать здание' if not doit and game.dragon.mana == 0:
            $ game.dragon.drain_energy()
            "[game.dragon.name] тщательно обследует огромный амбар. Зерна тут хватит чтобы целыый городо прокормить. Эх сжечь бы это всё до тла и люди начали бы голодать, только вот огонька нет..."
        'Пройти мимо' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    
    return

label lb_enc_gooze:
    'Босоногая крестьянская девчёнка пасёт гусей. Слишком молода чтобы рожать.'
    nvl clear
    menu:
        'Сожрать гусей' if game.dragon.hunger > 0:
            'Дракон ловит и проглатывает одного жирного гуся, но остальные разлетаются.'
            $ game.dragon.drain_energy()
            $ if game.dragon.bloodiness > 0: game.dragon.bloodiness -= 1
        'Сожрать девчёнку' if game.dragon.hunger > 0:
            'Дракон хватает девчёнку и съедает её.'
            $ game.dragon.drain_energy()
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            $ if game.dragon.bloodiness > 0: game.dragon.bloodiness = 0
            $ game.dragon.hunger -= 1
        'Устрить побоище' if game.dragon.bloodiness >= 5:
            $ game.dragon.drain_energy()
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            'Дракон нападает, убивая девочку и всех гусей которых только может поймать, просто ради забавы.'    
        'Оставить их в покое' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    
    return
    
label lb_enc_pigs:
    'Свиньи пасутся в дубовой роще. Свинопас убегает, стадо охраняет злая собака.'
    nvl clear
    menu:
        'Напасть на стадо' if game.dragon.hunger > 0:
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('dog', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            'Дракон съедает свинью.'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            $ if game.dragon.bloodiness > 0: game.dragon.bloodiness = 0
            $ game.dragon.hunger -= 1
        'Напасть на стадо' if game.dragon.hunger == 0:
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('dog', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            'Дракон догоняет и убивает свинопаса, после чего разгоняет стадо.'
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
        'Отступить' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            return    
    
    return    

label lb_enc_sheepherd:
    'Овцы на выпасе. Пастух убегает, остаётся собака.'
    nvl clear
    menu:
        'Напасть на стадо' if game.dragon.hunger > 0:
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('dog', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            'Дракон съедает овцу.'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            $ if game.dragon.bloodiness > 0: game.dragon.bloodiness = 0
            $ game.dragon.hunger -= 1
        'Напасть на стадо' if game.dragon.hunger == 0:
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('dog', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            'Дракон убивает несколько овец, хотя не хочет есть.'
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
        'Отступить' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            return    
    
    return


label lb_enc_cattle:
    'Коровы на выпасе. Пастух убегает, один из быков защищает стадо.'
    nvl clear
    menu:
        'Напасть на стадо' if game.dragon.hunger > 0:
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('bull', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            $ if game.dragon.bloodiness > 0: game.dragon.bloodiness = 0
            $ game.dragon.hunger -= 1
            'Дракон съедает корову.'
            $ game.dragon.reputation.points +=1
            '[game.dragon.reputation.gain_description]'
        'Напасть на стадо' if game.dragon.hunger == 0:
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('bull', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            'Дракон убивает несколько коров и разгоняет стадо, хотя не хочет есть.'
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
        'Отступить' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            return    
    
    return

label lb_enc_noting:
    show expression 'img/bg/special/village_burned.png' as bg          
    'Здесь лишь запустение и разруха. Хотя когда-то тут можно было встретить людей или животных, сейчас их больше нету. Кругом лишь разрушенные дома да заросшие бурьяном пашни.'
    python:
        if game.dragon.bloodiness < 5: 
            game.dragon.gain_rage()
    return


#разные деревни
label lb_village:
    python:
        a = 10 + game.poverty.value - village_size
        chance = random.randint(1,a)
        if chance > 10: village_size = 0
        txt1 = village['overview'][village_size]
    show expression 'img/bg/special/village.png' as bg     
    '[txt1]'
    nvl clear
    menu:
        'Наложить дань' if village_size > 0 and game.dragon.fear > 0:
            $ game.dragon.drain_energy()
            show expression 'img/bg/special/fear.png' as bg
            if village_size == 1:
                'Хоторяне отдают дракону свою единственную корову. [game.dragon.name] съедает её.'
                python:
                    if game.dragon.bloodiness > 0 and game.dragon.hunger > 0: 
                        game.dragon.bloodiness = 0
                        game.dragon.hunger -= 1
            elif village_size == 2:
                'Жители деревни отдают дракону молодую крестьянку.'
                $ description = game.girls_list.new_girl('peasant')
                nvl clear
                game.girl.third "[description]"
                call lb_nature_sex                   
            elif village_size == 3:
                'Жена старосты отдаёт своё самое дорогое украшение:'
                python:
                    count = 1
                    alignment = 'human'
                    min_cost = 10
                    max_cost = 250
                    obtained = "Часть дани, выплаченной одной из деревень."
                    trs = treasures.gen_treas(count, data.loot['jeweler'], alignment, min_cost, max_cost, obtained)
                    trs_list = game.lair.treasury.treasures_description(trs)
                    trs_descrptn = '\n'.join(trs_list)
                    game.lair.treasury.receive_treasures(trs)
                '[trs_descrptn]'
            elif village_size == 4:
                'Селяне собирают с каждого двора деньги, чтобы выплатить дракону дань:'
                python:
                    count = 1
                    alignment = 'human'
                    min_cost = 100
                    max_cost = 1000
                    t_list = ['farting']
                    obtained = "Часть дани, выплаченной одной из деревень."
                    trs = treasures.gen_treas(count, t_list, alignment, min_cost, max_cost, obtained)
                    trs_list = game.lair.treasury.treasures_description(trs)
                    trs_descrptn = '\n'.join(trs_list)
                    game.lair.treasury.receive_treasures(trs)
                '[trs_descrptn]'
            else:
                'Горожане отдают дракону свою первую красавицу.'
                $ description = game.girls_list.new_girl('citizen')
                nvl clear
                game.girl.third "[description]"
                call lb_nature_sex        
            
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'

        'Ограбить' if village_size > 0:
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy(village['deffence'][village_size], gameRef=game, base_character=NVLCharacter)
            call lb_fight
            'Поселение успешно разграблено. Добыча:'
            python:
                count = random.randint(3,7)
                alignment = 'human'
                min_cost = 10*village_size
                max_cost = 100*village_size
                obtained = "Это предмет из разграбленного людского поселения."
                trs = treasures.gen_treas(count, data.loot['klad'], alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
            '[trs_descrptn]'
            $ game.lair.treasury.receive_treasures(trs)
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
            'Очков репутации: [game.dragon.reputation.points]'
        
        'Разорить' if village_size > 0:
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy(village['deffence'][village_size], gameRef=game, base_character=NVLCharacter)
            call lb_fight
            'Поселение разорено. Разруха в стране растёт. В разрушенных домах и на телах убитых нашлись кое-какие ценности:'
            python:
                count = random.randint(3,7)
                alignment = 'human'
                min_cost = 10*village_size
                max_cost = 100*village_size
                obtained = "Это предмет из разграбленного людского поселения."
                trs = treasures.gen_treas(count, data.loot['klad'], alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
            '[trs_descrptn]'
            $ game.lair.treasury.receive_treasures(trs)
            $ game.poverty.value += 1            
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]'
    
        'Отступить' if game.dragon.bloodiness < 5 and village_size > 0:
            $ game.dragon.gain_rage()
            
        'Убраться прочь' if village_size == 0:
            python:
                if game.dragon.bloodiness < 5: 
                    game.dragon.gain_rage()
        
    return

label lb_patrool_plains:
    python:
        game.dragon.drain_energy()
        chance = random.randint(0,game.mobilization.level)
        if chance < 4:
            patrool = 'archer'
            dtxt = 'Стрелок шерифа.'
        elif chance < 7:
            patrool = 'xbow_rider'
            dtxt = 'Конный разъезд.'
        elif chance < 11:
            patrool = 'heavy_cavalry'
            dtxt = 'Тяжелая кавалерия.'
        elif chance < 16:
            patrool = 'griffin_rider'
            dtxt = 'Всадник на грифоне.'
        else:
            patrool = 'angel'
            dtxt = '%s вынужден зажмуриться от яркого света бьющего в глаза. Громогласный оклик возвещает: "Умри мерзкое порождение греха!!!". Это ангел-хранитель посланный людям Небесами для защиты.' % game.dragon.name
    '[dtxt]'
    $ game.foe = core.Enemy(patrool, gameRef=game, base_character=NVLCharacter)
    call lb_fight
    
    return
    