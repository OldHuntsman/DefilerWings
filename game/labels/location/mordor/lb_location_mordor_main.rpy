label lb_location_mordor_main:
    $ place = 'mordor' 
    show place as bg
    nvl clear
    
    if game.dragon.energy() == 0:
        'Даже драконам надо иногда спать. Особенно драконам!'
        return
        
    menu:
        'Армия Тьмы':
            $ pass
        'Аудиенция с владычицей':
            if game.is_quest_complete:
                menu:
                    "Продолжить род?"
                    "Да":
                        call lb_choose_dragon
                    "Нет":
                        pass
            else:
                "Текущее задание:\n[game.quest_text]\n[game.quest_time_text]"
        'Назад':
            $ pass
        
    return
    
label lb_location_mordor_questtime:
    $ place = 'mordor' 
    show place as bg
    show screen status_bar
    "Ты выполнил задание и за это положена награда."
    if game.is_quest_complete:
        call lb_choose_dragon
    else:
        "Ты проиграл. Какая досада."
    return