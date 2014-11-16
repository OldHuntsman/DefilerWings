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
                # Если делаем подарок - удаляем его из списка сокровищ
                if game.quest_task == 'gift' and len(game.lair.treasury.jewelry) > 0:
                    $ del game.lair.treasury.jewelry[game.lair.treasury.most_expensive_jewelry_index]
                menu:
                    "Задание выполнено! Продолжить род?"
                    "Да":
                        call lb_choose_dragon
                    "Нет":
                        pass
            else:
                "Текущее задание:\n[game.quest_text]\n[game.quest_time_text]"
        'В земли Вольных Народов':
            $ pass
        
    return
    
label lb_location_mordor_questtime:
    $ place = 'mordor' 
    show place as bg
    show screen status_bar
    if game.is_quest_complete:
        "Ты выполнил задание и за это положена награда."
        call lb_choose_dragon
    else:
        $ game.defeat()
        "Квест провален. Ты проиграл. Какая досада."
        
    return