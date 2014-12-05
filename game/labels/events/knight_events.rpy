label lb_event_knight_spawn(knight):
    show expression "img/scene/oath.png" as bg
    nvl clear
    "[knight.title] принимает на себя священный обет убить дракона"
    knight "Готовься исчадие зла, я иду за тобой!"
    return

label lb_event_knight_receive_item(knight, item):
    show expression "img/scene/quest_knight.png" as bg
    nvl clear
    "Рыцарь выполняет квест и получает [item.name]"
    knight "Теперь дракону не уйти от моего возмездия!"
    return
