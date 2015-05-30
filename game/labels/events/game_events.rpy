# coding=utf-8
label lb_event_mobilization_increase:
    show expression core.get_img("img/scene/mobilization") as bg
    nvl clear
    "Правители вольных народов обеспокоены бесчинством дракона. Они мобилизуют войска и усиливают охрану в своих владениях."
    return

label lb_event_poverty_increase:
    show expression core.get_img("img/scene/poverty") as bg
    nvl clear
    "Деяния дракона привели к росту бедности и разрухи в стране. Люди голодают, многие остались без крова и средств к существованию. Мобилизационный потенциал уменьшается."
    return