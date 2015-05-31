# coding=utf-8
label lb_location_mordor_main:
    $ reinforcement_used = False
    $ place = 'mordor' 
    hide bg
    show place as bg
    python:
        if renpy.music.get_playing(channel='music') != "mus/dark.ogg":
            renpy.music.play("mus/dark.ogg")
            renpy.music.queue(get_random_files('mus/ambient'))
    nvl clear
    python:
        mistress = core.Sayer(game_ref=game)
        mistress.avatar = "img/avahuman/mistress.jpg"
        mistress.name = "Владычица"
    
    menu:
        'В земли Вольных Народов':
            $ pass
        'Армия Тьмы' if not freeplay:
            show expression 'img/bg/special/army.png' as bg
            '[game.army.army_description]'
            nvl clear
            menu:
                'Собрать армию и начать войну!':
                    $ mistrss_helps = True
                    call lb_war_border
                'Продолжить подготовку':
                    'Армия пока не готова.'
                    
            call lb_location_mordor_main
            
        'Аудиенция с владычицей' if not freeplay:
            jump lb_mistress
        'Уйти на покой':
            menu:
                "Это действие сбросит текущую игру и позволит начать заново!"
                "Сдаешься?"
                "Да":
                    python:
                        if not freeplay:
                            renpy.unlink_save("1-1")
                            renpy.full_restart()
                        else:
                            renpy.unlink_save("1-3")
                            renpy.full_restart()
                "Нет":
                    return
    return
    
label lb_mistress:
    python:
        if not persistent.isida_done:
            renpy.movie_cutscene("mov/isida.ogv")
            persistent.isida_done = True
    nvl clear
    show expression 'img/scene/mistress.png' as bg    
    menu:
        'Получить награду' if game.is_quest_complete:
            # Если делаем подарок - удаляем его из списка сокровищ
            if game.quest_task == 'gift' and len(game.lair.treasury.jewelry) > 0:
                $ del game.lair.treasury.jewelry[game.lair.treasury.most_expensive_jewelry_index]
            game.dragon 'Я выполнил твоё задание. Помнится мне была обещана награда...'    
            mistress 'Иди ко мне, милый. Ты не пожалеешь, обещаю.'
            call lb_mistress_fuck
            call lb_choose_dragon
            return
        'Уточнить задание' if not game.is_quest_complete:
            "Текущее задание:\n[game.quest_text]\n[game.quest_time_text]"
            call lb_mistress
        'Завести разговор':
            $ txt = game.interpolate(random.choice(txt_advice))
            mistress '[txt]'   
            nvl clear            
            call lb_mistress
        'Предательски напасть':
            game.dragon 'Независимо от того выиграю ли я эту битву, мой род прервётся. Стоит ли убивать свою мать?'
            menu:
                'Она не смеет повелевать мной!':
                    jump lb_betrayal
                'Она же всётаки Мать...':
                    'От Госпожи не укрылось напряжение сына, но она лишь загадочно улыбнулась не высказывая ни малейшего беспокойства.'
                    call lb_location_mordor_main
        'Лизнуть её руку и уйти':
            'Иногда просто хочется прикоснуться к ней ещё раз...'  
            call lb_location_mordor_main
    return

label lb_location_mordor_questtime:
    $ place = 'mordor' 
    show place as bg
    show screen status_bar
    if game.is_quest_complete:
        mistress '[game.dragon.name] ты слишком много времени тратишь на игры с людьми, я устала ждать. Разве ты забыл о своём задании?'
        game.dragon 'Отнюдь, Владычица, я сделал всё о чём ты просила. Вот. Смотри.'
        mistress 'Великолепно. В таком случае, тебе полагается заслуженная награда. Иди ко мне, милый.'
        call lb_mistress_fuck
        call lb_choose_dragon
    else:
        $ game.dragon.die()
        mistress 'Отпущенное тебе время истекло [game.dragon.name]. И я спрошу лишь один раз: выполнил ли ты моё задание?'
        game.dragon 'Я не успел, Владычица. Мне нужно ещё немного времени. Прости меня.'
        mistress 'Я не обижаюсь. Но и жалость мне не ведома. Ты подвёл меня а это можно сделать лишь однажды. Продолжателем рода станет кто-то другой, ты же доживай свои дни как пожелаешь. Изыди с глаз моих!'
        menu:
            "Дать шанс другому дракону":
                call lb_choose_dragon
                return
    return
    

