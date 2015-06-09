# coding=utf-8
screen sc_equip_editor(object, equip_variants):
    # :param object: Объект, чьи предметы будут редактироваться, например рыцарь.
    # :param equip_variants: Список из вариантов экипировки
    
    python:
        class Unequip(Action):
            def __init__(self, target, type):
                self._target = target
                self._type = type

            def __call__(self):
                self._target.unequip(self._type)
                renpy.restart_interaction()

        class Equip(Action):
            def __init__(self, target, item):
                self._target = target
                self._item = item

            def __call__(self):
                self._target.equip(self._item)
                renpy.restart_interaction()
    
    vbox:
        text("Инструкции:\n"
             "Кликните на объект в списке одетых вещей чтобы снять его.\n"
             "Кликните на объект в номерном контейнере чтобы одеть его.")
        hbox:
            vbox:
                text "Одето:"
                for i in object.items:
                    if object.items[i] is not None:
                        textbutton "%s: %s" % (i, object.items[i].name) action Unequip(object, i)
                    else:
                        textbutton "%s: %s" % (i, "None") action Unequip(object, i)
            for d in equip_variants:
                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    vbox:
                        text "%s:" % d.id
                        for type in object._equip_slots:
                            text "%s:" % type
                            for i in d.contains("type", type):
                                textbutton d[i].name action Equip(object, d[i])