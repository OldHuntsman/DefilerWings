# coding=utf-8
label lb_location_road_main:
    $ place = 'road'
    show expression get_place_bg(place) as bg
    nvl clear
    
    if game.dragon.energy() == 0:
        'Даже драконам надо иногда спать. Особенно драконам!'
        return
        
    $ nochance = game.poverty.value * 3
    $ choices = [
        ("lb_enc_tornament", 10),
        ("lb_enc_inn", 10),
        ("lb_enc_peasant_cart", 10),
        ("lb_enc_carriage", 10),
        ("lb_enc_questing_knight", 10),
        ("lb_enc_trader", 10),
        ("lb_enc_caravan", 10),
        ("lb_enc_lcaravan", 10),
        ("lb_enc_outpost", 10),
        ("lb_manor_found", 10),
        ("lb_wooden_fort_found", 10),
        ("lb_abbey_found", 10),
        ("lb_castle_found", 10),
        ("lb_palace_found", 10),
        ("lb_patrool_road", 3 * game.mobilization.level),
        ("lb_enc_noting", nochance)]
    $ enc = core.Game.weighted_random(choices)
    $ renpy.call(enc)
        
    return
    
    
label lb_enc_tornament:
    'Шум вдалеке...'
    show expression 'img/bg/special/tornament.png' as bg
    '...это рыцарский турнир. Победитель готов возложить золотой венец на "королеву любви и красоты".'
    nvl clear
    menu:
        'Вызвать победителя на бой':
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('champion', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            'Увидев что их чемпион повержен, гости турнира в панике разбегаются бросая вещи и вопя от ужаса. [game.dragon.name] не обращает на них внимания, он забирает свой приз - "королеву любви и красоты" и её золотой венец.'
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]'
            $ description = game.girls_list.new_girl('princess')
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex      
        'Не ввязываться' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            'Осторожность не повредит. Если этот рыцарь действительно лучше в округе, он может быть опасен. А девицу и кусок золота можно найти где-нибудь ещё...'
    return
    
label lb_enc_inn:
    show expression 'img/bg/special/tabern.png' as bg    
    'Придорожный трактир.'
    nvl clear
    python:
        doit = False
        if 'fire_breath' in game.dragon.modifiers(): 
            doit = True
    menu:
        'Дыхнуть огнём' if doit:
            $ game.dragon.drain_energy()
            "Трактир сгорает вместе с забаррикадировавшимися внутри людьми."
            $ game.poverty.value += 1
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]'
        'Наколдовать синее пламя' if game.dragon.magic > 0:
            $ game.dragon.drain_energy()
            "Трактир сгорает синим пламенем вместе с забаррикадировавшимися внутри людьми."
            $ game.poverty.value += 1
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]'
        'Потребовать бочку эля':
            show expression 'img/bg/special/fear.png' as bg  
            $ game.dragon.drain_energy()
            "[game.dragon.name] получает от испуганного хозяина трактира целую бочку лучшего эля. После такой выпивки так и тянет на приключения и хорошую закуску!"
            python:
                if game.dragon.bloodiness < 5:
                    game.dragon.bloodiness += 1
                if game.dragon.lust < 3:
                    game.dragon.lust += 1
                if game.dragon.hunger < 3:
                    game.dragon.hunger += 1
        'Пройти мимо' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            
    return
    
label lb_enc_peasant_cart:
    'Телега с сеном.'
    menu:
        'Убить крестьянина' if game.dragon.bloodiness >= 5:
            $ game.dragon.drain_energy()
            'Дав волю своему гневу, [game.dragon.name] переворачивает повозку, убивает лошадь и разрывает крестьянина на куски. У жалкого смертного нет ничего ценного! Да как он посмел встретить дракона если с него и взять нечего?!'
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
        'Сожрать лошадь' if game.dragon.hunger > 0: 
            $ game.dragon.drain_energy()
            'Пока [game.dragon.name] пожирает жилистую крестьянскую лошадку, хозяин повозки в ужасе убегает прочь. Ничего, пусть поведает жалким смертным о вашем величии.'
            $ if game.dragon.bloodiness > 0: game.dragon.bloodiness = 0
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
        'Пропустить' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    return
    
label lb_enc_carriage:
    'Карета благородной дамы с несколькими тяжело-вооруженными конными арбалетчиками в качестве охраны.'
    nvl clear
    menu:
        'Перевернуть карету':
            $ game.foe = core.Enemy('mounted_guard', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            'Внутри благородная дева.'
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]'
            $ description = game.girls_list.new_girl('princess')
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex      
        
        'Пропустить' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()        
    return
    
