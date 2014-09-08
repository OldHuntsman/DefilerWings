#Одноразовые противники
mob = {
        'dog' : {
            'name' : u"Овчарка",            #название моба применяемое в описании
            'power': {'base' : (1, 0)},         #сила атаки моба (обычная, верная)
            'defence' : {'base' : (1, 0)},      #надежность защиты моба (обычная, верная)
            'modifiers' : [],                   #особые модификаторы
            'image' : 'dog',                   #фоновое изображение для драки в "img/scene/fight/%s.png"
            #набор описаний сцены боя
            'descriptions' : [
                    [['foe_intro'], u"{0} бросается на {1}", ['foe_name', 'dragon_name'], 0],
                    [['foe_intro'], u"{0} роет копытами землю, готовясь напасть", ['foe_name'], 0],
                    [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
                    [['foe_fear'], u"{0} бежит в страхе от {1}", ['foe_name', 'dragon_name'], 0],
                    [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
                    [['foe_dead', 'dragon_wounded'], u"{0} наносит сильный удар, {1} яростным контрударом убивает его", ['foe_name', 'dragon_name'], 0],
                    [['foe_alive', 'dragon_wounded'], u"{0} наносит сильный удар и уворачивается от ответного удара", ['foe_name'], 0],
                    [['foe_alive', 'dragon_undamaged'], u"Противники маневрируют, готовясь к удару", [], 0],
                    [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову", ['foe_name'], 0],
                    [['foe_dead', 'lost_head'], u"{0} ценой головы убивает врага", ['dragon_name'], 0],
                    [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
                ]
            },
        
        'bull' : {
            'name' : u"Бык",            #название моба применяемое в описании
            'power': {'base' : (2, 0)},         #сила атаки моба (обычная, верная)
            'defence' : {'base' : (2, 0)},      #надежность защиты моба (обычная, верная)
            'modifiers' : [],                   #особые модификаторы
            'image' : 'bull',                   #фоновое изображение для драки в "img/scene/fight/%s.png"
            #набор описаний сцены боя
            'descriptions' : [
                    [['foe_intro'], u"{0} бросается на {1}", ['foe_name', 'dragon_name'], 0],
                    [['foe_intro'], u"{0} роет копытами землю, готовясь напасть", ['foe_name'], 0],
                    [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
                    [['foe_fear'], u"{0} бежит в страхе от {1}", ['foe_name', 'dragon_name'], 0],
                    [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
                    [['foe_dead', 'dragon_wounded'], u"{0} наносит сильный удар, {1} яростным контрударом убивает его", ['foe_name', 'dragon_name'], 0],
                    [['foe_alive', 'dragon_wounded'], u"{0} наносит сильный удар и уворачивается от ответного удара", ['foe_name'], 0],
                    [['foe_alive', 'dragon_undamaged'], u"Противники маневрируют, готовясь к удару", [], 0],
                    [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову", ['foe_name'], 0],
                    [['foe_dead', 'lost_head'], u"{0} ценой головы убивает супостата", ['dragon_name'], 0],
                    [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
                ]
            },
                
        'bull_champion' : {
            'name' : u"Призовой бык",            #название моба применяемое в описании
            'power': {'base' : (3, 0)},         #сила атаки моба (обычная, верная)
            'defence' : {'base' : (3, 0)},      #надежность защиты моба (обычная, верная)
            'modifiers' : [],                   #особые модификаторы
            'image' : 'bull',                   #фоновое изображение для драки в "img/scene/fight/%s.png"
            #набор описаний сцены боя
            'descriptions' : [
                    [['foe_intro'], u"{0} бросается на {1}", ['foe_name', 'dragon_name'], 0],
                    [['foe_intro'], u"{0} роет копытами землю, готовясь напасть", ['foe_name'], 0],
                    [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
                    [['foe_fear'], u"{0} бежит в страхе от {1}", ['foe_name', 'dragon_name'], 0],
                    [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
                    [['foe_dead', 'dragon_wounded'], u"{0} наносит сильный удар, {1} яростным контрударом убивает его", ['foe_name', 'dragon_name'], 0],
                    [['foe_alive', 'dragon_wounded'], u"{0} наносит сильный удар и уворачивается от ответного удара", ['foe_name'], 0],
                    [['foe_alive', 'dragon_undamaged'], u"Противники маневрируют, готовясь к удару", [], 0],
                    [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову", ['foe_name'], 0],
                    [['foe_dead', 'lost_head'], u"{0} ценой головы убивает супостата", ['dragon_name'], 0],
                    [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
                ]
            },
       
        'militia' : {
            'name' : u"Отряд ополчения",            #название моба применяемое в описании
            'power': {'base' : (2, 0)},         #сила атаки моба (обычная, верная)
            'defence' : {'base' : (4, 0)},      #надежность защиты моба (обычная, верная)
            'modifiers' : [],                   #особые модификаторы
            'image' : 'militia',                   #фоновое изображение для драки в "img/scene/fight/%s.png"
            #набор описаний сцены боя
            'descriptions' : [
                    [['foe_intro'], u"{0} бросается на {1}", ['foe_name', 'dragon_name'], 0],
                    [['foe_intro'], u"{0} роет копытами землю, готовясь напасть", ['foe_name'], 0],
                    [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
                    [['foe_fear'], u"{0} бежит в страхе от {1}", ['foe_name', 'dragon_name'], 0],
                    [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
                    [['foe_dead', 'dragon_wounded'], u"{0} наносит сильный удар, {1} яростным контрударом убивает его", ['foe_name', 'dragon_name'], 0],
                    [['foe_alive', 'dragon_wounded'], u"{0} наносит сильный удар и уворачивается от ответного удара", ['foe_name'], 0],
                    [['foe_alive', 'dragon_undamaged'], u"Противники маневрируют, готовясь к удару", [], 0],
                    [['foe_alive', 'lost_head'], u"{0} метким ударом сносит голову", ['foe_name'], 0],
                    [['foe_dead', 'lost_head'], u"{0} ценой головы убивает супостата", ['dragon_name'], 0],
                    [['dragon_dead'], u"{0} умирает от полученных ран", ['dragon_name'], 0]
                ]
            },
        
       }