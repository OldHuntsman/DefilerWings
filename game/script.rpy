# определяем персонажей
define dr = Character("Дракон")
define pr = Character("Принцесса")


# Начало игры
label start:
    $ avatars = Avatars() # Инициализируем модуль с аватарками
    $ avatars.DisplayCenter("far scape") #отображение бэка так чтобы не надо было писать где он находится
    #show ava dragon at topright
    
    $ avatars.DisplayLeft("princess ava ") # Показываем принцессу слева
    $ avatars.DisplayRight("dragon ava") # Показываем дракона справа
    pr 'Hello world!'
    dr 'Grrrrr'

    
    return
