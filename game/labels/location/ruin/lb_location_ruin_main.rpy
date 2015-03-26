# coding=utf-8
label lb_location_ruin_main:
    show expression 'img/bg/special/haunted.png' as bg

    python:
        witch = core.Sayer(game_ref=game)
        witch.avatar = "img/avahuman/witch.jpg"
        witch.name = "Ведьма"

    witch "Приветствую тебя."
    
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
            python:
                gain = game.dragon.level * 5
                game.lair.treasury.dublon += gain
            witch 'Вот тебе [gain] дублонов.'
        'Научи меня колдовству':
            witch 'Я передам тебе часть своей силы, но это не навсегда. Ты сможешь сотворить одно заклятье по своему выбору когда тебе потребуется...'
            $ game.dragon.spells.append('griffin_meat')
            # старый вариант "поколдуй для меня"
            # $ game.choose_spell(u"Отказаться от заклинания")   
        'У меня всё есть':
            return
            
    
    return