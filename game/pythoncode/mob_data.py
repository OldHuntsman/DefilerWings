# coding=utf-8
# Одноразовые противники
mob = {
    'airfleet': {
        'name': u"Воздушные крейсера",  # название моба применяемое в описании
        'power': {'base': (5, 2)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (6, 3)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'airfleet',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'airship': {
        'name': u"Летучий корабль",  # название моба применяемое в описании
        'power': {'base': (4, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (5, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'airship',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'angel': {
        'name': u"Ангел",  # название моба применяемое в описании
        'power': {'base': (6, 3)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (6, 3)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'angel',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'archer': {
        'name': u"Стрелок",  # название моба применяемое в описании
        'power': {'base': (4, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (2, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'archer',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'band': {
        'name': u"Банда разбойников",  # название моба применяемое в описании
        'power': {'base': (2, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (4, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'xbow',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'boar': {
        'name': u"Огромный вепрь",  # название моба применяемое в описании
        'power': {'base': (3, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (3, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'boar',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },


    'bear': {
        'name': u"Пещерный медведь",  # название моба применяемое в описании
        'power': {'base': (3, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (3, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'bear',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'bull': {
        'name': u"Бык",  # название моба применяемое в описании
        'power': {'base': (2, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (2, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'bull',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} бросается на {1}", ['foe_name', 'dragon_name'], 0],
            [['foe_intro'], u"{0} роет копытами землю, готовясь напасть", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе от {1}", ['foe_name', 'dragon_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наносит сильный удар, {1} яростным контрударом убивает его",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит сильный удар и уворачивается от ответного удара",
             ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Противники маневрируют, готовясь к удару", [], 0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} ценой головы убивает супостата", ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'bull_champion': {
        'name': u"Призовой бык",  # название моба применяемое в описании
        'power': {'base': (3, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (3, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'bull',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} бросается на {1}", ['foe_name', 'dragon_name'], 0],
            [['foe_intro'], u"{0} роет копытами землю, готовясь напасть", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе от {1}", ['foe_name', 'dragon_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наносит сильный удар, {1} яростным контрударом убивает его",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит сильный удар и уворачивается от ответного удара",
             ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Противники маневрируют, готовясь к удару", [], 0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} ценой головы убивает супостата", ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'champion': {
        'name': u"Рыцарь-чемпион",  # название моба применяемое в описании
        'power': {'base': (5, 1)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (5, 1)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'champion',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'city_guard': {
        'name': u"Городская стража",  # название моба применяемое в описании
        'power': {'base': (5, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (4, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'city_guard',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'dog': {
        'name': u"Овчарка",  # название моба применяемое в описании
        'power': {'base': (1, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (1, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'dog',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'druid': {
        'name': u"Друид",  # название моба применяемое в описании
        'power': {'base': (5, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (5, 1)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'druid',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'dwarf_champion': {
        'name': u"Король цвергов",  # название моба применяемое в описании
        'power': {'base': (4, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (4, 2)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'dwarf_champion',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'dwarf_citizen': {
        'name': u"Цверг",  # название моба применяемое в описании
        'power': {'base': (2, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (3, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'dwarf_citizen',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'dwarf_guards': {
        'name': u"Стражи тоннелей",  # название моба применяемое в описании
        'power': {'base': (4, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (2, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'dwarf_guards',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'elf_ranger': {
        'name': u"Страж границ",  # название моба применяемое в описании
        'power': {'base': (6, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (1, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'elf_ranger',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'footman': {
        'name': u"Пехотинцы",  # название моба применяемое в описании
        'power': {'base': (3, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (4, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'footman',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'golem': {
        'name': u"Железный голем",  # название моба применяемое в описании
        'power': {'base': (3, 2)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (3, 3)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'golem',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'griffin': {
        'name': u"Дикий грифон",  # название моба применяемое в описании
        'power': {'base': (5, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (3, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'griffin',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'griffin_rider': {
        'name': u"Всадник на грифоне",  # название моба применяемое в описании
        'power': {'base': (7, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (5, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'griffin_rider',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'heavy_cavalry': {
        'name': u"Тяжелая кавалерия",  # название моба применяемое в описании
        'power': {'base': (5, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (6, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'heavy_cavalry',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'heavy_infantry': {
        'name': u"Латники",  # название моба применяемое в описании
        'power': {'base': (4, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (5, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'heavy_infantry',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'ifrit': {
        'name': u"Ифрит",  # название моба применяемое в описании
        'power': {'base': (5, 2)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (5, 3)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'ifrit',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'jotun': {
        'name': u"Йотун",  # название моба применяемое в описании
        'power': {'base': (5, 2)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (5, 3)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'jotun',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'jagger': {
        'name': u"Егерь",  # название моба применяемое в описании
        'power': {'base': (3, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (1, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'jagger',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'knight': {
        'name': u"Кракен",  # название моба применяемое в описании
        'descriptions': [
            [['foe_intro', 'foe_alive'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ],
    },

    'kraken': {
        'name': u"Кракен",  # название моба применяемое в описании
        'power': {'base': (6, 3)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (6, 3)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'kraken',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'merman': {
        'name': u"Страж мелководья",  # название моба применяемое в описании
        'power': {'base': (2, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (2, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'merman',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'militia': {
        'name': u"Отряд ополчения",  # название моба применяемое в описании
        'power': {'base': (2, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (4, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'militia',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} бросается на {1}", ['foe_name', 'dragon_name'], 0],
            [['foe_intro'], u"{0} роет копытами землю, готовясь напасть", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе от {1}", ['foe_name', 'dragon_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наносит сильный удар, {1} яростным контрударом убивает его",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит сильный удар и уворачивается от ответного удара",
             ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Противники маневрируют, готовясь к удару", [], 0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} ценой головы убивает супостата", ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'mob': {
        'name': u"Крестьяне",  # название моба применяемое в описании
        'power': {'base': (1, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (3, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'mob',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} бросается на {1}", ['foe_name', 'dragon_name'], 0],
            [['foe_intro'], u"{0} роет копытами землю, готовясь напасть", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе от {1}", ['foe_name', 'dragon_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наносит сильный удар, {1} яростным контрударом убивает его",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит сильный удар и уворачивается от ответного удара",
             ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Противники маневрируют, готовясь к удару", [], 0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} ценой головы убивает супостата", ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'mounted_guard': {
        'name': u"Конные телохранители",  # название моба применяемое в описании
        'power': {'base': (4, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (5, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'mounted_guard',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },


    'ogre': {
        'name': u"Людоед",  # название моба применяемое в описании
        'power': {'base': (6, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (6, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'ogre',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'old_knight': {
        'name': u"Старый рыцарь",  # название моба применяемое в описании
        'power': {'base': (4, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (5, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'knight/knight1',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'shark': {
        'name': u"Отряд ополчения",  # название моба применяемое в описании
        'power': {'base': (3, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (3, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'shark',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} бросается на {1}", ['foe_name', 'dragon_name'], 0],
            [['foe_intro'], u"{0} роет копытами землю, готовясь напасть", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе от {1}", ['foe_name', 'dragon_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наносит сильный удар, {1} яростным контрударом убивает его",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит сильный удар и уворачивается от ответного удара",
             ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Противники маневрируют, готовясь к удару", [], 0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} ценой головы убивает супостата", ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },


    'ship': {
        'name': u"Корабль",  # название моба применяемое в описании
        'power': {'base': (3, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (4, 1)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'ship',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} бросается на {1}", ['foe_name', 'dragon_name'], 0],
            [['foe_intro'], u"{0} роет копытами землю, готовясь напасть", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе от {1}", ['foe_name', 'dragon_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наносит сильный удар, {1} яростным контрударом убивает его",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит сильный удар и уворачивается от ответного удара",
             ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Противники маневрируют, готовясь к удару", [], 0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} ценой головы убивает супостата", ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },


    'steamgun': {
        'name': u"Паровая пушка",  # название моба применяемое в описании
        'power': {'base': (2, 3)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (4, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'steamgun',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} бросается на {1}", ['foe_name', 'dragon_name'], 0],
            [['foe_intro'], u"{0} роет копытами землю, готовясь напасть", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе от {1}", ['foe_name', 'dragon_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наносит сильный удар, {1} яростным контрударом убивает его",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит сильный удар и уворачивается от ответного удара",
             ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Противники маневрируют, готовясь к удару", [], 0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} ценой головы убивает супостата", ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },


    'titan': {
        'name': u"Титан",  # название моба применяемое в описании
        'power': {'base': (7, 2)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (7, 2)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'titan',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} бросается на {1}", ['foe_name', 'dragon_name'], 0],
            [['foe_intro'], u"{0} роет копытами землю, готовясь напасть", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе от {1}", ['foe_name', 'dragon_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наносит сильный удар, {1} яростным контрударом убивает его",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит сильный удар и уворачивается от ответного удара",
             ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Противники маневрируют, готовясь к удару", [], 0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} ценой головы убивает супостата", ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'town': {
        'name': u"Защитники города",  # название моба применяемое в описании
        'power': {'base': (4, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (6, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'town',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} бросается на {1}", ['foe_name', 'dragon_name'], 0],
            [['foe_intro'], u"{0} роет копытами землю, готовясь напасть", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе от {1}", ['foe_name', 'dragon_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наносит сильный удар, {1} яростным контрударом убивает его",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит сильный удар и уворачивается от ответного удара",
             ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Противники маневрируют, готовясь к удару", [], 0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} ценой головы убивает супостата", ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'treant': {
        'name': u"Чащобный страж",  # название моба применяемое в описании
        'power': {'base': (6, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (6, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'treant',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'triton': {
        'name': u"Тритон",  # название моба применяемое в описании
        'power': {'base': (7, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (7, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'triton',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'wizard': {
        'name': u"Чародей",  # название моба применяемое в описании
        'power': {'base': (5, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (5, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'wizard',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} готовится к бою 1", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 2", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою 3", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе", ['foe_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наностит дракону ранение, но {1} побеждает",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит дракону серьёзную рану", ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Бой продолжается некоторое время но никто не может взять верх", [],
             0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову дракону", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} побеждает, но одна из его голов умирает от полученых ран",
             ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'xbow': {
        'name': u"Арбалетчики",  # название моба применяемое в описании
        'power': {'base': (4, 0)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (4, 0)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'xbow',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} бросается на {1}", ['foe_name', 'dragon_name'], 0],
            [['foe_intro'], u"{0} роет копытами землю, готовясь напасть", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе от {1}", ['foe_name', 'dragon_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наносит сильный удар, {1} яростным контрударом убивает его",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит сильный удар и уворачивается от ответного удара",
             ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Противники маневрируют, готовясь к удару", [], 0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} ценой головы убивает супостата", ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

    'xbow_rider': {
        'name': u"Конные арбалетчики",  # название моба применяемое в описании
        'power': {'base': (4, 1)},  # сила атаки моба (обычная, верная)
        'defence': {'base': (4, 1)},  # надежность защиты моба (обычная, верная)
        'modifiers': [],  # особые модификаторы
        'image': 'xbow_rider',  # фоновое изображение для драки в "img/scene/fight/%s.png"
        # набор описаний сцены боя
        'descriptions': [
            [['foe_intro'], u"{0} бросается на {1}", ['foe_name', 'dragon_name'], 0],
            [['foe_intro'], u"{0} роет копытами землю, готовясь напасть", ['foe_name'], 0],
            [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
            [['foe_fear'], u"{0} бежит в страхе от {1}", ['foe_name', 'dragon_name'], 0],
            [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
            [['foe_dead', 'dragon_wounded'], u"{0} наносит сильный удар, {1} яростным контрударом убивает его",
             ['foe_name', 'dragon_name'], 0],
            [['foe_alive', 'dragon_wounded'], u"{0} наносит сильный удар и уворачивается от ответного удара",
             ['foe_name'], 0],
            [['foe_alive', 'dragon_undamaged'], u"Противники маневрируют, готовясь к удару", [], 0],
            [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову", ['foe_name'], 0],
            [['foe_dead', 'lost_head'], u"{0} ценой головы убивает супостата", ['dragon_name'], 0],
            [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
        ]
    },

}