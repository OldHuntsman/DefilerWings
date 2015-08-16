# coding=utf-8
init python:
    from pythoncode.utils import weighted_random
    from pythoncode.characters import Enemy
        
label lb_location_sea_main:
    python:
        if not renpy.music.is_playing():
            renpy.music.play(get_random_files('mus/ambient'))    
    $ place = 'sea'
    hide bg
    show expression get_place_bg(place) as bg
    nvl clear
    
    if game.dragon.energy() == 0:
        '[game.dragon.name] need some sleep!'
        return
        
    if not game.dragon.can_swim: 
        '[game.dragon.name] пробует когтем солёную морскую влагу. Если бы только он умел дышать под водой...'
    else:
        call lb_encounter_sea from _call_lb_encounter_sea
    return
    
label lb_encounter_sea:
    $ choices = [
        ("lb_enc_fishers", 10),
        ("lb_enc_yacht", 10),
        ("lb_enc_bark", 10),
        ("lb_enc_tuna", 10),
        ("lb_enc_shark", 10),
        ("lb_triton_found", 10),
        ("lb_enc_galeon", 10),
        ("lb_enc_diver", 10),
        ("lb_enc_mermaid", 10),
        ("lb_enc_merfolks", 10),
        ("lb_enc_mermaids", 10),
        ("lb_enc_shipwreck", 10),
        ("lb_patrool_sea", 3 * game.mobilization.level)]
    $ enc = weighted_random(choices)
    $ renpy.call(enc)

    return 
    
label lb_enc_tuna:
    '[game.dragon.fullname] замечает крупный косяк тунца плывущий по течению. Некоторые рыбины такие здоровые что могут поспорить по весу с деревенскими быками. Но наверняка они даже вкуснее!'
    nvl clear
    menu:
        'Eat the tuna' if game.dragon.hunger > 0:
            $ game.dragon.drain_energy()
            '[game.dragon.name] ловит и пожирает самую крупную рыбу из стаи. Вскоре на кровь сплываются многочисленные акулы, но увидив кто тут трапезничает, мгновенно уплывают прочь.'
            python:
                if game.dragon.bloodiness > 0:
                    game.dragon.bloodiness = 0
        'Murder a fish scool' if game.dragon.bloodiness >= 5 and game.dragon.hunger == 0:
            $ game.dragon.drain_energy()
            'Хорошенько разогнавшись [game.dragon.name] врезается в косяк рыбы буквально взрывая его изнутри. Располосованная зубами и когтями рыба отчаянно бьётся в воде, так что кровь расплывается облаками и вода становится красной. Словно из ниоткуда появляются опьяневшие от крови акулы превнося в действие ещё больше хаоса и смерти. Неплохой способ выпустить ярость, кто бы подумал что можно получить столько радости от отдного единственного косяка?'    
        'Swim away' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    return
    
label lb_enc_shark:
    'Навстречу дракону величественно выплывает большая белая акула. Это действительно выдающийся экземпляр, не менее шести метров в длинну. Похоже она считает себя королевой этих вод.'
    nvl clear
    menu:
        'Fight the shark':
            $ game.dragon.drain_energy()
            $ game.foe = Enemy('shark', game_ref=game)
            call lb_fight from _call_lb_fight_20
            if game.dragon.hunger > 0:
                'Голодный [game.dragon.name] съедает разрывает поверженную акулу на куски и заглатывает самые крупные в то время как за куски помельче дерутся откуда ни возьмись маленькие акулы.'
                python:
                    if game.dragon.bloodiness > 0:
                        game.dragon.bloodiness = 0
                    game.dragon.hunger -= 1
                    game.dragon.add_effect('shark_meat')
            else:
                '[game.dragon.fullname] сейчас не голоден, поэтому оставляет изрангенную акулу на растерзание её более мелким но агрессивным сородичам, приплывшим на запах крови.'
        'Dive deeper' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    return
    
label lb_enc_fishers:
    '[game.dragon.fullname] натыкается на рыбацкую лодку идущую в порт. У них на борту полно рыбы.'
    nvl clear
    menu:
        'Snatch the fish' if game.dragon.hunger > 0:
            $ game.dragon.drain_energy()
            'Рыбаки кричат от удивления и ужаса, когда прямо из воды высовывается голова на длинной шее и хватает рыбу прямо у них из лодки. А потом ещё и ещё, до тех пор пока судно не причалило к берегу. Наверное рыбаки попрыгали бы от страху в море, если бы не знали что там ещё опасней.'
            python:
                if game.dragon.bloodiness > 0:
                    game.dragon.bloodiness = 0
                game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
        'Topple the boat' if game.dragon.bloodiness >= 5 and game.dragon.hunger == 0:
            $ game.dragon.drain_energy()
            '[game.dragon.kind] выпрыгивает из воды словно резвящийся дельфин и всем своим весом падает поперёк лодки, так что та с хрустом ломается посередине, здымая облака брызг и раскидывая рыбаков встороны. Осталось пустить одному кровь, чтобы акулы доделали своё дело. Но меожеи быть кто-то и спасётся...'    
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
        'Swim away' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    return
    
