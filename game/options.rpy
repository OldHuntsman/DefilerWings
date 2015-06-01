# coding=utf-8
# This file contains some of the options that can be changed to customize
# your Ren'Py game. It only contains the most common options... there
# is quite a bit more customization you can do.
#
# Lines beginning with two '#' marks are comments, and you shouldn't
# uncomment them. Lines beginning with a single '#' mark are
# commented-out code, and you may want to uncomment them when
# appropriate.

init -1 python hide:

    # Should we enable the use of developer tools? This should be
    # set to False before the game is released, so the user can't
    # cheat using developer tools.

    config.developer = False

    # These control the width and height of the screen.

    config.screen_width = 1280
    config.screen_height = 720
    config.game_menu_action = ShowMenu('load')

    # This controls the title of the window, when Ren'Py is
    # running in a window.

    config.window_title = u"Крылья Осквернителя"

    # These control the name and version of the game, that are reported
    # with tracebacks and other debugging logs.
    config.name = "Defiler Wings"

    def get_version():
        """
        Функция для поиска текущей версии.
        Читает версию из неотслеживаемого файла game/version. Его можно заполнять и ручками, но
        можно и используя автоматически выполняемые скрипты post-commit (чтобы версия писалась после
        каждого коммита) и post-checkout (чтобы был корректный номер после смены ревизии). Оба эти
        файла должны находиться в .git/hooks/. Пример содержания такого скрипта:
        #### FILE START ####
        #!/bin/sh
        git describe --tag --long --always > game/version
        # где:
        #   git describe - выводит верисию c опциями:
        #       --tag - Если есть, то текущий тег
        #       --long - Всегда длинном формате, указывая количество коммитов и номер коммита
        #       --always - если тег не найден, то просто номер текущего коммита
        #   >  - перенаправляем вывод этой команды в файл перезаписывая его.
        #   game/version - путь к файлу
        #### FILE END ####
        Если такого файла не найдено, то можно пропробовать определить версию "на горячую" выполнив
        то же самое в консоли. В релизнутой игре это точно не получится, но в dev-версии стоит
        попробовать.
        :return: Возвращает строку с версией игры, читая ее из game/version. Если этот файл найти не
        удалось возвращает "Unknown".
        """
        import os
        version_file = os.path.join(config.basedir, "game/version")  # Получаем путь до файла с версией
        if os.path.isfile(version_file):    # Проверяем есть ли такой файл
            f = open(version_file)          # и если есть
            return f.read()                 # возвращаем его содержание
        else:                               # Если это не получилось, то пробуем получить версию файла самостоятельно
            from subprocess import Popen, PIPE, STDOUT  # Импортирует все немобходимое
            cmd_ops = [
                "--git-dir=%s" % os.path.join(config.basedir, ".git"),  # Составляем список опций.
                "describe",
                "--tags",
                "--long",
                "--always"
            ]
            # Для винды делаем там чтобы не выскакивало окно консоли.
            startupinfo = None
            if os.name == 'nt':
                from subprocess import STARTUPINFO, STARTF_USESHOWWINDOW
                startupinfo = STARTUPINFO()
                startupinfo.dwFlags |= STARTF_USESHOWWINDOW
                cmd = os.path.join(os.environ["PROGRAMFILES"], "Git", "bin", "git")
            else:
                cmd = "git"
            # Выполняем эту команду
            try:  # Пробуем выполнить один из этих бинаринков
                p = Popen([cmd] + cmd_ops, stdout=PIPE, stderr=PIPE, startupinfo=startupinfo)
                if p.wait() == 0:           # Проверяем удачно ли она завершилась
                    return p.stdout.read()  # Возвращаем ее результат
            except:     # Поймали эксепшен, скорее всего из-за того OS не нашла такой файл, пробуем следущий
                pass
        return "Unknown"                # Возвращаем "Unknown", если ничего не получилось.

    # config.version = get_version()
    config.version = "0.2.2 b"

    #########################################
    # Themes

    # We then want to call a theme function. theme.roundrect is
    # a theme that features the use of rounded rectangles.
    #
    # The theme function takes a number of parameters that can
    # customize the color scheme.

    theme.threeD(
        # Theme: 3D
        # Color scheme: Mocha Latte

        # The color of an idle widget face.
        widget="#4D3B29",

        # The color of a focused widget face.
        widget_hover="#996E45",

        # The color of the text in a widget.
        widget_text="#B99D83",

        # The color of the text in a selected widget. (For
        # example, the current value of a preference.)
        widget_selected="#ffffff",

        # The color of a disabled widget face.
        disabled="#614D3A",

        # The color of disabled widget text.
        disabled_text="#80654D",

        # The color of informational labels.
        label="#F1EBE5",

        # The color of a frame containing widgets.
        frame="#926841",

        # The background of the main menu. This can be a color
        # beginning with '#', or an image filename. The latter
        # should take up the full height and width of the screen.
        mm_root="img/menu/mmenu.png",  # фон главного экрана

        # The background of the game menu. This can be a color
        # beginning with '#', or an image filename. The latter
        # should take up the full height and width of the screen.
        gm_root=None,  # фон менюшек (настройки, пауза и пр.)

        # If this is True, the in-game window is rounded. If False,
        # the in-game window is square.
        rounded_window=False,

        # And we're done with the theme. The theme will customize
        # various styles, so if we want to change them, we should
        # do so below.
    )

    #########################################
    # These settings let you customize the window containing the
    # dialogue and narration, by replacing it with an image.

    # The background of the window. In a Frame, the two numbers
    # are the size of the left/right and top/bottom borders,
    # respectively.

    # style.window.background = Frame("frame.png", 12, 12)

    # Margin is space surrounding the window, where the background
    # is not drawn.

    # style.window.left_margin = 200
    # style.window.right_margin = 200
    # style.window.top_margin = 6
    # style.window.bottom_margin = 6

    # Padding is space inside the window, where the background is
    # drawn.

    # style.window.left_padding = 6
    # style.window.right_padding = 6
    # style.window.top_padding = 6
    # style.window.bottom_padding = 6

    # This is the minimum height of the window, including the margins
    # and padding.

    style.window.yminimum = 720

    #########################################
    # This lets you change the placement of the main menu.

    # The way placement works is that we find an anchor point
    # inside a displayable, and a position (pos) point on the
    # screen. We then place the displayable so the two points are
    # at the same place.

    # An anchor/pos can be given as an integer or a floating point
    # number. If an integer, the number is interpreted as a number
    # of pixels from the upper-left corner. If a floating point,
    # the number is interpreted as a fraction of the size of the
    # displayable or screen.

    # style.mm_menu_frame.xpos = 0.5
    # style.mm_menu_frame.xanchor = 0.5
    # style.mm_menu_frame.ypos = 0.75
    # style.mm_menu_frame.yanchor = 0.5

    #########################################
    # These let you customize the default font used for text in Ren'Py.

    # The file containing the default font.

    # style.default.font = "DejaVuSans.ttf"

    # The default size of text.

    # style.default.size = 22

    # Note that these only change the size of some of the text. Other
    # buttons have their own styles.

    #########################################
    # These settings let you change some of the sounds that are used by
    # Ren'Py.

    # Set this to False if the game does not have any sound effects.

    config.has_sound = True

    # Set this to False if the game does not have any music.

    config.has_music = True

    # Set this to True if the game has voicing.

    config.has_voice = False

    # Sounds that are used when button and imagemaps are clicked.

    # style.button.activate_sound = "click.wav"
    # style.imagemap.activate_sound = "click.wav"

    # Sounds that are used when entering and exiting the game menu.

    # config.enter_sound = "click.wav"
    # config.exit_sound = "click.wav"

    # A sample sound that can be played to check the sound volume.

    # config.sample_sound = "click.wav"

    # Music that is played while the user is at the main menu.

    # config.main_menu_music = "main_menu_theme.ogg"

    #########################################
    # Help.

    # This lets you configure the help option on the Ren'Py menus.
    # It may be:
    # - A label in the script, in which case that label is called to
    #   show help to the user.
    # - A file name relative to the base directory, which is opened in a
    #   web browser.
    # - None, to disable help.
    config.help = "readme.txt"

    #########################################
    # Transitions.
    
    config.fade_music = 2.0

    # Used when entering the game menu from the game.
    config.enter_transition = None

    # Used when exiting the game menu to the game.
    config.exit_transition = None

    # Used between screens of the game menu.
    config.intra_transition = None

    # Used when entering the game menu from the main menu.
    config.main_game_transition = None

    # Used when returning to the main menu from the game.
    config.game_main_transition = None

    # Used when entering the main menu from the splashscreen.
    config.end_splash_transition = None

    # Used when entering the main menu after the game has ended.
    config.end_game_transition = None

    # Used when a game is loaded.
    config.after_load_transition = None

    # Used when the window is shown.
    config.window_show_transition = None

    # Used when the window is hidden.
    config.window_hide_transition = None

    # Used when showing NVL-mode text directly after ADV-mode text.
    config.adv_nvl_transition = None

    # Used when showing ADV-mode text directly after NVL-mode text.
    config.nvl_adv_transition = None

    # Used when yesno is shown.
    config.enter_yesno_transition = None

    # Used when the yesno is hidden.
    config.exit_yesno_transition = None

    # Used when entering a replay
    config.enter_replay_transition = None

    # Used when exiting a replay
    config.exit_replay_transition = None

    # Used when the image is changed by a say statement with image attributes.
    config.say_attribute_transition = None
    #########################################
    # This is the name of the directory where the game's data is
    # stored. (It needs to be set early, before any other init code
    # is run, so the persistent information can be found by the init code.)
