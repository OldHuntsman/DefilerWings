# coding=utf-8
label lb_location_city_main:
    python:
        if not renpy.music.is_playing():
            renpy.music.play(get_random_files('mus/ambient'))        
    $ place = "city_gates"
    hide bg
    show place as bg
    
    if game.dragon.energy() == 0:
        'Даже драконам надо иногда спать. Особенно драконам!'
        return      
        
    'Столица королевства людей.'
    menu:
        'Тайный визит' if game.dragon.mana > 0:
            'Дракон превращается в человека и проходит в город. На это пришлось потратить драгоценную волшебную силу...'
            $ game.dragon.drain_mana()
            nvl clear
            call lb_city_walk
        'Штурморвать ворота' if not game.dragon.can_fly:
            'Заметив приближение опасности бдительные стражники закрывают ворота. Прийдётся порываться с боем...'
            call lb_city_gates
        'Влететь внутрь' if game.dragon.can_fly:
            'Легко перемахнув через городскую стену, [game.dragon.type] оказывается в самом центре города. От летучего врага укрепления не спасут...'
            call lb_city_raze
        'Уйти прочь':
            return
            
    return

label lb_city_gates:
    $ game.dragon.drain_energy()
    $ game.foe = core.Enemy('city', gameRef=game, base_character=NVLCharacter)
    call lb_city_raze
    return

label lb_city_raze:
    'Беззащитный город готов познать ярость отродья Госпожи.'
    nvl clear
    menu:
        'Королевский дворец':
            call lb_city_palace_atk

        'Рыночная площадь':
            call lb_city_market_atk

        'Кафедральный собор':
            call lb_city_cathedral_atk
            
        'Богатые кварталы':
            call lb_city_jew_atk
            
        'Покинуть город':
            return
            
    return

label lb_city_walk:
    show expression 'img/bg/city/inside.png' as bg
    'Загадочный путник проходит мимо бдительной стражи и входит в бурлящий жизнью город.'
    nvl clear

    menu:
        'Королевский дворец':
            call lb_city_palace

        'Рыночная площадь':
            call lb_city_market

        'Кафедральный собор':
            call lb_city_cathedral
            
        'Мастерская ювелира':
            call lb_city_jewler
            
        'Покинуть город':
            return
            
    return

label lb_city_palace:
    'Гордая цитадель возвышается на холме в центре города. Здесь находится зимняя резиденция короля. Изнутри доносятся соблазнительные ароматы драгоценностей и благородных дев. На воротах стоят бдительные гвардейцы.'
    $ game.foe = core.Enemy('palace_guards', gameRef=game, base_character=NVLCharacter)
    $ chances = show_chances(game.foe)
    nvl clear
    menu:
        'Напасть':
            call lb_city_palace_atk
        'Уйти':
            call lb_city_walk
    
    return

label lb_city_palace_atk:
    $ game.dragon.drain_energy()
    $ game.foe = core.Enemy('palace_guards', gameRef=game, base_character=NVLCharacter)
    $ chances = show_chances(game.foe)
    call lb_fight
    'Пока остальные защитники цитадели находятся в замешательстве, у дракона появился отилинчый шанс для грабежа и разбоя.'
    $ game.dragon.reputation.points += 3
    '[game.dragon.reputation.gain_description]'
    menu:
        'Обесчестить благородную девицу':
            $ game.dragon.drain_energy()
            $ description = game.girls_list.new_girl('princess')
            'Дракон ловит благородную девицу'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex     
        'Вороватъ @ убиватъ':
            $ game.dragon.drain_energy()
            python:
                count = random.randint(4, 9)
                alignment = 'knight'
                min_cost = 200
                max_cost = 2000
                obtained = "Это предмет из королевской сокровищницы."
                trs = treasures.gen_treas(count, data.loot['palace'], alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
            'С кровожадным рёвом [game.dragon.fullname] проносится по коридорам дворца убивая всех на своём пути и присваивая каждую понравившуся ему вещь:'
            '[trs_descrptn]'
            $ game.lair.treasury.receive_treasures(trs)
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]'
        'Убежать':
            'Решив не искушать судьбу и использовать поднявшуюся суматоху для безопасного отхода, [game.dragon.type] уходит прочь из города.'
    return

label lb_city_market:
    show expression 'img/bg/city/market.png' as bg
    'Рыночная площадь полна народу. Люди покупают и продают всевозможные ненужные вещи вроде картошки и одежды. Глупые смертные даже не догадываются что прямо здесь стоит их самый жуткий ночной кошмар. Они беззащитны перед внезапной атакой.'
    nvl clear
    menu:
        'Принять истинный облик':
            call lb_city_market_atk
        'Уйти':
            call lb_city_walk

    return

label lb_city_market_atk:
    show expression 'img/bg/city/market.png' as bg
    'Дракон возвращает себе истинную форму. Люди в ужасе разбегаются.'
    nvl clear
    menu:
        'Устроить резню':
            $ game.dragon.drain_energy()
            'Кровь, кишки, распидорасило...'
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]'
        'Схватить девицу':
            $ game.dragon.drain_energy()
            $ description = game.girls_list.new_girl('citizen')
            'Дракон ловит девицу вышедшую за покупками.'
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex     
        'Покинуть площадь':
            call lb_city_walk
    return

