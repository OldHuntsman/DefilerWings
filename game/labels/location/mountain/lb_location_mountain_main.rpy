label lb_location_mountain_main:
    $ place = 'mountain'
    show expression get_place_bg(place) as bg
    nvl clear
    
    if game.dragon.energy() == 0:
        'Даже драконам надо иногда спать. Особенно драконам!'
        return
        
    $ nochance = game.poverty.value*10      
    $ choices = [("lb_enc_miner", 10),
                ("lb_enc_dklad", 10),
                ("lb_enc_mines", 10),
                ("lb_enc_ram", 10),
                ("lb_enc_bear", 10),   
                ("lb_enc_jotun", 10),
                ("lb_enc_ifrit", 10),
                ("lb_enc_smuglers", 10),
                ("lb_enc_slavers", 10),                
                ("lb_enc_frontgates", 10),
                ("lb_enc_cavegates", 10),
                ("lb_patrool_mountain", 3*game.mobilization.level),                
                ("lb_enc_noting", nochance),]
    $ enc = core.Game.weighted_random(choices)
    $ renpy.call(enc)
        
    return
    
    
label lb_enc_miner:
    'Одинокий златоискатель.'
    nvl clear
    menu:
        'Убить и ограбить':
            'В мешке златоискателя обнаруживается почти фунт золотого песка и мелких самородков. Глупцы, вечно они всё богатсво с собой таскают.'
            python:
                gold_trs = treasures.Ingot('gold')
                gold_trs.weight = 1
                game.lair.treasury.receive_treasures([gold_trs])
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            
        'Пусть идёт' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            return
    return
    
label lb_enc_dklad:
    'Дракон учуял сокровища спрятанные где-то н подалёку.'
    nvl clear
    python:
        tr_lvl = random.randint(1,100)
        count = random.randint(1,10)
        alignment = 'human'
        min_cost = 1*tr_lvl
        max_cost = 10*tr_lvl
        obtained = "Это предмет из клада, спрятанного в горной расщелине."
        trs = treasures.gen_treas(count, data.loot['klad'], alignment, min_cost, max_cost, obtained)
        trs_list = game.lair.treasury.treasures_description(trs)
        trs_descrptn = '\n'.join(trs_list)
    menu:
        'Отыскать и забрать':
            $ game.dragon.drain_energy()
            'Перевернув каждый камень и заглянув в каждую расселину по близости [game.dragon.name] находит наконец тщательно схороненный тайник. Внутри лежит:'
            '[trs_descrptn]'
            $ game.lair.treasury.receive_treasures(trs)
                        
        'Пусть пока лежат'  if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            'Конечно сокровища полезны, но то что тут могли спрятать жалкие смертные вряд ли стоит драгоценного времени благородного змея.'    
    return

    
label lb_enc_ram:
    'По скалам скачет пушистый баран.'
    nvl clear
    menu:
        'Сожрать барана' if game.dragon.hunger > 0:
            $ game.dragon.drain_energy()
            '[game.dragon.name] ловит и пожирает барана.'
            $ if game.dragon.bloodiness > 0: game.dragon.bloodiness = 0
        'Разорвать оленя' if game.dragon.bloodiness >= 5 and game.dragon.hunger == 0:
            $ game.dragon.drain_energy()
            '[game.dragon.name] жестоко задирает барана просто ради забавы.'    
        'Просто шугануть' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    return
    
