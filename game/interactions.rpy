# локация взаимодействий

label lb_nature_sex:
    if game.girl.jailed:
        $ place = 'prison'
        show place as bg
    nvl clear
    menu:
        'Надругаться' if game.girls_list.is_mating_possible:
            $ description = game.girls_list.impregnate()
            game.girl.third "[description]"
        'Ограбить' if game.girl.treasure:
            $ description = game.girls_list.rob_girl()
            game.girl.third "[description]"
        'Сожрать' if game.dragon.hunger > 0:
            $ description = game.girls_list.eat_girl()
            game.girl.third "[description]"
            return
        'Вернуть в темницу' if game.girl.jailed:
            $ description = game.girls_list.jail_girl()
            game.girl.third "[description]"
            return
        'Утащить в логово' if not game.girl.jailed:
            $ description = game.girls_list.steal_girl()
            game.girl.third "[description]"
            $ place = game.lair.type_name
            show place
            nvl clear
            $ description = game.girls_list.jail_girl()
            game.girl.third "[description]"
            return
        'Отпустить восвояси':
            $ description = game.girls_list.free_girl()
            game.girl.third "[description]"
            return
    jump lb_nature_sex


label lb_lair_sex:
    if game.girl.jailed:
        $ place = 'prison'
        show place as bg
    nvl clear
    menu:
        'Надругаться' if game.girls_list.is_mating_possible:
            $ description = game.girls_list.impregnate()
            game.girl.third "[description]"
        'Ограбить' if game.girl.treasure:
            $ description = game.girls_list.rob_girl()
            game.girl.third "[description]"
        'Сожрать' if game.dragon.hunger > 0:
            $ description = game.girls_list.eat_girl()
            game.girl.third "[description]"
            return
        'Вернуть в темницу' if game.girl.jailed:
            $ description = game.girls_list.jail_girl()
            game.girl.third "[description]"
            return
        'Утащить в логово' if not game.girl.jailed:
            $ description = game.girls_list.steal_girl()
            game.girl.third "[description]"
            $ place = game.lair.type_name
            show place
            nvl clear
            $ description = game.girls_list.jail_girl()
            game.girl.third "[description]"
            return
        'Отпустить восвояси':
            $ description = game.girls_list.free_girl()
            game.girl.third "[description]"
            return
    jump lb_nature_sex

label lb_gigant_sex:
    nvl clear
    menu:
        'Надругаться' if game.girls_list.is_mating_possible:
            $ description = game.girls_list.impregnate()
            game.girl.third "[description]"
        'Ограбить' if game.girl.treasure:
            $ description = game.girls_list.rob_girl()
            game.girl.third "[description]"
        'Сожрать' if game.dragon.hunger > 0:
            $ description = game.girls_list.eat_girl()
            game.girl.third "[description]"
            return
        'Отпустить восвояси':
            $ description = game.girls_list.free_girl()
            game.girl.third "[description]"
            return
    jump lb_nature_sex


label lb_knight_new:
    show expression 'img/bg/special/oath.png' as bg
    'Рыцарь дал клятву убить дракона.'
    return