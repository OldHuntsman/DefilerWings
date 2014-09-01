# имена девушек генерируются из списков имен (тип девушки_first) и фамилий (тип девушки_last). Если списка фамилий нет - генерируется только из списка имен. 
girls_names = {}
girls_names['peasant_first'] = [u'Манька', u'Зойка', u'Жанна', u'Танька', u'Катька',]
girls_names['citizen_first'] = [u'Афина', u'Лира']
girls_names['citizen_last'] = [u'Тимохина', u'Светина']

girls_info = { #Информация о всех типах девушек 
                'peasant' : {
                        'magic_rating' : 0, #магический рейтинг
                        'regular_spawn' : 'poisonous_asp', #идентификатор обычного отродья
                        'advanced_spawn' : 'winged_asp', #идентификатор продвинутого отродья
                        'giantess' : False, #является ли великаншей
                        'avatar' : 'peasant', #аватарка
                        't_count_min' : 0, #количество сокровищ минимальное
                        't_count_max' : 2, #количество сокровищ максимальное
                        't_price_min' : 1, #минимальная цена предмета
                        't_price_max' : 50, #максимальная цена предмета
                        't_alignment' : 'human'
                        't_list' : [casket, statue, mirror, comb, phallos, band, earring, necklace, pendant, ring, broch, armbrace, legbrace, fibula, farting], #список возможных предметов в сокровищах 
                        
                    },
                'citizen' : {
                        'magic_rating' : 0,
                        'regular_spawn' : 'kokatriks',
                        'advanced_spawn' : 'basilisk',
                        'giantess' : False,
                        'avatar' : 'citizen',
                        't_count_min' : 2,
                        't_count_max' : 5,
                        't_price_min' : 25,
                        't_price_max' : 250,
                        't_alignment' : 'human'
                        't_list' : [casket, statue, mirror, comb, phallos, band, diadem, tiara, earring, necklace, pendant, ring, broch, gemring, armbrace, legbrace, chain, fibula, farting, taller], 
                    },
                'thief' : {
                        'magic_rating' : 0,
                        'regular_spawn' : 'kokatriks',
                        'advanced_spawn' : 'basilisk',
                        'giantess' : False,
                        'avatar' : 'thief',
                        't_count_min' : 2,
                        't_count_max' : 5,
                        't_price_min' : 25,
                        't_price_max' : 250,
                        't_alignment' : 'human'
                        't_list' : [casket, statue, mirror, comb, phallos, band, diadem, tiara, earring, necklace, pendant, ring, broch, gemring, armbrace, legbrace, chain, fibula, taller, dublon],                         
                    }, 
                'knight' : {
                        'magic_rating' : 1,
                        'regular_spawn' : 'kobold',
                        'advanced_spawn' : 'raptor',
                        'giantess' : False,
                        'avatar' : 'knight',
                        't_count_min' : 2,
                        't_count_max' : 5,
                        't_price_min' : 25,
                        't_price_max' : 250,
                        't_alignment' : 'knight'
                        't_list' : [casket, statue, mirror, comb, phallos, band, diadem, tiara, earring, necklace, pendant, ring, broch, gemring, armbrace, legbrace, chain, fibula, taller, dublon],                         
                    },
                'princess' : {
                        'magic_rating' : 1,
                        'regular_spawn' : 'kobold',
                        'advanced_spawn' : 'raptor',
                        'giantess' : False,
                        'avatar' : 'princess',
                        't_count_min' : 4,
                        't_count_max' : 10,
                        't_price_min' : 250,
                        't_price_max' : 100000,
                        't_alignment' : 'human'
                        't_list' : [casket, statue, mirror, comb, phallos, band, diadem, tiara, earring, necklace, pendant, ring, broch, gemring, armbrace, legbrace, chain, fibula, taller, dublon], 
                    },
                'elf' : { 
                        'magic_rating' : 2,
                        'regular_spawn' : 'dragonborn',
                        'advanced_spawn' : 'gargoyle',
                        'giantess' : False,
                        'avatar' : 'elf',
                        't_count_min' : 3,
                        't_count_max' : 7,
                        't_price_min' : 250,
                        't_price_max' : 100000,
                        't_alignment' : 'elf'
                        't_list' : [casket, statue, mirror, comb, phallos, band, diadem, tiara, earring, necklace, pendant, ring, broch, gemring, armbrace, legbrace, chain],                         
                    },
                'mermaid' : {
                        'magic_rating' : 2,
                        'regular_spawn' : 'sea_bastard',
                        'advanced_spawn' : 'poisonous_octopus',
                        'giantess' : False,
                        'avatar' : 'mermaid',
                        't_count_min' : 2,
                        't_count_max' : 5,
                        't_price_min' : 10,
                        't_price_max' : 500,
                        't_alignment' : 'merman'
                        't_list' : [casket, statue, mirror, comb, phallos, band, diadem, tiara, earring, necklace, pendant, ring, broch, gemring, armbrace, legbrace, chain],  
                    },               
                'ogre' : {  
                        'magic_rating' : 2,
                        'regular_spawn' : 'troglodyte',
                        'advanced_spawn' : 'minotaur',
                        'giantess' : True,
                        'avatar' : 'ogre',
                        't_count_min' : 2,
                        't_count_max' : 5,
                        't_price_min' : 25,
                        't_price_max' : 250,
                        't_alignment' : 'knight'
                        't_list' : [casket, statue, mirror, comb, phallos, band, diadem, tiara, earring, necklace, pendant, ring, broch, gemring, armbrace, legbrace, chain, fibula, farting, taller, dublon],                         
                    },    
                'siren' : {
                        'magic_rating' : 3,
                        'regular_spawn' : 'murloc',
                        'advanced_spawn' : 'naga',
                        'giantess' : True,
                        'avatar' : 'mermaid',
                        't_count_min' : 2,
                        't_count_max' : 5,
                        't_price_min' : 100,
                        't_price_max' : 5000,
                        't_alignment' : 'merman'
                        't_list' : [casket, statue, mirror, comb, phallos, band, diadem, tiara, earring, necklace, pendant, ring, broch, gemring, armbrace, legbrace, chain, taller, dublon],                          
                    },
                'ice' : {  
                        'magic_rating' : 3,
                        'regular_spawn' : 'yettie',
                        'advanced_spawn' : 'troll',
                        'giantess' : True,
                        'avatar' : 'ice',
                        't_count_min' : 3,
                        't_count_max' : 7,
                        't_price_min' : 100,
                        't_price_max' : 1000,
                        't_alignment' : 'human'
                        't_list' : [casket, statue, mirror, comb, phallos, band, diadem, tiara, earring, necklace, pendant, ring, broch, gemring, armbrace, legbrace, chain, taller, dublon],                            
                    },
                'fire' : {  
                        'magic_rating' : 3,
                        'regular_spawn' : 'devas',
                        'advanced_spawn' : 'barlog',
                        'giantess' : True,
                        'avatar' : 'fire',
                        't_count_min' : 3,
                        't_count_max' : 7,
                        't_price_min' : 100,
                        't_price_max' : 1000,
                        't_alignment' : 'dwarf'
                        't_list' : [casket, statue, mirror, comb, phallos, band, diadem, tiara, earring, necklace, pendant, ring, broch, gemring, armbrace, legbrace, chain, taller, dublon],  
                    },
                'titan' : {  
                        'magic_rating' : 4,
                        'regular_spawn' : 'chimera',
                        'advanced_spawn' : 'typhon',
                        'giantess' : True,
                        'avatar' : 'titan',
                        't_count_min' : 3,
                        't_count_max' : 7,
                        't_price_min' : 100,
                        't_price_max' : 1000,
                        't_alignment' : 'elf'
                        't_list' : [casket, statue, mirror, comb, phallos, band, diadem, tiara, earring, necklace, pendant, ring, broch, gemring, armbrace, legbrace, chain, taller, dublon],                          
                    },
            }
            
spawn_info = { #Информация о всех типах отродий
            'poisonous_asp' : {
                        'power' : 1,  #сила
                        'modifier' : ['poisonous'], #возможные роли
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
        'free_prison' : ( #Описание процесса выпускания на свободу из тюрьмы
            u"Описание процесса выпускания на свободу из тюрьмы",
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
            u"{0} рожает кучу тварей, известных людям под именем {2}",
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
        'prison' : ( #Проведываем девушку в тюрьме 
            u"{0} в тюрьме",
            ),
        },
    'peasant' : { #используется для крестьянок
        'sex' : ( #Возможные описания секса с крестьянкой
            u"Подходящая сцена секса c крестьянкой",
            )
        },
    }