label lb_mistress_fuck:
    mistress 'Я могу принять любой облик, приятный тебе. Выбирай, какой ты хочешь меня видеть?'
    menu:
        'Облик прекрасной девы, мне милее всего':
            show expression sex_imgs("mistress") as xxx
            pause (500.0)
            $ txt = game.interpolate(random.choice(txt_human_mistress_fuck[game.dragon.kind]))
            '[txt]'    
            hide xxx
        'Стань драконицей, я устал от немощных смертных дев':
            show expression sex_imgs("dragon") as xxx
            pause (500.0)            
            $ txt = game.interpolate(random.choice(txt_dragon_mistress_fuck[game.dragon.kind]))
            '[txt]'
            hide xxx
    show expression 'img/scene/mistress.png' as bg
    mistress 'Благодарю тебя за твоё могучее семя, сын мой. Наши дети превзойдут всех рождённых ранее.'
    game.dragon 'Пусть мои сыновья продолжат моё дело когда вырастут.'
    mistress 'Когда они вылупятся, ты должен будешь выбрать своего приемника, возлюбленный мой.'
    nvl clear
    'Прошло девять месяцев и кладка новых яиц проклюнулась...'
    python:
        if not persistent.lada_done:
            renpy.movie_cutscene("mov/lada.ogv")
            persistent.lada_done = True    
    return

label lb_betrayal:
    $ renpy.movie_cutscene("mov/kali.ogv")
    $ atk_tp = 'pysical'
    $ mistress_hp = 3
    call lb_new_round
    return

label lb_new_round:
    nvl clear    
    if mistress_hp < 1:
        mistress 'Я ещё вернусь!'
        $data.achieve_target("betray", "win")
        $ game.win()
        return
    $ aspect = 'lb_' + random.choice(['kali','garuda','shiva','agni','indra','pangea','nemesis','amphisbena','gekata','hell',])
    $ renpy.call(aspect)
    return

label lb_tactics_choice:
    menu:
        'Рвать зубами':
            $ atk_tp = 'physical'
        'Ударить заклятьем' if game.dragon.mana > 0:
            $ atk_tp = 'magic'
        'Изрыгнуть пламя' if 'fire_breath' in game.dragon.modifiers():
            $ atk_tp = 'fire'
        'Леденящее дыхание' if 'ice_breath' in game.dragon.modifiers():
            $ atk_tp = 'ice'
        'Громовой рёв' if 'sound_breath' in game.dragon.modifiers():
            $ atk_tp = 'thunder'
        'Ужалить ядом'  if 'poison_breath' in game.dragon.modifiers() or 'poisoned_sting' in game.dragon.modifiers():
            $ atk_tp = 'poison'
        'Взмыть в небеса' if game.dragon.can_fly:
            $ atk_tp = 'air'
        # 'Зарыться под землю' if game.dragon.can_dig: #TODO надо понять как это правильно проверить
        #    $ atk_tp = 'earth'
        'Юлить и уклоняться':
            $ atk_tp = 'dodge'
        'Спрятаться и затихнуть':
            $ atk_tp = 'hide'
    return

label lb_kali:
    show expression 'img/scene/fight/mistress/kali.png' as bg    
    'Владычица принимает облик многорукой богини Кали, с чёрной как уголь кожей и красным словно кровь языком. Она вооружена несколькими острыми серпами и очень опасна в ближнем бою.'
    call lb_tactics_choice
    if game.dragon.defence_power()[1] > 0:
        game.dragon 'Мою чешую невозможно разрубить, Мать. Ты родила меня неуязвимым!'
    else:
        'Одним взмахом острого серпа кали отрубает голову дракона.'
        if 'dragon_dead' in game.dragon.decapitate():
            mistress 'Вот и всё сынок... ты зря решил встать на путь Иуды.'
            jump lb_game_over
        else:
            mistress 'Одной головой меньше сынок. Жаль это уже не прибавит тебе ума!'
            
    if atk_tp == 'magic':
        game.dragon 'Твои серпы не защитят тебя от магии смерти, многорукая!!!'
        $ mistress_hp -= 1
    else:
        mistress 'Так меня не одолеть, глупец!'
    call lb_new_round
    return

