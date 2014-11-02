label lb_choose_dragon:
    #Хардкод на трех драконов.
    python:
        lost = False
        if game.dragon is None:
            dragons = []
            dragons_choosed = []
        if game.dragon is not None and game.dragon.heads:
            dragons = []
            dragons_choosed = []
            # добавляем 1 гоблина в армию тьмы
            game.army.add_warrior('goblin')
            # добавляем всё неправедно нажитое богатство в казну Владычицы
            game.army.money += game.lair.treasury.wealth
            # создаем новое логово
            game.create_lair()
        if game.dragon is None or game.dragon.heads:
            # задаем квест
            game.set_quest()
        child_choose = None
        child_selected = None
        togle_dragonchoose_button = None
        if game.dragon and len(game.dragon.heads)==0 and len(dragons_choosed)==3:
            lost = True
    if lost:#TODO: приделать что-то что происходит при поражении
        "Вы проиграли"
        
    python hide:
        used_gifts = []
        used_avatars = []
        if game.dragon is not None:
            used_avatars.append(game.dragon.avatar)
            
        
        while len(dragons) < 3:
            child = core.Dragon(parent=game.dragon, gameRef=game,base_character=game.adv_character)
            if child._gift not in used_gifts and child.avatar not in used_avatars:
                dragons.append(child)
                used_gifts.append(child._gift)
                used_avatars.append(child.avatar)
        renpy.childimg1 = ui.image(dragons[0].avatar) if dragons[0] not in dragons_choosed else ui.image(im.Grayscale(dragons[0].avatar))
        renpy.childimg2 = ui.image(dragons[1].avatar) if dragons[1] not in dragons_choosed else ui.image(im.Grayscale(dragons[1].avatar))
        renpy.childimg3 = ui.image(dragons[2].avatar) if dragons[2] not in dragons_choosed else ui.image(im.Grayscale(dragons[2].avatar))
        def get_breedbg():
            import random
            import os
            rel_path = "img/scene/hatch"
            abs_path = os.path.join(renpy.config.basedir, "game", rel_path)
            if game.dragon is not None:
                if game.dragon.heads and game.dragon.color_eng() in os.listdir(abs_path):
                    color_filename = random.choice(os.listdir(os.path.join(abs_path, game.dragon.color_eng())))
                    return rel_path + "/" + game.dragon.color_eng() + "/" + color_filename
                else:
                    return "img/scene/hatch/base.png"
            else:
                return "img/scene/hatch/base.png"
        renpy.breedbg = ui.image(get_breedbg())
    screen ava_screen:
        add renpy.breedbg
        add renpy.childimg1 xalign 0.0 yalign 0.0
        add renpy.childimg2 xalign 0.0 yalign 0.5
        add renpy.childimg3 xalign 0.0 yalign 1.0
        imagebutton idle "img/bg/frame.png" hover "img/bg/frame_light.png" selected_idle "img/bg/frame_light.png" xalign 0.0 yalign 0.0 action SetVariable("child_choose",dragons[0]),SetVariable("togle_dragonchoose_button", True),Show("text_screen"), SelectedIf(child_choose == dragons[0]), SensitiveIf(dragons[0] not in dragons_choosed)
        imagebutton idle "img/bg/frame.png" hover "img/bg/frame_light.png" selected_idle "img/bg/frame_light.png" xalign 0.0 yalign 0.5 action SetVariable("child_choose",dragons[1]),SetVariable("togle_dragonchoose_button", True),Show("text_screen"), SelectedIf(child_choose == dragons[1]), SensitiveIf(dragons[1] not in dragons_choosed)
        imagebutton idle "img/bg/frame.png" hover "img/bg/frame_light.png" selected_idle "img/bg/frame_light.png" xalign 0.0 yalign 1.0 action SetVariable("child_choose",dragons[2]),SetVariable("togle_dragonchoose_button", True),Show("text_screen"), SelectedIf(child_choose == dragons[2]), SensitiveIf(dragons[2] not in dragons_choosed)
    screen text_screen:
        $renpy.childtext = child_choose.description
        window:
            xsize 760
            xpos 200
            align (0.0,0.0)
            text renpy.childtext
        if togle_dragonchoose_button is True:
            fixed:
                xalign 1.0
                xmaximum 320
                textbutton "Выбрать":
                    pos(72,649)
                    xysize(174,36)
                    text_xalign 0.5
                    text_yalign 0.5
                    background "img/bg/logovo.png"
                    text_size 22
                    action SetVariable("child_selected",child_choose),SetVariable("togle_dragonchoose_button", False), Show("main_map"), Hide("ava_screen"), Hide("text_screen"), Return("return")
    while True:
        nvl clear
        call screen ava_screen
        $ game.dragon = child_selected
        $ dragons_choosed.append(game.dragon)
        return
