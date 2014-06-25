# Как это работает
#
# В листе map_data содержатся названия локаций
# По маске 'img/map/button_<localtion>_%s.png' выбираются картинки для imagebutton
# TODO: добавить описание для Action
#
# Добавление локации на карте
# Для того чтобы добавить локацию на карте, нужно добавить в лис map_data название этой локации (location)
# и добавить как минимум две картинки в img/map/ с названиями button_<location>_idle и button_<location>_hover
# для положений не выделенной локации и локации при наведении соотвественно.
# Изображения должны по размеру совпадать с размером задника и содержать только саму кнопку - все остальное прозрачный альфа-слой.
#
# TODO: Можно добавить map_data куда-нибудь в Game, для того чтобы была возможность управления налету.


screen main_map:
    python:
        map_data = []
        map_data.append("sea")
        map_data.append("mordor")
        map_data.append("sky")
        map_data.append("forest")
        map_data.append("smugler")
        map_data.append("mountain")
        map_data.append("road")
        map_data.append("ruin")
        map_data.append("gremlin")
        map_data.append("city")
        map_data.append("plains")
        
    add "img/map/ground.png"
    
    for target in map_data:
        imagebutton: # target
            auto "img/map/button_" + target + "_%s.png"
            action Return(target)
            focus_mask True
    
    use status_bar
    if game.lair is not None:
        use to_lair_button
            
screen status_bar:
    fixed:
        xalign 1.0
        xmaximum 320
        
        add "img/bg/status-bar.png"
            
screen to_lair_button:
    fixed:
        xalign 1.0
        xmaximum 320
        textbutton "{font=fonts/Tchekhonin2.ttf}В{/font} {font=fonts/times.ttf}пещеру{/font}":
            pos (72,649)
            xysize (174,36)
            text_xalign 0.5
            text_yalign 0.5
            background "img/bg/logovo.png"
            text_size 22
            action Jump("lb_location_lair_main")