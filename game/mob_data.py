#Одноразовые противники
mob = {
        'calf' : {
            'name' : u"Теленок",
            'power': {'base' : (2, 0)},
            'defence' : {'base' : (2, 0)},
            'modifiers' : [],
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
        
        'bull' : {
            'name' : u"Бык",
            'power': {'base' : (3, 0)},
            'defence' : {'base' : (3, 0)},
            'modifiers' : [],
            'image' : 'bull',
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
        
        'buffalo' : {
            'name' : u"Бизон",
            'power': {'base' : (10, 0)},
            'defence' : {'base' : (10, 0)},
            'modifiers' : [],
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
        
        'minotaur' : {
            'name' : u"Минотавр",
            'power': {'base' : (15, 0)},
            'defence' : {'base' : (15, 0)},
            'modifiers' : [],
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
            
        'Jupiter' : {
            'name' : u"Юпитер",
            'power': {'base' : (20, 0)},
            'defence' : {'base' : (20, 0)},
            'modifiers' : [],
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