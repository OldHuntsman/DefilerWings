label lb_event_knight_spawn(knight):
    show expression "img/scene/oath.png" as bg
    nvl clear
    "[knight.title] принимает на себя священный обет убить дракона"
    knight "Готовься исчадие зла, я иду за тобой!"
    return

label lb_event_knight_receive_item(knight, item):
    show expression "img/scene/quest_knight.png" as bg
    nvl clear
    "[item.name]"
    return