label lb_garuda:
    show expression 'img/scene/fight/mistress/garuda.png' as bg    
    'Целиком покрывшись яркими перьями и отрастив острые медные когти, Владычица принимает аспект Гаруды. Ни на земле ни в небесах нет места чтобы укрыться от её соколиного удара, но всё же сейчас она очень уязвима.'
    call lb_tactics_choice
    if atk_tp = 'earth':
        game.dragon 'Под землёй тебе меня не достать, пернатая тварь!'
    else:
        'С невероятной силой Гаруда терзает дракона когтями и отрывает ему голову.'
        if 'dragon_dead' in game.dragon.decapitate():
            mistress 'От змеи рождённый, умри как червь!'
            jump lb_game_over
        else:
            mistress 'Всё ещё жив змеёнышь?!'
        
    if atk_tp != 'dodge' and atk_tp != 'hide' and atk_tp != 'earth' and atk_tp != 'air':
        game.dragon 'Получи!'
        $ mistress_hp -= 1
    else:
        mistress 'Беги-беги! А ведь у тебя был шанс ранить меня, идиот!'   
            
    call lb_new_round
    return
    

label lb_shiva:
    show expression 'img/scene/fight/mistress/sheeva.png' as bg    
    'Аспект Шивы наделяет Владычицу неограниченной властью над холодом и льдом. От её поступи земля покрывается коркой инея и холодеет чешуя.'
    call lb_tactics_choice
    if 'ice_immunity' in game.dragon.modifiers():
        game.dragon 'Холод мне не страшен, Мать. Уж ты то должна была об этом помнить!'
    else:
        'Единственного прикосновения Шивы достаточно, чтобы превратить голову дракона в хрупкую ледышку и затём расколоть её на множество осколком одинм ударом.'
        if 'dragon_dead' in game.dragon.decapitate():
            mistress 'Да поглотит тебя ледяное безмолвие, неверный сын!'
            jump lb_game_over
        else:
            mistress 'Вот видишь, это даже не больно. Холод милостив. Но следующей голове повезёт меньше!'

    if atk_tp == 'fire':
        game.dragon 'Пламенем Я командую! Сгори, растай, испарись!!!'
        $ mistress_hp -= 1
    else:
        mistress 'Лишь огонь мог бы тебе помочь, но тебе он неподвластен! Я знаю все твои слабости!'
            
    call lb_new_round
    return

label lb_agni:
    show expression 'img/scene/fight/mistress/agni.png' as bg    
    'Принимая аспект Агни, Владычица закутывается в наряд из багряного пламени и удушающего черного дыма. От неё исходит испепеляющий всё живое жар выдержать который смог бы разве что Ифрит.'
    call lb_tactics_choice
    if 'fire_immunity' in game.dragon.modifiers():
        game.dragon 'Ха! Безумная старуха, неужели ты решила сжечь повелителя пламени? Я стану лишь сильнее от твоего жара, иди же ко мне!'
    else:
        "От касания Агни, голова дракона вспыхивает и мигом превращается в почергевшую головешку."
        if 'dragon_dead' in game.dragon.decapitate():
            mistress 'Почувствуй ярость огня моей души, жалкий предатель! УМРИ!!!'
            jump lb_game_over
        else:
            mistress 'Почувствуй ярость огня моей души! Ещё дергаешься, жалкий червяк?!'
        
    if atk_tp == 'ice':
        game.dragon 'Твой огонь умрёт скованный хладом моего дыхания, Агни!'
        $ mistress_hp -= 1
    else:
        mistress 'Разве можно надеяться сокрушить само пламя, глупец?'
                            
    call lb_new_round
    return

label lb_indra:
    show expression 'img/scene/fight/mistress/indra.png' as bg    
    'В аспекте Индры Владычица получает власть над молнией и громом небесным. Она неуязвима как сам чистый и свежий воздух и небо что питают её могущество. '
    call lb_tactics_choice
    if 'lightning_immunity' in game.dragon.modifiers():
        game.dragon 'Титаны не могли поразить меня своими молниями. Не сможешь и ты, Индра. В штормовом облаке я как в родном доме!'
    else:
        'Удар молнии попадает точно в глову дракона, испепеляя её в одно мгновение!'
        if 'dragon_dead' in game.dragon.decapitate():
            mistress 'Моё возмездие быстро как небесный гром. Тебе стоило подумать об этом, предатель!'
            jump lb_game_over
        else:
            mistress 'Минус одна. А теперь прощайся и со следующей головой!'
        
    if atk_tp == 'poison':
        game.dragon 'Я отравлю воздух дающий тебе силы! Никто не устоит перед токсическим смрадом, даже Небо, даже Аллах!'
        $ mistress_hp -= 1
    else:
        mistress 'Да ты силён, но силы что повергнет сами чистые Небеса ты не сыщешь, предатель!'
                            
    call lb_new_round
    return
    

