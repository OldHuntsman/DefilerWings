# coding=utf-8
python:
    witch = Sayer(game_ref=game)
    witch.avatar = "img\avahuman\witch"
    witch.name = "Ведьма"

label lb_location_ruin_main:
    show expression 'img/bg/special/haunted.png' as bg
    
    menu:
        'Посетить загадочную ведьму':
            show expression 'img/scene/witch.png' as bg
            if game.dragon.lust == 3: 
                call lb_witch_agree
            else:
                call lb_witch_refuse
            
        'Уйти прочь':
            return
        
    return
    
label lb_witch_agree:
    witch 'Услуга за услугу.'
    menu:
        'Дать себя подоить':
            'Ведьма выдаивает дракона досуха'
            $ game.dragon.lust = 0
            call lb_witch_reward
            
        'Уйти':
            return
    
    return

label lb_witch_refuse:
    #TODO: сделать фразу от имени ведьмы
    witch 'Ты уже потратил слишком много семени. Мне не нужны жалкие остатки. Возвращайся когда отдохнёшь.'
    
    return

label lb_witch_reward:
    witch 'Выбери награду.'
    menu:
        'Исцели меня' if game.dragon.health < 2:
            $ game.dragon.health = 2
            'Раны затянулись'
        'Дай мне золота':
            #TODO: нужно чтобы ведьма давала по 5 дублонов на уровень дракона
            witch 'Вот тебе [gain] дублонов.'
        'Поколдуй для меня':
            witch 'Какое заклинание ты хочешь?'
            #TODO: Сделать меню заклинаний такое же как когда колдует сам дракон но без траты маны и даже при условии что дракон колдоватьв вообще не умеет
            
        'У меня всё есть':
            return
            
    
    return