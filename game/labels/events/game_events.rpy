# coding=utf-8
init python:
    from pythoncode.utils import get_random_image
    
label lb_event_mobilization_increase:
    show expression get_random_image("img/scene/mobilization") as bg
    nvl clear
    "Rulers of the Free Kingdoms concerned with dragom mischief. Mobilization raises."
    return

label lb_event_poverty_increase:
    show expression get_random_image("img/scene/poverty") as bg
    nvl clear
    "Dragon evil deeds lead to devastation thorouht the Free Kingdoms. Poverty rises and mobilization piotential diminishing."
    return
    
label lb_event_no_thief:
    "There no thief in this land whio wants to take humble treashures of [game.dragon.fullname]."
    return

label lb_event_no_knight:
    "[game.dragon.fullname] have not famous enough to attract questing knights."
    return

label lb_event_sleep_start:
    '[game.dragon.fullname] sleeps...'
    nvl clear
    return

label lb_event_sleep_new_year:
    return

label lb_event_sleep_end:
    nvl clear
    '[game.dragon.fullname] rises from slumber!'
    return
