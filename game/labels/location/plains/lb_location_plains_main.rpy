# coding=utf-8
init python:
    from pythoncode.characters import Enemy, Talker
    from pythoncode.utils import weighted_random
    
label lb_location_plains_main:
    python:
        if not renpy.music.is_playing():
            renpy.music.play(get_random_files('mus/ambient'))
    $ place = 'plain'
    hide bg
    show expression get_place_bg(place) as bg
    nvl clear
    
    if game.dragon.energy() == 0:
        'Даже драконам надо иногда спать. Особенно драконам!'
        return
        
    menu:
        'Рыскать за околицей':
            call lb_encounter_plains from _call_lb_encounter_plains
            return
        'Одинокий хутор':
            $ village_size = 1
            call lb_village from _call_lb_village
        'Маленький посёлок':
            $ village_size = 2
            call lb_village from _call_lb_village_1
        'Деревня':
            $ village_size = 3
            call lb_village from _call_lb_village_2
        'Село':
            $ village_size = 4
            call lb_village from _call_lb_village_3
        'Городок':
            $ village_size = 5
            call lb_village from _call_lb_village_4
        'Прочь отсюда':
            return
        
    return
    
label lb_encounter_plains:
    $ nochance = game.poverty.value * 3
    $ choices = [
        ("lb_enc_fair", 5),
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
        ("lb_enc_redhood", 3),        
        ("lb_patrool_plains", 3 * game.mobilization.level),
        ("lb_enc_noting", nochance)]
    $ enc = weighted_random(choices)
    $ renpy.call(enc)
    return
  
label lb_enc_redhood:
    python: #делаем аватарку волка для диалогового окна
        wolf = Talker(game_ref=game)
        wolf.avatar = "img/avahuman/wolf.jpg"
        wolf.name = 'Сергей "BBW" Волков'    
    if "redhood_done" in persistent.easter_eggs: #проверяем не было ли уже этого энкаунтера за всё время игры
        jump lb_encounter_plains #если уже был хотя бы раз, игнорируем и переходим к обычным встречам
    $ persistent.easter_eggs.append("redhood_done") #отмечаем что энкаунтер с красной шапочкой произошел
    "[game.dragon.fullname] замечает издалека маленькую фигурку в ярко-красной накидке уходящую по тропинке в лес. У неё в руке тяжелая корзинка с пирожками. Крестьяне обычно не носят красные накидки. [game.dragon.kind] решает проследить за девочкой, но она уже скрылась за деревьями и идти приходится на запах."
    show expression 'img/bg/forest/1.jpg' as bg    
    "Судя по следам, красная шапочка встретилась на перекрёстке с необычным существом. От него остался сложный запах, напоминающий одновременно отродий Владычицы, человечину и мокрую псину. Существо не напало на шапочку, они немного потоптались на месте, а потом пошли разными дорогами но в одну и ту же сторону. Интересно…"
    "Следы красной шапочки ведут к поляне на которой стоит небольшой домик, очень аккуратный для жилища расположенного в глухом лесу. Изнутри раздаётся шум - женские крики, утробный рык и шум переворачиваемой мебели."
    nvl clear
    show expression 'img/scene/wolf_sex.jpg' as bg
    pause (50.0)
    "Заглянув в окошко [game.dragon.name] видит внутри картину разгрома. Огромный антропоморфный волк жестоко насилует девушку в красной накидке, прямо у трупа старой седой женщины. Девушка визжит и отбивается, но волчару это похоже только распаляет. С невероятно довольным выражением на морде, он выкручивает руки красной шапочки за спину и с утробным рычанием сношает её по собачьи. "
    "Острые длинные когти чудовища оставляют на нежной коже девочки глубокие кровавые полосы, когда он сжимает лапы от удовольствия, наполняя семенем её истерзанную утробу. Удовлетворённый зверочеловек тяжело дыша ложится на пол чтобы перевести дух. Его окровавленная жертва пытается отползти к двери, но оборотень ещё не закончил."
    "Привычным движением он хватает девочку за ляжку и легко подтягивает обратно к себе. Бедняжка визжит и умоляет его прекратить, но волк лишь улыбается вывалив язык на бок.  Покрепче ухватив аппетитную попку жертвы когтистыми лапами, он с видимым усилием втискивает свой внушительны собачий инструмент прямо в её аккуратненькую анальную дырочку. Судя по приложенным на вхождение усилиям, мохнатый просто разодрал её сфинктер, чтобы протиснуться внутрь."
    nvl clear
    "Красная шапочка визжит так что уши закладывает, но и это не может остановить жестокого зверочеловека. Напротив, распалившись от криков своей окровавленной жертвы он вгрызается в неё зубами и отрывает ей правую руку. [game.dragon.name] по собственному опыту знает как приятно совмещать секс и завтрак, а волчара с таким аппетитом хрустит косточкой что у дракона аж слюнки потекли."
    "Через несколько минут кровавого пиршества девочка (точнее то что от неё осталось) затихает на полу. Сытый и довольный волк методично отгрызает её неповреждённую ногу, прямо с хоршим куском ягодицы. Затем оборотень принимает человеческий облик и закинув кровавый трофей на плечо выходит из дома чтобы нос к носу столкнуться с драконом."
    show expression 'img/bg/forest/1.jpg' as bg                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    game.dragon "Привет. Ты из маминой своры? Что-то я тебя не припомню, братишка…"
    wolf "(мне пиздец, это ж дракон) Ээээ… кхм... Нет. Я из Москвы. Сергей. Сергей Волков."
    game.dragon "В первый раз слышу. У вас там в Москве всегда так развлекаются? Весёлое должно быть местечко."
    wolf "Да, я там шороху навёл в своё время, но теперь уж никак не вернуться. Туманы не пускают. Слушай… может я пойду уже, у тебя свои дела у меня свои, что нам тут лясы точить?"
    game.dragon "А ножкой не угостишь? Я что-то проголодался."
    wolf "Не, мужик, мне же ребёнка надо кормить. Я только ради этого сюда и выполз. Там в доме ещё осталось кое что. И старуха почти целая."
    game.dragon "Ну ладно. Дети это святое, у самого спиногрызов куча по всему свету бегает. Счастливого пути, Сергей Волков из Москвы."
    nvl clear
    "Сдержанно кивнув друг-другу чудовища разошлись в разные стороны и продолжили свои приключения."    

    return

