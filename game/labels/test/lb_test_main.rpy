label lb_test_main:
    nvl clear
    while True:
        menu:
            "Примеры":
                call lb_test_examples
            "Отладка":
                pass
            "Назад":
                return
    return
    
label lb_test_examples:
    menu:
        "Примеры"
        "Цикл с возвратом":
            call lb_test_example_returnLoop
        "Назад":
            return
    return