label lb_pangea:
    show expression 'img/scene/fight/mistress/pangea.png' as bg    
    'Тело владычицы превращается в один огромный живой кристалл, совершенное воплощение аспекта богини земли Пангеи. Её плоть тверда как алмаз.'
    call lb_tactics_choice
    if game.dragon.defence_power()[0] + game.dragon.defence_power()[1] >= 5:
        game.dragon 'Моя чешуя не мягче твоей алмазной кожи, Пангея! Ты даже не поцарапаешь меня.'
    else:
        "Пангея сжимает глову дракона мёртвой хваткой и давит её словно спелый арбуз."
        if 'dragon_dead' in game.dragon.decapitate():
            mistress 'Кто поднял руку на Мать, да будет сокрушён!'
            jump lb_game_over
        else:
            mistress 'Я сокрушу тебя! Каким бы живучим ты ни был, рано или поздно ты сдохнешь, поганец!'
        
    if atk_tp == 'thunder':
        game.dragon 'Попал!'
        $ mistress_hp -= 1
    else:
        mistress 'Промазал!'   
                            
    call lb_new_round
    return

label lb_nemesis:
    show expression 'img/scene/fight/mistress/nemesis.png' as bg    
    'Владычица принимает аспект богини Немезиды. Всё её тело покрывается острыми шипами, олицетворяя неминуемое возмездие. '
    call lb_tactics_choice
    if atk_tp == 'dodge' or atk_tp == 'hide' or atk_tp == 'earth' or atk_tp == 'air':
        game.dragon 'Я знаю справедливость Немезиды. Если я не буду атаковать, ты тоже не сможешь!'
    else:
        'Нападение на Немезиду ведёт к неотвратимому воздаянию. Дракон теряет голову.'
        if 'dragon_dead' in game.dragon.decapitate():
            mistress 'Такова судьба всех предателей - СМЕРТЬ!'
            jump lb_game_over
        else:
            mistress 'Моё возмездие ещё не завершено, но час твоей смерти уже близок, предатель!'
        
    if atk_tp != 'dodge' and atk_tp != 'hide' and atk_tp != 'earth' and atk_tp != 'air':
        game.dragon 'Но и тебе здоровой не уйти!'
        $ mistress_hp -= 1
    else:
        mistress 'Ты правильно делаешь что прячешься, проживёшь лишнюю минуту, а то и две!'  
                            
    call lb_new_round
    return

label lb_amphisbena:
    show expression 'img/scene/fight/mistress/amfisbena.png' as bg    
    'Тело Владычицы покрывается яркой цветной чешуёй, когда она принимает аспект Амфисбены, ползучей ядовитой смерти несущей погибель всем тварям земным.'
    call lb_tactics_choice
    if atk_tp == 'air':
        game.dragon 'Рождённый ползать, летать не может. Попробуй-ка тут меня достать, тварь ползучая!'
    else:
        'От яда амфисбены голова дракона сморщивается и отсыхает.'
        if 'dragon_dead' in game.dragon.decapitate():
            mistress 'Я надеялась что ты будешь мучаться дольше, Иуда!'
            jump lb_game_over
        else:
            mistress 'Чувствуешь этот яд? Я рада что ты ещё трепыхаешься, так моя месть будет слаще.'
        
    if game.dragon.attack_strength()[1] > 0:
        game.dragon 'Я раздавлю тебя, гадюка!'
        $ mistress_hp -= 1
    else:
        mistress 'И это всё на что ты способен?! Слабак!'
                            
    call lb_new_round
    return
    

label lb_gekata:
    show expression 'img/scene/fight/mistress/gekata.png' as bg    
    'Аспект Гекаты даёт Владычице силу самой Ночи и Смерти. Сражаться с ней может лишь смельчак не боящийся смертельных ран, но порой лучше быть трусом.'
    call lb_tactics_choice
    if atk_tp != 'hide':
        game.dragon 'Я укроюсь от Тьмы во Тьме.'
    else:
        'Смертоносная Геката с лёгкостью отрывает дракону голову.'
        if 'dragon_dead' in game.dragon.decapitate():
            mistress 'А твоё тело я скормлю шакалам, потому что ты падаль!'
            jump lb_game_over
        else:
            mistress 'Всё ещё дёргаешься, падаль?!'
        
    if game.dragon.attack_strength()[0] + game.dragon.attack_strength()[1] >= 5:
        game.dragon 'Вот тебе! Получай! Меня не так то просто убить.'
        $ mistress_hp -= 1
    else:
        mistress 'А я то надеялась что моё чадо будет бить сильнее чем крестьянская девчёнка...' 
                            
    call lb_new_round
    return

