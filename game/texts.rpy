# coding=utf-8
# здесь хранятся тексты для игры
python early:
    
    chance_win_texts = {
        0: "{color=#ff0000}призрачные{/color}",
        10: "{color=#ff00ff}невысокие{/color}",
        30: "{color=#0000ff}приемлемые {/color}",
        60: "{color=#EAC117}значительные{/color}",
        90: "{color=#00ff00}отличные{/color}"
    }
    
    chance_wound_texts = {
        0: "{color=#00ff00}минимальная{/color}",
        10: "{color=#EAC117}допустимая{/color}",
        30: "{color=#0000ff}средняя{/color}",
        60: "{color=#ff00ff}значительная{/color}",
        90: "{color=#ff0000}катастрофическая{/color}"
    }
    
    def show_chances(foe):
        """
        Вывод шансов победы и ранения дракона для игрока 
        """
        from pythoncode import data
        chance = battle.victory_chance(game.dragon, foe)
        chance_win = data.get_description_by_count(chance_win_texts, chance)

        chance = battle.victory_chance(foe, game.dragon)
        chance_wound = data.get_description_by_count(chance_wound_texts, chance)
        
        return " Шансы на победу: %s.\n Опасность ранения: %s." % (chance_win, chance_wound)

    # Описания дракона
    hunger_texts = {
        0: '{font=fonts/AnticvarShadow.ttf}{color=#ff0000}Обожрался{/color}{/font}',
        1: '{font=fonts/AnticvarShadow.ttf}{color=#ff00ff}Сытый{/color}{/font}',
        2: '{font=fonts/AnticvarShadow.ttf}{color=#0000ff}Заморил червячка{/color}{/font}',
        3: '{font=fonts/AnticvarShadow.ttf}{color=#00ff00}Голодный{/color}{/font}'
    }

    lust_texts = {
        0: '{font=fonts/AnticvarShadow.ttf}{color=#ff0000}Вялый{/color}{/font}',
        1: '{font=fonts/AnticvarShadow.ttf}{color=#ff00ff}Возбужден{/color}{/font}',
        2: '{font=fonts/AnticvarShadow.ttf}{color=#0000ff}Осеменитель{/color}{/font}',
        3: '{font=fonts/AnticvarShadow.ttf}{color=#00ff00}Сосуд похоти{/color}{/font}'
    }

    bloodlust_texts = [
        '{font=fonts/AnticvarShadow.ttf}{color=#00ff00}Умиротворен{/color}{/font}',
        '{font=fonts/AnticvarShadow.ttf}{color=#ccccff}Спокоен{/color}{/font}',
        '{font=fonts/AnticvarShadow.ttf}{color=#0000ff}Напряжен{/color}{/font}',
        '{font=fonts/AnticvarShadow.ttf}{color=#ff00ff}Раздражен{/color}{/font}',
        '{font=fonts/AnticvarShadow.ttf}{color=#ff00ff}Разъярен{/color}{/font}',
        '{font=fonts/AnticvarShadow.ttf}{color=#ff0000}Взбешен{/color}{/font}'
    ]

    health_texts = {
        0: '{font=fonts/AnticvarShadow.ttf}{color=#ff0000}Полудохлый{/color}{/font}',
        1: '{font=fonts/AnticvarShadow.ttf}{color=#ff00ff}Раненый{/color}{/font}',
        2: '{font=fonts/AnticvarShadow.ttf}{color=#00ff00}Цел и невредим{/color}{/font}'
    }

    womennum = ['основная', 'вторая', 'третья', 'четвёртая', 'пятая', 'шестая', 'седьмая']
    
    # Описания эффекта события на дурную славу
    reputation_rise = [
        'Этот дурной поступок люди наверняка заметят.',
        'Дурная слава о поступках дракона разносится по королевству.',
        'Сегодня дракон стяжал немалую дурную славу.',
        'Об этом деянии услышат  жители всего королевства. И ужаснутся.',
        'О деянии столь ужасном будут сложены легенды, которые не забудутся и через сотни лет'
    ]

    # Описание деревень
    village = {
        'overview': [
            u'Заброшенное поселение',
            u'Одинокий хутор. У людей сдесь нет другой защиты, кроме крупного цепного пса.',
            u'Маленький посёлок. Завидев приближение дракона люди хватают любые подручные предметы, которые можно использовтаь в качестве оружия и сбиваются в толпу.',
            u'Деревня. Дракона заметили издалека, это очевидно по отчаянному звону рынды. Жители спешно собирают отряд ополчения, готовясь к самому худщему.',
            u'Село. Колокол в церкви отчанно звонит, призывая людей укрыться. На центральной улице собирается небольшой отряд арбалетчиков, готовых защитить село от супостата.',
            u'Городок. Стоит дракону приблизиться как его ворота спешно закрываются а на стены поднимаются воины, вооруженные луками и копьями.',
        ],
        'deffence': [
            'dog',
            'dog',
            'mob',
            'militia',
            'xbow',
            'town',
        ]
    }

