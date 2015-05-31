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
label lb_event_no_thief:
    "Не нашлось вора, готового ограбить драконa."
    return

label lb_event_no_knight:
    "Не нашлось рыцаря, готового бросить вызов дракону."
    return

label lb_event_sleep_start:
    return

label lb_event_sleep_new_year:
    return

label lb_event_sleep_end:
    return
