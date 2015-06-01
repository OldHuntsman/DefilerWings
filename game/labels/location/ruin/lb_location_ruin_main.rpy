# coding=utf-8
label lb_location_ruin_main:
    python:
        if not renpy.music.is_playing():
            renpy.music.play(get_random_files('mus/ambient'))    
    hide bg
    show expression 'img/bg/special/haunted.png' as bg

    python:
        witch = core.Sayer(game_ref=game)
        witch.avatar = "img/avahuman/witch.jpg"
        witch.name = "Ведьма"
    
    if game.dragon.energy() == 0:
        'Даже драконам надо иногда спать. Особенно драконам!'
        return
        
    menu:
        'Посетить ведьму':
            show expression 'img/scene/witch.png' as bg
            if game.dragon.lust == 3: 
                call lb_witch_agree from _call_lb_witch_agree
            else:
                call lb_witch_refuse from _call_lb_witch_refuse
            
        'Уйти прочь':
            return
        
    return
    
label lb_witch_agree:
    nvl clear
    witch 'Услуга за услугу. Я помогу тебе если ты поделишься со мной своей уникальной спермой. Она нужна мне для алхимических нужд. Не бойся, процесс приятный, тебе понравится. Только учти - я высосу из тебя всё до капли!'
    menu:
        'Дать себя подоить':
            $ game.dragon.drain_energy()            
            stop music fadeout 1.0            
            show expression "img/scene/witch_sex.png" as xxx
            play sound "sound/milking.ogg"
            pause (500.0)
            'Ведьма достаёт ведро и приступает к долгому но приятному процессу. Чтобы выдоить дракона досуха, ей приходится без устали работать ротиком и руками в течение нескольких часов, но похоже она ОЧЕНЬ хочет драконье семя. Всё что только можно добыть.'
            hide xxx  
            $ game.dragon.lust = 0
            stop sound fadeout 1.0
            call lb_witch_reward from _call_lb_witch_reward
            
        'Уйти':
            return
    
    return

label lb_witch_refuse:
    nvl clear    
    witch 'Я бы рада тебе помочь, но всё на свете требует оплаты. А ты уже потратил слишком много семени на деревенских потаскушек. Мне не нужны жалкие остатки. Возвращайся когда отдохнёшь.'
    
    return

label lb_witch_reward:
    nvl clear    
    witch 'Мммм... Какая густота, какие объёмы. На год-другой мне этого хватит. Удружил чешуйчатый. Проси чего хочешь!'
    menu:
        'Исцели меня' if game.dragon.health < 2:
            $ game.dragon.health = 2
            'Раны затянулись'
        'Дай мне золота':
            python:
                gain = game.dragon.level + 1
                game.lair.treasury.dublon += gain
            witch 'Дракон клянчит золото? Ну и дела! Ладно, вот все дублоны что у меня есть: [gain]. Это того стоило.'
        'Научи меня колдовству':
            witch 'Я передам тебе часть своей силы, но это не навсегда. Ты сможешь сотворить одно заклятье по своему выбору когда тебе потребуется...'
            $ game.dragon.spells.append('griffin_meat')
            # старый вариант "поколдуй для меня"
            # $ game.choose_spell(u"Отказаться от заклинания")   
        'У меня всё есть':
            witch 'Оооо... да уж не влюбился ли ты? Ха-ха. Шучу. Спасибо за семя - приходи в любой момент если нужно будет ещё... ммм... разрядиться. Мой ротик к всегда к твоим услугам, здоровяк.'
            return
            
    
    return