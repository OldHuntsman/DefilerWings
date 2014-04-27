screen main_map:
    # Вариант отобаржаение статус-бара. Но в этом варианте он отображается не сразу.
    #on "show" action Show("status_bar")
    #on "replace" action Show("status_bar")
    #on "hide" action Hide("status_bar")
    #on "replaced" action Hide("status_bar")

        
    add "img/map/ground.png"
    
    imagebutton: # Sea
        auto "img/map/button_sea_%s.png" 
        action NullAction()
        focus_mask True
    imagebutton: # Cave
        auto "img/map/button_cave_%s.png" 
        action NullAction()
        focus_mask True
    imagebutton: # Cloud1
        auto "img/map/button_cloud1_%s.png" 
        action NullAction()
        focus_mask True
    imagebutton: # Cloud2
        auto "img/map/button_cloud2_%s.png" 
        action NullAction()
        focus_mask True
    imagebutton: # Forest
        auto "img/map/button_forest_%s.png" 
        action NullAction()
        focus_mask True
    imagebutton: # Island
        auto "img/map/button_island_%s.png" 
        action NullAction()
        focus_mask True
    imagebutton: # Mountain
        auto "img/map/button_mountain_%s.png" 
        action NullAction()
        focus_mask True
    imagebutton: # Road
        auto "img/map/button_road_%s.png" 
        action NullAction()
        focus_mask True
    imagebutton: # Ruin
        auto "img/map/button_ruin_%s.png" 
        action NullAction()
        focus_mask True
    imagebutton: # Strange
        auto "img/map/button_strange_%s.png" 
        action NullAction()
        focus_mask True
    imagebutton: # Town
        auto "img/map/button_town_%s.png" 
        action NullAction()
        focus_mask True
    imagebutton: # Village
        auto "img/map/button_village_%s.png" 
        action NullAction()
        focus_mask True

screen status_bar:
    fixed:
        xalign 1.0
        xmaximum 320
        
        add "img/bg/status-bar.png"
        textbutton "{font=fonts/Tchekhonin2.ttf}В{/font} {font=fonts/times.ttf}пещеру{/font}":
            pos (72,649)
            xysize (174,36)
            text_xalign 0.5
            text_yalign 0.5
            background "img/bg/logovo.png"
            text_size 22
            action Jump("lair")
