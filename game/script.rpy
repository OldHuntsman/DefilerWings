init python:
    #Импортируем нужные библиотеки. Возможно это надо засунуть в какой-то отдельный файл инициализации.
    from pythoncode import data
    from pythoncode import core
    from copy import deepcopy
    
    #Заряжаем пасхалки. Их можно будет встретить в игре лишь однажды
    one_time_encounters = ['enc_redcape']
    for encounter in one_time_encounters:
        if persistent.encounter == None:
            persistent.encounter = False
    
    #Нужные переменные
    girls_list = []
    
    #Нужные функции
    def impregnate():
        """
        Осеменение женщины.
        """
        game.girl.virgin = False
        game.girl.pregnant = 1
        if game.girl.quality < game.dragon.magic():
            game.girl.pregnant = 2
        game.dragon.lust -= 1

    def get_girl(type = 'peasant'):
        game.girl = core.Girl(gameRef=game, base_character=NVLCharacter)
        girls_list.append(game.girl)
        relative_path = "img/avahuman/"+type # Относительный путь для движка ренпи
        absolute_path = os.path.join(config.basedir, "game", relative_path) # Cоставляем абсолютный путь где искать
        filename = random.choice(os.listdir(absolute_path)) # получаем название файла
        game.girl.avatar = relative_path + "/" + filename # Возвращаем правильно отформатированно значение
    
init:
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


# Начало игры
    
label start:
    
    python:
        #Инициализируем game в начале игры, а не при инициализации. Для того чтобы 
        game = core.Game(NVLCharacter)
        game.dragon.avatar = get_dragon_avatar('green')
        narrator = game.narrator    # Ради совместимости с обычным синтаксисом RenPy
        
    # Прокручиваем заставку.
    call screen sc_intro
    nvl clear
    $ win = False
    while not win:
        $ target_label = renpy.call_screen("main_map")
        if renpy.has_label(target_label):
            $ renpy.call(target_label)
        else:
            $ renpy.call("lb_location_missed")
    
    return
