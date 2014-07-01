label lb_location_plains_main:
    $ place = 'plain'
    show place
    nvl clear
      
    menu:
        'Рыскать за околицей':
            call lb_encounter_plains
            return
        'Одинокий хутор':
            $ pass
        'Маленький посёлок':
            $ pass
        'Деревня':
            $ pass
        'Село':
            $ pass
        'Городок':
            $ pass
        'Отступить':
            $ pass
        
    return
    
label lb_encounter_plains:
    $ choices = [("lb_enc_fair", 1000),
                ("lb_enc_girls", 10),
                ("lb_enc_militia", 10),
                ("lb_enc_mill", 10),
                ("lb_enc_granary", 10),
                ("lb_enc_cattle", 10)]
    $ enc = core.Game.weighted_random(choices)
    $ renpy.call(enc)
    return
    
    
label lb_enc_fair:
    'Ярмарка'
    menu:
        'Оставить их в покое':
            $ game.dragon.bloodiness = 3
            return
    
    return
    
    
label lb_enc_girls:
    'Девушки в лесу'
    
    return
    
    
label lb_enc_cattle:
    'Скот на выпасе'
    
    return

    
label lb_enc_militia:
    'На поле тренируются ополченцы-новобранцы'
    
    return
    
    
label lb_enc_mill:
    'Ветряная мельница'
    
    return

    
label lb_enc_granary:
    'Амбар полный зерна'
    
    
    return
