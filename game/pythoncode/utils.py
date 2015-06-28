# coding=utf-8

import bisect, random

def weighted_random(choice_options):
    """
    :param choice_options: list of tuples (option, weight), где option - возвращаемый вариант, а
                 weight - вес варианта. Чем больше, тем вероятнее что он выпадет.
    :return: option, или None, если сделать выбор не удалось.
    Пример использования:
    coin_flip = weighted_random([("орёл", 1), ("решка",1)])
    """
    if len(choice_options) > 0:
        # Складываем вес всех доступных энкаунтеров
        accumulated = []
        total = 0
        for option, weight in choice_options:
            assert weight >= 0
            accumulated.append(weight + total)
            total += weight
        # Проверяем, что суммарный вес не равен нулю.
        if total == 0:
            return None
        r = random.random() * accumulated[-1]
        return choice_options[bisect.bisect(accumulated, r)][0]
    return None