label lb_enc_yacht:
    'Вдоль берега неспеша плывёт изящная прогулочная яхта. Судя по запаху, на борту есть невинная девица, наверное дочь какого-нибудь богатого купца а может быть даже и лорда. В любом случае, это законная добыча повелителя окрестных вод!'
    nvl clear
    menu:
        'Snatch the girl from board':
            $ chance = random.choice(['citizen', 'citizen', 'citizen', 'princess'])
            $ game.dragon.drain_energy()
            $ description = game.girls_list.new_girl(chance)
            'Аккуратно, чтобы на яхте не заметили его приближения, [game.dragon.kind] подплывает к судну и ложится на паралельный курс, выжидая подходящего момента. И момент не заставляет себя долго ждать. Красивая юная [game.girl.type] выходит на палубу и оболокачивается на перила, наблюая за резвящимися в волнах рыбками. Недолго думая, [game.dragon.name] хватает девушку и утаскивает в море и невзирая на обеспокоенные крики команды выволакивает её на берег, в уютное и тихое местечко, пригодное для романтического ужина...'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex from _call_lb_nature_sex_12      
        'Let her be' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()    
    return
    
label lb_enc_bark:
    'Зная что вдоль береговой линии пролегают торговые маршруты, [game.dragon.kind] решает проплыть вдоль одного из них и натыкается на тяжело гружёный парусник. Судя по запаху, он везёт груз вина, оливкового масла и специй из заморских стран. Наверняка на борту должны быть и звонкие монетки, для украшения дракоьньей кучи.'
    menu:
        'Wring the money':
            python:
                game.dragon.drain_energy()
                passing_tool = random.randint(1, 20)
                gold_trs = treasures.Coin('dublon', passing_tool)
                game.lair.treasury.receive_treasures([gold_trs])
            'Капитан решает не испытывать судьбу и отдаёт дракону несколько золотых дублонов, чтобы тот его не трогал и пропустил корабль с миром.'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
        'Sink the ship' if game.dragon.bloodiness >= 5:
            $ game.dragon.drain_energy()
            $ game.foe = Enemy('ship', game_ref=game)
            call lb_fight from _call_lb_fight_21
            'Пока накренившийся на борт корабль медленно идёт ко дну а оставшиеся в живых члены команды озабочены спасением своих жизней, [game.dragon.name] методично осматирвает трюм и каюту капитна, выгребая каждую монетку:'
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
        'Swim away' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    return
        
label lb_enc_galeon:
    'А вот это называется "везёт по крупному" - паруса показавшиеся на горизонте принадлежат тяжело вооружённому галеону. Именно на таких судах люди короля перевозят золото из нового света. И суда по осадке у этой посудины трюмы отнюдь не пусты. Хотя опустошить их будет возможно не легко...'
    $ game.foe = Enemy('battleship', game_ref=game)
    $ narrator(show_chances(game.foe))
    menu:
        'Sink the galleon':
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_22
            python:
                count = random.randint(10, 25)
                alignment = 'human'
                min_cost = 1
                max_cost = 1000000
                t_list = ['gold']
                obtained = "Просто золото."
                trs = treasures.gen_treas(count, t_list, alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
                game.lair.treasury.receive_treasures(trs)
            'В трюмах галеона [game.dragon.kind] обнаруживает тяжелые слитки жёлтого металла, с эмблемой короля удостоверяющей высокую пробу:'
            '[trs_descrptn]'
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]'
            
        'Swim away' if game.dragon.bloodiness < 5:
            'Груз золота невероятно заманчив, но разумеется у такого груза есть достойная охрана. И как бы ни хотелось быть богатым, живым быть всё же важнее.'       
            $ game.dragon.gain_rage()
    return
    
label lb_enc_diver:
    'Эти тёплые прозрачные воды облюбовали ловцы жемчуга. Раз за разом ныряют они на глубину, выискивая раковины-жемчужницы в надежде найти внутри драгоценное содержимое. [game.dragon.fullname] знает что грабить их бесполезно, бедняги считают что им повезло если за целый день работы обнаруживается хотя бы одна стоящая жемчужина. Но на этот раз дракона привлекает пожива другого рода. Загорелая ныряльщица с сильными и крепкими ногами источает аромат невинности привлекающий не менее чем запах денег. Такая может выносить здоровое потомсвто...'
    nvl clear
    menu:
        'Snatch the swimmer':
            $ game.dragon.drain_energy()
            $ description = game.girls_list.new_girl('peasant')
            'Дракон ловит ныряльщицу.'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex from _call_lb_nature_sex_13      
        'Go away' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    return
    
