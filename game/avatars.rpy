init python:
    def get_dragon_avatar(type):
        directory = 'img/avadragon/' + type #получаем путь простым сложением
        filename = random.choice(os.listdir(directory)) # получаем название файла
        return directory + '/' + filename

    class Avatars:
        def __init__(self):
            # Размер аватарки по высоте. TODO: нужно чтобы этот прараметр влилял на отображаемый размер аватарки.
            self._sizey = 200
            # Отступы от края для аватки слева и справа соответственно
            self._posLeft = 1
            self._posRight = 825
            # Листы с картинками слева и справа соотвественно. Используются для упорядочивания аватарок после удаления.
            self._imgLeft = list()
            self._imgRight = list()
            pass
            
        
        def DisplayLeft(self, image):
            """Размещает изображение image слева. Изображение должно быть преформатировано."""
            renpy.show(image, at_list=[Position(xpos = self._posLeft, ypos = self._CountLeft() * self._sizey, xanchor=1, yanchor=1)])
            # Добавляем аватарку в лист.
            self._imgLeft.append(image)

        def DisplayRight(self, image):
            """Размещает изображение image справа. Изображение должно быть преформатировано."""
            renpy.show(image, at_list=[Position(xpos = self._posRight, ypos = self._CountRight() * self._sizey, xanchor=1, yanchor=1)])
            # Добавляем аватарку в лист.
            self._imgRight.append(image)
            
        def HideLeft(self, image):
            """Сркывает изображение image слева."""
            renpy.hide(image)
            # Удаляем аватарку из листа.
            self._imgLeft.remove(image)
        
        def HideRight(self, image):
            """Сркывает изображение image справа."""
            renpy.hide(image)
            # Удаляем аватарку из листа.
            self._imgRight.remove(image)
        
        def _CountLeft(self):
            """Текущее количество изображений слева."""
            return len(self._imgLeft)
        
        def _CountRight(self):
            """Текущее количество изображений справа."""
            return len(self._imgRight)
        
        def RearrangeLeft(self):
            """Упорядочить аватарки слева."""
            #Cначала прячем все аватарки
            for i in self._imgLeft:
                renpy.hide(i)
            #Затем показываем
            j = 0
            for i in self._imgLeft:
                renpy.show(i, at_list=[Position(xpos = self._posLeft, ypos = j * self._sizey, xanchor=1, yanchor=1)])
                j += 1
         
        def RearrangeRight(self):
            """Упорядочить аватарки справа."""
            for i in self._imgRight:
                renpy.hide(i)
            j = 0
            for i in self._imgRight:
                renpy.show(i, at_list=[Position(xpos = self._posRight, ypos = j * self._sizey, xanchor=1, yanchor=1)])
                j += 1