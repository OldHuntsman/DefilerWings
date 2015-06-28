# coding=utf-8

class Mortal(object):
    _alive = True  # По умолчанию все живые

    @property
    def is_alive(self):
        return self._alive

    @property
    def is_dead(self):
        return not self._alive

    def die(self):
        self._alive = False