label lb_enc_bear:
    'Огромный пещерный медведь.'
    nvl clear
    menu:
        'Сразиться с медведем':
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('bear', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            if game.dragon.hunger > 0:
                'Дракон съедает медведя.'
                $ if game.dragon.bloodiness > 0: game.dragon.bloodiness = 0
                $ game.dragon.hunger -= 1
            else:
                'Дракон торжествует победу.'
                
        'Отступить' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    
    return
    
label lb_enc_smuglers:
    'Отряд контрабандистов.'
    menu:
        'Вымогать деньги':
            python:
                game.dragon.drain_energy()
                passing_tool = game.dragon.fear()*2 + 1 
                gold_trs = treasures.Coin('taller', passing_tool)
                game.lair.treasury.receive_treasures([gold_trs])
            'Контрабандисты скидываются по таллеру и отдают [passing_tool] чтобы откупиться и пройти мирно. С паршивой овцы хоть шерсти клок...'
            
        'Отнять весь товар':
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('band', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            python:
                count = random.randint(5,15)
                alignment = 'human'
                min_cost = 5
                max_cost = 100
                t_list = smuggler_list
                obtained = "Это часть груза контрабандистов, которых дракон ограбил на тайном перевале в северных горах."
                trs = treasures.gen_treas(count, data.loot['smuggler'], alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
                game.lair.treasury.receive_treasures(trs)
                
            'Обыскав тюки контрабандистов [dragon.name] находит кое-какие ценные вещи:'
            '[trs_descrptn]'
            
        'Отпустить их с миром' if game.dragon.bloodiness < 5:    
            'Пусть налаживают торговлю, чем богаче станет страна тем больше можно будет нажиться ограбляя её!'
            $ game.dragon.gain_rage()
    
    return
    
label lb_enc_slavers:
    'Караван работорговцев. Они ведут несколько рабов на веревке, среди рабынь есть одна невинная девушка.'
    menu:
        'Потребовать бесполезного раба' if game.dragon.hunger > 0:
            'Для работорговцев это не слишком большая потеря - они соглашаются отдать самого заморенного раба, чтобы [game.dragon.name] пропустил их без боя. Они даже жалеают дракону приятного аппетита.'
            $ game.dragon.drain_energy()
            'Дракон пожирает измождённого раба. Не самая лучшая закуска на свете, но голод не тётка...'
            $ if game.dragon.bloodiness > 0: game.dragon.bloodiness = 0
            $ game.dragon.hunger -= 1
        
        'Потребовать невинную девушку' if game.dragon.lust > 0:
            $ game.dragon.drain_energy()
            'Среди всех рабов, юная красавица самая ценная. Похоже чтобы получить её придётся разогнать охрану, так просто работорговцы её не отдадут...'
            $ game.foe = core.Enemy('band', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            'Дракон получает девушку.'
            $ description = game.girls_list.new_girl('citizen')
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex    
        
        'Перебить караван':
            $ game.dragon.drain_energy()
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('band', gameRef=game, base_character=NVLCharacter)
            call lb_fight
        
        'Отпустить их с миром' if game.dragon.bloodiness < 5:
            'Пусть налаживают торговлю, чем богаче станет страна тем больше можно будет нажиться ограбляя её!'        
            $ game.dragon.gain_rage()
    
    return

label lb_enc_mines:
    'Серебрянный рудник. Охраняется небольшим отрядом арабалетчиков.'
    menu:
        'Вымогать серебро':
            $ game.dragon.drain_energy()
            'Начальник рудника отдаёт большой серебряный слиток, чтобы избежать конфликта.'
            python:
                gold_trs = treasures.Ingot('silver')
                gold_trs.weight = 16
                game.lair.treasury.receive_treasures([gold_trs])
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            
        'Ограбить рудник':
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('xbow', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            python:
                count = random.randint(1,15)
                alignment = 'human'
                min_cost = 1
                max_cost = 1000000
                t_list = ['silver']
                obtained = "Просто серебро."
                trs = treasures.gen_treas(count, t_list, alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
                game.lair.treasury.receive_treasures(trs)
            'На складе дракон находит драгоценный металл, выплавленный и готовый к отправке в казну:'
            '[trs_descrptn]'
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
            
        'Пройти мимо' if game.dragon.bloodiness < 5:
            'Человеческое серебро не стоит того чтобы получить в глаз их железо!'       
            $ game.dragon.gain_rage()
    return
    
label lb_enc_jotun:
    'Йотун. Плейсхолдер.'
    
    return
    
label lb_enc_ifrit:
    'Ифрит. Плейсхолдер.'
    
    return
   
label lb_enc_frontgates:
    'Главный вход в подгорное царство. Плейсхолдер.'    
    return
    
label lb_enc_cavegates:
    'Потайной вход в подгорное царство. Плейсхолдер.'
    
    return
    
label lb_patrool_mountain:
    python:
        game.dragon.drain_energy()
        chance = random.randint(0,game.mobilization.level)
        if chance < 4:
            patrool = 'jagger'
            dtxt = 'В заросшей низким кустарником седловине %s нарывается на засаду, устроенную горным егерем, патрулирующим эти места.' % game.dragon.name
        elif chance < 7:
            patrool = 'footman'
            dtxt = 'На перевале %s сталкивается с хорошо вооруженным отрядом пехоты. Они настроены весьма серьёзно.' % game.dragon.name
        elif chance < 11:
            patrool = 'heavy_infantry'
            dtxt = '%s попадает в хитроумную ловушку, накрывающую его огромной сетью из толстой веревки. Такая сеть не удержит дракона надолго, однако из-за поворота слышится оглушительный зов рога и тяжелые шаги отряда панцирной пехоты.' % game.dragon.name
        elif chance < 16:
            patrool = 'griffin_rider'
            dtxt = '%s Громкий клёкот эхом отражается от горных склонов. Сверху пикирует грифон, с вооруженным всадником на спине!' % game.dragon.name
        else:
            patrool = 'angel'
            dtxt = '%s вынужден зажмуриться от яркого света бьющего в глаза. Громогласный оклик возвещает: "Умри мерзкое порождение греха!!!". Это ангел-хранитель посланный людям Небесами для защиты.' % game.dragon.name
    '[dtxt]'
    $ game.foe = core.Enemy(patrool, gameRef=game, base_character=NVLCharacter)
    call lb_fight
    
    return
    