label lb_city_cathedral:
    'Огромный готический собор, высится над городом. Кругом нет ни одного здания котором могло бы по вышине сравниться со шпилем соборной колокольни.'
    nvl clear
    menu:
        'Разграбить собор':
            'Загадочный незнакомец входит под своды храма и прямо на глазах у молящихся преображается в чудовище.'
            call lb_city_cathedral_atk

        'Уйти':
            call lb_city_walk
    return

label lb_city_cathedral_atk:
    $ game.dragon.drain_energy()
    python:
        count = random.randint(4, 10)
        alignment = 'cleric'
        min_cost = 10
        max_cost = 500
        obtained = "Это предмет из столичного кафедрального собора."
        trs = treasures.gen_treas(count, data.loot['church'], alignment, min_cost, max_cost, obtained)
        trs_list = game.lair.treasury.treasures_description(trs)
        trs_descrptn = '\n'.join(trs_list)
    'С демоническим хохотом [game.dragon.fullname] врывается в святилище, убивая всех на своём пути и присваивая каждую понравившуся ему вещь:'
    '[trs_descrptn]'
    $ game.lair.treasury.receive_treasures(trs)
    $ game.dragon.reputation.points += 5
    '[game.dragon.reputation.gain_description]'    
    return

label lb_city_jewler:
    'В этом богатом квартале работают самые искустные ремесленники - оружейники, ювелиры и краснодеревщики. Кругом стоит одуряющий запах сокровищ и благородных женщин вышедших за покупками. К сожалению стражи тут тоже много - стоят на каждом углу.'
    $ game.foe = core.Enemy('city_guard', gameRef=game, base_character=NVLCharacter)
    $ chances = show_chances(game.foe)
    nvl clear
    menu:
        'Купить драгоценности':
            $ new_item = game.lair.treasury.craft(**data.craft_options['jeweler_buy'])
            if new_item:
                $ game.lair.treasury.receive_treasures([new_item])
                $ test_description = new_item.description()
                "Куплено: [test_description]."
        'Продать драгоценности':
            menu:
                'Самую дорогую' if len(game.lair.treasury.jewelry) > 0:
                    $ item_index = game.lair.treasury.most_expensive_jewelry_index
                'Самую дешёвую' if len(game.lair.treasury.jewelry) > 0:
                    $ item_index = game.lair.treasury.cheapest_jewelry_index
                'Случайную' if len(game.lair.treasury.jewelry) > 0:
                    $ item_index = random.randint(0, len(game.lair.treasury.jewelry))
                'Отмена':
                    return
            python:
                from pythoncode import treasures
                from treasures import number_conjugation_rus
                description = u"%s.\nПродать украшение за %s?" % (
                    game.lair.treasury.jewelry[item_index].description().capitalize(),
                    treasures.number_conjugation_rus(game.lair.treasury.jewelry[item_index].cost, u"фартинг"))
            menu:
                "[description]"
                'Продать':
                    python:
                        description = u"%s.\nПродано за %s" % (
                            game.lair.treasury.jewelry[item_index].description().capitalize(),
                            treasures.number_conjugation_rus(game.lair.treasury.jewelry[item_index].cost, u"фартинг"))
                        game.lair.treasury.money += game.lair.treasury.jewelry[item_index].cost
                        game.lair.treasury.jewelry.pop(item_index)
                'Оставить':
                    pass
        'Драгоценности на заказ':
            $ new_item = game.lair.treasury.craft(**data.craft_options['jeweler_craft'])
            if new_item:
                $ game.lair.treasury.receive_treasures([new_item])
                $ test_description = new_item.description()
                "Изготовлено: [test_description]."
        'Принять истинный облик':
            call lb_city_jew_atk
        'Вернуться на площадь':
            call lb_city_walk
    
    return


label lb_city_jew_atk:
    $ game.dragon.drain_energy()
    $ game.foe = core.Enemy('city_guard', gameRef=game, base_character=NVLCharacter)
    call lb_fight
    'В ближайшей округе не осталось ни одного живого стражника. Кругом царит паника, люди бегут прочь от дракона спасая самое ценное. [game.dragon.name] оглядывает сцену разрушения и хаоса. Толстый ювелир, тащит тяжелую деревянную шкатулку с драгоценностями. Благнородная девица с визгом убегает прочь. В подвале горящего дома, который вот вот обрушится лежат без присмотра драгоценные слитки и камни.'
    $ game.dragon.reputation.points += 3
    '[game.dragon.reputation.gain_description]'
    menu:
        'Схватить ювелира':
            python:
                count = random.randint(3, 10)
                alignment = 'human'
                min_cost = 10
                max_cost = 500
                obtained = "Это предмет из лавки ювелира."
                trs = treasures.gen_treas(count, data.loot['jeweler'], alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
            'Ограбить неуклюжего ювелира всё равно что отнять конфетку у ребёнка. В шкатулке много интересного:'
            '[trs_descrptn]'
            $ game.lair.treasury.receive_treasures(trs)
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]' 
    
        'Догнать благородную девицу':
            $ game.dragon.drain_energy()
            $ description = game.girls_list.new_girl('princess')
            'Дракон ловит благородную девицу'
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]'
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex     
            
        'Спасти сокровища из горящего дома':
            python:
                count = random.randint(3, 10)
                alignment = 'human'
                min_cost = 10
                max_cost = 1000
                obtained = "Это предмет из лавки ювелира."
                trs = treasures.gen_treas(count, data.loot['raw_material'], alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
            'Действовать надо быстро, пока горящий дом не обрушился и не похоронил под своими обломками ценности:'
            '[trs_descrptn]'
            $ game.lair.treasury.receive_treasures(trs)
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]' 
    
    return
    