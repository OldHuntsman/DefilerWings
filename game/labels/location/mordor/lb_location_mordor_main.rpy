# coding=utf-8
label lb_location_mordor_main:
    $ place = 'mordor' 
    hide bg
    show place as bg
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
    nvl clear
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
            'Обсуждение'
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
    mistress 'Я могу принять любой облик, приятный тебе. Выбирай, каой ты хочешь меня видеть?'
    menu:
        'Облик прекрасной девы, мне милее всего':
            $ txt = game.interpolate(random.choice(txt_human_mistress_fuck[game.dragon.kind]))
            '[txt]'    
        'Стань драконицей, я устал от немощных смертных дев':
            $ txt = game.interpolate(random.choice(txt_dragon_mistress_fuck[game.dragon.kind]))
            '[txt]'
    show expression 'img/scene/mistress.png' as bg
    mistress 'Благодарю тебя за твоё могучее семя, сын мой. Наши дети превзойдут всех рождённых ранее.'
    game.dragon 'Пусть мои сыновья продолжат моё дело когда вырастут.'
    mistress 'Когда они вылупятся, ты должен будешь выбрать своего приемника, возлюбленный мой.'
    'Прошло девять месяцев и кладка новых яиц проклюнулась...'
    return

label lb_betrayal:
    # TODO: Сражение дракона и Госпожи. Подробности в диздоке, картинки готовы.
    $ atk_tp = 'pysical'
    $ mistress_hp = 3
    call lb_new_round
    return

label lb_new_round:
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
    'Многорукий облик. Атака попадает если у дракона нет верной защиты. Уязвима для магической атаки.'
    call lb_tactics_choice
    if game.dragon.defence_power()[1] > 0:
        game.dragon 'Защищён'
    else:
        if dragon.decapitate() == 'dragon_dead':
            mistress 'Убит'
            jump lb_you_win
        else:
            mistress 'Ранен'
            
    if atk_tp == 'magic':
        game.dragon 'Попал!'
        $ mistress_hp -= 1
    else:
        mistress 'Промазал!'
    call lb_new_round
    return

label lb_garuda:
    show expression 'img/scene/fight/mistress/garuda.png' as bg    
    'Облик птицы. Атака попадает если дракон не закопался в землю. Уязвима для любой атаки.'
    call lb_tactics_choice
    if atk_tp = 'earth':
        game.dragon 'Защищён'
    else:
        if dragon.decapitate() == 'dragon_dead':
            mistress 'Убит'
            jump lb_you_win
        else:
            mistress 'Ранен'
        
    if atk_tp != 'dodge' and atk_tp != 'hide' and atk_tp != 'earth' and atk_tp != 'air':
        game.dragon 'Попал!'
        $ mistress_hp -= 1
    else:
        mistress 'Промазал!'   
            
    call lb_new_round
    return
    

label lb_shiva:
    show expression 'img/scene/fight/mistress/sheeva.png' as bg    
    'Ледяной облик. Атака попадает если у дракона нет защиты от холода. Уязвима для огненного дыхания.'
    call lb_tactics_choice
    if 'ice_immunity' in game.dragon.modifiers():
        game.dragon 'Защищён'
    else:
        if dragon.decapitate() == 'dragon_dead':
            mistress 'Убит'
            jump lb_you_win
        else:
            mistress 'Ранен'

    if atk_tp == 'fire':
        game.dragon 'Попал!'
        $ mistress_hp -= 1
    else:
        mistress 'Промазал!'
            
    call lb_new_round
    return

label lb_agni:
    show expression 'img/scene/fight/mistress/agni.png' as bg    
    'Огненный облик. Атака попадает если у дракона нет защиты от огня. Уязвима для ледяного дыхания.'
    call lb_tactics_choice
    if 'fire_immunity' in game.dragon.modifiers():
        game.dragon 'Защищён'
    else:
        if dragon.decapitate() == 'dragon_dead':
            mistress 'Убит'
            jump lb_you_win
        else:
            mistress 'Ранен'
        
    if atk_tp == 'ice':
        game.dragon 'Попал!'
        $ mistress_hp -= 1
    else:
        mistress 'Промазал!'
                            
    call lb_new_round
    return

