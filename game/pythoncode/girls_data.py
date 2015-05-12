# coding=utf-8
# имена девушек генерируются из списков имен (тип девушки_first) и фамилий (тип девушки_last). Если списка фамилий
# нет - генерируется только из списка имен.
girls_names = {
    'peasant_first': [
        u'Жанна', u'Герда', u'Баббета', u'Cюзи', u'Альба', u'Амели', u'Аннета', u'Жоржетта', u'Бетти',
        u'Бетси', u'Бланка', u'Бьянка', u'Дейзи', u'Джинни', u'Джуди', u'Дороти', u'Зои', u'Ирен', u'Ивет',
        u'Колет', u'Криси', u'Кэтти', u'Кэт', u'Лили', u'Лиди', u'Лулу'
    ],
    'citizen_first': [
        u'Аделия', u'Аврора', u'Альбертина', u'Анджелла', u'Аврелия', u'Беатрис', u'Бернадетт',
        u'Бриджит', u'Вероник', u'Виолет', u'Вирджиния', u'Габриэлла', u'Джаннет', u'Джулиана', u'Доминика',
        u'Жаклина', u'Жозефина', u'Джульетта', u'Камилла', u'Каролина', u'Кэйтлин', u'Ирен', u'Мелисса', u'Марджори',
        u'Натали', u'Пенелопа', u'Розали', u'Розета', u'Селеста', u'Симона', u'Стефани', u'Сюзанна',
        u'Тереза', u'Флора', u'Эммануэль', u'Адалинда', u'Альбертина', u'Амелинда', u'Гризельда',
        u'Виктория', u'Ирма', u'Каролина', u'Кристиана', u'Кэтрин', u'Лиона', u'Лорели', u'Маргарита', u'Франциска',
        u'Хенелора', u'Хильда', u'Элеонора', u'Абигайль', u'Антония', u'Долорес', u'Доротея',
        u'Женевьева', u'Жозефина', u'Инесс', u'Кармелита', u'Консуэлла', u'Летиция', u'Марселла', u'Присцилла',
        u'Рамона', u'София', u'Ефимия', u'Ефания', u'Лидия', u'Беатриче',
    ],
    'princess_first': [
        u'Аннабель', u'Аделия', u'Авелин', u'Айседора', u'Альбертина', u'Анастасия', u'Антуанетта',
        u'Беатрис', u'Валентина', u'Виктория', u'Габриэлла', u'Джиневра', u'Доминика', u'Джулианна',
        u'Джульетта', u'Жюстина', u'Жозефина', u'Ивонна', u'Изабелла', u'Камилла', u'Клариса',
        u'Клементина', u'Кристина', u'Лукреция', u'Марго', u'Матильда', u'Мелисента', u'Марианна', u'Олимпия',
        u'Пенелопа', u'Розалинда', u'Розамунда', u'Селестина', u'Серафина', u'Сюзанна', u'Стефания', u'Тереза',
        u'Флафия', u'Фелиция', u'Генриэтта', u'Гертруда', u'Шарлотта', u'Эмммануэль', u'Альбертина', u'Амелинда',
        u'Брунгильда', u'Вильгельмина', u'Изольда', u'Рафаэлла', u'Амаранта', u'Дельфиния', u'Доротея',
        u'Мерседес', u'Офелия',
    ],
    'princess_last': [
        u'дэ Мюзи', u'фон Баургафф', u'дэ Альбре', u'дэ Блуа', u'дэ Виржи', u'ди Гиз', u'дэ Бриенн',
        u'дэ Колиньи', u'дэ Ла Тур', u'дэ Лузиньян', u'дэ Фуа', u'дэ Брисак', u'дэ Круа', u'дэ Лин',
        u'дэ Кюлот', u'дэ Сен-При', u'фон Баттенберг', u'фон Беннгис', u'фон Вальбиц', u'фон Вительсбах',
        u'фон Гогеншауфен', u'фон Зальф', u'фон Люденштафф', u'фон Мирбах', u'фон Розен', u'фон Церинген',
        u'фон Грюнберг', u'фон Штюрберг', u'фон Шелленбург', u'Строцци', u'Сфорца', u'Альбици',
        u'Барбариго', u'Пацци', u'Бранкаччо', u'да Верана', u'Висконти', u'Гримальди', u'да Полента', u'делла Тори',
        u'да Камино', u'Монтрефельто', u'Манфреди', u'Фарнезе', u'Фрегозо', u'де Мендоза', u'ла Серда',
    ],
    'elf_first': [
        u'Берунвен', u'Фанавен', u'Арвен', u'Лучиэнь', u'Феалиндэ', u'Эстелендиль', u'Астера', u'Теолинвен',
        u'Куивэн', u'Мрвэн', u'Интиальвен', u'Анарвен', u'Аманиэль', u'Анариэль', u'Лариэль', u'Лотанариэ',
        u'Исильиндиль', u'Селфарианис', u'Йорингель', u'Оросинвиль', u'Гилэстель', u'Валакирэ'
    ],
    'ogre_first': [
        u'Хунн', u'Йорва', u'Дирга', u'Велга', u'Сига', u'Йалгуль', u'Дорба', u'Гирга', u'Давири', u'Шалга',
        u'Орва', u'Дезра', u'Арга', u'Бигра', u'Варга', u'Енза', u'Зарта', u'Икла', u'Корда', u'Логаза',
        u'Мирбу', u'Нира',
    ],
    'mermaid_first': [
        u'Ариэль', u'Блажена', u'Будимила', u'Ведана', u'Велина', u'Венцеслава', u'Верея', u'Велезара',
        u'Веселина', u'Витана', u'Влада', u'Весемлиа', u'Годица', u'Горлина', u'Далина', u'Ждана',
        u'Деяна', u'Дивина', u'Доляна', u'Есена', u'Жилена', u'Завида', u'Зоряна', u'Златина', u'Ивица',
        u'Калёна', u'Красоя', u'Купава', u'Лада', u'Леля', u'Малиша', u'Млава', u'Милана', u'Младлена',
        u'Мирана', u'Невена', u'Обрица', u'Пава', u'Пригода', u'Рада', u'Ракита', u'Ружана',
        u'Силимина', u'Серебрина', u'Славена', u'Станимира', u'Стояна', u'Томила', u'Умила', u'Ундина',
        u'Цветана', u'Чаруна', u'Янина', u'Яромила', u'Ясмания'
    ],
    'siren_first': [
        u'Ариэль', u'Блажена', u'Будимила', u'Ведана', u'Велина', u'Венцеслава', u'Верея', u'Велезара',
        u'Веселина', u'Витана', u'Влада', u'Весемлиа', u'Годица', u'Горлина', u'Далина', u'Ждана', u'Деяна',
        u'Дивина', u'Доляна', u'Есена', u'Жилена', u'Завида', u'Зоряна', u'Златина', u'Ивица', u'Калёна',
        u'Красоя', u'Купава', u'Лада', u'Леля', u'Малиша', u'Млава', u'Милана', u'Младлена', u'Мирана',
        u'Невена', u'Обрица', u'Пава', u'Пригода', u'Рада', u'Ракита', u'Ружана', u'Силимина', u'Серебрина',
        u'Славена', u'Станимира', u'Стояна', u'Томила', u'Умила', u'Ундина', u'Цветана', u'Чаруна',
        u'Янина', u'Яромила', u'Ясмания'
    ],
    'ice_first': [
        u'Астрид', u'Бригита', u'Боргильда', u'Вигдис', u'Вилла', u'Гурдун', u'Гунхильд', u'Дорта', u'Ингрид',
        u'Ингеборга', u'Йорнун', u'Матильда', u'Рангильда', u'Руна', u'Сигурд', u'Сванхильда', u'Сигюнд',
        u'Ульрика', u'Фрида', u'Хлодвен', u'Хильда', u'Эрика'
    ],
    'fire_first': [
        u'Азиль', u'Азиза', u'Базайна', u'Багира', u'Будур', u'Бушра', u'Гюльчатай', u'Гуля', u'Гульнара',
        u'Гулистан', u'Фируза', u'Фатима', u'Ясмин', u'Айгюль', u'Зульфия', u'Ламия', u'Лейла', u'Марьям',
        u'Самира', u'Хурма',
        u'Чинара', u'Эльмира'
    ],
    'titan_first': [
        u'Агата', u'Адонисия', u'Алексино', u'Амброзия', u'Антигона', u'Ариадна', u'Артемисия', u'Афродита',
        u'Гликерия', u'Дельфиния', u'Деметра', u'Зиновия', u'Калисто', u'Калипсо', u'Кора', u'Ксения',
        u'Медея', u'Мельпомена', u'Мнемозина', u'Немезида', u'Олимпия', u'Пандора', u'Персефона',
        u'Таисия', u'Персея', u'Персея', u'Психея', u'Сапфо', u'Талия', u'Терпсихора', u'Фаломена',
        u'Гаромония', u'Хрисеида', u'Эфимия', u'Юнона'
    ]
}

