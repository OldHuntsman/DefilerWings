# coding=utf-8
label lb_location_city_main:
        
    $ place = "city_gates"
    show place as bg
    
    if game.dragon.energy() == 0:
        dragon 'Даже драконам надо иногда спать. Особенно драконам!'
        return      
        
    'Столица королевства людей.'
    menu:
        'Тайный визит' if game.dragon.mana > 0:
            'Дракон превращается в человека и проходит в город.'
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
            # TODO: Разграбление для богатого квартала.
            'Плейсхолдер'
            call lb_city_walk
            
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
    nvl clear
    $ game.foe = core.Enemy('heavy_infantry', gameRef=game, base_character=NVLCharacter)
    $ narrator(show_chances(game.foe))
    menu:
        'Напасть':
            call lb_city_palace_atk
        'Уйти':
            call lb_city_walk
    
    return

label lb_city_palace_atk:
    $ game.dragon.drain_energy()
    $ game.foe = core.Enemy('heavy_infantry', gameRef=game, base_character=NVLCharacter)
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
        'Воровать и убивать':
            $ game.dragon.drain_energy()
            python:
                count = random.randint(5, 15)
                alignment = 'knight'
                min_cost = 100
                max_cost = 1000
                obtained = "Это предмет из королевской сокровищницы."
                trs = treasures.gen_treas(count, data.loot['palace'], alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
            'С демоническим хохотом [game.dragon.fullname] проносится по коридорам дворца убивая всех на своём пути и присваивая каждую понравившуся ему вещь:'
            '[trs_descrptn]'
            $ game.lair.treasury.receive_treasures(trs)
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]'
        'Убежать':
            'Решив не искушать судьбу и использовать поднявшуюся суматоху для безопасного отхода, [game.dragon.type] уходит прочь из города.'
    return

label lb_city_market:
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
        count = random.randint(3, 10)
        alignment = 'cleric'
        min_cost = 10
        max_cost = 1000
        obtained = "Это предмет из столичного кафедрального собора."
        trs = treasures.gen_treas(count, data.loot['church'], alignment, min_cost, max_cost, obtained)
        trs_list = game.lair.treasury.treasures_description(trs)
        trs_descrptn = '\n'.join(trs_list)
    'С демоническим хохотом [game.dragon.fullname] проносится по коридорам дворца убивая всех на своём пути и присваивая каждую понравившуся ему вещь:'
    '[trs_descrptn]'
    $ game.lair.treasury.receive_treasures(trs)
    $ game.dragon.reputation.points += 5
    '[game.dragon.reputation.gain_description]'    
    return

label lb_city_jewler:
    'Мастерская ювелира'
    nvl clear
    menu:
        'Купить драгоценности':
            $ new_item = game.lair.treasury.craft(**data.craft_options['jeweler_buy'])
            if new_item:
                $ game.lair.treasury.receive_treasures([new_item])
                $ test_description = new_item.description()
                "Куплено: [test_description]."
        'Продать драгоценности':
            'Плейсхолдер'
            # TODO: схема продажи драгоценностей. Ювелир берёт вещь по 100% цене. Сделать как в сокровищнице: самая дорогая, самая дешёвая или случайная. Продемонстрировать и спросить продать / осавить?
        'Драгоценности на заказ':
            $ new_item = game.lair.treasury.craft(**data.craft_options['jeweler_craft'])
            if new_item:
                $ game.lair.treasury.receive_treasures([new_item])
                $ test_description = new_item.description()
                "Изготовлено: [test_description]."
        'Вернуться на площадь':
            call lb_city_walk
    
    return
