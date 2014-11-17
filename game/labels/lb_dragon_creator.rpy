label lb_dragon_creator:
    python:
        child = core.Dragon(parent=game.dragon, gameRef=game,base_character=game.adv_character)
        game.dragon = child
        mods_left = 12
    init python:
        class add_modifier:
            def __init__(self, mod, dragon):
                self.mod = mod
                self.dragon = dragon
            def __call__(self):
                if self.mod in data.dragon_heads.keys():
                    self.dragon.heads.append(self.mod)
                else:
                    self.dragon.anatomy.append(self.mod)
                renpy.restart_interaction()
    screen creator:
        window:
            text "Осталось модификаций [mods_left]" xalign 0.3
            hbox:
                vbox:
                    text "Головы"
                    for i in data.dragon_heads.keys():
                        textbutton data.heads_name_rus[i] action SetVariable("mods_left", mods_left-1), add_modifier(i, game.dragon), If(mods_left == 1, (Hide("creator"), Return("return")))
                vbox:
                    text "Анатомия"
                    textbutton "лапы" action SetVariable("mods_left", mods_left-1), add_modifier("paws", game.dragon), If(mods_left == 1, (Hide("creator"), Return("return")))
                    textbutton "крылья" action SetVariable("mods_left", mods_left-1), add_modifier("wings", game.dragon), If(mods_left == 1, (Hide("creator"), Return("return")))
                    textbutton "размер" action SetVariable("mods_left", mods_left-1), add_modifier("size", game.dragon), If(mods_left == 1, (Hide("creator"), Return("return")))
            use status_bar
            fixed:
                xalign 1.0
                xmaximum 320
                textbutton "Выпустить":
                    pos(72,649)
                    xysize(174,36)
                    text_xalign 0.5
                    text_yalign 0.5
                    background "img/bg/logovo.png"
                    text_size 22
                    action Jump("lb_location_mordor_main"), Hide("creator")
    nvl clear
    call screen creator
    jump lb_location_mordor_main