# Информация о всех типах девушек
girls_info = {
    'peasant': {
        'magic_rating': 0,  # магический рейтинг
        'regular_spawn': 'poisonous_asp',  # идентификатор обычного отродья
        'advanced_spawn': 'basilisk',  # идентификатор продвинутого отродья
        'giantess': False,  # является ли великаншей
        'avatar': 'peasant',  # аватарка
        'description': u'селянка',  # описание для вывода в текст
        't_count_min': 0,  # количество сокровищ минимальное
        't_count_max': 2,  # количество сокровищ максимальное
        't_price_min': 1,  # минимальная цена предмета
        't_price_max': 25,  # максимальная цена предмета
        't_alignment': 'human',  # тип украшений
        't_list': [
            'casket', 'statue', 'mirror', 'comb', 'phallos', 'band', 'earring', 'necklace',
            'pendant', 'ring', 'broch', 'armbrace', 'legbrace', 'fibula', 'farting'],
        # список возможных предметов в сокровищах
    },
    'citizen': {
        'magic_rating': 0,
        'regular_spawn': 'winged_asp',
        'advanced_spawn': 'kobold',
        'giantess': False,
        'avatar': 'citizen',
        'description': u'горожанка',
        't_count_min': 0,
        't_count_max': 4,
        't_price_min': 25,
        't_price_max': 100,
        't_alignment': 'human',
        't_list': [
            'casket', 'statue', 'mirror', 'comb', 'phallos', 'band', 'diadem', 'tiara', 'earring',
            'necklace', 'pendant', 'ring', 'broch', 'gemring', 'armbrace', 'legbrace', 'chain',
            'fibula', 'taller'],
    },
    'thief': {
        'magic_rating': 0,
        'regular_spawn': 'winged_asp',
        'advanced_spawn': 'kobold',
        'giantess': False,
        'avatar': 'thief',
        'description': u'воровка',
        't_count_min': 2,
        't_count_max': 5,
        't_price_min': 25,
        't_price_max': 250,
        't_alignment': 'human',
        't_list': [
            'casket', 'statue', 'mirror', 'comb', 'phallos', 'band', 'diadem', 'tiara', 'earring',
            'necklace', 'pendant', 'ring', 'broch', 'gemring', 'armbrace', 'legbrace', 'chain',
            'fibula', 'taller', 'dublon'],
    },
    'knight': {
        'magic_rating': 1,
        'regular_spawn': 'krokk',
        'advanced_spawn': 'lizardman',
        'giantess': False,
        'avatar': 'knight',
        'description': u'воительница',
        't_count_min': 2,
        't_count_max': 5,
        't_price_min': 25,
        't_price_max': 250,
        't_alignment': 'knight',
        't_list': [
            'casket', 'statue', 'mirror', 'comb', 'phallos', 'band', 'diadem', 'tiara', 'earring',
            'necklace', 'pendant', 'ring', 'broch', 'gemring', 'armbrace', 'legbrace', 'chain',
            'fibula', 'taller', 'dublon'],
    },
    'princess': {
        'magic_rating': 1,
        'regular_spawn': 'krokk',
        'advanced_spawn': 'lizardman',
        'giantess': False,
        'avatar': 'princess',
        'description': u'аристократка',
        't_count_min': 2,
        't_count_max': 5,
        't_price_min': 100,
        't_price_max': 1000,
        't_alignment': 'knight',
        't_list': [
            'casket', 'statue', 'mirror', 'comb', 'phallos', 'band', 'diadem', 'tiara', 'earring',
            'necklace', 'pendant', 'ring', 'broch', 'gemring', 'armbrace', 'legbrace', 'chain',
            'fibula'],
    },
    'elf': {
        'magic_rating': 2,
        'regular_spawn': 'gargoyle',
        'advanced_spawn': 'dragonborn',
        'giantess': False,
        'avatar': 'elf',
        'description': u'эльфийская дева',
        't_count_min': 1,
        't_count_max': 4,
        't_price_min': 250,
        't_price_max': 2000,
        't_alignment': 'elf',
        't_list': [
            'casket', 'statue', 'mirror', 'comb', 'phallos', 'band', 'diadem', 'tiara', 'earring',
            'necklace', 'pendant', 'ring', 'broch', 'gemring', 'armbrace', 'legbrace', 'chain'],
    },
    'mermaid': {
        'magic_rating': 2,
        'regular_spawn': 'octopus',
        'advanced_spawn': 'sea_bastard',
        'giantess': False,
        'avatar': 'mermaid',
        'description': u'русалка',
        't_count_min': 0,
        't_count_max': 4,
        't_price_min': 10,
        't_price_max': 200,
        't_alignment': 'merman',
        't_list': [
            'casket', 'statue', 'mirror', 'comb', 'phallos', 'band', 'diadem', 'tiara', 'earring',
            'necklace', 'pendant', 'ring', 'broch', 'gemring', 'armbrace', 'legbrace', 'chain'],
    },
    'ogre': {
        'magic_rating': 2,
        'regular_spawn': 'strigg',
        'advanced_spawn': 'minotaur',
        'giantess': True,
        'avatar': 'ogre',
        'description': u'людоедка',
        't_count_min': 0,
        't_count_max': 3,
        't_price_min': 250,
        't_price_max': 1500,
        't_alignment': 'knight',
        't_list': [
            'casket', 'statue', 'mirror', 'comb', 'phallos', 'band', 'diadem', 'tiara', 'earring',
            'necklace', 'pendant', 'ring', 'broch', 'gemring', 'armbrace', 'legbrace', 'chain',
            'fibula', 'farting', 'taller', 'dublon'],
    },
    'siren': {
        'magic_rating': 2,
        'regular_spawn': 'murloc',
        'advanced_spawn': 'naga',
        'giantess': True,
        'avatar': 'mermaid',
        'description': u'сирена',
        't_count_min': 1,
        't_count_max': 4,
        't_price_min': 250,
        't_price_max': 2000,
        't_alignment': 'merman',
        't_list': [
            'casket', 'statue', 'mirror', 'comb', 'phallos', 'band', 'diadem', 'tiara', 'earring',
            'necklace', 'pendant', 'ring', 'broch', 'gemring', 'armbrace', 'legbrace', 'chain',
            'taller', 'dublon'],
    },
    'ice': {
        'magic_rating': 2,
        'regular_spawn': 'ice_worm',
        'advanced_spawn': 'yettie',
        'giantess': True,
        'avatar': 'ice',
        'description': u'ледяная великанша',
        't_count_min': 1,
        't_count_max': 5,
        't_price_min': 250,
        't_price_max': 2500,
        't_alignment': 'human',
        't_list': [
            'casket', 'statue', 'mirror', 'comb', 'phallos', 'band', 'diadem', 'tiara', 'earring',
            'necklace', 'pendant', 'ring', 'broch', 'gemring', 'armbrace', 'legbrace', 'chain',
            'taller', 'dublon'],
    },
    'fire': {
        'magic_rating': 2,
        'regular_spawn': 'hell_hound',
        'advanced_spawn': 'barlog',
        'giantess': True,
        'avatar': 'fire',
        'description': u'огненная великанша',
        't_count_min': 1,
        't_count_max': 5,
        't_price_min': 250,
        't_price_max': 2500,
        't_alignment': 'dwarf',
        't_list': [
            'casket', 'statue', 'mirror', 'comb', 'phallos', 'band', 'diadem', 'tiara', 'earring',
            'necklace', 'pendant', 'ring', 'broch', 'gemring', 'armbrace', 'legbrace', 'chain',
            'taller', 'dublon'],
    },
    'titan': {
        'magic_rating': 3,
        'regular_spawn': 'chimera',
        'advanced_spawn': 'troll',
        'giantess': True,
        'avatar': 'titan',
        'description': u'титанида',
        't_count_min': 3,
        't_count_max': 6,
        't_price_min': 500,
        't_price_max': 5000,
        't_alignment': 'elf',
        't_list': [
            'casket', 'statue', 'mirror', 'comb', 'phallos', 'band', 'diadem', 'tiara', 'earring',
            'necklace', 'pendant', 'ring', 'broch', 'gemring', 'armbrace', 'legbrace', 'chain',
            'taller', 'dublon'],
    },
}

