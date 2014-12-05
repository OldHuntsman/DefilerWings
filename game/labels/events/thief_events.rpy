label lb_event_thief_spawn(thief):
    show expression "img/scene/thief.png" as bg
    nvl clear
    "[thief.title] по имени [game.thief.name] хочет порыться в сокровищнице дракона"
    nvl clear
    thief "Сокровища станут моими!"
    return

label lb_event_thief_receive_item(thief, item):
    show expression "img/scene/quest_thief.png" as bg
    nvl clear
    "[game.thief.name] планомерно готовится к большому делу. Его новое приобретение: [item.name]"
    thief "Это мне пригодится!"
    nvl clear
    return

