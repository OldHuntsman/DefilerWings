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
    return

label lb_war_border:
    # TODO: Дракон ведёт свою армию на вольные земли. На протяжении всех событий отступать нельзя - дракон умрёт или победит. Один раз можно попросить госпожу одолеть любого врага вместо дракона.
    # Чтобы пройти АТ нужно взять пограничную крепость. Дракон берёт на себя катапульты, армия штурмует стены.
    # Если и дракон и армия победили, засчитываем победу.
    # Если дракон победил, но армия слишком слаба даём второй энкаунтер для дракона - воздушный флот цвергов приходит
    # на помощь осаждённым, дракон должен их победить.
    python:
        army_battle = True #Из боя теперь нельзя отступить
        actual_army_force = army.force
        army_decimator = army.force/10
    
    show expression 'img/bg/special/dark_march.png' as bg
    'Сражение у границ, Армия Тьмы вступает в битву. Катапульты являются ключевым звеном обороны.'
    
    $ game.foe = core.Enemy('catapult', game_ref=game)
    $ narrator(show_chances(game.foe))
            
    menu:
        'Наблюдать за битвой' if actual_army_force >= 0: # Армия Тьмы теряет 10% силы и разбирается с противником без вмешательства дракона.
            'Армия Тьмы несёт потери, но передовые отряды прорываются к катапультам и уничтожают их. Теперь победа всего в одном шаге.'
            $ actual_army_force -= army_decimator
            
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
        'Наблюдать за битвой' if actual_army_force >= 0: # Армия Тьмы теряет 10% силы и разбирается с противником без вмешательства дракона.
            'Тяжелые летучие крейсера демонстративно зависают над скоплением монстров и скидывают прямо на головы воинам Владычицы пузатые бочки с заженнйми фитилями. Земля озаряется вспышками и заливается текучим огнём. Объятые пламенем гоблины с визгоми разбегаются и катаются по земле пытвась погасить огонь. Когда запас бомб на кораблях подходит к концу, они мерно разворачиваются и уходят на базу невредимыми. Эта атака стоила Армии Тьмы днсятой части воинов!'
            'Тем не менее, пограничные войска людей выдохнулись и вынуждены были отступить. Путь вглубь страны открыт.'
            $ actual_army_force -= army_decimator
            
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
        'Наблюдать за битвой' if actual_army_force >= 0: # Армия Тьмы теряет 10% силы и разбирается с противником без вмешательства дракона.
            ''
            $ actual_army_force -= army_decimator
            
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
        'Наблюдать за битвой' if actual_army_force >= 0: # Армия Тьмы теряет 10% силы и разбирается с противником без вмешательства дракона.
            'Это становится переломным моментом битвы. На закате разрозненные и разбитые войска людей отступают, открывая чудовищам путь вглубь страны.'
            $ actual_army_force -= army_decimator
            
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
        'Наблюдать за битвой' if actual_army_force >= 0: # Армия Тьмы теряет 10% силы и разбирается с противником без вмешательства дракона.
            'Это становится переломным моментом битвы. На закате разрозненные и разбитые войска людей отступают, открывая чудовищам путь вглубь страны.'
            $ actual_army_force -= army_decimator
            
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
        'Наблюдать за битвой' if actual_army_force >= 0: # Армия Тьмы теряет 10% силы и разбирается с противником без вмешательства дракона.
            'Это становится переломным моментом битвы. На закате разрозненные и разбитые войска людей отступают, открывая чудовищам путь вглубь страны.'
            $ actual_army_force -= army_decimator
            
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
        'Наблюдать за битвой' if actual_army_force >= 0: # Армия Тьмы теряет 10% силы и разбирается с противником без вмешательства дракона.
            'Это становится переломным моментом битвы. На закате разрозненные и разбитые войска людей отступают, открывая чудовищам путь вглубь страны.'
            $ actual_army_force -= army_decimator
            
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
        'Наблюдать за битвой' if actual_army_force >= 0: # Армия Тьмы теряет 10% силы и разбирается с противником без вмешательства дракона.
            'Это становится переломным моментом битвы. На закате разрозненные и разбитые войска людей отступают, открывая чудовищам путь вглубь страны.'
            $ actual_army_force -= army_decimator
            
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
    rerutn
    
label lb_orgy:
    'Красочное описание победной оргии'
    $ game.win()