# Прыдстория игры
    intro_text = '{font=fonts/AnticvarShadow.ttf}{size=+10}    Давным-давно, в незапамятные времена, наш мир был юн и чист. Все пять народов, жили в мире и гармонии, процветали и развивались. Люди, народ равнин, засеяли бескрайние поля золотой пшеницей и разбили на холмах цветущие сады полные сладких плодов. Дети богини Дану, мудрые и прекрасные альвы сплетали магические узоры из песен и лунного света в глубине своих обширных лесов. Искусные цверги ковали металлы и гранили сияющие словно звезды самоцветы под сенью своих резных чертогов. Беспечные русалки играли с серебристыми рыбками и танцевали хороводы под синей гладью океана. И даже старые словно сам мир великаны не трогали малых народов, но наставляли их в древнем знании.     {vspace=30}Те дни минули без следа, когда в наш мир вошло зло. Никто доподлинно не знает, откуда явилась Она. Нагая, крылатая, прекрасная как полуденная греза и ужасная как полуночный кошмар. В преданиях сказано, что она вышла из белого как молоко утреннего тумана что сгустился в глубине непролазного бурелома. Но многие верят что ее породила сама преисподняя.    {vspace=30}Способная принять любой облик, соблазнительный или внушающий леденящий страх, она несла за собой гниль и раздор. В своей противоестественной, неуемной похоти она сходилась со всеми до кого могла добраться. Жаждала всякого мужского семени от гордых королей и от грязных крестьян, от людей и от зверей. В сих противоестественных союзах она породила сонмы тварей, искаженных и злобных, жестоких, жадных и полных греха.    {vspace=30}Страхом и ненавистью Владычица Тьмы выковала себе армию и двинула ее на вольные народы, чтобы навеки поработить весь свет и заставить каждого служить себе. Могучая и безжалостная армия Тьмы оставляла за собой лишь трупы, пепелища и бесплодную землю.     {vspace=30}Но пять свободных народов дали ей отпор. Собравшись вместе армии людей, альвов, цвергов, русалок и великанов одолели темную силу и загнали исчадий Владычицы в бесплодные вулканические земли далеко на востоке. Чтобы защититься, люди построили неприступные крепости и возвели города с высокими стенами и башнями, цверги создали боевые машины и автоматы, альвы оградили свои рощи чарами сокрытия и выставили на границах бдительных стражей. Даже беспечные русалки взяли в руки трезубцы и сети, готовые отразить нападение.     {vspace=30}Глядя на эту неодолимую силу Владычица поклялась создать чудовище, перед мощью которого не устоит никто на свете. В дышащих ядовитыми испарениям южных болотах она сошлась с самым откормленным змеем которого только смогла сыскать и отложила три больших яйца из которых вылупились чудовища, подобных которым еще не знала земля - драконы.    {vspace=30}   Все смертные грехи слились в этих тварях. Яростные и кровожадные, драконы не знают пощады и милосердия. Их гордыня и зависть заставляет драконов стяжать себе дурную славу, разрушая все прекрасное и неся страдание всему живому. В неуемной похоти своей они оскверняют невинных девушек и те рожают им чудовищ подобных выродкам самой Владычицы. Ненасытные, пожирают драконы равно добрых людей и лесных зверей, и морских рыб, и птиц небесных. Алчные до серебра и злата, сгребают в своих зловонных пещерах груды сокровищ и спят на них годами, предаваясь праздности и самодовольству.     {vspace=30}Первые из драконов были не так уж и могучи, не многим больше чем огромные болотные змеи. Но Владычица раз за разом отбирает лучших, чтобы в кровосмесительно-мерзостном соитии породить новое, беспрестанно мутирующее потомство. Все крупнее, сильнее, все злобнее и коварнее становятся драконы. Если не пресечь их род, то наступит день когда перед их мощью не устоят ни самые высокие стены, ни самые большие армии. Даже богоподобные титаны в своих облачных цитаделях не смогут спать спокойно. Но покамест надежда еще жива...{/size}{/font}'
    
    # Названия мест
    toptxt = {
        'plain': u'СЕЛЬСКАЯ МЕСТНОСТЬ \n\n'
    }

    # Тексты для энкаунтеров
    txt_enc_fair = [
        ['%(dragon_name)s замечает разноцветные шатры на лугу, это большая ярмарка на которую собрались крестьне со всех окрестных деревень. Тут они торгуют, общаются и выставляют на показ свой лучший скот и самых завидных невест. Есть чем поживиться!'],
        ['%(dragon_name)s врывается в толпу крестьян и издаёт громовой рык. Люди бегут в ужасе, но ящер не тратит времени на погоню, ему нужда всего лишь одна девушка - самая красивая девственница, которая надеялась приглядеть себе лучщего жениха. Пришла пора ей узнать, кто первый парень на деревне!']
    ]

