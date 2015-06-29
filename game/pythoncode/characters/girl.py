# coding=utf-8

import random

from pythoncode import girls_data
from pythoncode.utils import get_random_image

from talker import Talker


class Girl(Talker):
    """
    Базовый класс для всего, с чем можно заниматься сексом.
    """

    def __init__(self, girl_type='peasant', *args, **kwargs):
        # Инициализируем родителя
        super(Girl, self).__init__(*args, **kwargs)
        # Указываем тип девушки (крестьянка, гигантша..)
        self.type = girl_type
        # Подбираем аватарку
        self.avatar = get_random_image("img/avahuman/" + girls_data.girls_info[girl_type]['avatar'])
        
        # @Alex: Added haicolor taken from avatar:
        hair_colors = ["black", "blond", "brown", "red", "unknown"]
        fn = self.avatar.split("/")[-1]
        for i in hair_colors:
            if i in fn:
                self.hair_color = i
                break
        else:
            self.hair_color = None
            
        # девственность = пригодность для оплодотворения драконом
        self.virgin = True
        # беременность: 0 - не беременна, 1 - беременна базовым отродьем, 2 - беременна продвинутым отродьем
        self.pregnant = 0
        # Репродуктивное качество женщины.
        # Если коварство дракона превышает её репродуктивное качество, то отродье будет продвинутым. Иначе базовым.
        self.quality = girls_data.girls_info[girl_type]['magic_rating']
        # генерация имени
        # Если указано имя берем имя
        if girl_type + '_first' in girls_data.girls_names:
            self.name = random.choice(girls_data.girls_names[girl_type + '_first'])
            # Если есть фамилия, прибавляем к имени фамилию
            if girl_type + '_last' in girls_data.girls_names:
                self.name += " " + random.choice(girls_data.girls_names[girl_type + '_last'])
        # Не найти имя для девушки, считаем ее неизвестной
        else:
            self.name = 'Неизвестная Красавица'
        self.jailed = False  # была ли уже в тюрьме, пригодится для описания
        self.treasure = []

