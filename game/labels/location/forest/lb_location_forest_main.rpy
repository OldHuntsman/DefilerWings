label lb_location_forest_main:
    $ place = 'forest'
    show expression get_place_bg(place) as bg
    nvl clear
    
    if game.dragon.energy() == 0:
        'Даже драконам надо иногда спать. Особенно драконам!'
        return
        
    $ nochance = game.poverty.value*10      
    $ choices = [("lb_enc_lumberjack", 10),
                ("lb_enc_onegirl", 10),
                ("lb_enc_wandergirl", 10),
                ("lb_enc_ogre", 10),
                ("lb_enc_deer", 10),   
                ("lb_enc_boar", 10),
                ("lb_enc_berries", 10),
                ("lb_enc_shrooms", 10),
                ("lb_enc_guardian", 10),
                ("lb_enc_lumbermill", 10),
                ("lb_enc_klad", 10),
                ("lb_patrool_forest", 3*game.mobilization.level),
                ("lb_enc_noting", nochance),]
    $ enc = core.Game.weighted_random(choices)
    $ renpy.call(enc)
    
    return
    
    
label lb_enc_lumberjack:
    'В лесу раздаётся топор дровосека. Дракон пытается подкрасться.'
    python:
        if game.dragon.size() > 2: 
            succes = True
        else:
            succes = False
    if succes: 
        'Дракон аккуратно подкрадывается. Дровосек работает.'
        nvl clear
        menu:
            'Наблюдать из засады':
                $ game.dragon.drain_energy()
                $ description = game.girls_list.new_girl('peasant')
                'Появляется дочь дровосека, которая приносит ему еду. Дракон неожиданно нападает, убивает дровосека и ловит девушку.'
                $ game.dragon.reputation.points += 1
                '[game.dragon.reputation.gain_description]'
                nvl clear
                game.girl.third "[description]"
                call lb_nature_sex      
                return        
            'Оставить его в покое' if game.dragon.bloodiness < 5:
                $ game.dragon.gain_rage()
    else: 
        'Дракона замечают. Дровосек убегает.' 
            
    return
    
    
label lb_enc_onegirl:
    'По лесной тропинке идёт девушка с корзинкой еды.'
    nvl clear
    menu:
        'Поймать девицу':
            $ game.dragon.drain_energy()
            $ description = game.girls_list.new_girl('peasant')
            'Сцена погони. Дракон настигает жертву.'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex      
        'Отпустить её' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    return

label lb_enc_wandergirl:
    'Крики "Ау". Дракон находит заблудившуюся в чаще невинную девушку.'
    nvl clear
    menu:
        'Поймать девицу':
            $ game.dragon.drain_energy()
            $ description = game.girls_list.new_girl('peasant')
            'Сцена погони. Дракон настигает жертву.'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex      
        'Отпустить её' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    return

label lb_enc_deer:
    'Откормленный лесной олень.'
    nvl clear
    menu:
        'Сожрать оленя' if game.dragon.hunger > 0:
            $ game.dragon.drain_energy()
            '[dragon.name] ловит и пожирает оленя.'
            $ if game.dragon.bloodiness > 0: game.dragon.bloodiness = 0
        'Разорвать оленя' if game.dragon.bloodiness >= 5 and game.dragon.hunger == 0:
            $ game.dragon.drain_energy()
            '[dragon.name] жестоко задирает оленя просто ради забавы.'    
        'Просто шугануть' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    return

