# Как это работает
#
# В листе map_data содержатся названия локаций
# По маске 'img/map/button_<localtion>_%s.png' выбираются картинки для imagebutton
# TODO: добавить описание для Action
#
# Добавление локации на карте
# Для того чтобы добавить локацию на карте, нужно добавить в лист map_data название этой локации (location, name)
# где location - внутреннее название локации, а name - отображаемое название локации пользователю
# и добавить как минимум две картинки в img/map/ с названиями button_<location>_idle и button_<location>_hover
# для положений не выделенной локации и локации при наведении соотвественно.
# Изображения должны по размеру совпадать с размером задника и содержать только саму кнопку - все остальное прозрачный альфа-слой.
#
# TODO: Можно добавить map_data куда-нибудь в Game, для того чтобы была возможность управления налету.

init python:
    style.map_tooltip = Style("prompt")
    style.map_tooltip.background = Frame("img/bg/logovo.png", 5,5)

screen main_map:
    python:
        map_data = [("sea", "Море"),
                    ("mordor", "Мордор"),
                    ("sky", "Небеса"),
                    ("forest", "Лес"),
                    ("smugler", "Приют контрабандиста"),
                    ("mountain", "Гора"),
                    ("road", "Дороги"),
                    ("ruin", "Руины"),
                    ("gremlin", "Гремлины"),
                    ("city", "Город"),
                    ("plains", "Равнины")]
    
    default map_tooltip = Tooltip("None") #Подсказка на что сейчас наведена мышка
    default status_bar_tooltip = Tooltip("None") #Тултип для статусбара, если не объявить в родительском окне, то почему-то не работает.
    
    fixed:
        fit_first True  #Принимаем размер следущей картинки. Нужно для корректного отображения подсказки посередине.
        add "img/map/ground.png"
    
        for target in map_data:
            imagebutton: # target
                auto "img/map/button_" + target[0] + "_%s.png"
                action Return(target[0])
                focus_mask True
                hovered map_tooltip.Action(target[1])
    
        if map_tooltip.value != "None": #Костыль-костылык. Не показываем подсказу если у нее значение по умолчанию
            frame:
                style "map_tooltip"
                xpadding 10
                ypadding 5
                xalign 0.5
                yalign 0.01
                text map_tooltip.value:
                    xalign 0.5
                    
    #Выводим из под действия fixed
    use status_bar
    if game.lair is not None:
        use to_lair_button
            
init python:
    style.status_bar_tooltip = Style("prompt")
    style.status_bar_tooltip.background = Frame("img/bg/logovo.png", 5,5)
    
screen status_bar:
    default status_bar_tooltip = Tooltip("None")
    fixed:
        xalign 1.0
        xmaximum 320
        
        add "img/bg/status-bar.png"
        
        text "%d" % game.dragon.energy():
            pos(63,365)
            anchor (0.5,0.5)
            size 30
            color "a7926d"      #Цвет взял с шаблона, но тут он почему-то выглядит по-другому.
            outlines [(2, "#0004", 0, 0),(4, "#0003", 0, 0),(6, "#0002", 0, 0),(8, "#0001", 0, 0)]
        mousearea:              #Зона при наведении на которую всплывет подсказка
            area(42,342,45,45)
            hovered status_bar_tooltip.Action("Энергия")
        
        if status_bar_tooltip.value != "None": #Костыль аналогичный map_tooltip
            frame:
                style "status_bar_tooltip"
                xpadding 10
                ypadding 5
                pos(158,396)
                text status_bar_tooltip.value:
                    xalign 0.5
            
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