label lb_hell:
    show expression 'img/scene/fight/mistress/hell.png' as bg    
    'Владычица выростает до небес, задевая макушкой облака, когда призывает на себя аспект великанши Хель - немёртвой владычицы нижнего мира. Её удары кажутся медленными, но они способны крушить даже гранитные скалы.'
    call lb_tactics_choice
    if atk_tp == 'dodge':
        game.dragon 'Слишком медленно! Тебе меня не достать.'
    else:
        "Сокрушающим землю ударом огромной руки, великанша расплющивает голову дракона."
        if 'dragon_dead' in game.dragon.decapitate():
            mistress 'ХА! И мокрого места не осталось.'
            jump lb_game_over
        else:
            mistress 'Познай боль! Я сокрушу тебя как мерзкого таракана!'
        
    if atk_tp == 'magic':
        game.dragon 'Мои чары превыше твоей грубой силы, Хель!'
        $ mistress_hp -= 1
    else:
        mistress 'Хорошая попытка малыш. Но для меня ты мелковат!'  
                            
    call lb_new_round
    return
    
label lb_war_border:
    # TODO: Дракон ведёт свою армию на вольные земли. На протяжении всех событий отступать нельзя - дракон умрёт или победит. Один раз можно попросить госпожу одолеть любого врага вместо дракона.
    # Чтобы пройти АТ нужно взять пограничную крепость. Дракон берёт на себя катапульты, армия штурмует стены.
    # Если и дракон и армия победили, засчитываем победу.
    # Если дракон победил, но армия слишком слаба даём второй энкаунтер для дракона - воздушный флот цвергов приходит
    # на помощь осаждённым, дракон должен их победить.
    python:
        army_battle = True #Из боя теперь нельзя отступить
        army_decimator = 10
    
    show expression 'img/scene/dark_march.png' as bg
    'Сражение у границ, Армия Тьмы вступает в битву. Катапульты являются ключевым звеном обороны.'
    
    $ game.foe = core.Enemy('catapult', game_ref=game)
    $ narrator(show_chances(game.foe))
            
    menu:
        'Наблюдать за битвой' if game.army.force >= 1000: # Армия Тьмы теряет 10% силы и разбирается с противником без вмешательства дракона.
            'Армия Тьмы несёт потери, но передовые отряды прорываются к катапультам и уничтожают их. Теперь победа всего в одном шаге.'
            $ game.army.power_percentage -= army_decimator
            
        'Сокрушить катапульты': #Дракон бережёт армию и сам уничтожает наиболее опасные очаги сопротивления
            call lb_fight

        'Молить Госпожу о помощи': #Владычица вступает в бой и выигрывает его вместо дракона и армии
            game.dragon '[reinforcement_ask]'
            python:
                if reinforcement_used:
                    reinforcement_answer = reinforcement_refuse
                else:
                    reinforcement_answer = reinforcement_agree
            mistress '[reinforcement_answer]'
            if reinforcement_used:
                call lb_war_border
            else:
                $ renpy.movie_cutscene("mov/kali.ogv")
                $ reinforcement_used = True

    call lb_war_border_continue
    return

label lb_war_border_continue:
    nvl clear
    show expression 'img/scene/dark_march.png' as bg
    'Сражение на земле практически выиграно, но дракон замечает новую опасность. Со стороны гор по воздуху приближается летучий флот цвергов. Если их не остановить они сбросят в гущу армии монстров бочки наполненные алхимическим огнём. Потери будут огромны.'
    $ game.foe = core.Enemy('airfleet', game_ref=game)
    $ narrator(show_chances(game.foe))
    
    menu:
        'Наблюдать за битвой' if game.army.force >= 1000: # Армия Тьмы теряет 10% силы и разбирается с противником без вмешательства дракона.
            'Тяжелые летучие крейсера демонстративно зависают над скоплением монстров и скидывают прямо на головы воинам Владычицы пузатые бочки с заженнйми фитилями. Земля озаряется вспышками и заливается текучим огнём. Объятые пламенем гоблины с визгоми разбегаются и катаются по земле пытвась погасить огонь. Когда запас бомб на кораблях подходит к концу, они мерно разворачиваются и уходят на базу невредимыми. Эта атака стоила Армии Тьмы днсятой части воинов!'
            'Тем не менее, пограничные войска людей выдохнулись и вынуждены были отступить. Путь вглубь страны открыт.'
            $ game.army.power_percentage -= army_decimator
            
        'Перехватить летучие корабли': #Дракон бережёт армию и сам уничтожает наиболее опасных врагов
            call lb_fight

        'Молить Госпожу о помощи': #Владычица вступает в бой и выигрывает его вместо дракона и армии
            game.dragon '[reinforcement_ask]'
            python:
                if reinforcement_used:
                    reinforcement_answer = reinforcement_refuse
                else:
                    reinforcement_answer = reinforcement_agree
            mistress '[reinforcement_answer]'
            if reinforcement_used:
                call lb_war_border_continue
            else:
                $ renpy.movie_cutscene("mov/kali.ogv")
                $ reinforcement_used = True
    
    call lb_war_field
    return

    