# Информация о всех типах отродий
spawn_info = {
    'goblin': {
        'power': 1,  # сила
        'modifier': [],  # возможные роли
        'name': u'Гоблин',  # название
    },
    'poisonous_asp': {
        'power': 1,  # сила
        'modifier': ['poisonous'],  # возможные роли
        'name': u'Ядовитый аспид',  # название
    },
    'winged_asp': {
        'power': 2,
        'modifier': ['poisonous'],
        'name': u'Крылатый аспид',
    },
    'krokk': {
        'power': 1,
        'modifier': ['servant'],
        'name': u'Крокк',
    },
    'basilisk': {
        'power': 3,
        'modifier': ['poisonous'],
        'name': u'Василиск',
    },
    'kobold': {
        'power': 2,
        'modifier': ['servant'],
        'name': u'Кобольд',
    },
    'lizardman': {
        'power': 3,
        'modifier': ['warrior'],
        'name': u'Ящерик',
    },
    'dragonborn': {
        'power': 3,
        'modifier': ['elite'],
        'name': u'Драконорождённый',
    },
    'gargoyle': {
        'power': 4,
        'modifier': ['warrior'],
        'name': u'Гаргуйль',
    },
    'sea_bastard': {
        'power': 3,
        'modifier': ['poisonous', 'marine'],
        'name': u'Рыбоглаз',
    },
    'octopus': {
        'power': 5,
        'modifier': ['poisonous', 'marine'],
        'name': u'Ядовитый спрут',
    },
    'hell_hound': {
        'power': 4,
        'modifier': ['poisonous'],
        'name': u'Адская гончая',
    },
    'minotaur': {
        'power': 5,
        'modifier': ['elite'],
        'name': u'Минотавр',
    },
    'murloc': {
        'power': 3,
        'modifier': ['warrior', 'marine'],
        'name': u'Мурлок',
    },
    'naga': {
        'power': 5,
        'modifier': ['elite', 'marine'],
        'name': u'Нага',
    },
    'ice_worm': {
        'power': 5,
        'modifier': ['poisonous'],
        'name': u'Ледяной червь',
    },
    'yettie': {
        'power': 5,
        'modifier': ['warrior'],
        'name': u'Йетти',
    },
    'troll': {
        'power': 6,
        'modifier': ['elite'],
        'name': u'Тролль',
    },
    'strigg': {
        'power': 6,
        'modifier': ['poisonous'],
        'name': u'Стригой',
    },
    'barlog': {
        'power': 7,
        'modifier': ['elite'],
        'name': u'Дэв',
    },
    'chimera': {
        'power': 10,
        'modifier': ['poisonous'],
        'name': u'Химера',
    },
}

