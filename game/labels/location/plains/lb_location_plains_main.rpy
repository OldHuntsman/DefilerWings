label lb_location_plains_main:
    $ place = 'plain'
    show place as bg
    nvl clear
      
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
    $ nochance = 10*poverty
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
                ("lb_enc_noting", nochance),]
    $ enc = core.Game.weighted_random(choices)
    $ renpy.call(enc)
    return
    
    
label lb_enc_fair:
    'Ярмарка. Тут юноши присматривают невест из окрестных деревень, а крестьяне демонстрируют свой лучший скот.'
    nvl clear
    menu:
        'Первая красавица':
            $ game.dragon.drain_energy()
            $ description = game.girls_list.new_girl('peasant')
            'Сцена погони. Все разбегаются, дракон остаётся с пойманной девушкой.'
            $ gain_rep()
            '[rep_text]'
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
                    $ gain_rep()
                    '[rep_text]'
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
    menu:
        'Невинная девица':
            $ game.dragon.drain_energy()
            'Сцена погони. Дракон ловит невинную девушку.'
            $ gain_rep()
            '[rep_text]'
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex      
            return
            
        'Девица с ягодами':
            $ game.dragon.drain_energy()
            'Сцена погони. Дракон ловит девушку с корзинкой ягод.'
            $ gain_rep()
            '[rep_text]'
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
    nvl clear
    $ description = game.girls_list.new_girl('peasant')
    menu:
        'Невинная девица':
            $ game.dragon.drain_energy()
            'Сцена погони. Дракон ловит невинную девушку.'
            $ gain_rep()
            '[rep_text]'
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex      
            return
            
        'Девица с грибным лукошком':
            $ game.dragon.drain_energy()
            'Сцена погони. Дракон ловит девушку с корзинкой грибов.'
            $ gain_rep()
            '[rep_text]'
            game.girl 'Ой только не ешьте меня пожалуйста.'
            menu:
                'Ограбить девицу' if game.girl.treasure != []:
                    $ description = game.girls_list.rob_girl()
                    game.girl.third "Дракон раздевает девушку догола и забирает всё ценное."
                    game.girl 'Можно я теперь пойду?'
                    menu:
                        'Поиграть с девицей' if game.dragon.lust > 0:
                            'Дракон заставляет девушку сделать ему минет.'
                            $ game.dragon.lust -= 1
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
    menu:
        'Схватить невинную девицу':
            $ game.dragon.drain_energy()
            $ description = game.girls_list.new_girl('peasant')
            'Сцена погони. Все разбегаются, дракон остаётся с пойманной девушкой.'
            $ gain_rep()
            '[rep_text]'
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex      
            return        
        'Оставить их в покое' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            return    
    return
    
label lb_enc_bath:
    'Прачки. Одна из них по запаху кажется невинной девушкой.'
    menu:
        'Схватить невинную девицу':
            $ game.dragon.drain_energy()
            $ description = game.girls_list.new_girl('peasant')
            'Сцена погони. Все разбегаются, дракон остаётся с пойманной девушкой.'
            $ gain_rep()
            '[rep_text]'
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex      
            return        
        'Оставить их в покое' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            return    
    return
    
