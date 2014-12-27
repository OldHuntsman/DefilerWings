# coding=utf-8
label lb_location_sky_main:
    $ place = 'sky'
    show expression get_place_bg(place) as bg    
    nvl clear
    
    if game.dragon.energy() == 0:
        'Даже драконам надо иногда спать. Особенно драконам!'
        return
        
    if not game.dragon.can_fly: 
        '[game.dragon.name] с тоской смотрит в небо. Если бы только он умел летать...'
    else:
        call lb_encounter_sky
    return
    
label lb_encounter_sky:
    $ choices = [
        ("lb_titan_found", 10),
        ("lb_enc_swan", 10),
        ("lb_enc_griffin", 10),
        ("lb_enc_skyboat", 10),
        ("lb_abbey_found", 10),
        ("lb_castle_found", 10),
        ("lb_palace_found", 10),
        ("lb_enc_fair_sky", 10),
        ("lb_enc_caravan_sky", 10),
        ("lb_enc_militia_sky", 10),
        ("lb_enc_cannontower", 10),
        ("lb_jotun_found", 10),
        ("lb_ifrit_found", 10),
        ("lb_patrool_sky", 3 * game.mobilization.level)]
    $ enc = core.Game.weighted_random(choices)
    $ renpy.call(enc)

    return
    
label lb_enc_swan:
    'Величественно паря в облаках [self.game.dragon.fullname] видит стаю белых лебедей. Впереди летит огромный откормленный вожак - он отлично сгодиться в качестве закуски!'
    nvl clear
    menu:
        'Сожрать гуся' if game.dragon.hunger > 0:
            $ game.dragon.drain_energy()
            '[game.dragon.name] ловит и пожирает гуся.'
            $ if game.dragon.bloodiness > 0: game.dragon.bloodiness = 0
        'Разогнать стаю' if game.dragon.bloodiness >= 5 and game.dragon.hunger == 0:
            $ game.dragon.drain_energy()
            '[game.dragon.name] жестоко задирает вожака и ещё несколько птиц, а остальная стая в панике разлетается кто куда.'    
        'Пролететь мимо' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    return
    
label lb_enc_griffin:
    'В вышине парит матёрый дикий грифон. Он облетает свои владения в поисках добычи и нарушителей, причём второе по его мнению относится и к драконам. Может быть стоит показать пернатому где его место?'
    $ game.dragon.drain_energy()
    $ game.foe = core.Enemy('griffin', gameRef=game, base_character=NVLCharacter)
    $ narrator(show_chances(game.foe))
    nvl clear
    menu:
        'Сразиться с грифоном':
            call lb_fight
            if game.dragon.hunger > 0:
                'Голодный [self.game.dragon.name] съедает грифона прямо в воздухе и бросает отсанки вниз на поживу шакалам.'
                $ if game.dragon.bloodiness > 0: game.dragon.bloodiness = 0
                $ game.dragon.hunger -= 1
                $ game.dragon.add_effect('boar_meat')
            else:
                '[self.game.dragon.fullname] сейчас не голоден, поэтому он даёт смертельно раненому грифону упасть вниз и разбиться о скалы.'
        'Избежать столкновения' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    return
    
label lb_enc_skyboat:
    'Над облаками вздымается парус! Это один из воздушных кораблей цвергов, судя по всему торговый. А значит там может быть добыча..'
    $ game.dragon.drain_energy()
    $ game.foe = core.Enemy('airship', gameRef=game, base_character=NVLCharacter)
    $ narrator(show_chances(game.foe))
    menu:
        'Напасть':
            call lb_fight
            '[game.dragon.name] стремительно обыскивает падающий вниз корабль и выгребает всё ценное:'
            python:
                count = random.randint(5, 15)
                alignment = 'dwarf'
                loot
                min_cost = 1
                max_cost = 10000
                obtained = "Это предмет с разграбленного воздушного судна цвергов."
                trs = treasures.gen_treas(count, data.loot['klad'], alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
                game.lair.treasury.receive_treasures(trs)
            '[trs_descrptn]'
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
        'Пропустить' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()    
    return
    
label lb_enc_fair_sky:
    'Паря в вышине [self.game.dragon.fullname] замечает внизу какие-то цветные пятна. Спустившись ниже становится понятно что это ярмарка, которую устроили люди.'
    call lb_enc_fair
    return
    
label lb_enc_militia_sky:
    '[self.game.dragon.fullname] замечает какое-то шевеление на земле далеко внизу. Так и есть - это собрались на тренировку ополченцы наспех собранные из окрестных деревень.'
    call lb_enc_militia
    return
    
label lb_enc_caravan_sky:
    'Пролетая вдоль змеящейся по земле дороги, [self.game.dragon.fullname] замечает на ней несколько точек. Это крупный торговый караван.'
    return
    
label lb_patrool_sky:
    python:
        game.dragon.drain_energy()
        chance = random.randint(0, game.mobilization.level)
        if chance < 4:
            patrool = 'archer'
            dtxt = 'Стрелок шерифа.'
        elif chance < 7:
            patrool = 'catapult'
            dtxt = 'Сторожевая башня с катапульой.'
        elif chance < 11:
            patrool = 'griffin_rider'
            dtxt = 'Всадник на грифоне.'
        elif chance < 16:
            patrool = 'airship'
            dtxt = 'Разрывая облака перед драконом вылетает огромный воздушный корабль. Это патрульный крейсер цвергов!' % game.dragon.name
        else:
            patrool = 'angel'
            dtxt = '%s вынужден зажмуриться от яркого света бьющего в глаза. Громогласный оклик возвещает: "Умри мерзкое порождение греха!!!". Это ангел-хранитель посланный людям Небесами для защиты.' % game.dragon.name
    '[dtxt]'
    $ game.foe = core.Enemy(patrool, gameRef=game, base_character=NVLCharacter)
    $ narrator(show_chances(game.foe))
    call lb_fight

    return
    