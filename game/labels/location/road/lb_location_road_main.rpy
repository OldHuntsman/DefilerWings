label lb_location_road_main:
    $ place = 'road'
    show place
    show expression get_place_bg(place) as bg
    nvl clear
    $ nochance = game.poverty.value*10      
    $ choices = [("lb_enc_tornament", 10),
                ("lb_enc_fortification", 10),
                ("lb_enc_inn", 10),
                ("lb_enc_peasant_cart", 10),
                ("lb_enc_carriage", 10),   
                ("lb_enc_qesting_knight", 10),
                ("lb_enc_trader", 10),
                ("lb_enc_caravan", 10),
                ("lb_enc_lcaravan", 10),
                ("lb_enc_outpost", 10),
                ("lb_enc_noting", nochance),]
    $ enc = core.Game.weighted_random(choices)
    $ renpy.call(enc)
        
    return
    
    
label lb_enc_tornament:
    
    return
    
label lb_enc_fortification:
    
    return
    
label lb_enc_inn:
    
    return
    
label lb_enc_peasant_cart:
    
    return
    
label lb_enc_carriage:
    
    return
    
label lb_enc_qesting_knight:
    
    return
    
label lb_enc_trader:
    
    return
    
label lb_enc_caravan:
    
    return
   
label lb_enc_lcaravan:
    
    return
    
label lb_enc_outpost:
    
    return