label lb_enc_fair:
    $ txt = game.interpolate(random.choice(txt_enc_fair[0]))
    '[txt]'
    nvl clear
    menu:
        'Первая красавица':
            python:
                game.dragon.drain_energy()
                description = game.girls_list.new_girl('peasant')
                txt = game.interpolate(random.choice(txt_enc_fair[1]))
            '[txt]'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex from _call_lb_nature_sex_3      
            return

        'Призовой бык':
            $ game.dragon.drain_energy()
            $ game.foe = Enemy('bull_champion', game_ref=game)
            call lb_fight from _call_lb_fight_2
            menu:
                'Сожрать призового быка' if game.dragon.hunger > 0:
                    'Бык съеден. -1 к голоду, +1 к похоти. Ярость обнуляется.'
                    $ game.dragon.reputation.points += 1
                    '[game.dragon.reputation.gain_description]'
                    python:
                        game.dragon.bloodiness = 0
                        if game.dragon.lust < 3:
                            game.dragon.lust += 1
                        game.dragon.hunger -= 1
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
            call lb_nature_sex from _call_lb_nature_sex_4      
            return
            
        'Девица с ягодами':
            $ game.dragon.drain_energy()
            'Сцена погони. Дракон ловит девушку с корзинкой ягод.'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            game.girl 'Ой только не ешьте меня пожалуйста.'
            menu:
                'Ограбить девицу' if game.girl.treasure:
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
                                    python:
                                        if game.dragon.bloodiness > 0:
                                            game.dragon.bloodiness = 0
                                        game.dragon.hunger -= 1
                                'Отпустить':
                                    'Голая крестьянка убегает пытаясь прикрыть срам руками.'
                            return
                        'Сожрать девицу' if game.dragon.hunger > 0:
                            'Дракон обмазывает девушку ягодами из лукошка и съедает.'
                            python:
                                if game.dragon.bloodiness > 0:
                                    game.dragon.bloodiness = 0
                                if game.dragon.lust < 3:
                                    game.dragon.lust += 1
                                game.dragon.hunger -= 1
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
                            python:
                                if game.dragon.bloodiness > 0:
                                    game.dragon.bloodiness = 0
                                game.dragon.hunger -= 1
                        'Отпустить':
                            'Голая крестьянка убегает пытаясь прикрыть срам руками.'
                    return
                'Сожрать девицу' if game.dragon.hunger > 0:
                    'Дракон срывает с девушки одежду, обмазывает её ягодами из лукошка и съедает.'
                    python:
                        if game.dragon.bloodiness > 0:
                            game.dragon.bloodiness = 0
                        if game.dragon.lust < 3:
                            game.dragon.lust += 1
                        game.dragon.hunger -= 1
                'Отнять ягоды и отпустить':
                    'Дракон закусывает сладкими ягодками и уходит.'
                    python:
                        if game.dragon.lust < 3:
                            game.dragon.lust += 1
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
            call lb_nature_sex from _call_lb_nature_sex_5      
            return
            
        'Девица с грибным лукошком':
            $ game.dragon.drain_energy()
            'Сцена погони. Дракон ловит девушку с корзинкой грибов.'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            game.girl 'Ой только не ешьте меня пожалуйста.'
            menu:
                'Ограбить девицу' if game.girl.treasure:
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
                                    python:
                                        if game.dragon.bloodiness > 0:
                                            game.dragon.bloodiness = 0
                                        if game.dragon.lust < 3:
                                            game.dragon.lust += 1
                                        game.dragon.hunger -= 1
                                'Отпустить':
                                    'Голая крестьянка убегает пытаясь прикрыть срам руками.'
                            return
                        'Сожрать девицу' if game.dragon.hunger > 0:
                            'Дракон заставляет крестьянку нажарить грибов, затем потрошит её, фарширует грибами и пожирает.'
                            python:
                                if game.dragon.bloodiness > 0:
                                    game.dragon.bloodiness = 0
                                if game.dragon.lust < 3:
                                    game.dragon.lust += 1
                                game.dragon.hunger -= 1
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
                            python:
                                if game.dragon.bloodiness > 0:
                                    game.dragon.bloodiness = 0
                                game.dragon.hunger -= 1
                        'Отпустить':
                            'Голая крестьянка убегает пытаясь прикрыть срам руками.'
                    return
                'Сожрать девицу' if game.dragon.hunger > 0:
                    'Дракон срывает с крестьянки одежду, потрошит и фарширует грибами а затем пожирает.'
                    python:
                        if game.dragon.bloodiness > 0:
                            game.dragon.bloodiness = 0
                        if game.dragon.lust < 3:
                            game.dragon.lust += 1
                        game.dragon.hunger -= 1
                'Отнять ягоды и отпустить':
                    'Дракон закусывает свежими грибами и уходит.'
                    python:
                        if game.dragon.lust < 3:
                            game.dragon.lust += 1
                    return
                    
        'Оставить их в покое': 
            '[game.dragon.name] берет одну из брошенных корзинок с грибами себе на закуску и уходит.'
            $ game.dragon.gain_rage()
            return
    
    return

    
