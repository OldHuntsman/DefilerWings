init python:
    from pythoncode.core import Game
    game = Game()

init:
    $ narrator = NVLCharacter(None, kind=nvl)
    define dragon =  Character("Дракон", color="#c8ffc8", kind=nvl, image="dragon")
    image side dragon = "dragon ava"
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
    # Прокручиваем заставку. Это черновой вариант, надо будет переделывать. Нужно чтобы текст одним куском прокручивался снизу вверх на фоне меняющихся картинок. И чтобы текст нормально читался нужно либо обвести буквы, либо сделать подложку.
    scene black
    play music "mus/intro.ogg"
    show intro 1 with dissolve
    show text intro_text[0]
    with Pause(10)
    show intro 2 with dissolve
    show text intro_text[1]
    with Pause(10)
    show intro 3 with dissolve
    show text intro_text[2]
    with Pause(10)
    show intro 4 with dissolve
    show text intro_text[3]
    with Pause(10)
    show intro 5 with dissolve
    show text intro_text[4]
    with Pause(10)
    show intro 6 with dissolve
    show text intro_text[5]
    with Pause(10)
    show intro 7 with dissolve
    show text intro_text[6]
    with Pause(10)
    show intro 8 with dissolve
    show text intro_text[7]
    with Pause(10)
    
    stop music
    
label lb_mainmap:
    $ avatars = Avatars() # Инициализируем модуль с аватарками
    nvl clear
    show screen status_bar
    call screen main_map
    
    if result == "castle":           # то что происходит после клика
        scene bg main
        $ bg ("Куда теперь?")
        menu:
            'Рынок':
                $ place = 'market'
            'Замок':
                $ place = 'castle'
            'Карта':
                jump start
    if result == "road":
        menu:
            'Дорога':
                $ place = 'road'
            'Карта':
                jump start
    if result == "cave":
        menu:
            'Пещера':
                $ place = 'cave'
            'Карта':
                jump start
    if result == "view":
        menu:
            'Красивый вид':
                $ place = 'farscape'
            'Карта':
                jump start
        
    
    show place
    $ avatars.DisplayLeft("princess ava ") # Показываем принцессу слева
    $ avatars.DisplayRight("dragon ava") # Показываем дракона справа
    pr 'Hello world!'
    dr 'Grrrrr'
    jump lb_mainmap

    
    return
 
label fight:
    $ renpy.say(None, game.battle(game.knight, game.dragon))
    jump lb_mainmap

label lb_lair:
    $ place = 'cave'
    show place
    
    menu:
        'Сотворить заклинание':
            $ pass
        'Чахнуть над златом':
            $ pass
        'Проведать пленниц':
            $ pass
        'Лечь спать':
            $ pass
        'Покинуть логово':
            $ pass
            
    jump lb_mainmap
    
label lb_forest_random:
    $ place = 'forest'
    show place
      
    'Появился случайный энакаунтер'
        
    jump lb_mainmap
    
label lb_mountain_random:
    $ place = 'mountain'
    show place
      
    'Появился случайный энакаунтер'
        
    jump lb_mainmap
    
label lb_road_random:
    $ place = 'road'
    show place
      
    'Появился случайный энакаунтер'
        
    jump lb_mainmap
    
label lb_sky_random:
    $ place = 'sky'
    show place
      
    'Появился случайный энакаунтер'
        
    jump lb_mainmap
    
label lb_sea_random:
    $ place = 'sea'
    show place
      
    'Появился случайный энакаунтер'
        
    jump lb_mainmap    
    
label lb_plain_choose:
    $ place = 'plain'
    show place
      
    menu:
        'Рыскать за околицей':
            $ pass
        'Одинокий хутор':
            $ pass
        'Маленький посёлок':
            $ pass
        'Деревня':
            $ pass
        'Село':
            $ pass
        'Городок':
            $ pass
        'Отступить':
            $ pass
        
    jump lb_mainmap      
    
label lb_city_choose:
    $ place = 'city_gate'
    show place
      
    menu:
        'Тайный визит':
            $ pass
        'Ворваться в город':
            $ pass
        'Осадить город':
            $ pass
        'Отступить':
            $ pass
        
    jump lb_mainmap        
        
    
label lb_gremlin_choose:
    $ place = 'gremlins'
    show place
      
    menu:
        'Нанять слуг':
            $ pass
        'Ловушки для логова':
            $ pass
        'Укрепления для логова':
            $ pass
        'Уйти':
            $ pass
        
    jump lb_mainmap        
        
    
label lb_smugler_choose:
    $ place = 'smuglers'
    show place
      
    menu:
        'Нанять охрану':
            $ pass
        'Финансировать террор':
            $ pass
        'Уйти':
            $ pass
            
    jump lb_mainmap        
        
    
label lb_mordor_choose:
    $ place = 'mordor'
    show place
      
    menu:
        'Армия Тьмы':
            $ pass
        'Аудиенция с Владычицей':
            $ pass
        
    jump lb_mainmap               
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
            