label lb_war_field:
    # TODO: Армия продвигается вглубь страны и встречает объединённые войска Вольных Народов. Дракон должен победить титана, армия сражается с войском.
    # Если дракон и АТ победили, продвигаемся дальше. Если дракон победил а АТ проигрывает, даём дракону схватку против короля людей.

    nvl clear    
    show expression 'img/scene/great_force.png' as bg
    'Битва на границе была просто цветочками. Теперь Вольные Народы собрали объединённую армию чтобы встретить тёмное воинство в чистом поле. Опаснее всех остальных врагов выглядит исполин в золотой броне - Титан решил сразиться на стороне вольных!'
    $ game.foe = core.Enemy('titan', game_ref=game)
    $ narrator(show_chances(game.foe))
    
    menu:
        'Наблюдать за битвой' if game.army.force >= 1000: # Армия Тьмы теряет 10% силы и разбирается с противником без вмешательства дракона.
            'Титан наносит тёмному воинству огромный урон, но всё же его удаётся одолеть. Вольные дрогнули, осталось лишь надавить!'
            $ game.army.power_percentage -= army_decimator
            
        'Атаковать': #Дракон бережёт армию и сам уничтожает наиболее опасных врагов
            '[game.dragon.fullname] лично вступает в битву с Титаном, чтобы сберечь войска.'
            call lb_fight

        'Молить Госпожу о помощи': #Владычица вступает в бой и выигрывает его вместо дракона и армии
            game.dragon '[reinforcement_ask]'
            python:
                if reinforcement_used:
                    reinforcement_answer = reinforcement_refuse
                else:
                    reinforcement_answer = reinforcement_agree
            mistress '[reinforcement_answer]'
            if reinforcement_used:
                call lb_war_border_continue
            else:
                $ renpy.movie_cutscene("mov/kali.ogv")
                $ reinforcement_used = True
    call lb_war_field_continue
    return

label lb_war_field_continue:
    # TODO: Армия продвигается вглубь страны и встречает объединённые войска Вольных Народов. Дракон должен победить титана, армия сражается с войском.
    # Если дракон и АТ победили, продвигаемся дальше. Если дракон победил а АТ проигрывает, даём дракону схватку против короля людей.
    
    nvl clear
    show expression 'img/scene/dark_march.png' as bg
    'Король людей воодушевляет бойцов и не даёт им отступать. Когда он будет повержен, битву можно считать выигранной.'
    $ game.foe = core.Enemy('king', game_ref=game)
    $ narrator(show_chances(game.foe))
    
    menu:
        'Наблюдать за битвой' if game.army.force >= 1000: # Армия Тьмы теряет 10% силы и разбирается с противником без вмешательства дракона.
            'Ценой огромный потерь, элитные отряды тёмных сил прорываются к королю и рассправляются с ним. Это становится переломным моментом битвы. На закате разрозненные и разбитые войска людей отступают, открывая чудовищам путь вглубь страны.'
            $ game.army.power_percentage -= army_decimator
            
        'Атаковать': #Дракон бережёт армию и сам уничтожает наиболее опасных врагов
            'Битву можно выиграть всего одним точным ударом. [game.dragon.fullname] бросает вызов королю людей!'
            call lb_fight

        'Молить Госпожу о помощи': #Владычица вступает в бой и выигрывает его вместо дракона и армии
            game.dragon '[reinforcement_ask]'
            python:
                if reinforcement_used:
                    reinforcement_answer = reinforcement_refuse
                else:
                    reinforcement_answer = reinforcement_agree
            mistress '[reinforcement_answer]'
            if reinforcement_used:
                call lb_war_field_continue
            else:
                $ renpy.movie_cutscene("mov/kali.ogv")
                $ reinforcement_used = True
    call lb_war_siege
    return
    