label lb_indra:
    show expression 'img/scene/fight/mistress/indra.png' as bg    
    'Облик громовержца. Атака попадает если у дракона нет защиты от молний. Уязвима для ядовитого дыхания.'
    call lb_tactics_choice
    if 'lightning_immunity' in game.dragon.modifiers():
        game.dragon 'Защищён'
    else:
        if dragon.decapitate() == 'dragon_dead':
            mistress 'Убит'
            jump lb_you_win
        else:
            mistress 'Ранен'
        
    if atk_tp == 'poison':
        game.dragon 'Попал!'
        $ mistress_hp -= 1
    else:
        mistress 'Промазал!'
                            
    call lb_new_round
    return
    

label lb_pangea:
    show expression 'img/scene/fight/mistress/pangea.png' as bg    
    'Кристаллический облик. Атака попадает если дракон имеет сумму обычной и верной брони менее пяти. Уязвима для громового рёва.'
    call lb_tactics_choice
    if game.dragon.defence_power()[0] + game.dragon.defence_power()[1] >= 5:
        game.dragon 'Защищён'
    else:
        if dragon.decapitate() == 'dragon_dead':
            mistress 'Убит'
            jump lb_you_win
        else:
            mistress 'Ранен'
        
    if atk_tp == 'thunder':
        game.dragon 'Попал!'
        $ mistress_hp -= 1
    else:
        mistress 'Промазал!'   
                            
    call lb_new_round
    return

label lb_nemesis:
    show expression 'img/scene/fight/mistress/nemesis.png' as bg    
    'Облик возмездия. Атака попадает если дракон производит любое агрессивное действие. Неуязвима.'
    call lb_tactics_choice
    if atk_tp == 'dodge' or atk_tp == 'hide' or atk_tp == 'earth' or atk_tp == 'air':
        game.dragon 'Защищён'
    else:
        if dragon.decapitate() == 'dragon_dead':
            mistress 'Убит'
            jump lb_you_win
        else:
            mistress 'Ранен'
        
    if atk_tp != 'dodge' and atk_tp != 'hide' and atk_tp != 'earth' and atk_tp != 'air':
        game.dragon 'Попал!'
        $ mistress_hp -= 1
    else:
        mistress 'Промазал!'  
                            
    call lb_new_round
    return

label lb_amphisbena:
    show expression 'img/scene/fight/mistress/amfisbena.png' as bg    
    'Облик змеи. Атака попадает если дракон не взлетел в воздух. Уязвима для физической атаки при условии что у дракона есть хотя бы одна верная атака.'
    call lb_tactics_choice
    if atk_tp == 'air':
        game.dragon 'Защищён'
    else:
        if dragon.decapitate() == 'dragon_dead':
            mistress 'Убит'
            jump lb_you_win
        else:
            mistress 'Ранен'
        
    if game.dragon.attack_strength()[1] > 0:
        game.dragon 'Попал!'
        $ mistress_hp -= 1
    else:
        mistress 'Промазал!'
                            
    call lb_new_round
    return
    

label lb_gekata:
    show expression 'img/scene/fight/mistress/gekata.png' as bg    
    'Облик смерти. Атака попадает если дракон не спрятался. Уязвима для физической атаки если дракон имеет сумму обычной и верной атаки не менее пяти.'
    call lb_tactics_choice
    if atk_tp != 'hide':
        game.dragon 'Защищён'
    else:
        if dragon.decapitate() == 'dragon_dead':
            mistress 'Убит'
            jump lb_you_win
        else:
            mistress 'Ранен'
        
    if game.dragon.attack_strength()[0] + game.dragon.attack_strength()[1] >= 5:
        game.dragon 'Попал!'
        $ mistress_hp -= 1
    else:
        mistress 'Промазал!' 
                            
    call lb_new_round
    return

