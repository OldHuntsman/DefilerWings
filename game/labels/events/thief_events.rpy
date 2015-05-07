# coding=utf-8
label lb_event_thief_spawn(thief):
    show expression "img/scene/thief.png" as bg
    nvl clear
    "[thief.title] по имени [game.thief.name] хочет порыться в сокровищнице дракона"
    nvl clear
    thief "Сокровища станут моими!"
    return

label lb_event_thief_steal_items(thief, items):
    $ descriptions = "\n".join(game.lair.treasury.treasures_description(items))
    show expression "img/scene/loot.png" as bg
    nvl clear
    "[game.thief.name] выкрал из сокровищницы: [descriptions]"
    thief "Вот это дело! Еле живым ушел. Зато теперь я могу жить в роскоши как король до конца дней сових!"
    nvl clear
    return

label lb_event_thief_lair_unreachable(thief):
    thief "Чертов дракон не мог выбрать себе логово в более доступном месте? Как туда добраться-то? Вот же гадство.."
    return

label lb_event_thief_prepare(thief):
    thief "Если я хочу уйти из дракньей берлоги живым и богатым, мне лучше как следует подговоиться к Делу."
    return

label lb_event_thief_prepare_usefull(thief):
    thief "Подготовка не прошла даром."
    return

label lb_event_thief_receive_item(thief, item):
    show expression "img/scene/quest_thief.png" as bg
    nvl clear
    "[game.thief.name] планомерно готовится к большому делу. Его новое приобретение: [item.name]"
    thief "Это мне пригодится!"
    nvl clear
    return

label lb_event_thief_prepare_useless(thief):
    thief "Чёрт! А я так надеялся получить что-то полезное для Большого Дела."
    return

label lb_event_thief_lair_enter(thief):
    thief "Ну вот и оно - логово дракона. Я войду словно тень и выскользну обратно с мешком сокровищ тяжким как мои грехи..."
    return

label lb_event_thief_die_item(thief, item):
    thief "Я умер от [item.name]. Это сообщение - ошибка."
    return

label lb_event_thief_die_inaccessability(thief):
    "[thief.title] [game.thief.name] не смог даже забраться в логово - укрепления слишком надёжные."
    thief 'Проклятый дракон окопался лучше чем король цвергов - стены, рвы, ставни, решётки и запоры... я не вижу ни единой лазейки. Видать такое дело мне не по зубам.'
    return

label lb_event_thief_die_trap(thief, trap):
    $ txt = game.interpolate(random.choice(txt_thief_fail[trap.id]))
    '[txt]' 
    return

label lb_event_thief_pass_trap(thief):
    $ txt = game.interpolate(random.choice(txt_thief_success[trap.id]))
    '[txt]' 
    return

label lb_event_thief_receive_no_item(thief):
    "Вор ничего не получил"
    return