label lb_war_siege:
    # TODO: Армия Тьмы осаждает столицу людей. Дракон должен пробить огромные ворота чтобы армия могла ворваться в город.
    # Если дракон и АТ победили, продвигаемся дальше. Если дракон победил а АТ проигрывает, даём дракону схватку
    # против городской стражи.

    nvl clear
    show expression 'img/scene/city_fire.png' as bg
    'Разбив главные силы Вольных Народов, Силы Тьмы подступают к стенам столицы. В этом отлично укреплённом городе сопортивление может продолжаться годами. Пока столица не взята, говорить о подчинении Вольных Земель не приходится.'
    $ game.foe = core.Enemy('city', game_ref=game)
    $ narrator(show_chances(game.foe))
    
    menu:
        'Наблюдать за битвой' if game.army.force >= 1000: # Армия Тьмы теряет 10% силы и разбирается с противником без вмешательства дракона.
            'Войска штурмуюие главные ворота города несут страшные потери, но защитников слишком мало. Монстры сносят ворота и врываются на улицы города.'
            $ game.army.power_percentage -= army_decimator
            
        'Атаковать': #Дракон бережёт армию и сам уничтожает наиболее опасных врагов
            'Если проломить главные ворота, обороняющиеся войска окажутся беззащитны перед монстрами Владычицы. [game.dragon.fullname] бросается на штурм. '
            call lb_fight

        'Молить Госпожу о помощи': #Владычица вступает в бой и выигрывает его вместо дракона и армии
            game.dragon '[reinforcement_ask]'
            python:
                if reinforcement_used:
                    reinforcement_answer = reinforcement_refuse
                else:
                    reinforcement_answer = reinforcement_agree
            mistress '[reinforcement_answer]'
            if reinforcement_used:
                call lb_war_siege
            else:
                $ renpy.movie_cutscene("mov/kali.ogv")
                $ reinforcement_used = True
                
    call lb_war_siege_inside
    return

    
label lb_war_siege_inside:
    # TODO: Армия Тьмы осаждает столицу людей. Дракон должен пробить огромные ворота чтобы армия могла ворваться в город.
    # Если дракон и АТ победили, продвигаемся дальше. Если дракон победил а АТ проигрывает, даём дракону схватку
    # против городской стражи.
    nvl clear
    show expression 'img/scene/city_raze.png' as bg
    'На улице города идут ожесточённые бои. Основу сопротивления составляюти элитные отряды городской стражи.'
    $ game.foe = core.Enemy('city_guard', game_ref=game)
    $ narrator(show_chances(game.foe))
    
    menu:
        'Наблюдать за битвой' if game.army.force >= 1000: # Армия Тьмы теряет 10% силы и разбирается с противником без вмешательства дракона.
            'Бой на улицах города отличается невероятной жестокостью, кровь течёт рекой и множетво раненых и убитых наблюдается с обеих сторон. Темне менее Силы Тьмы слишком многочисленны - защитники города обречены.'
            $ game.army.power_percentage -= army_decimator
            
        'Атаковать': #Дракон бережёт армию и сам уничтожает наиболее опасных врагов
            '[game.dragon.fullname] лично возглавляет атаку своих войск, помогая уничтожить стражей.'
            call lb_fight

        'Молить Госпожу о помощи': #Владычица вступает в бой и выигрывает его вместо дракона и армии
            game.dragon '[reinforcement_ask]'
            python:
                if reinforcement_used:
                    reinforcement_answer = reinforcement_refuse
                else:
                    reinforcement_answer = reinforcement_agree
            mistress '[reinforcement_answer]'
            if reinforcement_used:
                call lb_war_siege_inside
            else:
                $ renpy.movie_cutscene("mov/kali.ogv")
                $ reinforcement_used = True
                
    call lb_war_citadel
    return

label lb_war_citadel:
    # TODO: Армия Тьмы захватила город, но центральная цитадель ещё держится. Дракон должен схватиться в воздухе с ангелом-хранителем, пока АТ штурмует.
    # Если дракон и АТ победили, продвигаемся дальше. Если дракон победил а АТ проигрывает, даём дракону схватку
    # против стального стража цвергов.
    # После окончательной победы переходим к сцене финальной оргии и концу игры.
    nvl clear
    show expression 'img/scene/city_raze.png' as bg
    'Хотя город взят и уже полыхает, в цитадели на холме всё ещё есть недобитые защитники. Учитывая что именно там хранятся все драгоценнсоти короны, взять это укрепление совершенно необходимо. К сожалению над цитаделью парит ангел-защитник, посланный Небесами в ответ на мольбы невинных. Этот пернатый воин один стоит целой армии.'
    $ game.foe = core.Enemy('angel', game_ref=game)
    $ narrator(show_chances(game.foe))
    
    menu:
        'Наблюдать за битвой' if game.army.force >= 1000: # Армия Тьмы теряет 10% силы и разбирается с противником без вмешательства дракона.
            'Исчадия Тьмы выпускают в ангела сотни стрел, но они сгорают на подлёте. Небесный страж рубит отряды гоблинов своим мечём, словно скашивая пожухлую траву серпом. Наконец его удаётся сбить метким выстрелом тяжёлой катапульты, но потери очень велики.'
            $ game.army.power_percentage -= army_decimator
            
        'Атаковать': #Дракон бережёт армию и сам уничтожает наиболее опасных врагов
            'С этим противником [game.dragon.fullname] решает сразиться сам - обычным гоблинам он не по зубам.'
            call lb_fight

        'Молить Госпожу о помощи': #Владычица вступает в бой и выигрывает его вместо дракона и армии
            game.dragon '[reinforcement_ask]'
            python:
                if reinforcement_used:
                    reinforcement_answer = reinforcement_refuse
                else:
                    reinforcement_answer = reinforcement_agree
            mistress '[reinforcement_answer]'
            if reinforcement_used:
                call lb_war_citadel
            else:
                $ renpy.movie_cutscene("mov/kali.ogv")   
                $ reinforcement_used = True
                
    call lb_war_final
    return
    
