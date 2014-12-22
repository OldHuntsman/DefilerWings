# coding=utf-8
label lb_location_sea_main:
    $ place = 'sea'
    show expression get_place_bg(place) as bg
    nvl clear
    
    if game.dragon.energy() == 0:
        'Даже драконам надо иногда спать. Особенно драконам!'
        return
        
    if not game.dragon.can_swim: 
        '[game.dragon.name] пробует когтем солёную морскую влагу. Если бы только он умел дышать под водой...'
    else:
        call lb_encounter_sea
    return
    
label lb_encounter_sea:
    $ choices = [
        ("lb_enc_fishers", 10),
        ("lb_enc_yacht", 10),
        ("lb_enc_bark", 10),
        ("lb_enc_tuna", 10),
        ("lb_enc_shark", 10),
        ("lb_enc_sea_castle", 10),
        ("lb_enc_galeon", 10),
        ("lb_enc_diver", 10),
        ("lb_enc_mermaid", 10),
        ("lb_enc_merfolks", 10),
        ("lb_enc_mermaids", 10),
        ("lb_enc_shipwreck", 10),
        ("lb_patrool_sea", 3 * game.mobilization.level)]
    $ enc = core.Game.weighted_random(choices)
    $ renpy.call(enc)

    return 
    

label lb_enc_fishers:
    'Плейсхолдер'
    return
    
label lb_enc_yacht:
    'Плейсхолдер'
    return
    
label lb_enc_bark:
    'Плейсхолдер'
    return
    
label lb_enc_tuna:
    'Плейсхолдер'
    return
    
label lb_enc_shark:
    'Плейсхолдер'
    return
    
label lb_enc_sea_castle:
    'Плейсхолдер'
    return
    
label lb_enc_galeon:
    'Плейсхолдер'
    return
    
label lb_enc_diver:
    'Плейсхолдер'
    return
    
label lb_enc_mermaid:
    'Плейсхолдер'
    return
    
label lb_enc_merfolks:
    'Плейсхолдер'
    return
    
label lb_enc_mermaids:
    'Плейсхолдер'
    return
     
label lb_enc_shipwreck:
    'Плейсхолдер'
    return
    
label lb_patrool_sea:
    'Плейсхолдер'
    return