# coding=utf-8
# How it works
#
# map_data list contains locations names
# Images for imagebutton selected with mask 'img/map/button_<location>_%s.png
# TODO: add description for Action
#
# Adding locations on a map
# To add location on a map, you should add tuple(<location>, <name>) to map_data list
# where <location> - internal location name, and <name> - location name displayed to user
# and add at least two images in img/map/ with names button_<location>_idle and button_<location>_hover
# for hovered and unhovered states respectively.
# Image's sizes should match bg sizes and contain only button -
# everything else is transparent alpha-layer.
#
# TODO: Можно добавить map_data куда-нибудь в Game, для того чтобы была возможность управления налету.

# Making a tooltip style.
# TODO: выпилить, сделав нормальный стиль для prompt
init python:
    from pythoncode.focus_mask_ext import FocusMaskCallable
    
    style.map_tooltip = Style("prompt")
    style.map_tooltip.background = Frame("img/bg/logovo.png", 5, 5)

screen main_map:
    python:
        # After adding or updating buttons IT's NECESSARY to generate new coordinates
        # with function focus_mask_ext.create_focus_mask_data. Resulting file should 
        # be settled at focus_mask_ext.COORDINATES_FILE_PATH.
        map_data = [
            ("sea", "Море"),
            ("mordor", "Земли Владычицы"),
            ("sky", "Небеса"),
            ("forest", "Лес"),
            ("smuggler", "Приют контрабандистов"),
            ("mountain", "Горы"),
            ("road", "Торговый тракт"),
            ("ruin", "Старые руины"),
            ("gremlin", "Деревня гремлинов"),
            ("city", "Столица"),
            ("plains", "Обжитые земли")
        ]
    
    default map_tooltip = Tooltip("None")  # Tootip about what mouse is hoovering now
    # status bar tooltip, if not declared in parent window, it doesn't work for some reason.
    default status_bar_tooltip = Tooltip("None")
    fixed:
        fit_first True  # Receiving size of next image. To display tooltip at middle correctly.
        add "img/map/ground.jpg"
    
        for target, description in map_data:
            imagebutton:  # target
                auto "img/map/button_" + target + "_%s.png"
                action Return("lb_location_%s_main" % target)
                focus_mask FocusMaskCallable(target)
                hovered map_tooltip.Action(description)
    
        if map_tooltip.value != "None":  # Don't show tooltip with default value
            frame:                      # Create little frame to show tooltip
                style "map_tooltip"     # Makes frame's style
                xpadding 10
                ypadding 5
                xalign 0.5
                yalign 0.01
                text map_tooltip.value:  # Print tooltip's text
                    xalign 0.5
        
        if game.dragon is not None:
            text u"{font=fonts/AnticvarShadow.ttf} Год %d э.д. (Прошло %d) {/font}" % (game.year, game.dragon.age)
    
    if game.dragon is not None:
        text "{font=fonts/AnticvarShadow.ttf} %d фартингов {/font}" % game.lair.treasury.money:
            xalign 0.7
            yalign 1
            size 25


    # Leaving from <fixed> effect
    use status_bar
    if game.lair is not None:
        use to_lair_button
    
    if game.dragon is not None and game.dragon.special_places_count > 0:
        use special_places 

# Making tooltip style.
# TODO: выпилить, сделав нормальный стиль для prompt
init python:
    style.status_bar_tooltip = Style("prompt")
    style.status_bar_tooltip.background = Frame("img/bg/logovo.png", 5, 5)
    
screen status_bar:
    default status_bar_tooltip = Tooltip("None")
    fixed:
        xalign 1.0
        xmaximum 320
        
        add "img/bg/status-bar.png"
        
        if game.dragon is not None and game.dragon.is_alive:
            text "%d" % game.dragon.energy():
                pos(65, 365)
                anchor(0.5, 0.5)
                size 30
                color "a7926d"      # Цвет взял с шаблона, но тут он почему-то выглядит по-другому.
                outlines[(2, "#0004", 0, 0), (4, "#0003", 0, 0), (6, "#0002", 0, 0), (8, "#0001", 0, 0)]
            mousearea:              # Area which shows tooltip when hoovered
                area(42, 342, 45, 45)
                hovered status_bar_tooltip.Action("Запас сил")

            text "%d" % game.dragon.reputation.level:
                pos(160, 365)
                anchor(0.5, 0.5)
                size 30
                color "a7926d"     
                outlines[(2, "#0004", 0, 0), (4, "#0003", 0, 0), (6, "#0002", 0, 0), (8, "#0001", 0, 0)]
            mousearea:              # Area which shows tooltip when hoovered
                area(140, 342, 45, 45)
                hovered status_bar_tooltip.Action("Дурная слава")

            add '%s' % game.dragon.avatar:
                pos(160, 155)
                anchor(0.5, 0.5)

            text "{font=fonts/AnticvarShadow.ttf}%s{/font}" % game.dragon.name:
                pos(160, 315)
                anchor(0.5, 0.5)
                size 25
                color "a7926d"     
                outlines[(2, "#0004", 0, 0), (4, "#0003", 0, 0), (6, "#0002", 0, 0), (8, "#0001", 0, 0)]

            text "%d" % game.dragon.mana:
                pos(260, 365)
                anchor(0.5, 0.5)
                size 30
                color "a7926d"     
                outlines[(2, "#0004", 0, 0), (4, "#0003", 0, 0), (6, "#0002", 0, 0), (8, "#0001", 0, 0)]
            mousearea:              # Area which shows tooltip when hoovered
                area(240, 342, 45, 45)
                hovered status_bar_tooltip.Action("Коварство")

            text "%s" % hunger_texts[game.dragon.hunger]:
                pos(160, 447)
                anchor(0.5, 0.5)
                size 23

            text "%s" % lust_texts[game.dragon.lust]:
                pos(160, 477)
                anchor(0.5, 0.5)
                size 23

            text "%s" % bloodlust_texts[game.dragon.bloodiness]:
                pos(160, 503)
                anchor(0.5, 0.5)
                size 23

            text "%s" % health_texts[game.dragon.health]:
                pos(160, 530)
                anchor(0.5, 0.5)
                size 23
        
        if status_bar_tooltip.value != "None":  # look map_tooltip at screen main_map
            frame:
                style "status_bar_tooltip"
                xpadding 10
                ypadding 5
                pos(158, 396)
                text status_bar_tooltip.value:
                    xalign 0.5
        
        if config.developer:
            textbutton "{font=fonts/Tchekhonin2.ttf}О{/font}{font=fonts/times.ttf}тладка{/font}":
                pos(72, 549)
                xysize(174, 36)
                text_xalign 0.5
                text_yalign 0.5
                background "img/bg/logovo.png"
                text_size 22
                action ShowMenu("lb_test_main")
                
screen special_places:
    fixed:
        xalign 1.0
        xmaximum 320
        textbutton "{font=fonts/Tchekhonin2.ttf}М{/font}{font=fonts/times.ttf}еста{/font}":
            pos(72, 599)
            xysize(174, 36)
            text_xalign 0.5
            text_yalign 0.5
            background "img/bg/logovo.png"
            text_size 22
            action Return("lb_special_places")
        
screen to_lair_button:
    fixed:
        xalign 1.0
        xmaximum 320
        textbutton "{font=fonts/Tchekhonin2.ttf}Л{/font}{font=fonts/times.ttf}огово{/font}":
            pos(72, 649)
            xysize(174, 36)
            text_xalign 0.5
            text_yalign 0.5
            background "img/bg/logovo.png"
            text_size 22
            action Return("lb_location_lair_main")