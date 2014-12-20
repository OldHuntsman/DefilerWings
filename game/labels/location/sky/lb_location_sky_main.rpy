# coding=utf-8
label lb_location_sky_main:
    $ place = 'sky'
    show expression get_place_bg(place) as bg    
    nvl clear
    
    if game.dragon.energy() == 0:
        'Даже драконам надо иногда спать. Особенно драконам!'
        return
        
    if not game.dragon.can_fly: 
        '[game.dragon.name] с тоской смотрит в небо. Если бы только он умел летать...'
        return
        
    return
    # call lb_encounter_sky
    
label lb_encounter_sky:
    $ choices = [("lb_enc_cloud_castle", 10),
                 ("lb_enc_swan", 10),
                 ("lb_enc_griffin", 10),
                 ("lb_enc_skyboat", 10),
                 ("lb_enc_skyship", 10),
                 ("lb_abbey_found", 10),
                 ("lb_castle_found", 10),
                 ("lb_palace_found", 10),
                 ("lb_enc_fair_sky", 10),
                 ("lb_enc_caravan_sky", 10),
                 ("lb_enc_cannontower", 10),
                 ("lb_jotun_found", 10),
                 ("lb_ifrit_found", 10),
                 ("lb_enc_militia_sky", 10),
                 ("lb_patrool_sky", 3 * game.mobilization.level)]
    $ enc = core.Game.weighted_random(choices)
    $ renpy.call(enc)

    return

label lb_enc_cloud_castle:
    'Плейсхолдер'
    return
    
label lb_enc_swan:
    'Плейсхолдер'
    return
    
label lb_enc_griffin:
    'Плейсхолдер'
    return
    
label lb_enc_skyboat:
    'Плейсхолдер'
    return
    
label lb_enc_skyship:
    'Плейсхолдер'
    return
    
label lb_enc_fair_sky:
    'Плейсхолдер'
    return
    
label lb_enc_militia_sky:
    'Плейсхолдер'
    return
    
label lb_enc_caravan_sky:
    'Плейсхолдер'
    return
    
label lb_patrool_sky:
    'Плейсхолдер'
    return
    