python early:
    config.save_directory = "Defiler Wings"

init -1 python hide:
    #########################################
    # Default values of Preferences.

    # Note: These options are only evaluated the first time a
    # game is run. To have them run a second time, delete
    # game/saves/persistent

    # Should we start in fullscreen mode?

    config.default_fullscreen = False

    # The default text speed in characters per second. 0 is infinite.

    config.default_text_cps = 0

    # The default auto-forward time setting.

    config.default_afm_time = 10

    #########################################
    # More customizations can go here.

    config.thumbnail_height = 144
    config.thumbnail_width = 256

    # Определяем изображения автоматически
    config.automatic_images = ['_', '/']
    config.automatic_images_strip = ['img', 'avadragon', 'avahuman', 'bg', 'map']

# This section contains information about how to build your project into
# distribution files.
init python:

    # The name that's used for directories and archive files. For example, if
    # this is 'mygame-1.0', the windows distribution will be in the
    # directory 'mygame-1.0-win', in the 'mygame-1.0-win.zip' file.
    build.directory_name = "DefilerWings-1.0"

    # The name that's uses for executables - the program that users will run
    # to start the game. For example, if this is 'mygame', then on Windows,
    # users can click 'mygame.exe' to start the game.
    build.executable_name = "DefilerWings"

    # If True, Ren'Py will include update information into packages. This
    # allows the updater to run.
    build.include_update = False

    # File patterns:
    #
    # The following functions take file patterns. File patterns are case-
    # insensitive, and matched against the path relative to the base
    # directory, with and without a leading /. If multiple patterns match,
    # the first is used.
    #
    #
    # In a pattern:
    #
    # /
    #     Is the directory separator.
    # *
    #     Matches all characters, except the directory separator.
    # **
    #     Matches all characters, including the directory separator.
    #
    # For example:
    #
    # *.txt
    #     Matches txt files in the base directory.
    # game/**.ogg
    #     Matches ogg files in the game directory or any of its subdirectories.
    # **.psd
    #    Matches psd files anywhere in the project.

    # Classify files as None to exclude them from the built distributions.

    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)

    # To archive files, classify them as 'archive'.

    # build.classify('game/**.png', 'archive')
    # build.classify('game/**.jpg', 'archive')

    # Files matching documentation patterns are duplicated in a mac app
    # build, so they appear in both the app and the zip file.

    build.documentation('*.html')
    build.documentation('*.txt')

    # Улучшаем вывод ошибок Pickle
    if config.developer:
        config.use_cpickle = False

    config.save_dump = True
    
    # Getting rid of rollback:
    config.hard_rollback_limit = 0
    config.rollback_enabled = False

    # Дополнительная переменная для вывода всякой дополнительной инфы.
    config.debug = False
