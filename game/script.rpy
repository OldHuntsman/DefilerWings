init python:
    #Импортируем нужные библиотеки. Возможно это надо засунуть в какой-то отдельный файл инициализации.
    from pythoncode import data
    from pythoncode import core
    from pythoncode import treasures
    from copy import deepcopy
    
    #Заряжаем пасхалки. Их можно будет встретить в игре лишь однажды
    one_time_encounters = ['enc_redcape']
    for encounter in one_time_encounters:
        if persistent.encounter == None:
            persistent.encounter = False
    
init:    
    transform bot_to_top:
        align(-2, -2)
        linear 100 yalign 3.0
        repeat
    image side dragon = "dragon ava"
    image blur = "img/intro/blur.png"
    image bg main = "img/bg/main.jpg"  # заставка главного меню
    image place = ConditionSwitch(              
        "place == 'city_gates'", "img/bg/city/outside.png",    # определение фонов для разных мест (потребует доработки)  
        "place == 'lair'", "img/bg/lair/cave.png",
        "place == 'forest'", "img/bg/forest/1.png",
        "place == 'mountain'", "img/bg/mountain/1.png",
        "place == 'plain'", "img/bg/plain/3.png",
        "place == 'road'", "img/bg/road/1.png",
        "place == 'sea'", "img/bg/sea/1.png",
        "place == 'sky'", "img/bg/sky/1.png",
        "place == 'gremlins'", "img/bg/special/gremlins.png",
        "place == 'smuglers'", "img/bg/special/smuglers.png",
        "place == 'mordor'", "img/bg/special/mordor.png",
        )
    define narrator = Character(None, kind=nvl)


# Начало игры
    
label start:
    
    python:
        #Инициализируем game в начале игры, а не при инициализации. Для того чтобы 
        game = core.Game(NVLCharacter)
        game.dragon.avatar = get_dragon_avatar(game.dragon.color_eng())
        narrator = game.narrator    # Ради совместимости с обычным синтаксисом RenPy
        
        mobilization = 0 #уровень мобилизации сил королевства на борьбу с драконом
        poverty = 0 #уровень разрухи в королевстве вызванной действиями дракона
        pov_gain = 0 #сколько разрухи прибавят действия дракона в текущем цикле
        rpoints = 0 #ОЧКИ дурной славы
        rlvl = 0 #текущий уровень дурной славы (растёт и отображается через фуенкцию "reputation()")
        rp_gain = [0,1,3,5,10,25] #пять вариантов роста дурной славы
        def gain_rep(gain = 1): #функция злого поступка с 1 по 5 уровень
            global rep_text
            global rpoints
            rpoints += rp_gain[gain]        
            rep_text = reputation_rise[gain]
            return

        def reputation(): #демонстрируемый уровень дурной славы дракона
            rp = 0
            global rlvl
            global rpoints
            if rpoints >= 3: rp = 1
            if rpoints >= 6: rp = 2
            if rpoints >= 10: rp = 3
            if rpoints >= 15: rp = 4
            if rpoints >= 21: rp = 5
            if rpoints >= 28: rp = 6
            if rpoints >= 36: rp = 7
            if rpoints >= 45: rp = 8
            if rpoints >= 55: rp = 9
            if rpoints >= 66: rp = 10
            if rpoints >= 78: rp = 11
            if rpoints >= 91: rp = 12
            if rpoints >= 105: rp = 13
            if rpoints >= 120: rp = 14
            if rpoints >= 136: rp = 15
            if rpoints >= 153: rp = 16
            if rpoints >= 171: rp = 17
            if rpoints >= 190: rp = 18
            if rpoints >= 210: rp = 19
            if rpoints >= 231: rp = 20
            if rp > rlvl:
                rpoints = 0
                rlvl = rp
            return rlvl
            
        bloodlust = game.dragon.bloodiness
    
    # Прокручиваем заставку.
    call screen sc_intro
    show screen status_bar
    $ win = False
    while not win:
        $ renpy.block_rollback()
        $ target_label = renpy.call_screen("main_map")
        if renpy.has_label(target_label):
            $ renpy.call(target_label)
        else:
            $ renpy.call("lb_location_missed")
    
    return
