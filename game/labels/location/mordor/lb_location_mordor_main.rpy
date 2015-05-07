# coding=utf-8
label lb_location_mordor_main:
    $ place = 'mordor' 
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
    menu:
        'Получить награду' if game.is_quest_complete:
            # Если делаем подарок - удаляем его из списка сокровищ
            if game.quest_task == 'gift' and len(game.lair.treasury.jewelry) > 0:
                $ del game.lair.treasury.jewelry[game.lair.treasury.most_expensive_jewelry_index]
            mistress 'Иди ко мне'
            'Дракон оплодотворяет владычицу и на свет появляется новый выводок.'
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
        "Ты выполнил задание и за это положена награда."
        call lb_choose_dragon
    else:
        $ game.dragon.die()
        menu:
            "Квест провален. Ты проиграл. Какая досада."
            "Попробовать еще раз":
                call lb_choose_dragon
                return
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
    'Сражение у границ. Катапульты являются ключевым звеном обороны.'
    $ game.foe = core.Enemy('catapult', game_ref=game)
    $ narrator(show_chances(game.foe))
            
    menu:
        # Тут должна быть проверка силы армии. Если армия не может победить, опция не должна быть активной.
        'Наблюдать за битвой':
            # TODO: Армия теряет дополнительно 10% от своей начальной боевой силы (в сумме 20%) и энкаунтер выигран без вмешательства дракона.
            $ pass
            
        'Сокрушить катапульты': 
            # TODO: Сделать бой без отступления.
            call lb_fight
            # TODO: Если армия недостаточно сильна чтобы победить, переходим к схватке с воздушным флотом. Если АТ сильная, сразу переходим на следующий энкаунтер (битва в поле). Армия теряет 10% начальной боевой силы.
            call lb_war_field

        'Молить Госпожу о помощи':
            # TODO: Проверяем не использована ли ещё помощь Госпожи. Если нет - госпожа уничтожает катапульты и энкаунтер дракона выигран. Если уже использована - Госпожа отказываетося помогать. возвращаемсмя к прошлому выбору.
            # TODO: Если армия недостаточно сильна чтобы победить, переходим к схватке с воздушным флотом. Если АТ сильная, сразу переходим на следующий энкаунтер (битва в поле)
            call lb_war_field
            
    'Воздушный флот цвергов приходит на помощь'
    $ game.foe = core.Enemy('airfleet', game_ref=game)
    $ narrator(show_chances(game.foe))
    
    call lb_war_field
    menu:
        'Уничтожить воздушный флот': 
            # TODO: Сделать бой без отступления.
            call lb_fight
            # TODO: Если армия недостаточно сильна чтобы победить, переходим к схватке с воздушным флотом. Если АТ сильная, сразу переходим на следующий энкаунтер (битва в поле)

        'Молить Госпожу о помощи':
            $ pass
            # TODO: Проверяем не использована ли ещё помощь Госпожи. Если нет - госпожа уничтожает воздушный флот и энкаунтер дракона выигран. Если уже использована - Госпожа отказываетося помогать. возвращаемсмя к прошлому выбору.

    call lb_war_field

    
label lb_war_field:
    # TODO: Армия продвигается вглубь страны и встречает объединённые войска Вольных Народов. Дракон должен победить титана, армия сражается с войском.
    # Если дракон и АТ победили, продвигаемся дальше. Если дракон победил а АТ проигрывает, даём дракону схватку против короля людей.
    'Сражение в чистом поле'
    call lb_war_siege
    return
    
label lb_war_siege:
    # TODO: Армия Тьмы осаждает столицу людей. Дракон должен пробить огромные ворота чтобы армия могла ворваться в город.
    # Если дракон и АТ победили, продвигаемся дальше. Если дракон победил а АТ проигрывает, даём дракону схватку
    # против городской стражи.
    'Осада столицы'
    call lb_war_final
    return

    
label lb_war_final:
    # TODO: Армия Тьмы захватила город, но центральная цитадель ещё держится. Дракон должен схватиться в воздухе с ангелом-хранителем, пока АТ штурмует.
    # Если дракон и АТ победили, продвигаемся дальше. Если дракон победил а АТ проигрывает, даём дракону схватку
    # против стального стража цвергов.
    # После окончательной победы переходим к сцене финальной оргии и концу игры.
    'Битва за цитадель'
    jump lb_orgy
    
label lb_orgy:
    'Красочное описание победной оргии'
    $ game.win()
