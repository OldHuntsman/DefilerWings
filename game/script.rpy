


# Начало игры
label start:

    python:
        from pythoncode.treasures import generate_treasures

        lst = generate_treasures(10)
        s = ''
        total = 0
        for i in lst:
            s += str(i) + '\n'
            total += i.cost

        s += 'Total: ' + str(total)
        renpy.say(None, s)
    
    return
