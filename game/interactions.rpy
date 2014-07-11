#локация взаимодействий

label lb_nature_sex:
    nvl clear
    menu:
        'Надругаться' if game.girl.virgin and game.dragon.lust > 0:
            $ impregnate()
            game.girl.third 'Подходящая сцена секса'
        'Ограбить' if game.girl.treashure != []:
            $ pass
        'Сожрать' if game.dragon.hunger > 0:
            game.girl.third 'Описание обеда'
            $ game.dragon.hunger -= 1
            $ game.dragon.bloodiness = 0
            return
        'Утащить в логово':
            '[game.dragon.name] относит пленницу в своё логово...'
            $ place = 'lair'
            show place
            $ game.girl.status = 'hostage'
            '...и сажает её под замок'
            return
        'Отпустить восвояси':
            '[game.dragon.name] отправляется по своим делам.'
            return      
    jump lb_nature_sex