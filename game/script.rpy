# определяем персонажей
define dr = Character("Дракон")
define pr = Character("Принцесса")


# Начало игры
label start:
    $ avatars = Avatars()
    show bg farscape
    #show ava dragon at topright
    
    $ avatars.DisplayLeft("princess ava ")
    pr 'Hello world!'
    $ avatars.DisplayRight("dragon ava")
    dr 'Grrrrr'

    
    return
