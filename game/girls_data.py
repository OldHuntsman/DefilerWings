﻿girls_names = {}
girls_names['peasant'] = [u'Манька', u'Зойка', u'Жанна']

girls_texts = { #Подстановки: {0} - имя девушки, {1} - имя дракона, {2} - ситуативные описания - что украли, кого родила и прочее
    'girl' : { #используется, если нет подходящего текста или отсутствует нужный тип девушки 
        'sex' : ( #Описание секса с девушкой
            u"Случайная сцена секса вариант 1",
            u"Случайная сцена секса вариант 2",
            u"Случайная сцена секса вариант 3",
            ),
        'new' : ( #Описание новой девушки
            u"Описание девушки",
            ),
        'free' : ( #Описание процесса выпускания на свободу
            u"Описание процесса выпускания на свободу",
            ),
        'steal' : ( #Описание процесса воровства девушки 
            u"{1} относит пленницу в своё логово...",
            ),
        'jail' : ( #Описание процесса заточения в темницу
            u"...и сажает её под замок",
            ),
        'jailed' : ( #Описание процесса возврата в темницу 
            u"{1} возвращает девушку в темницу",
            ),
        'eat' : ( #Описание процесса поедания девушки. Как же ему не стыдно, червяку подколодному. 
            u"{1} кушает девушку",
            ),
        'rob' : ( #Описание процесса ограбления девушки. 
            u"{1} грабит девушку",
            ),
        'traps' : ( #Описание процесса побега и гибели в ловушке. 
            u"{0} убегает из темницы и гибнет в ловушках",
            ),
        'escape' : ( #Описание успешного побега 
            u"{0} спасается бегством",
            ),
        'birth' : ( #Описание родов
            u"{0} рожает что-то",
            ),
        'anguish' : ( #Описание смерти от тоски
            u"{0} умирает в тоске",
            ),    
        'hunger' : ( #Описание смерти от голода
            u"{0} умирает от голода",
            ),    
        'kill' : ( #Описание смерти от селян
            u"Люди узнают, что {0} беременна от дракона и убивают её",
            ),
        'free_birth' : ( #Описание родов на свободе
            u"{0} рожает что-то на воле",
            ),
        },
    'peasant' : { #используется для крестьянок
        'sex' : ( #Возможные описания секса с крестьянкой
            u"Подходящая сцена секса c крестьянкой",
            )
        },
    }