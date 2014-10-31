label lb_location_sea_main:
    $ place = 'sea'
    show expression get_place_bg(place) as bg
    nvl clear
    
    if game.dragon.energy() == 0:
        'Даже драконам надо иногда спать. Особенно драконам!'
        return
        
    if not game.dragon.can_swim: 
        '[game.dragon.name] пробует когтем солёную морскую влагу. Если бы только он умел дышать под водой...'
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
                ("lb_patrool_sea", 3*game.mobilization.level),
                
                ]
    $ enc = core.Game.weighted_random(choices)
    $ renpy.call(enc)
    
    return 