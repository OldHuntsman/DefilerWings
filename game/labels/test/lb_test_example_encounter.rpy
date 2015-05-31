# coding=utf-8
label lb_test_example_encounter:
    menu:
        "Простой пример взвешенного выбора с распределением 2:1:1":
            call lb_test_example_encounter_static from _call_lb_test_example_encounter_static
        "Более сложный пример с динамическим формированием списка":
            call lb_test_example_encounter_dynamic from _call_lb_test_example_encounter_dynamic
    return


label lb_test_example_encounter_static:
    nvl clear
    "Cлучайный взвешенный энкаунтер"
    python:
        # Для начала определяем энкаунтеры:
        choices = [("Location 1", 2),
                   ("Location 2", 1),
                   ("Location 3", 1)]
        # У нас есть три варианта с распределением 2:1:1, т.е. если переводить в проценты, то:
        # 50%:25%:25%
        # Проверим это
        distribution = {}                   # Cделаем словарь distribution
        for (option, weight) in choices:    # Затем в него занесем варианты из списка choices
            distribution[option] = 0        # Проставив количество выпавших варинтов
        for i in range(0, 1000):             # И в цикле считам распределение на 1000 попыток
            option = core.Game.weighted_random(choices)
            distribution[option] += 1
        for key, value in distribution.items():        # Затем выводим получившийся результат на экран
            narrator("%s : %d" % (key, value))
    "Конец"
    return

label lb_test_example_encounter_dynamic:
    nvl clear
    python:
        # Тут весь трюк в динамическом формирование списка
        # Поэтому чтобы правильно все посчитать мы будем формировать список перед каждым
        # случайным выбором
        distribution = {}       # Cделаем словарь distribution для подсчета результатов
        # Определям переменную, по которй будем определять доступна ли третья локация для выбора.
        location3_seen = False
        for i in range(0, 1000):
            choices = [("Location 1", 20),
                       ("Location 2", 10)]  # Создаем список вариантов
            if not location3_seen:      # Если мы не видели третью локацию, то добавляем ее в список
                choices.append(("Location 3", 1))

            # Проверяем распределение:
            result = core.Game.weighted_random(choices)
            if result in distribution:  # Проверяем занесли ли мы этот вариант в распределение
                distribution[result] += 1
            else:
                distribution[result] = 1
            if result == "Location 3":  # Если выпала третья локация, то выставляем переменную
                location3_seen = True   # location3_seen в True, чтобы при следущей генерации списка
                # третья локация в него не попала.
                # В реальном случае стоит использовать persistent и
                # выставлять ее уже где-то внутри этой локации.
                narrator("Третья локация выпала на %d-й попытке" % i)  # Информативно

        # Выводим получившийся результат
        for key, value in distribution.items():
            narrator("%s : %d" % (key, value))
    return
