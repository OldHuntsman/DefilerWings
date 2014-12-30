# coding=utf-8
label lb_test_example_returnLoop:
    # Пример цикла с возвратом без использования jump
    # while True:            # Вечный цикл до экспрессивного выхода
    # while not game.dragon.is_dead:    # Пока не наступит какое-то условие, например пока дракон не умер.
    while True:
        nvl clear
        # Дальше могут идти варианты. Из всех них мы попадем обратно в цикл, потому что в конце них стоит return -
        # т.е. продолжить с того место где остановились. Иначе игра закончится
        menu:
            "Некоторый выбор"
            "Вариант 1":
                call lb_test_example_choice1
            "Вариант 2":
                call lb_test_example_choice2
            "Закончить цикл":
                return
    return
    
label lb_test_example_choice1:
    "Выбор 1"
    return

label lb_test_example_choice2:
    "Выбор 2"
    return