label lb_enc_militia:
    show expression 'img/scene/fight/militia.png' as bg
    'На поле тренируются ополченцы-новобранцы.'
    menu:
        'Напасть':
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('militia', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            '  Отряд ополченцев готовившийся пополнить армию больше не существует. Немногие выжившие новобранцы разбежались в ужасе. Теперь королю будет сложнее собирать свои патрульные отряды.'
            $ gain_rep(2)
            '[rep_text]'
            $ if mobilization > 0: mobilization -= 1
                        
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
            $ pov_gain += 1
            $ gain_rep(2)
            '[rep_text]'
        'Заклятье гнили' if game.dragon.magic() > 0:
            $ game.dragon.drain_energy()
            "Амбар сгорает синим пламенем."
            $ pov_gain += 1
            $ gain_rep(2)
            '[rep_text]'
        'Обследовать здание' if game.dragon.size() <= 3 and game.dragon.magic() == 0:
            $ game.dragon.drain_energy()
            "[game.dragon.name] тщательно обследует необычное строение на предмет важности и уязвимых мест. Эту четырёхкрылую башню с каменным основанием люди используют чтобы делать из зерна муку. Очень хочется её разрушить, но стоит она прочно. Нужно либо размер иметь побольше чтобы расшатать её собственным телом, либо наслать гнилостное заклятье на внутренние деревянные механизмы."
            'Только время зря потерял. Придётся уйти несолоно хлебавши.'
        'Пройти мимо' if bloodlust < 5:
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
            $ pov_gain += 1
            $ gain_rep(3)
            '[rep_text]'
        'Наколдовать синее пламя' if game.dragon.magic() > 0:
            $ game.dragon.drain_energy()
            "Амбар сгорает синим пламенем."
            $ pov_gain += 1
            $ gain_rep(3)
            '[rep_text]'
        'Обследовать здание' if not doit and game.dragon.magic() == 0:
            $ game.dragon.drain_energy()
            "[game.dragon.name] тщательно обследует огромный амбар. Зерна тут хватит чтобы целыый городо прокормить. Эх сжечь бы это всё до тла и люди начали бы голодать, только вот огонька нет..."
        'Пройти мимо' if bloodlust < 5:
            $ game.dragon.gain_rage()
    
    return

label lb_enc_goose:
    'Босоногая крестьянская девчёнка пасёт гусей. Слишком молода чтобы рожать.'
    menu:
        'Сожрать гусей' if game.dragon.hunger > 0:
            'Дракон ловит и проглатывает одного жирного гуся, но остальные разлетаются.'
            $ if game.dragon.bloodiness > 0: game.dragon.bloodiness -= 1
        'Сожрать девчёнку' if game.dragon.hunger > 0:
            'Дракон хватает девчёнку и съедает её.'
            $ gain_rep()
            '[rep_text]'
            $ if game.dragon.bloodiness > 0: game.dragon.bloodiness = 0
            $ game.dragon.hunger -= 1
        'Устрить побоище' if game.dragon.bloodiness => 5:
            $ gain_rep()
            '[rep_text]'
            'Дракон нападает, убивая девочку и всех гусей которых только может поймать, просто ради забавы.'    
        'Оставить их в покое' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    
    return
    
label lb_enc_pigs:
    'Свиньи пасутся в дубовой роще. Свинопас убегает.'
    menu:
        'Напасть на стадо' if game.dragon.hunger > 0:
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('dog', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            'Дракон съедает свинью.'
            $ gain_rep()
            '[rep_text]'
            $ if game.dragon.bloodiness > 0: game.dragon.bloodiness = 0
            $ game.dragon.hunger -= 1
        'Напасть на стадо' if game.dragon.hunger == 0:
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('dog', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            'Дракон догоняет и убивает свинопаса, после чего разгоняет стадо.'
            $ gain_rep(2)
            '[rep_text]'
        'Отступить' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            return    
    
    return    

label lb_enc_sheepherd:
    'Овцы на выпасе. Пастух убегает, остаётся собака.'
    menu:
        'Напасть на стадо' if game.dragon.hunger > 0:
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('dog', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            'Дракон съедает овцу.'
            $ gain_rep()
            '[rep_text]'
            $ if game.dragon.bloodiness > 0: game.dragon.bloodiness = 0
            $ game.dragon.hunger -= 1
        'Напасть на стадо' if game.dragon.hunger == 0:
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('dog', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            'Дракон убивает несколько овец, хотя не хочет есть.'
            $ gain_rep(2)
            '[rep_text]'
        'Отступить' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            return    
    
    return


label lb_enc_cattle:
    'Коровы на выпасе. Пастух убегает, один из быков защищает стадо.'
    menu:
        'Напасть на стадо' if game.dragon.hunger > 0:
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('bull', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            $ if game.dragon.bloodiness > 0: game.dragon.bloodiness = 0
            $ game.dragon.hunger -= 1
            'Дракон съедает корову.'
            $ gain_rep()
            '[rep_text]'
        'Напасть на стадо' if game.dragon.hunger == 0:
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('bull', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            'Дракон убивает несколько коров и разгоняет стадо, хотя не хочет есть.'
            $ gain_rep(2)
            '[rep_text]'
        'Отступить' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            return    
    
    return

label lb_enc_noting:
    show expression 'img/bg/special/village_burned.png' as bg          
    'Здесь лишь запустение и разруха. Хотя когда-то тут можно было встретить людей или животных, сейчас их больше нету. Кругом лишь разрушенные дома да заросшие бурьяном пашни.'
    python:
        if bloodlust < 5: 
            game.dragon.gain_rage()
    return


#разные деревни
label lb_village:
    python:
        a = 10 + poverty - village_size
        chance = random.randint(1,a)
        if chance > 10: village_size = 0
        txt1 = village['overview'][village_size]
    show expression 'img/bg/special/village.png' as bg     
    '[txt1]'
    menu:
        'Наложить дань' if village_size > 0:
            show expression 'img/bg/special/fear.png' as bg
            'Переговоры о дани безуспешны (not implemented yet).'
            # TODO: сделать систему наложения дани. Если у дракона достаточно страха чтобы защитники убежали то вознкает актив "дань" соотвествующий уровню деревни. 
            # Пока этот актив у дракона есть, при каждом пробуждении он будет получать некую плюшку, в заивисмости от богатства деревни. 
            # Если защиники не боятся, то можно начать сражение, однако деревня будет разорена и дани дракон не получит.

        'Ограбить' if village_size > 0:
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy(village['deffence'][village_size], gameRef=game, base_character=NVLCharacter)
            call lb_fight
            'Поселение успешно разграблено.'
            $ gain_rep(2)
            '[rep_text]'
        
        'Разорить' if village_size > 0:
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy(village['deffence'][village_size], gameRef=game, base_character=NVLCharacter)
            call lb_fight
            'Поселение разорено. Разруха в стране растёт.'
            $ pov_gain += 1            
            $ gain_rep(3)
            '[rep_text]'
    
        'Отступить' if bloodlust < 5 and village_size > 0:
            $ game.dragon.gain_rage()
            
        'Убраться прочь' if village_size == 0:
            python:
                if bloodlust < 5: 
                    game.dragon.gain_rage()
        
    return
    