# Тексты для особых мест
    txt_place_manor = [
        ['Неподалёку от дороги стоит укреплённая каменная усадьба - манор какого-то небогатого рыцаря. Внутри могут быть женщины и золото, так что стоит разведать внимательнее.'],
        ['%(dragon_name)s принюхивается. Внутри явно есть девственница благородных кровей и немного сокровищ. Но пробиться внутрь будет не просто, слуги уже заметили приближение ящера и теперь хозяин манора спешно облачается в доспехи. Старый рыцарь не сдастся без боя!'],
        ['Не обращая внимания на бегущую в ужасе челядь, %(dragon_name)s обшаривает поместье в поисках ценностей:'],
        ['В просторной и светлой комнате на втором этаже дрожит спрятавшись под кроватью дочь убитого рыцаря. Но %(dragon_name)s способен учуять запах невинной плоти за много миль, от него не скрыться в маленькой комнате.'],
        ['Укрепления не спасли эту ныне уже безлюдную усадьбу от разграбления, однако крепкие стены могут послужить хорошей защитой для драконьих сокровищ. Не слишком крупный ящер мог бы устроить в винном погребе уютное логово, надо только протиснуться в узкие двери.'],
        ['%(dragon_name)s издаёт победный рык. Больше никто не стоит у него на пути и рыцарская усадьба беззащитна.']
    ]

    txt_place_wooden_fort = [
        ['На холме у дороги стоит деревянный форт. %(dragon_name)s решает разведать что там внутри.'],
        ['Этот деревянный форт построен по обычной схеме - большой двор окруженный рвом и частоколом, над которым доминирует башня возведённая на вершине рукотворной насыпи. Гарнизон составляют обычные пехотинцы, а хозяина и вовсе нет на месте. Зато с верхнего этажа башни доносится аромат девственницы.'],
        ['Сопротивление защитников сломлено. Всего минута нужна чтобы снести ворота башни на холме и ворваться внутрь. Слуги разбегаются в ужасе, но %(dragon_name)s не обращает на них внимания, методично извлекая всё ценное чем тут можно поживиться:'],
        ['На верхнем этаже башни расположена светлица. Там в страхе жмутся к углам две женщины - юная дева и нянька-старуха. %(dragon_name_full)s зашибает старуху одним щелчком хвоста и поворачивает голову к девушке.'],
        ['Деревянные укрепления находятся в плачевном состоянии, но башня на холме всё ещё стоит. В главном зале можно устроить логово и свалить сокровища а наверху держать пленных девиц. Не самое замечательное место для логова, но всё же лучше чем овраг или дыра в земле.'],
        ['%(dragon_name)s издаёт победный рык. Больше никто не стоит у него на пути и форт на холме теперь беззащитен.']
    ]
    
    txt_place_abbey = [
        ['Вдалеке видны стены и башни, но это не крепость - это укреплённый монастырь. Монахи часто собирают сокровища, почти как драконы. Но гораздо хуже умеют их охранять так что стоит посмотреть.'],
        ['Довольно богатый и хорошо укреплённый женский монастырь. Изнутри доносится запах золота, серебра и невинных женщин, но не только... Обитель защищают рыцари-крестоносцы.'],
        ['Глупые монахини собрали всё ценное в одной единственной комнате - возле алтаря которому они молятся. %(dragon_name)s прихватывает церковную утварь:'],
        ['В задней части обители находятся кельи монашек. Большинство из них невинны, хотя многие так стары что давно протухли, но есть тут и особый сладкий запах. Ориентируясь по нему %(dragon_name)s обнаруживает в самой дальней келье деву благородных кровей, которая только готовилась принять постриг в монахини. Но теперь её ждёт совсем иная судьба!'],
        ['У этого старого монастыря крепкие и высокие стены, а большой обеденный зал достаточно просторен чтобы обеспечить логово даже для крупного дракона. Здесь можно неплохо обустроиться.'],
        ['%(dragon_name_full)s издаёт победный рык. Больше никто не стоит у него на пути и монастырь теперь беззащитен.']
    ]

    txt_place_castle = [
        ['%(dragon_name)s находит большую каменную крепость, которую видно издалека.'],
        ['Таких сильно укреплённых замков с высокими стенами и башнями в королевстве не много. Драконье чутьё подсказывает, что в сокровищнице полно золота и драгоценных камней, а в высокой башне томится от безделия благородная девица. Надо бы её развлечь, однако этому будет упорно мешать гарнизон крепости.'],
        ['Центральная цитадель замка держалась упорнее всего и разломать её ворота оказалось непростым делом. Внутри находится всё самое ценное и первым делом надо обезопасить от разбегающихмя в ужасе слуг сокровища:'],
        ['На верхнем этаже башни расположена светлица. Там в страхе жмутся к углам две женщины - юная дева и нянька-старуха. %(dragon_name_full)s зашибает старуху одним щелчком хвоста и поворачивает голову к девушке.'],
        ['Этот заброшенный каменный замок великолепно укреплён и имеет множество просторных помещений - почти идеальное место для драконьего логова.'],
        ['%(dragon_name_full)s издаёт победный рык. Больше никто не стоит у него на пути и могучая крепость беззащитна.']
    ]
    
    txt_place_palace = [
        ['Вдалеке виднеется величественная крепость, это явно что-то стоящее внимания!'],
        ['Похоже что %(dragon_name)s нашёл королевский замок. Такие могучие укрепления в землях вольных народов встречаются очень редко, позволить себе такой дворец может только очень богатый лорд. И разумеется внутри много всего интересного... и куча охраны.'],
        ['%(dragon_type)s стремительно врывается в сокровищницу, жадно сгребая к себе драгоценности:'],
        ['В каждом уважающем себя дворце должна томиться принцесса и конечно она тут есть, как обычно в светлице на последнем этаже самой высокой башни.'],
        ['Этот обезлюдивший дворец просто огромен и великолепно размещён. Если устроить тут логово, люди будут трепетать при одном упоминаннии имени дракона который был настолько могущественен чтобы завоевать его для себя!'],
        ['%(dragon_name_full)s издаёт победный рык. Больше никто не стоит у него на пути и королевский дворец теперь беззащитен!']
    ]
    
    txt_place_enfr = [
        ['Эльфийский замок. Бинго!'],
        ['Священное древо альвов, выращенное из сменеи подареного самой богиней Дану огромно и необъятно. На его ветвях, под корнями и в дуплах альвы обустроили причудливый дворец из которого праят лесным краем король и королева. Внутри множество реких сокровищ, но к сожалепнию сердце леса бережёт огромный древесный страж, сразить которого будет непросто.'],
        ['Альвы не делают специальных сокровищниц для своих драгоценностей, а носят их с собой, однако тут достаточно богатых детей Дану с которых можно кое что позаимствовать:'],
        ['%(dragon_name)s находит королеву альвов.'],
        ['Теперь роща пуста, но древняя магия всё ещё теплится в стволе Великого Древа, оберегая окружающие места. Тут можно сделать тайное логово.'],
        ['%(dragon_name_full)s издаёт победный рык. Больше никто не стоит у него на пути и лесной дворец альвов беззащитен.']
    ]
    
    txt_enc_forest_guardian = [
        ['%(dragon_name_full)s некоторое время бродит по лесу. Внезапно...'],
        ['Появляется страж границ. Альвы тщательно охраняют свою священную рощу, выставляя дозорных с луками. Это один из них, возможно он знает путь в зачарованный край.'],
        ['%(dragon_name)s торжествует победу. Но найти тайную тропу что охранял страж никак не получается...'],
        ['%(dragon_name)s коварством выуживает у побеждённого стража информацию о тайных тропах, позволяющих пройти в заколдованный лес где живут альвы.']
    ]
    
    txt_place_jotun = [
        ['В этом исполинском дворце, сложенном из глыб векового льда живёт инеистый великан - йотун. Изнутри раздаётся запах сокровищ и большой женщины, а кроме того здесь можно было бы обустроить отличное логово. Но великан бдительно охраняет свой дом.'],
        ['В глубине логова прячестся инеистая великанша. В её холодной утробе драконье семя смогло бы дать исключительный всход.'],
        ['Ледяная цитадель теперь пустует. Тут можно устроить отличное логово, ведь защиту дадут не только выскоие ледяные стены но и отвесные горы и пронзительный морозный ветер.']
    ]
    
    txt_place_ifrit = [
        ['Укреплённая кузня, сложенная из черных обсидиановых глыб расположена в самом жерле действующего вулкана. Судя по запаху там есть чем поживиться, но огненный великан - ифрит, не отдасть свои сокровища без боя.'],
        ['Огненная великанша пытается дать отпор незванному гостю, но она намного слабее чем ифрит и не вооружена, поэтому дракон может делать с ней всё что пожелает.'],
        ['Вулканическая кузня огненного великана теперь пустует. Тут можно устроить отличное логово, ведь его будут охранять не только толстые стены но и отвесные скалы, и нестерпимый жар магматического озера.']
    ]

    txt_place_triton = [
        ['Это подводный дворец тритона - морского великана. Наверняка он скопил изрядные сокровища, но хотя тритоны и не так сильны как большинство великанов, это всё же серьёзный противник.'],
        ['В роскошно обставленных подводных покоях дожидается своей участи великанша с рыбьим хвостом - серена. Это шанс породить могучих морских тварей!'],
        ['Подводные хоромы где когда-то жил горды тритон, теперь могут стать отличным логовом для водоплавающего дракона. Добраться сюда сможет мало кто, ведь вход находится под водой!']
    ]
    
    txt_place_titan = [
        ['Этот летучий остров держтся над облаками благодаря волшебной силе грозового исполина - титана. Сам замок поражает монументальными размерами и роскошью. Наверняка внутри таятся несметные богатства, но титаны одни из самых могучих противников каких только можно предствить.'],
        ['Дракон идёт на запах женщины. По обычаю всех принцесс, титанида сидит в комнате на вершине башни. Похоже она даже не слышала звуков битвы вниз - вот это сюрприз!'],
        ['Этот пустой ныне замок раньше принадлежал могучему титану. Старая магия всё ещё держит остров в небе, над уровнем облаков. Учитывая как не просто сюда забраться и как просторны и прочны здешие строения лучшее логово придумать сложно.']
    ]
    
    #Сцены секса с госпожой в человеческом облике
    txt_human_mistress_fuck = {}
    txt_human_mistress_fuck['останки дракона'] = ['Это ошибка, текущий дракон мёртв.',]
    txt_human_mistress_fuck['ползучий гад'] = ['Плейсхолдер №11',]
    txt_human_mistress_fuck['линдвурм'] = ['Плейсхолдер №12',]
    txt_human_mistress_fuck['гидрус'] = ['Плейсхолдер №13',]
    txt_human_mistress_fuck['летучий гад'] = ['Плейсхолдер №14',]
    txt_human_mistress_fuck['виверн'] = ['Плейсхолдер №15',]
    txt_human_mistress_fuck['дракон'] = ['Плейсхолдер №16',]
    txt_human_mistress_fuck['многоглавый летучий гад'] = ['Плейсхолдер №17',]
    txt_human_mistress_fuck['многоглавый виверн'] = ['Плейсхолдер №18',]
    txt_human_mistress_fuck['многоглавый дракон'] = ['Плейсхолдер №19',]
    
    #Сцены секса с госпожой в драконьем облике
    txt_dragon_mistress_fuck = {}
    txt_dragon_mistress_fuck['останки дракона'] = ['Это ошибка, текущий дракон мертв.',]
    txt_dragon_mistress_fuck['ползучий гад'] = ['Плейсхолдер №21',]
    txt_dragon_mistress_fuck['линдвурм'] = ['Плейсхолдер №22',]
    txt_dragon_mistress_fuck['гидрус'] = ['Плейсхолдер №23',]
    txt_dragon_mistress_fuck['летучий гад'] = ['Плейсхолдер №24',]
    txt_dragon_mistress_fuck['виверн'] = ['Плейсхолдер №25',]
    txt_dragon_mistress_fuck['дракон'] = ['Плейсхолдер №26',]
    txt_dragon_mistress_fuck['многоглавый летучий гад'] = ['Плейсхолдер №27',]
    txt_dragon_mistress_fuck['многоглавый виверн'] = ['Плейсхолдер №28',]
    txt_dragon_mistress_fuck['многоглавый дракон'] = ['Плейсхолдер №29',]

    #Вор успешно обходит защиту логова
    txt_thief_success = {}
    txt_thief_success['mechanic_traps'] = ['Ворюга успешно преодолевает механические ловушки.',]
    txt_thief_success['magic_traps'] = ['Вовремя заметив свечение магической ловушки, вор избегает её и проходит дальше.',]
    txt_thief_success['poison_guards'] = ['Ядовитые твари не сумели остановить расхитителя сокровищ.',]
    txt_thief_success['regular_guards'] = ['Злоумышленник снимает ключевых охранников, перерезав им глотки кинжалом.',]
    txt_thief_success['smuggler_guards'] = ['Злоумышленник снимает наёмных охранников, перерезав им глотки кинжалом.',]
    txt_thief_success['elite_guards'] = ['Двигаясь словно ночная тень, вор проскальзывает незамеченным мимо огромного монстра охраняющего двери сокровищницы.',]

    #Вор убивается об защиту логова
    txt_thief_fail = {}
    txt_thief_fail['mechanic_traps'] = ['Незадачливый расхититель сокровищ наступает на нажимную плиту активирует смертоносную механическую ловушку.',]
    txt_thief_fail['magic_traps'] = ['Магическая ловушка распыляет неудачливого вора на атомы.',]
    txt_thief_fail['poison_guards'] = ['Ядовитая тварь неожиданно напала на вора из темноты и ужалила его. Смерть от токсина медленная и мучительная...',]
    txt_thief_fail['regular_guards'] = ['Охранники замечают вторжение и атакуют вора. Короткая но ожесточённая схватка оканичвается его смертью.',]
    txt_thief_fail['smuggler_guards'] = ['Наёмные охранники замечают вторжение и атакуют вора. Короткая но ожесточённая схватка оканичвается его смертью.',]
    txt_thief_fail['elite_guards'] = ['Вор пытается незаметно проскользнуть мимо монстра охраняющего двери в главный зал, но терпит неудачу. Кровожадная тварь разрывает его на куски и пожирает.',]
    
    #Сообщеения для битвы армий
    reinforcement_ask = 'Госпожа, мои войска несут слишком большие потери, а я сам не могу сейчас рисковать на передовой. Умоляю, помогите нам сокрушить врагов!'
    reinforcement_agree = 'Быть посему. Смотри и ужасайся ибо я смету врагов с лица земли как ураган сметает сухие осенние листья!'
    reinforcement_refuse = 'Разве зря мы готовили могучую армию? Разве зря я пестовала драконий столько веков? Хватит ныть - иди и принеси мне победу либо умри пытаясь!!!'
    
    
    #СОВЕТЫ ВЛАДЫЧИЦЫ
    txt_advice = ['Самые безопасные места для начала это сельская местность и леса. Но учти, что с ростом мобилизации там появятся патрули и они будут тем сильнее, чем больше военных сил собрали люди. Мобилизация требует времени.',
    'Если ищешь великанов, то самых слабых из них, огров-людоедов можно найти в лесных пещерах. Тритоны обитают в воде, Ифриты и Йотуны - высоко в горах, и они очень сильны. Но могущественее всех Титаны - они живут за облаками, на летающих островах-крепостях.',
    'Если бродить по дорогам людей, то можно найти их укрепления - рыцарские усадьбы, деревянные и каменные замки, монастыри... Это крепкие орешки, но внутри много сокровищ и благородные девы. А ещё из разграбленного замка можно сделать замечательное логово.',
    'Где-то в лесу живут альвы, народ Дану. Их девы очень хороши, но альвы защищают свои владения магией. Попробуй поймать и допросить кого-то из стражей границ остроухих. Они иногда выходят за магическую завесу.',
    'Обязательно посети остров контрабандистов. Там королевский закон почти не действует. Там ты сможешь продать краденные сокровища чтобы получить звонкие монеты, только учти что цены у них грабительские. Еще в притоне контрабандистов можно найти наёмников для охраны логова или борьбы с мобилизацией.',
    'Чтобы взететь в небо нужны крылья. Или заклинание полёта. С высоты можно разглядеть укрепления людей - замки в которых они держат сокровища и благородных дев. Впрочем эти места можно и на дорогах найти, зато взлетев над облаками у тебя будет шанс обнаружить летающий остров Титанов.',
    'В море живут русалки, но их дети будут годны лишь для охраны подводных логов и ничего более. Зато там можно грабить торговые корабли. Но чтобы добраться до кораблей и русалок надо уметь дышать под водой. Жабры помогут. Так же как и специальное заклинание.',
    'В своём логове ты можешь использовать разные заклинания. Конечно если тебе хватит на это коварства. Но не спеши использовать всё коварство как только проснёшься. Магия может пригодиться для того чтобы сменить облик или наложить проклятье на людские припасы.',
    'Крестьянку поймать очень просто, но они способны порождать лишь ядовитых тварей, бесполезных для армии тьмы. Вот горожанки уже интерснее, но их труднее найти. Вот тебе хороший совет - воспользуйся коварством, обратись в человека и похить горожанку на городском рынке.',
    'Обязательно навести деревню гремлинов. Эти ребята плохие вояки, но хорошие мастера по камню, дереву и металлу - не хуже цвергов. А ещё они жадные до золота. Ты можешь нанять их в качестве слуг или заплатить им за улучшения для логова. Они даже могут изготавливать ювелирные изделия, если есть материалы.',
    'Я не хочу чтобы ты водился с ведьмой что живёт на кладбище. Она слишком много о себе мнит - хочет стать такой же могущественной как я. За твоё семя она предложит тебе колдовские услуги, но лучше потрать свою мужскую силу на размножение чем на эту шлюху-колдунью. Она выдоит тебя до суха и ты не сможешь никого обрюхатить.',
    'В городе есть что пограбить, но ворота хорошо охраняются. Через них можно перелететь на крыльях или пройти внутри обернувшись человеком - если хватит коварства. В форме человека можно даже договориться с ювелирами - они дают лучшую цену за сокровища чем контрабандисты и могут кое что продать за деньги.',
    'Если ты обрюхатишь девицу и отпустишь её на волю, то ваше отродье будет терроризировать людей увеличивая разруху. Но лучше держать беременную деву под замком в логове, тогда ты сможешь взять отродье на службу или отправить в армию тьмы. Только не забудь что кто-то должен ухаживать за будущей мамашей пока ты спишь.',
    'Когда выполнишь задание, ты можешь прийти ко мне за наградой сразу. Но можешь и подождать конца срока, ничего страшного. Так ты накопишь деньги для снабжения моей армии и наплодишь больше монстров. Очень важно чтобы в нашей армии было много разных существ.',
    'Мой совет: \n Воруй \n @ \n Убивай',
    'Некоторые встречи бывают реже других. Например на дороге ты чаще встретишь крестьянина с сеном, чем богатый караван. Если встреча не интересна, не трать времени и сил зря, сдержи свою ярость до лучшего момента.',
    'С ростом мобилизации по всему королевству начнут бродить патрули - тем более сильные чем выше мобилизация. Но даже слабый патруль доставит тебе неприятности - ведь ты потратишь на них своё время и силы, а толку никакого. Большая разруха тоже не к добру - руины да пепелища ведь не ограбишь, верно?',
    'Рыцари и воры могут иметь очень разную силу. Чем выше твоя дураная слава, тем более опасных противников привлечёт твоё логово. Будь осторожен, следи за ними и вовремя предпринимай контр-меры.',
    'Если ты не совершаешь зла, хотя и мог бы - например отпускаешь бесполезную девку чтобы не тратить попусту времени и силы, ты будешь раздражаться. В итоге ярость помешает тебе контролировать себя и ты не сможешь сдержаться, будешь атаковать каждого встречного. Сожри кого-нибудь живьём и ярость уйдёт на время.',
    'В горах можно отыскать входы в подземное царство цвергов, таящее несметные сокровища. Кроме того там есть множество шахт где добывают драгоценные металлы и самоцветы из которых гремлины могут сделать тебе дорогие ювелирные изделия.']
    
    """
    Шаблон
    txt_ = [[
        '',
        ],
    
        ['',
        ],
    
        ['',
        ],
    
        ['',
        ],
        ]
    """