label lb_enc_boar:
    'Здоровенный волосатый вепрь.'
    nvl clear
    menu:
        'Сразиться с вепрем':
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('boar', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            if game.dragon.hunger > 0:
                'Дракон съедает вепря.'
                $ if game.dragon.bloodiness > 0: game.dragon.bloodiness = 0
                $ game.dragon.hunger -= 1
            else:
                'Дракон торжествует победу.'
        'Отступить' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    
    return
    
label lb_enc_guardian:
    'Дракон некоторое время бродит по лесу.'
    show expression 'img/scene/fight/elf_ranger.png' as bg
    'Появляется эльфийский страж границ.'
    nvl clear
    menu:
        'Атаковать стража':
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('elf_ranger', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            'Дракон торжествует победу. Но найти тайную тропу что охранял эльф никак не получается...'
            #TODO: Трижды победив эльфийских стражей, дракон открывает себе доступ к волшебным лесам
        'Отступить' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            return            
    return
    
label lb_enc_ogre:
    'Дракон некоторое время бродит по лесу...'
    show expression 'img/bg/special/cave_enter.png' as bg
    'И натыкается на вход в лесную пещеру, достаточно просторную чтобы устроить внутри логово. Судя по запаху, логово себе там уже успел устроить великан-людоед.'
    $ game.foe = core.Enemy('ogre', gameRef=game, base_character=NVLCharacter)
    $ chance_win = battle.victory_chance(game.dragon, game.foe)
    $ chance_wound = battle.victory_chance(game.foe, game.dragon)
    "Шанс победы дракона: [chance_win] %%, шанс ранения дракона: [chance_wound] %%"
    nvl clear
    menu:
        'Вызвать великана на бой':
            $ game.dragon.drain_energy()
            call lb_fight
            #TODO: Логово великана и великанша.
        'Запомнить место и уйти' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            return     
    return

label lb_enc_lumbermill:
    show expression 'img/bg/special/lumbermill.png' as bg
    'Лесопилка.'
    nvl clear
    python:
        doit = False
        if 'fire_breath' in game.dragon.modifiers(): 
            doit = True
    menu:
        'Дыхнуть огнём' if doit:
            $ game.dragon.drain_energy()
            "Лесопилка сгорает оставив людей без строительных материалов."
            $ game.poverty.value += 1
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
        'Наколдовать синее пламя' if game.dragon.magic() > 0:
            $ game.dragon.drain_energy()
            "Лесопилка сгорает синим пламенем."
            $ game.poverty.value += 1
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
        'Обследовать здание' if game.dragon.size() <= 3 and game.dragon.magic() == 0:
            $ game.dragon.drain_energy()
            "[game.dragon.name] тщательно обследует необычное строение на предмет важности и уязвимых мест. Вращаемое потоком воды колесо приводит в движение скрытые внутри здания пилы, при помощи которых люди изготавливают из брёвен доски. Огромный штабель готовой продукции сложен неподалёку. Если бы только было чем это всё поджечь..."
            'Только время зря потерял. Придётся уйти несолоно хлебавши.'
        'Пройти мимо' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    
    return
    
label lb_enc_klad:
    'Дракон учуял зарытые сокровища.'
    nvl clear
    python:
        tr_lvl = random.randint(1,100)
        count = random.randint(1,10)
        alignment = 'human'
        min_cost = 1*tr_lvl
        max_cost = 10*tr_lvl
        t_list = klad_list
        obtained = "Это предмет из клада, зарытого кем-то в лесу."
        trs = treasures.gen_treas(count, t_list, alignment, min_cost, max_cost, obtained)
        trs_list = game.lair.treasury.treasures_description(trs)
        trs_descrptn = '\n'.join(trs_list)
    menu:
        'Отыскать и раскопать':
            $ game.dragon.drain_energy()
            'Отыскал и раскопал. Внутри клада лежит:'
            '[trs_descrptn]'
            $ game.lair.treasury.receive_treasures(trs)
            
        'Пусть пока лежат'  if game.dragon.bloodiness < 5:
            'Конечно сокровища полезны, но то что тут могли закопать жалкие людишки вряд ли стоит драгоценного времени благородного змея.'

    
    return

label lb_patrool_forest:
    python:
        game.dragon.drain_energy()
        chance = random.randint(0,game.mobilization.level)
        if chance < 4:
            patrool = 'jagger'
            dtxt = 'Егерь.'
        elif chance < 7:
            patrool = 'footman'
            dtxt = 'Пехотинцы.'
        elif chance < 11:
            patrool = 'heavy_infantry'
            dtxt = 'Латники.'
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