label lb_enc_questing_knight:
    'Странствующий рыцарь.'
    menu:
        'Вызвать на бой':
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('champion', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            $ game.dragon.reputation.points += 5
            'Рыцарь повержен. [game.dragon.reputation.gain_description]'
            '[game.dragon.name] находит на трупе кое-что ценное:'
            python:
                count = random.randint(1, 5)
                alignment = 'knight'
                min_cost = 10
                max_cost = 100
                obtained = "Это предмет принадлежал когда-то беззвестному странствующему рыцарю."
                trs = treasures.gen_treas(count, data.loot['knight'], alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
            '[trs_descrptn]'
        'Пропустить' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()   
            
    return
    
label lb_enc_trader:
    'Фургон странствующего торговца.'
    menu:
        'Вымогать деньги':
            python:
                game.dragon.drain_energy()
                passing_tool = random.randint(10, 200)
                slvr_trs = [treasures.Coin('taller', passing_tool)]
                game.lair.treasury.receive_treasures(slvr_trs)
            'Торговец с облегчением отдаёт дракону несколько серебрянных таллеров, чтобы тот его не трогал и пропустил фургон.'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
        'Убить и ограбить' if game.dragon.bloodiness >= 5:
            python:
                game.dragon.drain_energy()
                gold_trs = [treasures.Coin('farting', 100), treasures.Coin('taller', 10)]
                game.lair.treasury.receive_treasures([gold_trs])
            'Дав волю своему гневу, [game.dragon.name] переворачивает фургон, убивает лошадь и разрывает торговца на куски. Его товары особого интереса не представляют, зато в кошельке находятся кое какие деньги:'
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
        'Пропустить' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            
    return
    
label lb_enc_caravan:
    'Торговый караван под охраной взвода наемных конных арбалетчиков.'
    menu:
        'Вымогать деньги' if game.dragon.fear > 3:
            python:
                game.dragon.drain_energy()
                passing_tool = random.randint(1, 20)
                gold_trs = treasures.Coin('dublon', passing_tool)
                game.lair.treasury.receive_treasures([gold_trs])
            'Караванщик с ворчанием отдаёт дракону несколько золотых дублонов, чтобы тот не трогал повозки и пропустил из дальше.'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
        'Разграбить корован':
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('xbow_rider', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            'Дав волю своему гневу, [game.dragon.name] переворачивает фургон, убивает лошадь и разрывает караванщика на куски. Его товары особого интереса не представляют, зато в кошельке находятся кое какие деньги:'
            python:
                count = random.randint(5, 15)
                alignment = 'human'
                min_cost = 1
                max_cost = 1000
                obtained = "Просто монеты."
                trs = treasures.gen_treas(count, ['taller', 'dublon'], alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
                game.lair.treasury.receive_treasures(trs)
            '[trs_descrptn]'
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
        'Пропустить' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()    
    return
   
label lb_enc_lcaravan:
    'Большой караван с тяжело вооруженной охраной.'
    menu:
        'Вымогать деньги' if game.dragon.fear > 6:
            python:
                game.dragon.drain_energy()
                passing_tool = random.randint(20, 100)
                gold_trs = treasures.Coin('dublon', passing_tool)
                game.lair.treasury.receive_treasures([gold_trs])
            'Караванщик с ворчанием отдаёт дракону увесистый кошель с золотыми дублонами, чтобы тот не трогал повозки и пропустил из дальше.'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
        'Разграбить корован':
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('mounted_guard', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            'Перебив охрану и караванщиков, [game.dragon.name] отыскивает в разбитых телегах всё ценное. В основном тут разные не нужные уважающему себя дракону товары - ткани, специи, оливковое масло и тому подобное, но у купцов и наемников есть в кошельках звонкие монеты:'
            python:
                count = random.randint(5, 15)
                alignment = 'human'
                min_cost = 1
                max_cost = 1000
                obtained = "Просто монеты."
                trs = treasures.gen_treas(count, ['taller', 'dublon'], alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
                game.lair.treasury.receive_treasures(trs)
            '[trs_descrptn]'
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
        'Пропустить' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()        
    return
    
label lb_enc_outpost:
    'Застава на дороге.'
    nvl clear
    menu:
        'Напасть на заставу':
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('footman', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            'Большинство стражников мертво, остальные бежали в ужасе, однако здание заставы всё ещё стоит у дороги и восстановить её работу будет не так уж сложно. Зато внутри находится сундук с собранными за последнее время торговыми пошлинами. Внутри приятно звенят монеты:'
            python:
                game.dragon.drain_energy()
                passing_tool = random.randint(50, 250)
                slvr_trs = treasures.Coin('taller', passing_tool)
                game.narrator(slvr_trs.description() + '.')
                game.lair.treasury.receive_treasures([slvr_trs])
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]'
            python:
                doit = False
                if 'fire_breath' in game.dragon.modifiers(): 
                    doit = True
            menu:
                'Развалить укрепления' if game.dragon.size() > 3:
                    $ game.dragon.drain_energy()
                    "Я твой застава щаталь!"
                    $ if game.mobilization.level >= 1: game.mobilization.level -= 1
                    '[game.dragon.reputation.gain_description]'
                'Дыхнуть огнём' if doit:
                    $ game.dragon.drain_energy()
                    "Амбар сгорает."
                    $ if game.mobilization.level >= 1: game.mobilization.level -= 1
                    '[game.dragon.reputation.gain_description]'
                'Наложить проклятье' if game.dragon.mana > 0:
                    $ game.dragon.drain_energy()
                    "Аутпост проклят."
                    $ if game.mobilization.level >= 1: game.mobilization.level -= 1
                    '[game.dragon.reputation.gain_description]'
                'Обследовать укрепления' if game.dragon.size() <= 3 and game.dragon.mana == 0 and not doit:
                    $ game.dragon.drain_energy()
                    "[game.dragon.name] тщательно обследует необычное строение на предмет важности и уязвимых мест. Укрепления, хорть и деревянные, но построены на славу. Сломать получается только хлипкие загородки которыми перекрывают дорогу, но их несложно сднелать заново. Чтобы сравнять заставу с землёй нужно использовать огонь или быть намного крупнее."
                    'Только время зря потерял. Придётся уйти несолоно хлебавши.'
                'Оставить заставу в целости':
                    $ pass
            
        'Аккуратно обойти заставу' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            'Там конечно можно было бы поживиться собранными с купцов пошлинами, но где деньги там и охрана. Связываться сейчас с королевскими латниками особого смысла нет, лучше поискать добычу попроще или хотя бы побогаче.'
        
    return
    
label lb_patrool_road:
    python:
        game.dragon.drain_energy()
        chance = random.randint(0, game.mobilization.level)
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