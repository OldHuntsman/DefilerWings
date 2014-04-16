# определяем персонажей
define dr = Character("Дракон")
define pr = Character("Принцесса")


# Начало игры
label start:
    $ avatars = Avatars()
    $ avatars.DisplayCenter("far scape") #отображение бэка так чтобы не надо было писать где он находится
    #show ava dragon at topright
    
    $ avatars.DisplayLeft("princess ava ")
    $ avatars.DisplayRight("dragon ava")
    pr 'Hello world!'
    dr 'Grrrrr'

    
    return
