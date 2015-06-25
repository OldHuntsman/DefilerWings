# coding=utf-8
label lb_choose_dragon:
    # Хардкод на трех драконов.
    python:
        if renpy.music.get_playing(channel='music') != "mus/lullaby.ogg":
            renpy.music.play("mus/lullaby.ogg")           
    $ game.mobilization.level = 0
    hide bg
    python:
        lost = False
        if game.dragon is None:
            dragons = []
            dragons_choosed = []
        elif game.dragon.is_alive and not game.is_lost:
            data.achieve_restart("new_dragon")# событие для ачивок
            dragons = []
            dragons_choosed = []
            # добавляем 1 гоблина в армию тьмы
            game.army.add_warrior('goblin')
            # без выполненного квеста сюда попасть нельзя
            game.complete_quest()
        child_choose = None
        child_selected = None
        togle_dragonchoose_button = None
        if game.dragon and game.dragon.is_dead and len(dragons_choosed) == len(dragons):
            lost = True
    if lost:
        jump lb_game_over


    python hide:
        used_gifts = []
        used_avatars = []
        if game.dragon is not None:
            used_avatars.append(game.dragon.avatar)

        for x in xrange(3):
            try:
                child = core.Dragon(parent=game.dragon, used_gifts=used_gifts, used_avatars=used_avatars, game_ref=game)
            except StopIteration:
                break  # TODO: действие в случае когда драконы закончились
            dragons.append(child)
            used_gifts.append(child._gift)
            used_avatars.append(child.avatar)
        if dragons[0] not in dragons_choosed:
            renpy.childimg1 = ui.image(dragons[0].avatar)
        else:
            renpy.childimg1 = ui.image(im.Grayscale(dragons[0].avatar))
        try:
            if dragons[1] not in dragons_choosed:
                renpy.childimg2 = ui.image(dragons[1].avatar)
            else:
                renpy.childimg2 = ui.image(im.Grayscale(dragons[1].avatar))
            if dragons[2] not in dragons_choosed:
                renpy.childimg3 = ui.image(dragons[2].avatar)
            else:
                renpy.childimg3 = ui.image(im.Grayscale(dragons[2].avatar))
        except IndexError:
            pass

        def get_breedbg():
            import random
                               
            # Важно проверить количество голов. color_eng берёт цвет из первой головы, но иногда её почему-то нет.
            if (game.dragon is not None) and (len(game.dragon.heads) > 0):
                hatches_colored = [f for f in renpy.list_files() if f.startswith("img/scene/hatch/%s" % game.dragon.color_eng)]
                
                if len(hatches_colored) > 0:
                    return random.choice(hatches_colored)

            return "img/scene/hatch/base.png"
                            
        renpy.breedbg = ui.image(get_breedbg())

    screen ava_screen:
        add renpy.breedbg
        add renpy.childimg1 xalign 0.0 yalign 0.0
        add renpy.childimg2 xalign 0.0 yalign 0.5
        add renpy.childimg3 xalign 0.0 yalign 1.0
        imagebutton idle "img/bg/frame.png" hover "img/bg/frame_light.png" selected_idle "img/bg/frame_light.png" xalign 0.0 yalign 0.0 action SetVariable("child_choose", dragons[0]), SetVariable("togle_dragonchoose_button", True), Show("text_screen"), SelectedIf(child_choose == dragons[0]), SensitiveIf(dragons[0] not in dragons_choosed)
        imagebutton idle "img/bg/frame.png" hover "img/bg/frame_light.png" selected_idle "img/bg/frame_light.png" xalign 0.0 yalign 0.5 action SetVariable("child_choose", dragons[1]), SetVariable("togle_dragonchoose_button", True), Show("text_screen"), SelectedIf(child_choose == dragons[1]), SensitiveIf(dragons[1] not in dragons_choosed)
        imagebutton idle "img/bg/frame.png" hover "img/bg/frame_light.png" selected_idle "img/bg/frame_light.png" xalign 0.0 yalign 1.0 action SetVariable("child_choose", dragons[2]), SetVariable("togle_dragonchoose_button", True), Show("text_screen"), SelectedIf(child_choose == dragons[2]), SensitiveIf(dragons[2] not in dragons_choosed)
        use status_bar

    screen text_screen:
        $renpy.childtext = child_choose.description
        window:
            xsize 760
            xpos 200
            align(0.0, 0.0)
            text renpy.childtext
        if togle_dragonchoose_button is True:
            fixed:
                xalign 1.0
                xmaximum 320
                textbutton "Выбрать":
                    pos(72, 649)
                    xysize(174, 36)
                    text_xalign 0.5
                    text_yalign 0.5
                    background "img/bg/logovo.png"
                    text_size 22
                    action SetVariable("child_selected", child_choose), SetVariable("togle_dragonchoose_button", False), Hide("ava_screen"), Hide("text_screen"), Return("return")
    while True:
        nvl clear
        call screen ava_screen
        $ game.dragon = child_selected
        $ dragons_choosed.append(game.dragon)
        show expression 'img/scene/mistress.png' as bg
        "[game.quest_text]"
        jump lb_location_mordor_main
