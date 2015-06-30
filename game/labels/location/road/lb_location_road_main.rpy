# coding=utf-8
label lb_location_road_main:
    python:
        if not renpy.music.is_playing():
            renpy.music.play(get_random_files('mus/ambient'))    
    $ place = 'road'
    hide bg
    show expression get_place_bg(place) as bg
    nvl clear
    
    if game.dragon.energy() == 0:
        'Даже драконам надо иногда спать. Особенно драконам!'
        return
        
    $ nochance = game.poverty.value * 3
    $ choices = [
        ("lb_enc_tornament", 5),
        ("lb_enc_inn", 15),
        ("lb_enc_peasant_cart", 15),
        ("lb_enc_carriage", 5),
        ("lb_enc_questing_knight", 10),
        ("lb_enc_trader", 10),
        ("lb_enc_caravan", 7),
        ("lb_enc_lcaravan", 3),
        ("lb_enc_outpost", 10),
        ("lb_manor_found", 15),
        ("lb_wooden_fort_found", 10),
        ("lb_abbey_found", 7),
        ("lb_castle_found", 5),
        ("lb_palace_found", 3),
        ("lb_patrool_road", 3 * game.mobilization.level),
        ("lb_enc_noting", nochance)]
    $ enc = core.Game.weighted_random(choices)
    $ renpy.call(enc)
        
    return
    
    
label lb_enc_tornament:
    'Шум вдалеке...'
    show expression 'img/bg/special/tornament.jpg' as bg
    '...это рыцарский турнир. Победитель готов возложить золотой венец на "королеву любви и красоты".'
    $ game.foe = core.Enemy('champion', game_ref=game)
    $ chances = show_chances(game.foe)
    nvl clear
    menu:
        'Вызвать победителя на бой':
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_13
            'Увидев что их чемпион повержен, гости турнира в панике разбегаются бросая вещи и вопя от ужаса. [game.dragon.name] не обращает на них внимания, он забирает свой приз - "королеву любви и красоты" и её золотой венец.'
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]'
            $ description = game.girls_list.new_girl('princess')
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex from _call_lb_nature_sex_10      
        'Не ввязываться' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            'Осторожность не повредит. Если этот рыцарь действительно лучше в округе, он может быть опасен. А девицу и кусок золота можно найти где-нибудь ещё...'
    return
    
label lb_enc_inn:
    show expression 'img/bg/special/tabern.jpg' as bg    
    'На оживлённом торговом перекрёстке стоит двухэтажный трактир. При виде дракона безоружные люди в ужасе забегают в здание и баррикадируют двери и окна.'
    nvl clear
    python:
        doit = False
        if 'fire_breath' in game.dragon.modifiers(): 
            doit = True
    menu:
        'Дыхнуть огнём' if doit:
            $ game.dragon.drain_energy()
            "Испольщуя своё огненное дыхание, [game.dragon.name] пожигает здание с четырёх разных сторон. Деревянный трактир сгорает стремительно, погребая под пылающими обломками людей забаррикадировавшихся внутри."
            $ game.poverty.value += 1
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]'
        'Наколдовать ядовитый туман' if game.dragon.magic > 0:
            $ game.dragon.drain_energy()
            "[game.dragon.name] призывает тёмную магию, чтобы заполнить помещения где заперлись испуганные люди ядовитым туманом. Трактир остаётся невредимым, но внутри все мертвы."
            $ game.poverty.value += 1
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]'
        'Потребовать бочку эля':
            show expression 'img/bg/special/fear.jpg' as bg  
            $ game.dragon.drain_energy()
            "[game.dragon.name] получает от испуганного хозяина трактира целую бочку лучшего эля. После такой выпивки так и тянет на женщин и хорошую закуску!"
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
    'По дороге медленно едет крестьянская телега гружёная сеном. Такие повозки тут встречаются часто и все как одна совершенно бесполезны, даже лошать и на вид такая жилистая и заморенная что не вызываетни особого аппетита. Аж злость берёт.'
    menu:
        'Убить крестьянина' if game.dragon.bloodiness >= 5:
            $ game.dragon.drain_energy()
            'Дав волю своему гневу, [game.dragon.kind] переворачивает повозку, убивает лошадь и разрывает крестьянина на куски. У жалкого смертного нет ничего ценного! Да как он посмел встретить дракона если с него и взять нечего?!'
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
        'Сожрать лошадь' if game.dragon.hunger > 0: 
            $ game.dragon.drain_energy()
            'Пока [game.dragon.name] пожирает жилистую крестьянскую лошадку, хозяин повозки в ужасе убегает прочь. Ничего, пусть поведает жалким смертным о вашем величии.'
            python:
                if game.dragon.bloodiness > 0:
                    game.dragon.bloodiness = 0
                game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
        'Пропустить' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    return
    
label lb_enc_carriage:
    'На дороге пыль стоит столбом, это едет карета благородной дамы с тяжело-вооруженными конными арбалетчиками в качестве охраны. Добрая добыча, хотя и не самая простая...'
    $ game.foe = core.Enemy('mounted_guard', game_ref=game)
    $ chances = show_chances(game.foe)
    nvl clear
    menu:
        'Атаковать кортеж':
            call lb_fight from _call_lb_fight_14
            'Теперь когда охрана не представляет угрозы, можно заглянуть внутрь кареты. Разодрав её кузов словно шуршащую подарочную упаковку, [game.dragon.name] обнаруживает внутри трёх женщин - очевидно мать, дочь и служанку. Старухи не представляют никаого интереса, а вот с девицей можно отлично развлечься!'
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]'
            $ description = game.girls_list.new_girl('princess')
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex from _call_lb_nature_sex_11      
        
        'Пропустить' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()        
    return
    
