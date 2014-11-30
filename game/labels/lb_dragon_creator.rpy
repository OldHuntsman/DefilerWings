label lb_dragon_creator:
    python:
        child = core.Dragon(parent=game.dragon, gameRef=game,base_character=game.adv_character)
        game.dragon = child
        mods_left = 12
        special_features_rus = {"tough_scale":"крепкая чешуя", "poisoned_sting":"ядовитое жало",\
                "clutches":"когти", "horns":"рога", "fangs":"клыки", "ugly":"уродство"}
        colored_heads = ["red", "white", "blue", "black", "iron", "bronze", "silver", "gold", "shadow"]
    init python:
        class add_modifier:
            def __init__(self, mod, dragon):
                self.mod = mod
                self.dragon = dragon
            def __call__(self):
                if self.mod in data.dragon_heads.keys():
                    if self.mod == "green":
                        self.dragon.heads.append(self.mod)
                    else:
                        self.dragon.heads[self.dragon.heads.index("green")] = self.mod
                        colored_heads.pop(colored_heads.index(self.mod))
                else:
                    self.dragon.anatomy.append(self.mod)
                    if self.mod in special_features_rus.keys():
                        special_features_rus.pop(self.mod)
                renpy.restart_interaction()
    screen creator:
        window:
            text "Осталось модификаций [mods_left]" xalign 0.45
            hbox:
                vbox:
                    text "Анатомия"
                    textbutton "голова" action SetVariable("mods_left", mods_left-1), add_modifier("green", game.dragon), If(mods_left == 1, (Hide("creator"), Return("return")))
                    textbutton "лапы" action SetVariable("mods_left", mods_left-1), add_modifier("paws", game.dragon), If(mods_left == 1, (Hide("creator"), Return("return")))
                    textbutton "крылья" action SetVariable("mods_left", mods_left-1), add_modifier("wings", game.dragon), If(mods_left == 1, (Hide("creator"), Return("return")))
                    textbutton "размер" action SetVariable("mods_left", mods_left-1), add_modifier("size", game.dragon), If(mods_left == 1, (Hide("creator"), Return("return")))
                    for i in special_features_rus.keys():
                        textbutton special_features_rus[i] action SetVariable("mods_left", mods_left-1), add_modifier(i, game.dragon), If(mods_left == 1, (Hide("creator"), Return("return")))
                showif game.dragon.heads.count("green") > 0:
                    vbox:
                        text "Цветные головы"
                        for i in colored_heads:
                                textbutton data.heads_name_rus[i] action SetVariable("mods_left", mods_left-1), add_modifier(i, game.dragon), If(mods_left == 1, (Hide("creator"), Return("return")))
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