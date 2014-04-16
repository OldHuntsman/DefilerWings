init python:

    class Avatars:
        def __init__(self):
            self._sizex = 100
            self._sizey = 100
            self._posLeft = 1
            self._posRight = 825
            self._imgLeft = list()
            self._imgRight = list()
            pass
            
        def DisplayLeft(self, image):
            renpy.show(image, at_list=[Position(xpos = self._posLeft, ypos = self._CountLeft() * self._sizey, xanchor=1, yanchor=1)])
            self._imgLeft.append(image)

        def DisplayRight(self, image):
            renpy.show(image, at_list=[Position(xpos = self._posRight, ypos = self._CountRight() * self._sizey, xanchor=1, yanchor=1)])
            self._imgRight.append(image)
            
        def DisplayCenter(self, image):
            renpy.show(image, at_list=[Position(xpos = 0, ypos = 0, xanchor=1, yanchor=1)]) #по моему сделал глупо, но я не знаю как по другому
            
        def HideLeft(self, image):
            renpy.hide(image)
            self._imgLeft.remove(image)
        
        def HideRight(self, image):
            renpy.hide(image)
            self._imgRight.remove(image)
        
        def _CountLeft(self):
            return len(self._imgLeft)
        
        def _CountRight(self):
            return len(self._imgRight)
        
        def RearrangeLeft(self):
            for i in self._imgLeft:
                renpy.hide(i)
            j = 0
            for i in self._imgLeft:
                renpy.show(i, at_list=[Position(xpos = self._posLeft, ypos = j * self._sizey, xanchor=1, yanchor=1)])
                j += 1
         
        def RearrangeRight(self):
            for i in self._imgRight:
                renpy.hide(i)
            j = 0
            for i in self._imgRight:
                renpy.show(i, at_list=[Position(xpos = self._posRight, ypos = j * self._sizey, xanchor=1, yanchor=1)])
                j += 1