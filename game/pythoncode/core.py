#!/usr/bin/python
# coding=utf-8


class Modifier(dict):
    """
    Класс для разнообразных модификаторов.
    К примеру: даров владычицы, снаряжения рыцарей, заклинаний и.т.д.
    """

    def __getattr__(self, name):
        """
        Переопределение логики доступа к аттрибуту.
        Теперь mod.name и mod["name"] возвращают одно значение
        """
        return self[name]

    def __init__(self, name, type):
        dict.__init__(self)
        self.name = name
        self.type = type
        # Список модификаторов от которых данный зависит
        # например модификатор "когти" зависят от модификатора "лапы"
        self.depends = []
        # Модификаторы с которыми данный конфиликтует
        # не уверен что нужно, можно убрать потом
        self.conflicts = []

        # self.attack = 0
        # self.sure_attack = 0
        # self.protection = 0
        # self.energy = 0
        # self.max_energy = 0
        # self.magic = 0
        # self.fear = 0
        # self.bloodiness = 0
        # self.lust = 0
        # self.hunger = 0
        # context -- Это функция влияющая на модификаторы противника
        # self.context = lambda x: x


class Character:
    """
    Базовый класс для любых персонажей в игре.
    """

    def __init__(self):
        self.name = ""  # У всех быть имя
        self.modifiers = []
        self.avatar = ""  # путь к аватарке

    def tags(self):
        """
        Для проверки наличия определенного свойства, подбора картики и.т.д
        Пример: "flying" in dragon.tags() проверка, что дракон летающий
        Касательно картинки: предпологается, что каждой картинке сопоставлен список тегов
        и мы отображаем ту для которой больше всего совпадений с данным списком.
        :return: Список тегов.
        """
        return [mod.name for mod in self.modifiers]

    def pick_avatar(self):
        """
        Логика подборки аватарки. Должна быть переопределена в наследниках.
        """
        pass


class Fighter(Character):
    """
    Базовый класс для всего, что способно драться.
    Декоратор нужен чтобы реализовывать эффекты вроде иммунитета или ядовитого дыхания.
    То есть такие которые воздействуют на модификаторы противника.
    """

    def __init__(self):
        Character.__init__(self)
        # Базовые значения атаки и защиты бойца
        self.base_attack = 1
        self.base_sure_attack = 0  # (_attack + _sure_attack) in range 1..20
        self.base_protection = 1  # range 1..20

    def attack(self, context=lambda x: x):
        """
        :param context: Функция декоратор для модификаторов.
        :return: Значение атаки данного бойца.
        """
        return self.base_attack + sum([mod.attack for mod in
                                       map(context, self.modifiers)
                                       if "attack" in self.modifiers])

    def sure_attack(self, context=lambda x: x):
        """
        :param context: Функция декоратор для модификаторов.
        :return: Значение уверенной атаки данного бойца.
        """
        return self.base_sure_attack + sum([mod.sure_attack for mod in
                                            map(context, self.modifiers)
                                            if "sure_attack" in self.modifiers])

    def protection(self, context=lambda x: x):
        """
        :param context: Функция декоратор для модификаторов.
        :return: Значение защиты данного бойца.
        """
        return self.base_protection + sum([mod.protection for mod in
                                           map(context, self.modifiers)
                                           if "protection" in self.modifiers])


class Dragon(Fighter):
    """
    Класс дракона.
    Совсем совсем черновой вариант.
    """

    def __init__(self):
        Fighter.__init__(self)
        # Здесь должна быть генерация имени.
        self.name = u"Змей Горыныч"
        # Если мы хотим переопределить базовые параметры бойца
        self.base_attack = 2
        self.base_sure_attack = 0
        self.base_protection = 1

        # Ниже идут специфичные для дракона свойства
        self.energy = 5
        self.max_energy = 10
        self.magic = 0  # range 0..6
        self.fear = 1  # range 1..20
        self.bloodiness = 0  # range 0..5
        self.lust = 0  # range 0..2
        self.hunger = 0  # range 0..2

    def kind(self):
        """
        :return: Текстовое представление 'вида' дракона
        """
        return u"Ползучий гад"

    def children(self):
        """
        Сгенерировать список потомков.
        Вызывается при отставке дракона.
        :return: list of Dragons
        """
        pass


class Knight(Fighter):
    """
    Класс рыцаря.
    Набросок для тестирования боя.
    Спутников, особенности и снаряжение предпологается засовывать в переменную _modifiers
    """

    def __init__(self):
        """
        Здесь должна быть генерация нового рыцаря.
        """
        Fighter.__init__(self)
        self.name = u"Сер Ланселот Озёрный"
        # Спецефичные для рыцаря свойства
        self.power = 1

    def title(self):
        """
        :return: Текстовое представление 'звания' рыцаря.
        """
        if self.power == 1:
            return u"Бедный рыцарь"
        elif self.power == 2:
            return u"Странствующий рыцарь"
        elif self.power == 3:
            return u"Межевой рыцарь"
        elif self.power == 4:
            return u"Благородный рыцарь"
        elif self.power == 5:
            return u"Паладин рыцарь"
        elif self.power == 6:
            return u"Прекрасный принц"
        else:
            assert False, u"Недопустимое значение поля power"

    def upgrade(self):
        """
        Метод вызвается если рыцать не пошел драться с драконом.
        Тут должна быть логика его усиления, которая пока еще не придумана.
        """
        pass


class Thief(Character):
    """
    Класс вора.
    """
    pass


class Game:
    def __init__(self):
        self.dragon = Dragon()
        self.knight = Knight()
        self.thief = None

    def battle(self, fighter1, fighter2):
        """
        Логика сражения.
        :return: Текст описывающий сражение.
        """
        return u"{0}(атака {2}, уверенная атака {3}, защита {4}) \n" \
               u"сражается с \n{1}(атака {5}, уверенная атака {6}, защита {7})".format(
            fighter1.name, fighter2.name,
            fighter1.attack(), fighter1.sure_attack(),
            fighter1.protection(),
            fighter2.attack(), fighter2.sure_attack(),
            fighter2.protection())

    def next_year(self):
        """
        Логика смены года.
        Проверки на появление/левелап/рейд рыцаря/вора.
        Изменение дурной славы.
        Что-то ещё?
        """
        pass

    def sleep(self):
        """
        Рассчитывается количество лет которое дракон проспит.
        Попытки бегства женщин.
        Сброс характеристик дракона.
        """
        pass