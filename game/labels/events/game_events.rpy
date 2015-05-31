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