label lb_enc_laundry:
    'Громкий плеск и девичий смех приводят дракона на берег реки. Женщины стирают тут бельё и конечно среди них найдётся хотя бы одна девственница достойная вынносить отродье древней крови...'
    nvl clear
    menu:
        'Схватить невинную девицу':
            $ game.dragon.drain_energy()
            $ description = game.girls_list.new_girl('peasant')
            '[game.dragon.name] с рычанинем выбегает из кустов и бабы на берегу поднимают такой истошный визг, что ушам больно. Женшины разбегаются врассыпную, но даркону нужна только одна из них и он легко её настигает. Пройдёт вполне достаточно времени прежде чем на шум сбегутся вооруженные люди, можно не спешить...'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex from _call_lb_nature_sex_6      
            return        
        'Оставить их в покое' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            return    
    return
    
label lb_enc_bath:
    'Громкий плеск и женский смех приводят дракона на берег реки. Девушки купаются в поросшей камышом и кувшинками заводи у реки. Как это мило, даже бегать не прийдётся...'
    nvl clear
    menu:
        'Выловить девицу из реки':
            $ game.dragon.drain_energy()
            $ description = game.girls_list.new_girl('peasant')
            'Люди значительно лучше бегают чем плавают, так что сватить плескающуюся в воде девушку не представляет ни малейшего труда.'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex from _call_lb_nature_sex_7      
        'Оставить их в покое' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    return
    
label lb_enc_militia:
    python:
        if game.mobilization.level <= 0:
            renpy.jump('lb_encounter_plains')
        else:
            renpy.jump('lb_enc_militia_true')
    return

