# coding=utf-8
label lb_event_knight_spawn(knight):
    scene
    show expression "img/scene/oath.jpg" as bg
    nvl clear
    "[knight.title] принимает на себя священный обет убить дракона"
    knight "Готовься исчадие зла, я иду за тобой!"
    return

label lb_event_knight_receive_item(knight, item):
    scene
    show expression "img/scene/quest_knight.jpg" as bg
    nvl clear
    "Рыцарь выполняет квест и получает [item.name]"
    knight "Теперь дракону не уйти от моего возмездия!"
    return

label lb_event_knight_challenge_start(knight):
    scene
    show expression "img/scene/quest_knight.jpg" as bg
    nvl clear
    $ game.foe = knight
    "[knight.title] нашел логово где спит [game.dragon.name] [game.dragon.surname] и вызывает его на бой."
    knight "Выходи подлый [game.dragon.kind] на честной бой, на побраночку!!!"
    $ narrator(knight.intro % game.format_data)
    $ narrator(show_chances(knight))  #TODO: уровень опасности боя
    menu:
        "Принять вызов и защитить логово":
            "Вы вступаете в бой"
            return True
        "Бежать и бросить логово":
            # Тут, неверное должна быть проверка на успех побега дракона от рыцаря, но ее нет. (Нет, не нужна. Побег всегда успешен, просто дракон теряет логово, золото и баб - OH)
            if random.choice(range(4)) in range(3): # 75% что рыцарь останется
                knight "Я все равно тебя найду!"
                return False
            else:
                knight "Ты подлый трус [game.dragon.kind], такой враг меня не достоин"
                return False

label lb_event_knight_challenge_end(knight, result):
    if result in ["defeat", "retreat"]:
        "Дракон был повержен доблестным рыцарем."
    if result in ["win"]:
        "Дракон разорвал в клочья рыцаря."