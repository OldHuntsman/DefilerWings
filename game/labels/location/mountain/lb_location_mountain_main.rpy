# coding=utf-8
label lb_location_mountain_main:
    python:
        if not renpy.music.is_playing():
            renpy.music.play(get_random_files('mus/ambient'))    
    $ place = 'mountain'
    hide bg
    show expression get_place_bg(place) as bg
    nvl clear
    
    if game.dragon.energy() == 0:
        'Даже драконам надо иногда спать. Особенно драконам!'
        return
        
    $ nochance = game.poverty.value * 3
    $ choices = [
        ("lb_enc_miner", 10),
        ("lb_enc_dklad", 10),
        ("lb_enc_mines_silver", 10),
        ("lb_enc_mines_gold", 5),
        ("lb_enc_mines_mithril", 3),
        ("lb_enc_mines_adamantine", 2),
        ("lb_enc_mines_gem_low", 15),
        ("lb_enc_mines_gem_high", 5),
        ("lb_enc_ram", 10),
        ("lb_enc_bear", 10),
        ("lb_jotun_found", 10),
        ("lb_ifrit_found", 10),
        ("lb_enc_smugglers", 10),
        ("lb_enc_slavers", 10),
        ("lb_enc_frontgates_found", 10),
        ("lb_enc_cannontower", 10),
        ("lb_patrool_mountain", 3 * game.mobilization.level),
        ("lb_enc_noting", nochance)]
    $ enc = core.Game.weighted_random(choices)
    $ renpy.call(enc)
        
    return
    
    
label lb_enc_miner:
    'Ветерок доносит едва заметный запах золота. Аромат приводит дракона к горному ручью. На берегу сидит человек с лотком, старательно просеивающий речной песок в поисках крупинок золота.'
    nvl clear
    menu:
        'Убить и ограбить':
            'В мешке златоискателя обнаруживается почти фунт золотого песка и мелких самородков. Спасибо за работу, смертный.'
            python:
                gold_trs = treasures.Ingot('gold')
                gold_trs.weight = 1
                game.lair.treasury.receive_treasures([gold_trs])
                game.dragon.drain_energy()
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            
        'Пусть идёт' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            return
    return
    
label lb_enc_dklad:
    'Чуткий нюх дракона подсказывает, что где то неподалёку лежат сокровища. Странно. Место тут дикое. Видимо кто-то решил спрятать здесь клад. Как это мило с его стороны...'
    nvl clear
    python:
        tr_lvl = random.randint(1, 100)
        count = random.randint(1, 10)
        alignment = 'human'
        min_cost = 1 * tr_lvl
        max_cost = 10 * tr_lvl
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
                        
        'Пусть пока лежат' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            'Конечно сокровища полезны, но то что тут могли спрятать жалкие смертные вряд ли стоит драгоценного времени благородного змея.'    
    return

    
label lb_enc_ram:
    'По скалам скачет здоровенный винторогий баран. Ничего, от дракона не ускачет. Закуска не выдающаяся, но питательная.'
    nvl clear
    menu:
        'Сожрать барана' if game.dragon.hunger > 0:
            $ game.dragon.drain_energy()
            $ game.dragon.hunger -= 1
            '[game.dragon.name] ловит и пожирает барана.'
            python:
                if game.dragon.bloodiness > 0:
                    game.dragon.bloodiness = 0
        'Разорвать барана' if game.dragon.bloodiness >= 5 and game.dragon.hunger == 0:
            $ game.dragon.drain_energy()
            '[game.dragon.name] жестоко задирает барана просто ради забавы.'    
        'Просто шугануть' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    return
    
label lb_enc_bear:
    'В склоне горы обнаруживается вход в пещеру. Какой же дракон не сунет нос в пещеру? Но пещеры как оказалось представляют интерес не только для драконов. Вот эту например облюбовал огромный пещерный медведь. Опасный противник, однако его жесткое мясо обладает действием укрепляющим организм.'
    nvl clear
    menu:
        'Сразиться с медведем':
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('bear', game_ref=game)
            call lb_fight from _call_lb_fight_56
            if game.dragon.hunger > 0:
                'Мясо пещерного медведя богато полезными минералами и витаминами, хорошо влияющими на чешую. Может быть это и не очень вкусно, зато плезно. Благодаря такому обеду защита от вражеского оружия будет немного выше.'
                python:
                    if game.dragon.bloodiness > 0:
                        game.dragon.bloodiness = 0
                    game.dragon.hunger -= 1
                    game.dragon.add_effect('bear_meat')
            else:
                'Дракон торжествует победу, однако есть уже совсем не хочется. Живот и так раздут как барабан. А жаль, такое редкое мясо могло бы придать дракону много здоровья и сил.'
                
        'Отступить' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    
    return
    
