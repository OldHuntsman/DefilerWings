# coding=utf-8
label lb_location_city_main:
        
    $ place = "city_gates"
    show place as bg
    
    if game.dragon.energy() == 0:
        dragon 'Даже драконам надо иногда спать. Особенно драконам!'
        return      
        
    menu:
        'Тайный визит' if game.dragon.mana > 0:
            'Дракон превращается в человека и проходит в город.'
            nvl clear
            call lb_city_walk
        'Ворваться в город':
            $ pass
        'Уйти прочь':
            return
            
    return
    
label lb_city_walk:
    show expression 'img/bg/city/inside.png' as bg
    'Загадочный путник проходит мимо бдительной стражи и входит в бурлящий жизнью город.'
    nvl clear
    menu:
        'Королевский дворец':
            call lb_city_palace
            
        'Кафедральный собор':
            call lb_city_cathedral
            
        'Мастерская ювелира':
            call lb_city_jewler
            
        'Покинуть город':
            return
            
    return

label lb_city_palace:
    'Плейсхолдер'
    nvl clear
    
    return
    
label lb_city_cathedral:
    'Плейсхолдер'
    nvl clear
    
    return
    
label lb_city_jewler:
    'Мастерская ювелира'
    nvl clear
    menu:
        'Купить драгоценности':
            'Плейсхолдер'
            #TODO: схема покупки драгоценностей.
        'Продать драгоценности':
            'Плейсхолдер'
            #TODO: схема продажи драгоценностей. Ювелир берёт вещь по 100% цене. Сделать как в сокровищнице: самая дорогая, самая дешёвая или случайная. Продемонстрировать и спросить продать / осавить?
        'Драгоценности на заказ':
            'Плейсхолдер'
            #TODO: схема крафта драгоценностей.
        'Вернуться на площадь':
            call lb_city_walk
    
    return
    