label lb_war_final:
    nvl clear
    show expression 'img/scene/city_raze.png' as bg
    'Воодушевлённые победой над ангелом выродки дракона врываются внутрь цитадели, но тут же выкатываются обратно. Внутренние ворота охраняет огромный механический страж цвергов - несокрушимый железный голем.'
    $ game.foe = core.Enemy('golem', game_ref=game)
    $ narrator(show_chances(game.foe))
    
    menu:
        'Наблюдать за битвой' if game.army.force >= 1000: # Армия Тьмы теряет 10% силы и разбирается с противником без вмешательства дракона.
            'Железного голема удаётся буквально похоронить под грудой мяса и железа, в которые превращаются идущие волна за волной в самоубийственную атаку Исчадия Тьмы. Тем не мене это победа!'
            $ game.army.power_percentage -= army_decimator
            
        'Атаковать': #Дракон бережёт армию и сам уничтожает наиболее опасных врагов
            'Как бы могуч не был железный страж, это всё что стоит на пути к окочательной победы. [game.dragon.fullname] бросается в атаку.'
            call lb_fight

        'Молить Госпожу о помощи': #Владычица вступает в бой и выигрывает его вместо дракона и армии
            game.dragon '[reinforcement_ask]'
            python:
                if reinforcement_used:
                    reinforcement_answer = reinforcement_refuse
                else:
                    reinforcement_answer = reinforcement_agree
            mistress '[reinforcement_answer]'
            if reinforcement_used:
                call lb_war_final
            else:
                $ renpy.movie_cutscene("mov/kali.ogv")               
                $ reinforcement_used = True    
    jump lb_orgy

label lb_orgy:
    nvl clear
    show expression 'img/scene/city_raze.png' as bg
    'Послений защитник пал и Земли Вольных Народов отныне под властью Владычицы, Матери Драконов!'
    game.dragon 'Мы победили!'
    mistress 'Да. Благодаря тебе, твоему роду и детям твоего рода... Как давно я ждала этого. Даю тебе и армии три дня на разграбление города, а затем мы начнём строить ПЕРВУЮ | ВСЕМИРНУЮ | ИМПЕРИЮ!'
    game.dragon 'Вы слышали Владычицу, воины мои. Тащите всех девок ко мне и кидайте в кучу!'    
    show expression 'img/scene/girls.png' as bg
    pause (500.0)
    nvl clear
    'Отродья дракона прочесали горящий город, похватав всех красивых и молодых женщин чтобы сорвать с них всю одежду и собрать в разгромленном тронном зале цитадели. Сотни обнаженных красавиц заполнили огромный зал до отказа так что дракону пришлось буквально плыть в море обнаженных тел чтобы добраться до середины.'
    game.dragon 'Сегодня вы можете насладиться победой месте со мной, дети мои! Делайте с этими девками всё что пожелаете.' 
    show expression 'img/scene/orgy.png' as bg
    pause (500.0)    
    nvl clear
    'Началось столпотворение. Озлобленные после отчаянного боя солдаты тьмы набросились на женщин словно безумные. Глядя на творящуюся вокруг оргию, дракон и сам не терял времени. Сдавленный обнаженными телами он не глядя вонзил в упругую женскую плоть одновременно и зубы и член, начав кровавый танец сочетающий в себе голод и ярость, алчность и похоть. Этот танец продлится до тех пор пока хотя бы одна женщина в зале сохранит способность визжать и дёргаться... '
    jump lb_you_win