label lb_enc_smugglers:
    'На горном перевале [game.dragon.name] натыкается на караван контрабандистов. Они вооружены но вероятно предпочтут откупиться чтобы не вступать в бой. Конечно если цена прохода будет разумной...'
    $ game.foe = core.Enemy('band', game_ref=game)
    $ chances = show_chances(game.foe)
    menu:
        'Вымогать деньги':
            python:
                game.dragon.drain_energy()
                passing_tool = game.dragon.fear * 2 + 1 
                gold_trs = treasures.Coin('taller', passing_tool)
                game.lair.treasury.receive_treasures([gold_trs])
            'Контрабандисты скидываются по таллеру и отдают [passing_tool] чтобы откупиться и пройти мирно. С паршивой овцы хоть шерсти клок...'
            
        'Отнять весь товар':
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_57
            python:
                count = random.randint(5, 15)
                alignment = 'human'
                min_cost = 5
                max_cost = 100
                obtained = "Это часть груза контрабандистов, которых дракон ограбил на тайном перевале в северных горах."
                trs = treasures.gen_treas(count, data.loot['smuggler'], alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
                game.lair.treasury.receive_treasures(trs)
                
            'Обыскав тюки контрабандистов [game.dragon.name] находит кое-какие ценные вещи:'
            '[trs_descrptn]'
            
        'Отпустить их с миром' if game.dragon.bloodiness < 5:    
            'Пусть налаживают торговлю, чем богаче станет страна тем больше можно будет нажиться ограбляя её!'
            $ game.dragon.gain_rage()
    
    return
    
label lb_enc_slavers:
    'На высокогорном перевале [game.dragon.name] подкарауливает караван разбойников-работорговцев. Они ведут несколько рабов на веревке, среди рабынь есть одна невинная девушка. Разбойнии вооружены не слишком то хорошо и скорее предпочтут отдать одного бесполезного раба чем сражаться.'
    $ game.foe = core.Enemy('band', game_ref=game)
    $ chances = show_chances(game.foe)
    menu:
        'Потребовать бесполезного раба' if game.dragon.hunger > 0:
            'Для работорговцев это не слишком большая потеря - они соглашаются отдать самого заморенного раба, чтобы [game.dragon.name] пропустил их без боя. Они даже жалеают дракону приятного аппетита.'
            $ game.dragon.drain_energy()
            'Дракон пожирает измождённого раба. Не самая лучшая закуска на свете, но голод не тётка...'
            python:
                if game.dragon.bloodiness > 0:
                    game.dragon.bloodiness = 0
                game.dragon.hunger -= 1
        
        'Потребовать невинную девушку' if game.dragon.lust > 0:
            $ game.dragon.drain_energy()
            'Среди всех рабов, юная красавица самая ценная. Похоже чтобы получить её придётся разогнать охрану, так просто работорговцы её не отдадут...'
            call lb_fight from _call_lb_fight_58
            'Дракон получает девушку.'
            $ description = game.girls_list.new_girl('citizen')
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex from _call_lb_nature_sex_24    
        
        'Перебить караван':
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('band', game_ref=game)
            call lb_fight from _call_lb_fight_59
        
        'Отпустить их с миром' if game.dragon.bloodiness < 5:
            'Пусть налаживают торговлю, чем богаче станет страна тем больше можно будет нажиться ограбляя её!'        
            $ game.dragon.gain_rage()
    
    return

label lb_enc_mines_silver:
    'Серебрянный рудник. Охраняется небольшим отрядом арабалетчиков.'
    $ game.foe = core.Enemy('xbow', game_ref=game)
    $ narrator(show_chances(game.foe))
    menu:
        'Вымогать серебро' if game.dragon.fear > 3:
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
            call lb_fight from _call_lb_fight_60
            python:
                count = random.randint(5, 20)
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

label lb_enc_mines_gold:
    'Золотой прииск. Охраняется небольшим отрядом тяжелой панцирной пехоты.'
    $ game.foe = core.Enemy('heavy_infantry', game_ref=game)
    $ narrator(show_chances(game.foe))
    menu:
        'Вымогать серебро' if game.dragon.fear > 5:
            $ game.dragon.drain_energy()
            'Начальник прииска отдаёт золотой слиток, чтобы избежать конфликта.'
            python:
                gold_trs = treasures.Ingot('gold')
                gold_trs.weight = 8
                game.lair.treasury.receive_treasures([gold_trs])
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
            
        'Ограбить рудник':
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_61
            python:
                count = random.randint(3, 15)
                alignment = 'human'
                min_cost = 1
                max_cost = 1000000
                t_list = ['gold']
                obtained = "Просто металл."
                trs = treasures.gen_treas(count, t_list, alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
                game.lair.treasury.receive_treasures(trs)
            'На складе дракон находит драгоценный металл, выплавленный и готовый к отправке в казну:'
            '[trs_descrptn]'
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]'
            
        'Пройти мимо' if game.dragon.bloodiness < 5:
            'Человеческое золото не стоит того чтобы получить в глаз их железо!'       
            $ game.dragon.gain_rage()
    return

label lb_enc_mines_mithril:
    'Рудник цвергов, здесь они добывают драгоценный мифрил. Вход в шахту надёжно охраняется.'
    $ game.foe = core.Enemy('dwarf_guards', game_ref=game)
    $ narrator(show_chances(game.foe))
    menu:
        'Вымогать серебро' if game.dragon.fear > 7:
            $ game.dragon.drain_energy()
            'Главый цверг отдаёт небольшой слиток мифрила, чтобы избежать конфликта.'
            python:
                gold_trs = treasures.Ingot('mithril')
                gold_trs.weight = 4
                game.lair.treasury.receive_treasures([gold_trs])
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            
        'Ограбить рудник':
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_62
            python:
                count = random.randint(2, 10)
                alignment = 'human'
                min_cost = 1
                max_cost = 1000000
                t_list = ['mithril']
                obtained = "Просто металл."
                trs = treasures.gen_treas(count, t_list, alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
                game.lair.treasury.receive_treasures(trs)
            'На складе дракон находит драгоценный металл, выплавленный и готовый к продаже альвам:'
            '[trs_descrptn]'
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
            
        'Пройти мимо' if game.dragon.bloodiness < 5:
            'Мифрил цвергов не стоит того чтобы получить в глаз их сталь!'       
            $ game.dragon.gain_rage()
    return

label lb_enc_mines_adamantine:
    'Рудник цвергов, здесь они добывают и выплавляют драгоценный адамант. На страже стоит практически неуязвимый стальной голем.'
    $ game.foe = core.Enemy('golem', game_ref=game)
    $ narrator(show_chances(game.foe))
    menu:
        'Вымогать серебро' if game.dragon.fear > 8:
            $ game.dragon.drain_energy()
            'Главый цверг отдаёт небольшой слиток адаманта, чтобы избежать конфликта.'
            python:
                gold_trs = treasures.Ingot('adamantine')
                gold_trs.weight = 4
                game.lair.treasury.receive_treasures([gold_trs])
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            
        'Ограбить рудник':
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_63
            python:
                count = random.randint(1, 5)
                alignment = 'human'
                min_cost = 1
                max_cost = 1000000
                t_list = ['adamantine']
                obtained = "Просто металл."
                trs = treasures.gen_treas(count, t_list, alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
                game.lair.treasury.receive_treasures(trs)
            'На складе дракон находит драгоценный металл, выплавленный и готовый к продаже альвам:'
            '[trs_descrptn]'
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
            
        'Пройти мимо' if game.dragon.bloodiness < 5:
            'Адамант цвергов не стоит того чтобы получить в глаз их сталь!'       
            $ game.dragon.gain_rage()
    return


label lb_enc_mines_gem_low:
    'На сколне гор виден вход в шахту. Судя по запаху тут добывают полудрагоценные камни. Прииск охраняется небольшим отрядом арабалетчиков.'
    $ game.foe = core.Enemy('xbow', game_ref=game)
    $ narrator(show_chances(game.foe))
    menu:
        'Вымогать камушки' if game.dragon.fear > 2:
            $ game.dragon.drain_energy()
            'Начальник рудника отдаёт кое-что чтобы задобрить дракона:'
            python:
                count = 1
                alignment = 'human'
                min_cost = 1
                max_cost = 1000000
                t_list = ['jasper', 'turquoise', 'jade', 'malachite', 'corall', 'agate', 'amber', 'crystall', 'beryll', 'tigereye', 'granate', 'turmaline', 'aqua']
                obtained = "Просто самоцветы."
                trs = treasures.gen_treas(count, t_list, alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
                game.lair.treasury.receive_treasures(trs)
            '[trs_descrptn]'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            
        'Ограбить шахту':
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_64
            python:
                count = random.randint(5, 20)
                alignment = 'human'
                min_cost = 1
                max_cost = 1000000
                t_list = ['jasper', 'turquoise', 'jade', 'malachite', 'corall', 'agate', 'amber', 'crystall', 'beryll', 'tigereye', 'granate', 'turmaline', 'aqua']
                obtained = "Просто самоцветы."
                trs = treasures.gen_treas(count, t_list, alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
                game.lair.treasury.receive_treasures(trs)
            'На складе дракон полудрагоценные камни самых разных форм, цветов и размеров:'
            '[trs_descrptn]'
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
            
        'Пройти мимо' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    return

label lb_enc_mines_gem_high:
    'На сколне гор виден вход в шахту. Судя по запаху тут добывают самоцветы, причём очень высокого качества. Аж слюнки текут. Но вход охраняет отряд тяжёлой панцирной пехоты.'
    $ game.foe = core.Enemy('heavy_infantry', game_ref=game)
    $ narrator(show_chances(game.foe))
    menu:
        'Вымогать камушки' if game.dragon.fear > 5:
            $ game.dragon.drain_energy()
            'Начальник рудника отдаёт кое-что чтобы задобрить дракона:'
            python:
                count = 1
                alignment = 'human'
                min_cost = 1
                max_cost = 1000000
                t_list = ['elven_beryll', 'topaz', 'saphire', 'ruby', 'emerald', 'goodruby', 'goodemerald', 'star', 'diamond', 'black_diamond', 'rose_diamond']
                obtained = "Просто самоцветы."
                trs = treasures.gen_treas(count, t_list, alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
                game.lair.treasury.receive_treasures(trs)
            '[trs_descrptn]'
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
            
        'Ограбить шахту':
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_65
            python:
                count = random.randint(3, 10)
                alignment = 'human'
                min_cost = 1
                max_cost = 1000000
                t_list = ['elven_beryll', 'topaz', 'saphire', 'ruby', 'emerald', 'goodruby', 'goodemerald', 'star', 'diamond', 'black_diamond', 'rose_diamond']
                obtained = "Просто самоцветы."
                trs = treasures.gen_treas(count, t_list, alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
                game.lair.treasury.receive_treasures(trs)
            'На складе дракон полудрагоценные камни самых разных форм, цветов и размеров:'
            '[trs_descrptn]'
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]'
            
        'Пройти мимо' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    return
        
label lb_enc_frontgates_found:
    'Блуждая среди горных круч, [game.dragon.fullname] наткнулся на...'
    show expression 'img/bg/special/gates_dwarf.jpg' as bg
    'Врата в Подгорное Царство!'
    $ game.dragon.add_special_place('frontgates', 'frontgates_guarded')
    call lb_frontgates from _call_lb_frontgates    
    return
    
label lb_enc_cannontower:
    'На склоне горы, словно вырастая прямо из каменной кручи угнездилось небольшой но мощный бастион. Судя по запаху внутри полно цвергов и их механизмов.'
    menu:
        'Подобраться и заглянуть в бойницу':
            'В прорезь бойницы видны суетящиеся цверги. Они готовят ПУШКУ... зачем?'
            show expression 'img/scene/fight/steamgun.jpg' as bg
            'А! Они будут стрелять!'
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('steamgun', game_ref=game)
            call lb_fight from _call_lb_fight_66
            'Внутри бастиона нет никаких сокровищ, только железо, провиант и бумаги. В глубине был проход в подгорное цраство, но едва поняв что проигрывают бой, цверги взорвали заряд пороха который обрушил тоннель завалив его сотянми тонн камней. Через завал никому не пробораться.'
            menu:
                'Расшифровать архивы':
                    'Основная часть бумаг это разнообразные технические чертежи а так же накладные на боеприпасы и провиант. Но помимо прочего есть тут и весьма занимательные архитектурные планы. Согласно этим данным, помимо очень сильно укреплённых главных ворот и пушечных бастионов, в подгорное царство есть ещё один почти не охраняемый но замаскированный "задний проход". При случае можно будет его "раздраконить"...'
                    $ game.dragon.add_special_place('backdor', 'backdor_open')
                'Уйти прочь':
                    $ game.dragon.gain_rage()
                            
        'Убраться отсюда поскорее' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            
    return
    
label lb_patrool_mountain:
    python:
        game.dragon.drain_energy()
        chance = random.randint(0, game.mobilization.level)
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
    python:
        game.foe = core.Enemy(patrool, game_ref=game)
        battle_status = battle.check_fear(game.dragon, game.foe)
    if 'foe_fear' in battle.check_fear(game.dragon, game.foe):
        $ narrator(game.foe.battle_description(battle_status, game.dragon))
        return
    $ game.dragon.drain_energy()
    call lb_fight(skip_fear=True) from _call_lb_fight_67
    return
