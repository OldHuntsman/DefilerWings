label lb_location_mountain_main:
    $ place = 'mountain'
    show expression get_place_bg(place) as bg
    nvl clear
    $ nochance = game.poverty.value*10      
    $ choices = [("lb_enc_miner", 10),
                ("lb_enc_dklad", 10),
                ("lb_enc_lowmines", 10),
                ("lb_enc_mines", 10),
                ("lb_enc_highmines", 10),   
                ("lb_enc_dmines", 10),                
                ("lb_enc_ram", 10),
                ("lb_enc_bear", 10),   
                ("lb_enc_jotun", 10),
                ("lb_enc_ifrit", 10),
                ("lb_enc_highpass", 10),
                ("lb_enc_smuglers", 10),
                ("lb_enc_frontgates", 10),
                ("lb_enc_cavegates", 10),
                ("lb_enc_noting", nochance),]
    $ enc = core.Game.weighted_random(choices)
    $ renpy.call(enc)
        
    return
    
    
label lb_enc_miner:
    
    return
    
label lb_enc_dklad:
    
    return
    
label lb_enc_mines:
    
    return
    
label lb_enc_ram:
    
    return
    
label lb_enc_bear:
    
    return
    
label lb_enc_jotun:
    
    return
    
label lb_enc_ifrit:
    
    return
    
label lb_enc_smuglers:
    
    return
   
label lb_enc_frontgates:
    
    return
    
label lb_enc_cavegates:
    
    return