label lb_enc_militia_true:
    show expression 'img/scene/fight/militia.jpg' as bg
    'На поле тренируются ополченцы-новобранцы. Они непредставляют такой большой угрозы как опытные бойцы, да и взять с них нечего, однако если не разогнать этот сброд, то со временем они пополнят ряды армии и будут мешаться...'
    nvl clear
    menu:
        'Напасть':
            $ game.dragon.drain_energy()
            $ game.foe = Enemy('militia', game_ref=game)
            call lb_fight from _call_lb_fight_3
            '  Отряд ополченцев готовившийся пополнить армию больше не существует. Немногие выжившие новобранцы разбежались в ужасе. Теперь королю будет сложнее собирать свои патрульные отряды.'
            $game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
            $ game.mobilization.level -= 1
                        
        'Убраться прочь' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    
    return
    
label lb_enc_mill:
    show expression 'img/bg/special/windmill.jpg' as bg
    'На вершине холма стоит высокая деревянная башня с лопастями вращающимися под напором ветра. Очевидно это какой-то человеческий сельско-хозяйственный механизм. Не очень интересно, однако его разрушение может быть забавным, а главное это принесёт округе разорение и голод.'
    nvl clear
    menu:
        'Расшатать мельницу' if game.dragon.size > 3:
            $ game.dragon.drain_energy()
            "[game.dragon.name] достаточно огромен чтобы потягаться силами с этой винтокрылой башней. Слегка размявшись, дракон поднимается во весь рост и что есть мочи налегает на башню. Из рассыпающегося строения выскакивает обсыпанный мукой толстяк и смешно размахивая руками кубарем скатывается с холма. Вслед за ним летят облмки мельницы. Если людям будет нечего есть, они меньше станут думать о том как сражаться с драконами!"
            $ game.poverty.value += 1
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
        'Заклятье гнили' if game.dragon.mana > 0:
            $ game.dragon.drain_energy()
            "[game.dragon.name] шепчет заклинание призывающее магический огонь и тут же разворачивается чтобы уйти гордо подняв хвост. Понято же что произойдёт - возникшая на мельнице искра перекинется на взвесь мучной пыли в воздухе и та мгновенно сгорит вызвав детонацию по принципу объёмного взрыва. А драконы на взрывы не оглядываются!"
            $ game.poverty.value += 1
            $ game.dragon.reputation.points += 3
            $ game.dragon.drain_mana()
            '[game.dragon.reputation.gain_description]'
        'Обследовать здание' if game.dragon.size <= 3 and game.dragon.mana == 0:
            $ game.dragon.drain_energy()
            "[game.dragon.name] тщательно обследует необычное строение на предмет важности и уязвимых мест. Эту четырёхкрылую башню с каменным основанием люди используют чтобы делать из зерна муку. Очень хочется её разрушить, но стоит она прочно. Нужно либо размер иметь побольше чтобы расшатать её собственным телом, либо наслать гнилостное заклятье на внутренние деревянные механизмы."
            'Только время зря потерял. Придётся уйти несолоно хлебавши.'
        'Пройти мимо' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    
    return
    
label lb_enc_granary:
    show expression 'img/bg/plain/granary.jpg' as bg    
    'В полях, поодаль от деревень стоит здоровенный деревянный дом. Судя по запаху там никто не живёт, внутри просто лежит зерно. Люди почему-то очень любят есть зерно... глупые люди. Как можно жить без мяса?'
    nvl clear
    python:
        doit = False
        if 'fire_breath' in game.dragon.modifiers(): 
            doit = True
    menu:
        'Дыхнуть огнём' if doit:
            $ game.dragon.drain_energy()
            "[game.dragon.name] изрыгает поток жидкого пламени прямо на соломенную крышу амбара. Потушить его уже не удастся, а когда зерно сгорит, людям будет пора задуматься не о том как убивать драконов, а о том как набить животы."
            $ game.poverty.value += 1
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]'
        'Заклятье гнили' if game.dragon.mana > 0:
            $ game.dragon.drain_energy()
            "[game.dragon.name] произносит древнюю колдовскую формулу и подбрасывает в окно амбара дохлую лягушку. Всего за пару часов от неё по зерну расползётся чеёрна плесень, которая сделает зерно негодным. Людям не чем будет кормить войска, а значит дракону и его отродьем станет немного легче жить в следующем году."
            $ game.poverty.value += 1
            $ game.dragon.reputation.points += 5
            $ game.dragon.drain_mana()
            '[game.dragon.reputation.gain_description]'
        'Обследовать здание' if not doit and game.dragon.mana == 0:
            $ game.dragon.drain_energy()
            "[game.dragon.name] тщательно обследует огромный амбар. Зерна тут хватит чтобы целыый городо прокормить. Эх сжечь бы это всё до тла и люди начали бы голодать, только вот огонька нет..."
        'Пройти мимо' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    
    return

