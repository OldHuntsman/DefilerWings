screen sc_dialog(name='', avatar=None, what=''):
    add "img/style/dialog.png":
        ypos 120
    add avatar:
        pos (99,195)
    text name:
        pos (310,370)
    viewport:
        pos (110,420)
        xysize (800,500)
        text what id "what"