# coding=utf-8
label lb_event_mobilization_increase:
    show expression core.get_img("img/scene/mobilization") as bg
    nvl clear
    "Мобилизация выросла"
    return

label lb_event_poverty_increase:
    show expression core.get_img("img/scene/poverty") as bg
    nvl clear
    "Разруха выросла"
    return

label lb_event_creature_spawn:
    show expression core.get_img("img/scene/spawn") as bg
    nvl clear
    "Родилось существо"
    return
