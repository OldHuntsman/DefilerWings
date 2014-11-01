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
    
    $ nochance = game.poverty.value*3      
    $ choices = [("lb_enc_lumberjack", 10),
                ("lb_enc_onegirl", 10),
                ("lb_enc_wandergirl", 10),
                ("lb_enc_ogre", 10),
                ("lb_enc_deer", 10),   
                ("lb_enc_boar", 10),
                ("lb_enc_berries", 10),
                ("lb_enc_shrooms", 10),
                ("lb_enc_guardian", 10),
                ("lb_enc_lumbermill", 10),
                ("lb_enc_klad", 10),
                ("lb_patrool_forest", 3*game.mobilization.level),
                ("lb_enc_noting", nochance),]
    $ enc = core.Game.weighted_random(choices)
    $ renpy.call(enc)
    
    return 