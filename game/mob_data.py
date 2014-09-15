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
                    [['foe_intro'], u"{0} готовится к бою.", ['foe_name'], 0],
                    [['foe_intro'], u"{0} готовится к бою.", ['foe_name'], 0],
                    [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
                    [['foe_fear'], u"{0} убегает в страхе.", ['foe_name'], 0],
                    [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
                    [['foe_dead', 'dragon_wounded'], u"{0} побеждает, но только ценой серьёзных ран.", ['dragon_name',], 0],
                    [['foe_alive', 'dragon_wounded'], u"{0} ранен, {1} продолжает бой.", ['dragon_name'], ['foe_name'], 0],
                    [['foe_alive', 'dragon_undamaged'], u"Силы примерно равны, и никто не может нанести другому значительного вреда.", [], 0],
                    [['foe_alive', 'lost_head'], u"{0} теряет одну голову.", ['dragon_name'], 0],
                    [['foe_dead', 'lost_head'], u"{0} побеждает, но тяжелой ценой. Одна из его голов мертва.", ['dragon_name'], 0],
                    [['dragon_dead'], u"{0} умирает от полученных ран.", ['dragon_name'], 0]
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
                    [['foe_intro'], u"{0} готовится к бою.", ['foe_name'], 0],
                    [['foe_intro'], u"{0} готовится к бою.", ['foe_name'], 0],
                    [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
                    [['foe_fear'], u"{0} убегает в страхе.", ['foe_name'], 0],
                    [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
                    [['foe_dead', 'dragon_wounded'], u"{0} побеждает, но только ценой серьёзных ран.", ['dragon_name',], 0],
                    [['foe_alive', 'dragon_wounded'], u"{0} ранен, {1} продолжает бой.", ['dragon_name'], ['foe_name'], 0],
                    [['foe_alive', 'dragon_undamaged'], u"Силы примерно равны, и никто не может нанести другому значительного вреда.", [], 0],
                    [['foe_alive', 'lost_head'], u"{0} теряет одну голову.", ['dragon_name'], 0],
                    [['foe_dead', 'lost_head'], u"{0} побеждает, но тяжелой ценой. Одна из его голов мертва.", ['dragon_name'], 0],
                    [['dragon_dead'], u"{0} умирает от полученных ран.", ['dragon_name'], 0]
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
                    [['foe_intro'], u"{0} готовится к бою.", ['foe_name'], 0],
                    [['foe_intro'], u"{0} готовится к бою.", ['foe_name'], 0],
                    [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
                    [['foe_fear'], u"{0} убегает в страхе.", ['foe_name'], 0],
                    [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
                    [['foe_dead', 'dragon_wounded'], u"{0} побеждает, но только ценой серьёзных ран.", ['dragon_name',], 0],
                    [['foe_alive', 'dragon_wounded'], u"{0} ранен, {1} продолжает бой.", ['dragon_name'], ['foe_name'], 0],
                    [['foe_alive', 'dragon_undamaged'], u"Силы примерно равны, и никто не может нанести другому значительного вреда.", [], 0],
                    [['foe_alive', 'lost_head'], u"{0} теряет одну голову.", ['dragon_name'], 0],
                    [['foe_dead', 'lost_head'], u"{0} побеждает, но тяжелой ценой. Одна из его голов мертва.", ['dragon_name'], 0],
                    [['dragon_dead'], u"{0} умирает от полученных ран.", ['dragon_name'], 0]
                ]
            },
            
        'mob' : {
            'name' : u"Крестьяне",            #название моба применяемое в описании
            'power': {'base' : (1, 0)},         #сила атаки моба (обычная, верная)
            'defence' : {'base' : (3, 0)},      #надежность защиты моба (обычная, верная)
            'modifiers' : [],                   #особые модификаторы
            'image' : 'mob',                   #фоновое изображение для драки в "img/scene/fight/%s.png"
            #набор описаний сцены боя
            'descriptions' : [
                    [['foe_intro'], u"{0} готовится к бою.", ['foe_name'], 0],
                    [['foe_intro'], u"{0} готовится к бою.", ['foe_name'], 0],
                    [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
                    [['foe_fear'], u"{0} убегает в страхе.", ['foe_name'], 0],
                    [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
                    [['foe_dead', 'dragon_wounded'], u"{0} побеждает, но только ценой серьёзных ран.", ['dragon_name',], 0],
                    [['foe_alive', 'dragon_wounded'], u"{0} ранен, {1} продолжает бой.", ['dragon_name'], ['foe_name'], 0],
                    [['foe_alive', 'dragon_undamaged'], u"Силы примерно равны, и никто не может нанести другому значительного вреда.", [], 0],
                    [['foe_alive', 'lost_head'], u"{0} теряет одну голову.", ['dragon_name'], 0],
                    [['foe_dead', 'lost_head'], u"{0} побеждает, но тяжелой ценой. Одна из его голов мертва.", ['dragon_name'], 0],
                    [['dragon_dead'], u"{0} умирает от полученных ран.", ['dragon_name'], 0]
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
                    [['foe_intro'], u"{0} готовится к бою.", ['foe_name'], 0],
                    [['foe_intro'], u"{0} готовится к бою.", ['foe_name'], 0],
                    [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
                    [['foe_fear'], u"{0} убегает в страхе.", ['foe_name'], 0],
                    [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
                    [['foe_dead', 'dragon_wounded'], u"{0} побеждает, но только ценой серьёзных ран.", ['dragon_name',], 0],
                    [['foe_alive', 'dragon_wounded'], u"{0} ранен, {1} продолжает бой.", ['dragon_name'], ['foe_name'], 0],
                    [['foe_alive', 'dragon_undamaged'], u"Силы примерно равны, и никто не может нанести другому значительного вреда.", [], 0],
                    [['foe_alive', 'lost_head'], u"{0} теряет одну голову.", ['dragon_name'], 0],
                    [['foe_dead', 'lost_head'], u"{0} побеждает, но тяжелой ценой. Одна из его голов мертва.", ['dragon_name'], 0],
                    [['dragon_dead'], u"{0} умирает от полученных ран.", ['dragon_name'], 0]
                ]
            },

        'xbow' : {
            'name' : u"Арбалетчики",            #название моба применяемое в описании
            'power': {'base' : (4, 0)},         #сила атаки моба (обычная, верная)
            'defence' : {'base' : (3, 0)},      #надежность защиты моба (обычная, верная)
            'modifiers' : [],                   #особые модификаторы
            'image' : 'xbow',                   #фоновое изображение для драки в "img/scene/fight/%s.png"
            #набор описаний сцены боя
            'descriptions' : [
                    [['foe_intro'], u"{0} готовится к бою.", ['foe_name'], 0],
                    [['foe_intro'], u"{0} готовится к бою.", ['foe_name'], 0],
                    [['foe_intro'], u"{0} готовится к бою", ['foe_name'], 0],
                    [['foe_fear'], u"{0} убегает в страхе.", ['foe_name'], 0],
                    [['foe_dead', 'dragon_undamaged'], u"{0} побеждает", ['dragon_name'], 0],
                    [['foe_dead', 'dragon_wounded'], u"{0} побеждает, но только ценой серьёзных ран.", ['dragon_name',], 0],
                    [['foe_alive', 'dragon_wounded'], u"{0} ранен, {1} продолжает бой.", ['dragon_name'], ['foe_name'], 0],
                    [['foe_alive', 'dragon_undamaged'], u"Силы примерно равны, и никто не может нанести другому значительного вреда.", [], 0],
                    [['foe_alive', 'lost_head'], u"{0} теряет одну голову.", ['dragon_name'], 0],
                    [['foe_dead', 'lost_head'], u"{0} побеждает, но тяжелой ценой. Одна из его голов мертва.", ['dragon_name'], 0],
                    [['dragon_dead'], u"{0} умирает от полученных ран.", ['dragon_name'], 0]
                ]
            },

        'town' : {
            'name' : u"Защитники города",            #название моба применяемое в описании
            'power': {'base' : (4, 0)},         #сила атаки моба (обычная, верная)
            'defence' : {'base' : (6, 0)},      #надежность защиты моба (обычная, верная)
            'modifiers' : [],                   #особые модификаторы
            'image' : 'town',                   #фоновое изображение для драки в "img/scene/fight/%s.png"
            #набор описаний сцены боя
            'descriptions' : [
                    [['foe_intro'], u"{0} готовится к бою.", ['foe_name'], 0],
                    [['foe_intro'], u"{0} готовится к бою.", ['foe_name'], 0],
                    [['foe_intro'], u"{0} готовится к бою.", ['foe_name'], 0],
                    [['foe_fear'], u"{0} убегает в страхе.", ['foe_name'], 0],
                    [['foe_dead', 'dragon_undamaged'], u"{0} побеждает.", ['dragon_name'], 0],
                    [['foe_dead', 'dragon_wounded'], u"{0} побеждает, но только ценой серьёзных ран.", ['dragon_name',], 0],
                    [['foe_alive', 'dragon_wounded'], u"{0} ранен, {1} продолжает бой.", ['dragon_name'], ['foe_name'], 0],
                    [['foe_alive', 'dragon_undamaged'], u"Силы примерно равны, и никто не может нанести другому значительного вреда.", [], 0],
                    [['foe_alive', 'lost_head'], u"{0} теряет одну голову.", ['dragon_name'], 0],
                    [['foe_dead', 'lost_head'], u"{0} побеждает, но тяжелой ценой. Одна из его голов мертва.", ['dragon_name'], 0],
                    [['dragon_dead'], u"{0} умирает от полученных ран.", ['dragon_name'], 0],
                ]
            },
                                
       }