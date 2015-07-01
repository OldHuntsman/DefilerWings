# coding=utf-8

from copy import deepcopy

from pythoncode import mob_data

from fighter import Fighter

class Enemy(Fighter):
    """
    Класс одноразового противника для энкаунтера.
    """

    def __init__(self, kind='generic', *args, **kwargs):
        """
        Создание врага.
        """
        super(Enemy, self).__init__(*args, **kwargs)
        self.kind = kind
        self.name = mob_data.mob[kind]['name']
        self.power = mob_data.mob[kind]['power']
        self.defence = mob_data.mob[kind]['defence']
        for description in mob_data.mob[self.kind]['descriptions']:
            descript = deepcopy(description)  # Создаём новый объект для описания
            if len(descript) == 2:
                descript.append(0)  # Добавляем число использований описания
            elif type(descript[2]) <> int:
                descript[2] = 0
            if len(descript) > 3:
                descript = descript[:3]
                # Отсекание лишних данных, если таковые есть
            self.descriptions.append(descript)  # Добавляем в список
        if 'modifiers' in mob_data.mob[kind]:
            self._modifiers = mob_data.mob[kind]['modifiers']
        self.abilities = []
        self.equipment = []
        self.bg = '' "img/scene/fight/%s.jpg" % mob_data.mob[kind]['image']

    def modifiers(self):
        return self._modifiers

    def attack(self):
        return self.power

    def protection(self):
        return self.defence
