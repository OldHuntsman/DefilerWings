# coding=utf-8
init python:
    from pythoncode.utils import get_random_image
    
label lb_event_mobilization_increase:
    show expression get_random_image("img/scene/mobilization") as bg
    nvl clear
    "Правители вольных народов обеспокоены бесчинством дракона. Они мобилизуют войска и усиливают охрану в своих владениях."
    return

label lb_event_poverty_increase:
    show expression get_random_image("img/scene/poverty") as bg
    nvl clear
    "Деяния дракона привели к росту бедности и разрухи в стране. Люди голодают, многие остались без крова и средств к существованию. Мобилизационный потенциал уменьшается."
    return
label lb_event_no_thief:
    "Ни один вор не позарился пока на сокровища, которые собрал у себя в логове [game.dragon.fullname]."
    return

label lb_event_no_knight:
    "Во всём королевстве не нашлось героя, желающего бросить вызов дракону. Видимо [game.dragon.fullname] просто не успел ещё прославиться."
    return

label lb_event_sleep_start:
    '[game.dragon.fullname] засыпает, устав от нечестивых дел. Его сон продлится долго...'
    nvl clear
    return

label lb_event_sleep_new_year:
    return

label lb_event_sleep_end:
    nvl clear
    'Полный сил и коварной злобы, [game.dragon.fullname] просыпается в своём логове. Время для грабежа и насилия!'
    return