label lb_enc_questing_knight:
    'По дороге едет облачённый в броню всадник, в сопровождении оседлавшего ослика слуги. Странствующему рыцарю просто грех не вызвать на поединок дракона, только вот сможет ли он пережить такой бой чтобы рассказать о нём?'
    $ game.foe = core.Enemy('champion', game_ref=game)
    $ chances = show_chances(game.foe)
    menu:
        'Принять вызов':
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_15
            $ game.dragon.reputation.points += 5
            'Рыцарь повержен. [game.dragon.reputation.gain_description]'
            '[game.dragon.name] находит на трупе кое-что ценное:'
            python:
                count = random.randint(1, 5)
                alignment = 'knight'
                min_cost = 10
                max_cost = 250
                obtained = "Это предмет принадлежал когда-то беззвестному странствующему рыцарю."
                trs = treasures.gen_treas(count, data.loot['knight'], alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                game.lair.treasury.receive_treasures(trs)                
                trs_descrptn = '\n'.join(trs_list)
            '[trs_descrptn]'
        'Пропустить' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()   
            
    return
    
label lb_enc_trader:
    'На дороге показывается большой крытый фургон, расписанный красочными рекламными надписями. Это какой-то странствующий торговец, не слишком преуспевающий но судя по запаху кое-какое серебро у него в кармана водится. Надо бы облегчить его ношу.'
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
                game.lair.treasury.receive_treasures(gold_trs)
            'Дав волю своему гневу, [game.dragon.name] переворачивает фургон, убивает лошадь и разрывает торговца на куски. Его товары особого интереса не представляют, зато в кошельке находятся кое какие деньги:'
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
        'Пропустить' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    return
    
label lb_enc_caravan:
    '[game.dragon.name] натыкается на торговый караван, сулящий неплохую добычу. К сожалению торговцы не стали экономить на охране - их сопровождает взвод конных арбалетчиков.'
    $ game.foe = core.Enemy('xbow_rider', game_ref=game)
    $ chances = show_chances(game.foe)
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
            call lb_fight from _call_lb_fight_16
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
    '[game.dragon.name] решает подойти к вопросу обстоятельно и залегает в засаду в укрытой кустами придорожной канаве. Полдня ожидания наконецт-то приносят достойную награду - на дороге появляется богатый купеческий караван. Судя по качеству и количеству охраны, эти торговцы платят золотом.'
    $ game.foe = core.Enemy('mounted_guard', game_ref=game)
    $ chances = show_chances(game.foe)
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
            call lb_fight from _call_lb_fight_17
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
    'Для поддержания порядка и сбора пошлин на дорогах королевства устроено множество застав. Гарнизон составляют обычные пехотинцы, сержант, повар и писарь. Зато внутри хранится касса с дорожными сборами за день!'
    $ game.foe = core.Enemy('footman', game_ref=game)
    nvl clear
    menu:
        'Напасть на заставу':
            $ game.dragon.drain_energy()
            $ chances = show_chances(game.foe)
            call lb_fight from _call_lb_fight_18
            'Большинство стражников мертво, остальные бежали в ужасе, однако здание заставы всё ещё стоит у дороги и восстановить её работу будет не так уж сложно. Зато внутри находится сундук с собранными за последнее время торговыми пошлинами. Внутри приятно звенят монеты:'
            python:
                game.dragon.drain_energy()
                passing_tool = random.randint(10, 50)
                slvr_trs = treasures.Coin('taller', passing_tool)
                game.narrator(slvr_trs.description() + '.')
                game.lair.treasury.receive_treasures([slvr_trs])
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]'
  
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
            dtxt = 'Вдоль просёлочной дороги прохаживается бородач с длинным луком, это стрелок местного шерифа отправленный в дозор чтобы проверять подозрительных людей на дороге. Хватит ли ему смелости сразиться?'
        elif chance < 7:
            patrool = 'xbow_rider'
            dtxt = 'Торговый тракт патрулирует отряд лёгкой кавалерии. Они готовы быстро отреагировать на любую угрозу будь то разбойники, монстры или даже дракон.'
        elif chance < 11:
            patrool = 'heavy_cavalry'
            dtxt = 'Дракон нарывается на отряд тяжелой кавалерии. Раз уж в дорожные патрули стали посылать рыцарей, люди видимо запуганы в край.'
        elif chance < 16:
            patrool = 'griffin_rider'
            dtxt = 'Пронзительный кличь раздаётся с небес - это всадник на грифоне пикирует с высоты, завидев у дороги блеск драконьей чешуи.'
        else:
            patrool = 'angel'
            dtxt = '%s вынужден зажмуриться от яркого света бьющего в глаза. Громогласный оклик возвещает: "Умри мерзкое порождение греха!!!". Это ангел-хранитель посланный людям Небесами для защиты.' % game.dragon.name
    '[dtxt]'
    python:
        game.foe = core.Enemy(patrool, game_ref=game)
        battle_status = battle.check_fear(game.dragon, game.foe)
    if 'foe_fear' in battle.check_fear(game.dragon, game.foe):
        $ narrator(game.foe.battle_description(battle_status, game.dragon))
        return
    $ game.dragon.drain_energy()
    call lb_fight(skip_fear=True) from _call_lb_fight_19
    return
