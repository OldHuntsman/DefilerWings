# DONE: Нужно чтобы текст одним куском прокручивался снизу вверх на фоне меняющихся картинок. И чтобы текст нормально читался нужно либо обвести буквы, либо сделать подложку.
# DONE: Нужно чтобы при нажатии esc и прочих вызовов меню прокрутка останавливалась.
    
transform bottom_to_top:                #Трансформ прокручивающий текст
        ypos 720 xalign 0.5             #Начальное положение текста - по вертикали убран занижний край и выровнен посередине
        linear 200.0 ypos 0 yanchor 1.0  #За 200 секунд поднимаем текст до верхней кромки и смещаем якорь (по которому высчитывается положение текста)

transform intro_bg:
    "intro 1" with dissolve     #Начальная картинка (нужна чтобы показать ее если пошел повтор
    pause 35                    #Задержка перед следущей картинкой
    "intro 2" with dissolve     #Показываем следущую картинку
    pause 20
    "intro 3" with dissolve
    pause 15
    "intro 4" with dissolve
    pause 15
    "intro 5" with dissolve
    pause 25
    "intro 6" with dissolve
    pause 15
    "intro 7" with dissolve
    pause 37
    "intro 8" with dissolve
    pause 50
    repeat                      #Повторяем по кругу
    
screen sc_intro:
    add "intro 1" at intro_bg           #Показываем фон и добавляем трансформ чтобы он менялся по ходу сцены
    add "img/bg/blur.png"               #Добавляем блюр.
    on "show" action Play("music","mus/intro.ogg") #Ставим играть музыку при открытии этого экрана
    on "hide" action Stop("music")      #Останавливаем при закрытии
    text intro_text at bottom_to_top:   #Добавляем текст (определен в text.py) с прокруткой
        first_indent 30                 #Отступ для первой строки в параграфе
        #newline_indent True            #Нужно применять отступ для каждой первой строки в параграфе.
        layout "tex"                    #Разбивка текста на строки
        justify True                    #Выровнять текст по ширине
        outlines [(1, "#0008", 1, 1)]   #Обводка текста, иначе его плохо видно
        xmaximum 820                    #Максимальная ширина текста
        
        #    Кстати, в ренпи есть баг, не работает newline_indent, 
        #    но если его починить, то текст криво разбивается на строки
        #    в layout "tex".
    
    #Назначаем кнопки, чтобы вернуться с этого экрана.
    key "K_SPACE" action Return()
    key 'K_RETURN' action Return()
    key 'K_KP_ENTER' action Return()
    key 'mouseup_1' action Return()     # Почему-то при нажатии мышкой в зону imagebatton еще (теоритически) не нарисованного screen main_map вызывалась сцена
                                        # Fixed, ренпи реагирует на поднятие кнопки, а не на нажим. Таким образом до того как кнопку отпускали успела загрузиться карта
    timer 200.0 action Return()         # Едем дальше если слишком долго ждали