girl_events = {
    'escape': 'lb_event_girl_escape',  # событие "побег из заключения"
    'spawn': 'lb_event_girl_spawn',  # событие "рождение отродий"
    'free_spawn': 'lb_event_girl_free_spawn',  # событие "рождение отродий на воле"
    'hunger_death': 'lb_event_girl_hunger_death',  # событие "смерть девушки от голода"
    'kill': 'lb_event_girl_kill',  # событие "беременную девушку убивают на свободе"
}

girls_texts = {
    # Подстановки:
    # %(dragon_name)s = Краткое имя текущего дракона
    # %(dragon_name_full)s = Имя дракона с эпитетом
    # %(dragon_type)s = Тип анатомии дракона (змей, линдвурм и т.п.)
    # %(girl_name)s = имя текущей женщины (однако, игра слов :) )
    # %(girl_title)s = тип женщины (крестьянка, горожанка, леди, русалка, эльфийска дева и т.п.)
    # %(spawn_name)s - тип отродий для описаний рождения (начинается с заглавной буквы)
    # %(rob_list)s - список украденного
    'girl': {  # используется, если нет подходящего текста или отсутствует нужный тип девушки
        'shout': (  # Реакция девушки, прямой речью
            u"Ой, а мне текст не написали (((",
        ),
        'prelude': (  # Описание прелюдий
            u"Одним неуловимым движением %(dragon_name)s подобрался вплотную к женщине и сбил её с "
            u"ног, а затем начал рвать зубами её одежду словно остервенелый пёс. %(girl_name)s "
            u"отчаянно отбивалась и кричала, но толку от этого было не много, изодранная одежда "
            u"разлетелась клочками оставляя её полностью обнаженной и беззащитной перед охваченным "
            u"похотью ящером.",
        ),
        'sex': (  # Описание секса с девушкой
            u"Отчаянно пытаясь спасти свою невинность, %(girl_title)s закрылась руками но %(dragon_type)s "
            u"предпринял обходной манёвр. Широко разинув свою зубастую пасть он обхватил голову девушки "
            u"челюстями, так что всё её лицо оказалось внутри, лишаясь доступа к воздуху. Девушка широко "
            u"открыла рот пытаясь вдохнуть хоть немного кислорода, но вместо этого в её глотку проник "
            u"длинный раздвоенный язык ящера. Теперь все когда все силы девушки были направлены на то "
            u"чтобы оторвать смрадную пасть от своего лица она и думать забыла о невинности. Скребя "
            u"ногтями по твёрдой чешуе дракона и дрыгая ногами %(girl_name)s внезапно почувствовала как "
            u"снизу в неё проникает что-то большое и твёрдое. Покрытый слизью рептилоидный член с "
            u"лёгкостью прорвал тонкую плёнку защищавшую вход в тугое молодое влагалище, безжалостно "
            u"растягивая и продавливая всё на своём пути. Почти теряя сознание от боли и недостатка "
            u"воздуха, %(girl_name)s внезапно почувствовала что челюсти насильника размыкаются, вновь "
            u"позволяя ей вдохнуть. %(dragon_name)s хотел насладиться её воплями и плачем.",
        ),
        'impregnate': (  # Оплодотворение
            u"Сдавленная в безжалостных объятьях ящера, %(girl_title)s почувствовала как он "
            u"ускоряет темп своих движений. Боль стала практически невыносимой но крик девушки "
            u"потерялся, перекрытый рёвом наслаждения насильника. Конвульсивно содрагаясь всем "
            u"телом %(dragon_type)s вливал в истерзанное лоно девушки целые литры липкого и "
            u"густого семени, заставляя её маленький животик раздуться изнутри. Когда "
            u"%(dragon_name)s наконец отстранился от своей жертвы из неё вытек целый водопад "
            u"семени, но тем не менее количества оставшегося внутри было более чем достаточно "
            u"чтобы гарантировать надёжное оплодотворение. Дело было сделано надёжно.",
        ),
        'new': (  # Описание новой девушки
            u"%(girl_name)s - %(girl_title)s.",
        ),
        'free': (  # Описание процесса выпускания на свободу
            u"Пусть сама заботится о себе. Если её не убьют свои же, узнав что за отродье растёт в её чреве...",
        ),
        'free_prison': (  # Описание процесса выпускания на свободу из тюрьмы
            u"Незачем держать её взаперти, охранять ещё... пусть катится на все четыре стороны.",
        ),
        'steal': (  # Описание процесса воровства девушки
            u"%(dragon_name)s относит пленницу в своё логово...",
        ),
        'jail': (  # Описание процесса заточения в темницу
            u"...и сажает её под замок.",
        ),
        'jailed': (  # Описание процесса возврата в темницу
            u"%(dragon_name)s возвращает девушку в темницу.",
        ),
        'eat': (  # Описание процесса поедания девушки. Как же ему не стыдно, червяку подколодному.
            u"%(dragon_name)s кушает девушку.",
        ),
        'rob': (  # Описание процесса ограбления девушки.
            u"%(dragon_name)s грабит девушку и получает: \n %(rob_list)s.",
        ),
        'traps': (  # Описание процесса побега и гибели в ловушке.
            u"%(girl_name)s убегает из темницы и гибнет в ловушках.",
        ),
        'escape': (  # Описание успешного побега
            u"%(girl_name)s спасается бегством",
        ),
        'spawn_common': (  # Описание родов
            u"%(girl_name)s рожает кучу тварей, известных людям под именем %(spawn_name)s.",
        ),
        'spawn_elite': (  # Описание родов
            u"%(girl_name)s рожает злобную тварь, известную под именем %(spawn_name)s.",
        ),
        'anguish': (  # Описание смерти от тоски
            u"%(girl_name)s умирает в тоске.",
        ),
        'hunger_death': (  # Описание смерти от голода
            u"%(girl_name)s умирает от голода.",
        ),
        'kill': (  # Описание смерти от селян
            u"Люди узнают, что %(girl_name)s беременна от дракона и убивают её.",
        ),
        'free_spawn': (  # Описание родов на свободе
            u"%(girl_name)s рожает что-то на воле.",
        ),
        'prison': (  # Проведываем девушку в тюрьме
            u"%(girl_name)s в тюрьме.",
        ),
    },
    'peasant': {  # используется для крестьянок
        'new': (  # описание крестьянки
            u"Сельская красавица по имени %(girl_name)s.",
        )
    },
}