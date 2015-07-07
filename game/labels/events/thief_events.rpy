# coding=utf-8
label lb_event_thief_spawn(thief):
    show expression "img/scene/thief.jpg" as bg
    nvl clear
    "[thief.title] по имени [game.thief.name] хочет порыться в сокровищнице дракона"
    nvl clear
    thief "Сокровища станут моими!"
    return

label lb_event_thief_steal_items(thief, items):
    $ descriptions = "\n".join(game.lair.treasury.treasures_description(items))
    show expression "img/scene/loot.jpg" as bg
    nvl clear
    "[game.thief.name] выкрал из сокровищницы: [descriptions]"
    thief "Вот это дело! Еле живым ушел. Зато теперь я могу жить в роскоши как король до конца дней своих!"
    nvl clear
    return

label lb_event_thief_lair_unreachable(thief):
    nvl clear    
    thief "Чертов [game.dragon.kind] не мог выбрать себе логово в более доступном месте? Как туда добраться-то? Вот же гадство.."
    return

label lb_event_thief_prepare(thief):
    # nvl clear    
    # thief "Если я хочу уйти из дракньей берлоги живым и богатым, мне лучше как следует подготовиться к Делу."
    return

label lb_event_thief_prepare_usefull(thief):
    nvl clear    
    thief "Хе-хе... точно по плану!."
    return

label lb_event_thief_receive_item(thief, item):
    show expression "img/scene/quest_thief.jpg" as bg
    nvl clear
    "[game.thief.name] планомерно готовится к большому делу. Его новое приобретение: [item.name]"
    thief "Это мне пригодится!"
    nvl clear
    return

label lb_event_thief_prepare_useless(thief):
    nvl clear
    show expression "img/scene/quest_thief.jpg" as bg
    '[game.thief.name] хочет найти логово дракона, но безуспешно.'
    thief "Да где же прячется эта змеюка... Чёрт!"
    return

label lb_event_thief_lair_enter(thief):
    nvl clear
    show expression "img/scene/thief_in_lair.jpg" as bg
    thief "Ну вот и оно - логово дракона. Я войду словно тень и выскользну обратно с мешком сокровищ тяжким как мои грехи..."
    return

label lb_event_thief_die_inaccessability(thief):
    "[thief.title] [game.thief.name] не смог даже забраться в логово - укрепления слишком надёжные."
    thief 'Проклятый [game.dragon.kind] окопался лучше чем король цвергов - стены, рвы, ставни, решётки и запоры... я не вижу ни единой лазейки. Видать такое дело мне не по зубам.'
    return

label lb_event_thief_die_trap(thief, trap):
    nvl clear    
    show expression "img/scene/thief_in_lair.jpg" as bg    
    $ txt = game.interpolate(random.choice(data.lair_upgrades[trap].fail))
    '[txt]' 
    return

label lb_event_thief_pass_trap(thief, trap):
    if config.debug:
        'pass_trap [trap]'
    show expression "img/scene/thief_in_lair.jpg" as bg    
    $ txt = game.interpolate(random.choice(data.lair_upgrades[trap].success))
    '[txt]' 
    return

label lb_event_thief_receive_no_item(thief):
    nvl clear    
    show expression "img/scene/thief_in_lair.jpg" as bg    
    "Вор ничего не получил"
    return
    
# @Review: Alex: Added a bunch of new events to fill in the gaps:
label lb_event_thief_checking_accessability(thief):
    # Checking if thief can get past layer defences:
    # Debug message: thief(u"Проверяю неприступность")
    return
    
label lb_event_thief_checking_accessability_success(thief):
    # Thief can gain access:
    # Debug message: thief(u"I can get into the Layer!")
    return
    
label lb_event_thief_trying_to_avoid_traps_and_guards(thief):
    # Thief is trying to avoid traps and guards:
    # Debug message: thief(u"Пробую обойти ловушки и стражей")
    return
    
label lb_event_thief_retreat_and_try_next_year(thief):
    # Could not get passed traps and guards but did not die either:
    # Debug message: thief(u"Ниосилить, попробую в следущем году")
    thief "Пока что тут для меня крутовато... Надо подготовиться получше. Но я не сдамся!"
    return
    
label lb_event_thief_starting_to_rob_the_lair(thief):
    # Got past all traps and guards, thief is starting to rob the lair:
    # Debug message: thief(u"Начинаю вычищать логово")
    show expression "img/scene/loot.jpg" as bg    
    thief "Ух ты! Вот она сокровищница. И [game.dragon.kind], зараза прямо на золоте лежит... Ничего, я аккуратненько... надо только выбрать вещи поценнее."
    return

label lb_event_thief_took_an_item(thief, item):
    # Got an item!
    # Debug message: thief(u"Взял шмотку %s" % stolen_items[i])
    # show expression "img/scene/loot.jpg" as bg    
    # "[game.thief.name] аккуратно вытягивает из под брюха спящего дракона понравившийся предмет:"
    # "[item]"
    return
    
label lb_event_thief_lair_empty(thief):
    # There were no treasures in the lair:
    # Debug message: thief(u"В сокровищнице нечего брать. Сваливаю.")
    show expression "img/scene/thief_in_lair.jpg" as bg        
    thief "Тут больше нечем поживиться... проклятье, я думал драконы кудв богаче. Надо сваливать!"
    return
    
label lb_event_thief_awakened_dragon(thief, stolen_items):
    # Thief awakens the dragon and gets killed... stolen_items: items that dragon takes back from the thief.
    # Debug message: thief(u"Разбудил дракона")
    show expression "img/scene/wokeup.jpg" as bg    
    "Зазевашийся вор обрушивает кучку монет, которые со звоном раскатываются по полу."
    thief "Упс..."
    game.dragon "Так-так... какая встреча. А я то думал кто тут шебуршится."
    nvl clear
    "[game.dragon.fullname] раздирает неудачливого расхитителя сокровищ в клочья и перекусив снова ложится спать."
    return