label lb_hell:
    show expression 'img/scene/fight/mistress/hell.png' as bg    
    'Облик великанши. Атака попадает если дракон не уклонялся. Уязвима для магической атаки.'
    call lb_tactics_choice
    if atk_tp == 'dodge':
        game.dragon 'Защищён'
    else:
        if dragon.decapitate() == 'dragon_dead':
            mistress 'Убит'
            jump lb_you_win
        else:
            mistress 'Ранен'
        
    if atk_tp == 'magic':
        game.dragon 'Попал!'
        $ mistress_hp -= 1
    else:
        mistress 'Промазал!'  
                            
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
    
    show expression 'img/bg/special/dark_march.png' as bg
    'Сражение у границ, Армия Тьмы вступает в битву. Катапульты являются ключевым звеном обороны.'
    
    $ game.foe = core.Enemy('catapult', game_ref=game)
    $ narrator(show_chances(game.foe))
            
    menu:
        'Наблюдать за битвой' if game.army.force >= 0: # Армия Тьмы теряет 10% силы и разбирается с противником без вмешательства дракона.
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
                $ reinforcement_used = True

    call lb_war_border_continue
    return

label lb_war_border_continue:
    show expression 'img/bg/special/dark_march.png' as bg
    'Сражение на земле практически выиграно, но [dragon.name] замечает новую опасность. Со стороны гор по воздуху приближается летучий флот цвергов. Если их не остановить они сбросят в гущу армии монстров бочки наполненные алхимическим огнём. Потери будут огромны.'
    $ game.foe = core.Enemy('airfleet', game_ref=game)
    $ narrator(show_chances(game.foe))
    
    menu:
        'Наблюдать за битвой' if game.army.force >= 0: # Армия Тьмы теряет 10% силы и разбирается с противником без вмешательства дракона.
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
                $ reinforcement_used = True
    
    call lb_war_field
    return

    
label lb_war_field:
    # TODO: Армия продвигается вглубь страны и встречает объединённые войска Вольных Народов. Дракон должен победить титана, армия сражается с войском.
    # Если дракон и АТ победили, продвигаемся дальше. Если дракон победил а АТ проигрывает, даём дракону схватку против короля людей.
    
    show expression 'img/bg/special/great_force.png' as bg
    'Сражение в чистом поле'
    $ game.foe = core.Enemy('titan', game_ref=game)
    $ narrator(show_chances(game.foe))
    
    menu:
        'Наблюдать за битвой' if game.army.force >= 0: # Армия Тьмы теряет 10% силы и разбирается с противником без вмешательства дракона.
            ''
            $ game.army.power_percentage -= army_decimator
            
        'Атаковать': #Дракон бережёт армию и сам уничтожает наиболее опасных врагов
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
                $ reinforcement_used = True
    call lb_war_field_continue
    return

label lb_war_field_continue:
    # TODO: Армия продвигается вглубь страны и встречает объединённые войска Вольных Народов. Дракон должен победить титана, армия сражается с войском.
    # Если дракон и АТ победили, продвигаемся дальше. Если дракон победил а АТ проигрывает, даём дракону схватку против короля людей.
    
    show expression 'img/bg/special/dark_march.png' as bg
    'Сражение в чистом поле'
    $ game.foe = core.Enemy('champion', game_ref=game)
    $ narrator(show_chances(game.foe))
    
    menu:
        'Наблюдать за битвой' if game.army.force >= 0: # Армия Тьмы теряет 10% силы и разбирается с противником без вмешательства дракона.
            'Это становится переломным моментом битвы. На закате разрозненные и разбитые войска людей отступают, открывая чудовищам путь вглубь страны.'
            $ game.army.power_percentage -= army_decimator
            
        'Атаковать': #Дракон бережёт армию и сам уничтожает наиболее опасных врагов
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
                $ reinforcement_used = True
    call lb_war_siege
    return
    
label lb_war_siege:
    # TODO: Армия Тьмы осаждает столицу людей. Дракон должен пробить огромные ворота чтобы армия могла ворваться в город.
    # Если дракон и АТ победили, продвигаемся дальше. Если дракон победил а АТ проигрывает, даём дракону схватку
    # против городской стражи.
    show expression 'img/bg/special/city_fire.png' as bg
    'Осада столицы'
    $ game.foe = core.Enemy('city', game_ref=game)
    $ narrator(show_chances(game.foe))
    
    menu:
        'Наблюдать за битвой' if game.army.force >= 0: # Армия Тьмы теряет 10% силы и разбирается с противником без вмешательства дракона.
            'Это становится переломным моментом битвы. На закате разрозненные и разбитые войска людей отступают, открывая чудовищам путь вглубь страны.'
            $ game.army.power_percentage -= army_decimator
            
        'Атаковать': #Дракон бережёт армию и сам уничтожает наиболее опасных врагов
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
                $ reinforcement_used = True
                
    call lb_war_siege_inside
    return

    
