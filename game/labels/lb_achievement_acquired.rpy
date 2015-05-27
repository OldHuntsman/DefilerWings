label lb_achievement_acquired:
    $ achieved = data.store_achievements(persistent.achievements)
    $ names_list = achieved.keys()
    while len(names_list) != 0:
        $ achievement_name = names_list.pop()
        $ achievement_description = achieved[achievement_name]
        "Вы получили достижение [achievement_name]"
        "[achievement_description]"
    return