label lb_enc_mermaid:
    'У берега на большом камне сидит русалочка, она рассчёсывает длинные волосы блестящим перламутровым гребнем. Похоже ждёт своего принца... или дракона.'
    nvl clear
    menu:
        'Catch the little merrimaid':
            $ game.dragon.drain_energy()
            $ description = game.girls_list.new_girl('mermaid')
            'Дракон ловит русалку.'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            nvl clear
            game.girl.third "[description]"
            call lb_water_sex from _call_lb_water_sex      
        'Swim away' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()    
    return
    
label lb_enc_merfolks:
    'Русалка и водяной плывут взявшись за руки. Водяной вооружен и вряд ли отдаст свою подругу без боя.'
    $ game.foe = Enemy('merman', game_ref=game)
    $ narrator(show_chances(game.foe))
    nvl clear
    menu:
        'Attak fishman':
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_23
            $ description = game.girls_list.new_girl('mermaid')
            'Дракон ловит русалку.'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            nvl clear
            game.girl.third "[description]"
            call lb_water_sex from _call_lb_water_sex_1      
        'Swim away' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()       
    return
    
label lb_enc_mermaids:
    'Русалки водят подводный хоровод.'
    nvl clear
    menu:
        'Catch the merrimaid':
            $ game.dragon.drain_energy()
            $ description = game.girls_list.new_girl('mermaid')
            'Держась на глубине [game.dragon.name] подплывает к самому камню и поднимает из воды шею прямо перед испуганной водяной девой. Та в ужасе дергает хвостом и падает в воду, прямо в объятья морского змея.'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            nvl clear
            game.girl.third "[description]"
            call lb_water_sex from _call_lb_water_sex_2      
        'Swim away' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()       
    return
     
label lb_enc_shipwreck:
    'Глубоко на дне лежат обломки корабля потопленного штормом. Найти их было бы нереально, если бы не настойчивый запах золотоа идущий откуда-то из его поросших водорослями трюмов. Драконы просто не могут ингонировать запах золота. Даже под водой.'
    nvl clear
    python:
        tr_lvl = random.randint(1, 100)
        count = random.randint(1, 10)
        alignment = 'human'
        min_cost = 1 * tr_lvl
        max_cost = 10 * tr_lvl
        obtained = "Это предмет с затонувшего корабля."
        trs = treasures.gen_treas(count, data.loot['klad'], alignment, min_cost, max_cost, obtained)
        trs_list = game.lair.treasury.treasures_description(trs)
        trs_descrptn = '\n'.join(trs_list)
    menu:
        'dive for treashures':
            $ game.dragon.drain_energy()
            'Разворотив гнилые борта затонувшего корабля [game.dragon.fullname] добирается до ценного содержимого. В тёмном затопленном трюме покоится тяжёленкий сундук, а внутри сундука:'
            '[trs_descrptn]'
            $ game.lair.treasury.receive_treasures(trs)
            
        'No time for this' if game.dragon.bloodiness < 5:
            'Конечно сокровища полезны, но у дракона есть дела поважнее. Какие интересно? Сложно даже представить... ЧТО МОЖЕТ БЫТЬ ВАЖНЕЕ СОКРОВИЩ???!'
    return
    
label lb_patrool_sea:
    python:
        chance = random.randint(0, game.mobilization.level)
        if chance < 4:
            patrool = 'merman'
            dtxt = 'В прибрежных водах несёт дозоро вооружённый трезубцем водяной. Такому только акул гонять.'
        elif chance < 7:
            patrool = 'merman'
            dtxt = 'В прибрежных водах несёт дозоро вооружённый трезубцем водяной. Такому только акул гонять.'
        elif chance < 11:
            patrool = 'griffin_rider'
            dtxt = 'Пронзительный кличь раздаётся с небес - это всадник на грифоне пикирует с высоты, завидев нв водной глади блеск драконьей чешуи.'
        elif chance < 16:
            patrool = 'battleship'
            dtxt = 'Вдоль обжитых человеческих берегов рыщет патрульный корабль, вооружённый пушками. Люди серьёзно взялись за охрану своих берегов.'
        else:
            patrool = 'triton'
            dtxt = 'Обычно на большой глубине морской змей не встречает никаких врагов, разве что шальная акула попадётся, но на этот раз судьба свела его с рыбохвостым морским великаном. Тритон вооружён и похоже специально вышел на охоту за досаждающим его подданным гадом.'
    '[dtxt]'
    python:
        game.foe = Enemy(patrool, game_ref=game)
        battle_status = battle.check_fear(game.dragon, game.foe)
    if 'foe_fear' in battle_status:
        $ narrator(game.foe.battle_description(battle_status, game.dragon))
        return
    $ game.dragon.drain_energy()
    call lb_fight(skip_fear=True) from _call_lb_fight_24
    return