label lb_enc_gooze:
    'Босоногая крестьянская девчёнка пасёт гусей. Она слишком молода чтобы рожать, однако достаточно аппетитна чтобы сойти на завтрак.'
    nvl clear
    menu:
        'Сожрать гусей' if game.dragon.hunger > 0:
            '[game.dragon.name] ловит и проглатывает одного жирного гуся, но остальные разлетаются.'
            python:
                game.dragon.drain_energy()
                if game.dragon.bloodiness > 0:
                    game.dragon.bloodiness -= 1
        'Сожрать девчёнку' if game.dragon.hunger > 0:
            '[game.dragon.name] хватает девчёнку и съедает её живьём, с хрустом разгрызая тоненькие косточки.'
            $ game.dragon.drain_energy()
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
            python:
                if game.dragon.bloodiness > 0:
                    game.dragon.bloodiness = 0
                game.dragon.hunger -= 1
        'Устрить побоище' if game.dragon.bloodiness >= 5:
            $ game.dragon.drain_energy()
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            '[game.dragon.name] нападает, убивая девочку и всех гусей которых только может поймать, просто ради забавы.'    
        'Оставить их в покое' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    
    return
    
label lb_enc_pigs:
    'За полями пшеницы, в дубраве пасётся сдао свиней. Свинопас, который должен за ними наблюдать, дрыхнет под деревом укрыв лицо соломенной шляпой, но у свиней есть и другой сторож, куда более бдительный - здоровенный злой волкодав.'
    $ game.foe = Enemy('dog', game_ref=game)
    $ chances = show_chances(game.foe)
    nvl clear
    menu:
        'Напасть на стадо' if game.dragon.hunger > 0:
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_4
            'К моменту когда собака повержена, и свиньи и свинопас уже успевают разбежаться, но бежать от дракона идея глупая - [game.dragon.name] обладает совершенным нюхом и никогда не теряет след намеченной жертвы. Вскоре одной жирненькой свиньёй в стаде становится меньше.'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            python:
                if game.dragon.bloodiness > 0:
                    game.dragon.bloodiness = 0
                game.dragon.hunger -= 1
        'Напасть на стадо' if game.dragon.hunger == 0:
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_5
            'Разодрав в клочки собаку, [game.dragon.name] догоняет и убивает свинопаса. Свиньи разбегаются прочь, но это уже не важно.'
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
        'Отступить' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            return    
    
    return    

label lb_enc_sheepherd:
    'В зелёных холмах, покрытых сочной травой старый чабан пасёт атару овец. Звидев приближение дракона, мудрый старик предпочитает по быстрому сделать ноги, а вот верная овчарка похоже готова охранять стадо до последнего вздоха.'
    $ game.foe = Enemy('dog', game_ref=game)
    $ chances = show_chances(game.foe)
    nvl clear
    menu:
        'Напасть на стадо' if game.dragon.hunger > 0:
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_6
            'Во время драки с собакой овцы разбежались, но их белая шерсть видна на зелёных холмах издалека. Так что поймать себе на обед жирненького барашка не составляет труда.'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            python:
                if game.dragon.bloodiness > 0:
                    game.dragon.bloodiness = 0
                game.dragon.hunger -= 1
        'Напасть на стадо' if game.dragon.hunger == 0:
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_7
            '[game.dragon.name] догоняет и убивает несколько овец, хотя не хочет есть. Просто иногда надо выпустить пар и дать волю первобытной ярости.'
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
        'Отступить' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            return    
    
    return


label lb_enc_cattle:
    'Ну какая же пасторальная картина без пасущихся коровок? [game.dragon.name] набредает на деревенское стадо, так и просящееся дракону на обед. Пастух в ужасе убегает прочь, но вот один из быков, самый крупный, полон решимости защитить стадо.'
    $ game.foe = Enemy('bull', game_ref=game)
    $ chances = show_chances(game.foe)
    nvl clear
    menu:
        'Напасть на стадо' if game.dragon.hunger > 0:
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_8
            python:
                if game.dragon.bloodiness > 0:
                    game.dragon.bloodiness = 0
                game.dragon.hunger -= 1
            '[game.dragon.name] разрывает быка в клочья и проглатывает куски дымящегося мяса, стремительно наедаясь.'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
        'Напасть на стадо' if game.dragon.hunger == 0:
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_9
            '[game.dragon.name] убивает несколько коров и разгоняет стадо, хотя вовсе не хочет есть - он просто зол.'
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
        'Отступить' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            return    
    
    return

