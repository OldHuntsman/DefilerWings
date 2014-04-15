# определяем персонажей
define dr = Character("Дракон", kind=nvl, image = 'ava')
define pr = Character("Принцесса", kind=nvl, image = 'ava')

# Начало игры
label start:
    show bg farscape
    show ava dragon at topright
    
    dr dragon 'Hello world!'
    pr princess 'Сам такой'

    
    return
