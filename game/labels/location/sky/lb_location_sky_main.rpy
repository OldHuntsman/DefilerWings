label lb_location_sky_main:
    $ place = 'sky'
    show expression get_place_bg(place) as bg    
    
    $ place = 'sky'
    show expression get_place_bg(place) as bg
    nvl clear
    
<<<<<<< HEAD
    if not game.dragon.can_fly: 
        '[game.dragon.name] с тоской смотрит в небо. Если бы только он умел летать...'
=======
    if game.dragon.energy() == 0:
        'Даже драконам надо иногда спать. Особенно драконам!'
>>>>>>> OldHuntsman/master
        return
        
    if not game.dragon.can_fly: 
        '[game.dragon.name] с тоской смотрит в небо. Если бы только он умел летать...'
        return
    
    $ choices = [("lb_enc_", 10),
                ("lb_enc_", 10),
                ("lb_enc_", 10),
                ("lb_enc_", 10),
                ("lb_enc_", 10),   
                ("lb_enc_", 10),
                ("lb_enc_", 10),
                ("lb_enc_", 10),
                ("lb_enc_", 10),
                ("lb_enc_", 10),
                ("lb_enc_", 10),
                ("lb_enc_", 10),
                ("lb_enc_", 10),
                ("lb_enc_", 10),
                ("lb_enc_", 10),   
                ("lb_enc_", 10),
                ("lb_enc_", 10),
                ("lb_enc_", 10),
                ("lb_enc_", 10),
                ("lb_enc_", 10),
                ("lb_enc_", 10),
                ("lb_patrool_sky", 3*game.mobilization.level),
                ]
    $ enc = core.Game.weighted_random(choices)
    $ renpy.call(enc)
    
    return
    