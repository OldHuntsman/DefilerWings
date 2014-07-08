#локация взаимодействий

label lb_nature_sex:
    nvl clear
    menu:
        'Надругаться' if game.girl.virgin and game.dragon.lust > 0:
            $ impregnate()
            'Подходящая сцена секса'
        'Ограбить' if game.girl.treashure != []:
            $ pass
        'Сожрать':
            $ pass
        'Утащить в логово':
            $ pass
        'Отпустить восвояси':
            return      
    jump lb_nature_sex