label lb_enc_noting:
    show expression 'img/bg/special/village_burned.jpg' as bg          
    'Здесь лишь запустение и разруха. Хотя когда-то тут можно было встретить людей или животных, сейчас их больше нету. Кругом лишь разрушенные дома да заросшие бурьяном пашни.'
    python:
        if game.dragon.bloodiness < 5: 
            game.dragon.gain_rage()
    return


# разные деревни
label lb_village:
    python:
        a = 10 + game.poverty.value - village_size
        chance = random.randint(1, a)
        if chance > 10:
            village_size = 0
        txt1 = village['overview'][village_size]
    show expression 'img/bg/special/village.jpg' as bg     
    '[txt1]'
    $ game.foe = Enemy(village['deffence'][village_size], game_ref=game)    
    $ chances = show_chances(game.foe)    
    nvl clear
    menu:
        'Наложить дань' if village_size > 0 and game.dragon.fear > village_size:
            $ game.dragon.drain_energy()
            show expression 'img/bg/special/fear.jpg' as bg
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
                call lb_nature_sex from _call_lb_nature_sex_8                   
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
                    max_cost = 500
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
                call lb_nature_sex from _call_lb_nature_sex_9        
            
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'

        'Ограбить' if village_size > 0:
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_10
            'Поселение успешно разграблено. Добыча:'
            python:
                count = random.randint(5, 10)
                alignment = 'human'
                min_cost = 5 * village_size
                max_cost = 25 * village_size
                obtained = "Это предмет из разграбленного людского поселения."
                trs = treasures.gen_treas(count, data.loot['klad'], alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
            '[trs_descrptn]'
            $ game.lair.treasury.receive_treasures(trs)
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
        
        'Разорить' if village_size > 0:
            $ game.dragon.drain_energy()
            $ game.foe = Enemy(village['deffence'][village_size], game_ref=game)
            call lb_fight from _call_lb_fight_11
            'Поселение разорено. Разруха в стране растёт. В разрушенных домах и на телах убитых нашлись кое-какие ценности:'
            python:
                count = random.randint(5, 10)
                alignment = 'human'
                min_cost = 5 * village_size
                max_cost = 25 * village_size
                obtained = "Это предмет из разграбленного людского поселения."
                trs = treasures.gen_treas(count, data.loot['klad'], alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
            '[trs_descrptn]'
            python:
                game.lair.treasury.receive_treasures(trs)
                game.poverty.value += 1
                game.dragon.reputation.points += 5
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
        chance = random.randint(0, game.mobilization.level)
        if chance < 4:
            patrool = 'archer'
            dtxt = 'Вдоль околицы прохаживается бородач с длинным луком, это стрелок местного шерифа отправленный в дозор чтобы защищать деревню.'
        elif chance < 7:
            patrool = 'xbow_rider'
            dtxt = 'Просёлочные дороги патрулирует отряд лёгкой кавалерии. Они готовы быстро отреагировать на любую угрозу будь то разбойники, монстры или даже дракон.'
        elif chance < 11:
            patrool = 'heavy_cavalry'
            dtxt = 'Дракон нарывается на отряд тяжелой кавалерии. Раз уж в деревенские патрули стали посылать рыцарей, люди видимо запуганы в край.'
        elif chance < 16:
            patrool = 'griffin_rider'
            dtxt = 'Пронзительный кличь раздаётся с небес - это всадник на грифоне пикирует с высоты, завидев в полях блеск драконьей чешуи.'
        else:
            patrool = 'angel'
            dtxt = '%s вынужден зажмуриться от яркого света бьющего в глаза. Громогласный оклик возвещает: "Умри мерзкое порождение греха!!!". Это ангел-хранитель посланный людям Небесами для защиты.' % game.dragon.name
    '[dtxt]'
    python:
        game.foe = Enemy(patrool, game_ref=game)
        battle_status = battle.check_fear(game.dragon, game.foe)
    if 'foe_fear' in battle.check_fear(game.dragon, game.foe):
        $ narrator(game.foe.battle_description(battle_status, game.dragon))
        return
    $ game.dragon.drain_energy()
    call lb_fight(skip_fear=True) from _call_lb_fight_12
    return
