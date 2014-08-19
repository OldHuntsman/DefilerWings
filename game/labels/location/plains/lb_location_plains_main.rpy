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
    'Ярмарка. Тут юноши присматривают невест из окрестных деревень, а крестьяне демонстрируют свой лучший скот.'
    nvl clear
    menu:
        'Красавица':
            $ game.dragon.drain_energy()
            $ description = game.girls_list.new_girl('peasant')
            'Сцена погони. Все разбегаются, дракон остаётся с пойманной девушкой.'
            nvl clear
            game.girl "[description]"
            call lb_nature_sex      
            return

        'Бык':
            $ game.dragon.drain_energy()
            $ game.foe = core.Enemy('bull', gameRef=game, base_character=NVLCharacter)
            call lb_fight
            menu:
                'Сожрать призового быка' if game.dragon.hunger > 0:
                    'Бык съеден. -1 к голоду, +1 к похоти. Ярость обнуляется.'
                    $ game.dragon.bloodiness = 0
                    $ if game.dragon.lust < 3: game.dragon.lust += 1
                    $ game.dragon.hunger -= 1
                'Уйти':
                    return
            return
            
        'Оставить их в покое' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
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