label lb_war_siege_inside:
    # TODO: Армия Тьмы осаждает столицу людей. Дракон должен пробить огромные ворота чтобы армия могла ворваться в город.
    # Если дракон и АТ победили, продвигаемся дальше. Если дракон победил а АТ проигрывает, даём дракону схватку
    # против городской стражи.
    show expression 'img/bg/special/city_raze.png' as bg
    'Осада столицы'
    $ game.foe = core.Enemy('city_guard', game_ref=game)
    $ narrator(show_chances(game.foe))
    
    menu:
        'Наблюдать за битвой' if game.army.force >= 0: # Армия Тьмы теряет 10% силы и разбирается с противником без вмешательства дракона.
            'Это становится переломным моментом битвы. На закате разрозненные и разбитые войска людей отступают, открывая чудовищам путь вглубь страны.'
            $ game.army.power_percentage -= army_decimator
            
        'Атаковать': #Дракон бережёт армию и сам уничтожает наиболее опасных врагов
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
                $ reinforcement_used = True
                
    call lb_war_citadel
    return

label lb_war_citadel:
    # TODO: Армия Тьмы захватила город, но центральная цитадель ещё держится. Дракон должен схватиться в воздухе с ангелом-хранителем, пока АТ штурмует.
    # Если дракон и АТ победили, продвигаемся дальше. Если дракон победил а АТ проигрывает, даём дракону схватку
    # против стального стража цвергов.
    # После окончательной победы переходим к сцене финальной оргии и концу игры.
    show expression 'img/bg/special/city_raze.png' as bg
    'Битва за цитадель'
    $ game.foe = core.Enemy('angel', game_ref=game)
    $ narrator(show_chances(game.foe))
    
    menu:
        'Наблюдать за битвой' if game.army.force >= 0: # Армия Тьмы теряет 10% силы и разбирается с противником без вмешательства дракона.
            'Это становится переломным моментом битвы. На закате разрозненные и разбитые войска людей отступают, открывая чудовищам путь вглубь страны.'
            $ game.army.power_percentage -= army_decimator
            
        'Атаковать': #Дракон бережёт армию и сам уничтожает наиболее опасных врагов
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
                $ reinforcement_used = True
                
    call lb_war_final
    return
    
label lb_war_final:
    show expression 'img/bg/special/city_raze.png' as bg
    'Последняя битва'
    $ game.foe = core.Enemy('golem', game_ref=game)
    $ narrator(show_chances(game.foe))
    
    menu:
        'Наблюдать за битвой' if game.army.force >= 0: # Армия Тьмы теряет 10% силы и разбирается с противником без вмешательства дракона.
            'Это становится переломным моментом битвы. На закате разрозненные и разбитые войска людей отступают, открывая чудовищам путь вглубь страны.'
            $ game.army.power_percentage -= army_decimator
            
        'Атаковать': #Дракон бережёт армию и сам уничтожает наиболее опасных врагов
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
                $ reinforcement_used = True    
    jump lb_orgy
    
label lb_orgy:
    show expression 'img/bg/special/city_raze.png' as bg
    game.dragon 'Мы победили!'
    mistress 'Да. Благодаря тебе, твоему роду и детям твоего рода... Как давно я ждала этого. Даю тебе и армии три дня на разграбление города, а затем мы начнём строить ПЕРВУЮ | ВСЕМИРНУЮ | ИМПЕРИЮ!'
    game.dragon 'Вы слышали Владычицу, воины мои. Тащите всех девок ко мне и кидайте в кучу!'    
    show expression 'img/bg/special/girls.png' as bg
    pause (500.0)
    'Прелюдия к победной оргии'
    show expression 'img/bg/special/orgy.png' as bg
    pause (500.0)    
    'Победная оргия'
    jump lb_you_win
