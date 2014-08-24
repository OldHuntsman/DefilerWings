girls_names = {}
girls_names['peasant'] = [u'Манька', u'Зойка', u'Жанна']

girls_info = { #Информация о всех типах девушек 
                'peasant' : {
                        'magic_rating' : 0, #магический рейтинг
                        'regular_spawn' : 'poisonous_asp', #идентификатор обычного отродья
                        'advanced_spawn' : 'winged_asp', #идентификатор продвинутого отродья
                        'giantess' : False, #является ли великаншей
                        'avatar' : 'peasant', #аватарка
                    },
                'citizen' : {
                        'magic_rating' : 0,
                        'regular_spawn' : 'kokatriks',
                        'advanced_spawn' : 'basilisk',
                        'giantess' : False,
                        'avatar' : 'citizen',
                    },
                'thief' : {
                        'magic_rating' : 0,
                        'regular_spawn' : 'kokatriks',
                        'advanced_spawn' : 'basilisk',
                        'giantess' : False,
                        'avatar' : 'thief',
                    }, 
                'knight' : {
                        'magic_rating' : 1,
                        'regular_spawn' : 'kobold',
                        'advanced_spawn' : 'raptor',
                        'giantess' : False,
                        'avatar' : 'knight',
                    },
                'princess' : {
                        'magic_rating' : 1,
                        'regular_spawn' : 'kobold',
                        'advanced_spawn' : 'raptor',
                        'giantess' : False,
                        'avatar' : 'princess',
                    },
                'elf' : { 
                        'magic_rating' : 2,
                        'regular_spawn' : 'dragonborn',
                        'advanced_spawn' : 'gargoyle',
                        'giantess' : False,
                        'avatar' : 'elf',
                    },
                'mermaid' : {
                        'magic_rating' : 2,
                        'regular_spawn' : 'sea_bastard',
                        'advanced_spawn' : 'poisonous_octopus',
                        'giantess' : False,
                        'avatar' : 'mermaid',
                    },               
                'ogre' : {  
                        'magic_rating' : 2,
                        'regular_spawn' : 'troglodyte',
                        'advanced_spawn' : 'minotaur',
                        'giantess' : True,
                        'avatar' : 'ogre',
                    },    
                'siren' : {
                        'magic_rating' : 3,
                        'regular_spawn' : 'murloc',
                        'advanced_spawn' : 'naga',
                        'giantess' : True,
                        'avatar' : 'mermaid',
                    },
                'ice' : {  
                        'magic_rating' : 3,
                        'regular_spawn' : 'yettie',
                        'advanced_spawn' : 'troll',
                        'giantess' : True,
                        'avatar' : 'ice',
                    },
                'fire' : {  
                        'magic_rating' : 3,
                        'regular_spawn' : 'devas',
                        'advanced_spawn' : 'barlog',
                        'giantess' : True,
                        'avatar' : 'fire',
                    },
                'titan' : {  
                        'magic_rating' : 4,
                        'regular_spawn' : 'chimera',
                        'advanced_spawn' : 'typhon',
                        'giantess' : True,
                        'avatar' : 'titan',
                    },
            }
            
spawn_info = { #Информация о всех типах отродий
            'poisonous_asp' : {
                        'power' : 1,  #сила
                        'modifier' : ['poisonous', 'warrior', 'elite', 'servant', 'marine'], #возможные роли
                        'name' : u'Ядовитый аспид', #название
                    },
            'winged_asp' : {
                        'power' : 2,  
                        'modifier' : ['poisonous'], 
                        'name' : u'Крылатый аспид', 
                    },
            'kokatriks' : {
                        'power' : 2, 
                        'modifier' : ['poisonous'], 
                        'name' : u'Кокатрикс',
                    },
            'basilisk' : {
                        'power' : 3,  
                        'modifier' : ['poisonous'],
                        'name' : u'Василиск',
                    }, 
            'kobold' : {
                        'power' : 2,  
                        'modifier' : ['servant'],
                        'name' : u'Кобольд',
                    }, 
            'raptor' : {
                        'power' : 3,  
                        'modifier' : ['servant'],
                        'name' : u'Ящерик',
                    },     
            'dragonborn' : {
                        'power' : 3,  
                        'modifier' : ['warrior'],
                        'name' : u'Драконорождённый',
                    }, 
            'gargoyle' : {
                        'power' : 4,  
                        'modifier' : ['warrior'],
                        'name' : u'Гаргуйль',
                    },   
            'sea_bastard' : {
                        'power' : 3,  
                        'modifier' : ['poisonous', 'marine'],
                        'name' : u'Морской гад',
                    }, 
            'poisonous_octopus' : {
                        'power' : 5,  
                        'modifier' : ['poisonous', 'marine'],
                        'name' : u'Ядовитый спрут',
                    },      
            'troglodyte' : {
                        'power' : 4,  
                        'modifier' : ['warrior'],
                        'name' : u'Троглодит',
                    }, 
            'minotaur' : {
                        'power' : 5,  
                        'modifier' : ['elite'],
                        'name' : u'Минотавр',
                    },     
            'murloc' : {
                        'power' : 3,  
                        'modifier' : ['servant', 'warrior', 'marine'],
                        'name' : u'Мурлок',
                    }, 
            'naga' : {
                        'power' : 5,  
                        'modifier' : ['elite', 'marine'],
                        'name' : u'Нага',
                    },    
            'yettie' : {
                        'power' : 5,  
                        'modifier' : ['warrior'],
                        'name' : u'Йетти',
                    }, 
            'troll' : {
                        'power' : 6,  
                        'modifier' : ['elite'],
                        'name' : u'Тролль',
                    },      
            'devas' : {
                        'power' : 6,  
                        'modifier' : ['warrior'],
                        'name' : u'Дэв',
                    }, 
            'barlog' : {
                        'power' : 7,  
                        'modifier' : ['elite'],
                        'name' : u'Барлог',
                    },          
            'chimera' : {
                        'power' : 10,  
                        'modifier' : ['poisonous'],
                        'name' : u'Химера',
                    }, 
            'typhon' : {
                        'power' : 10,  
                        'modifier' : ['elite'],
                        'name' : u'Тифон',
                    },                    
        }

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