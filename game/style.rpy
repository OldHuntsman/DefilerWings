init python:
    ###
    # vscrollbar
    ##
    
    style.vscrollbar.thumb = Image("img/style/vscrollbar/active_thumb.png")
    style.vscrollbar.selected_thumb = Image("img/style/vscrollbar/pressed_thumb.png")
    style.vscrollbar.idle_thumb = Image("img/style/vscrollbar/idle_thumb.png")
    #style.vscrollbar.thumb_offset = 20 # Половина высоты ползунка
    #style.vscrollbar.xmargin = 7 # Половина высоты ползунка
    #style.vscrollbar.top_padding = 108
    #style.vscrollbar.fore_bar = Frame("img/style/vscrollbar/idle_bar.png",4,4)
    active_fore_bar = Image("img/style/vscrollbar/active_bar.png")
    active_bottom_bar = Frame("img/style/vscrollbar/active_bar_bottom.png",4,4)
    idle_fore_bar = Image("img/style/vscrollbar/idle_bar.png")
    idle_bottom_bar = Frame("img/style/vscrollbar/idle_bar_bottom.png",4,4)
    style.vscrollbar.top_bar = active_fore_bar
    style.vscrollbar.bottom_bar = active_bottom_bar
    style.vscrollbar.idle_top_bar = idle_fore_bar
    style.vscrollbar.idle_bottom_bar = idle_bottom_bar
    style.vscrollbar.xsize = 14
    style.vscrollbar.unscrollable = "hide"
    #style.vscrollbar.bottom_gutter = 9