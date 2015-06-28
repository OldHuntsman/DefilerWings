# coding=utf-8

from renpy import store

class Talker(store.object):
    """
    Базовый класс для всего что умеет говорить
    """

    def __init__(self, game_ref=None, kind='adv'):
        """
        :type game_ref: Game
        :param game_ref: Game object
        """
        if game_ref is None:
            raise Exception('No game reference specified')
        self.avatar = None  # По умолчанию аватарки нет
        self._gameRef = game_ref  # Проставляем ссылку на игру
        # Создаем объект от которого будет вестись вещание
        if kind == 'adv':
            self._real_character = game_ref.adv_character()
        else:
            self._real_character = game_ref.nvl_character()
        self._third_character = game_ref.nvl_character()

    @property  # Задаем имя через свойство, чтобы при изменении его передавать в персонажа.
    def name(self):
        return self._real_character.name

    @name.setter
    def name(self, value):
        self._real_character.name = value

    def __call__(self, *args, **kwargs):
        """
        Этот метод используется при попытке сказать что-то персонажем.
        Переопределяем, чтобы сообщить игре, что сейчас говорит этот персонаж.
        """
        self._gameRef.currentCharacter = self  # Прописываем кто говорит в настоящий момент
        self._real_character(*args, **kwargs)  # На самом деле говорим

    def third(self, *args, **kwargs):
        """
        Говорим от третьего лица. Принимаются предложения на более удачное название.
        Например прямая речь:
        $ game.person ("Что-нибудь")
        game.person "Где-нибудь"
        Рассказ о том что делает этот персонаж:
        $ game.person.third("Делая что-нибудь")
        game.person.third "Делая где-нибудь"
        """
        self._gameRef.currentCharacter = self  # Делаем вид, что сказали сами
        self._third_character(*args, **kwargs)  # Говорим о лица нарратора. Грязный хак.


