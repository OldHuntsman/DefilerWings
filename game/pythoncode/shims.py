# coding=utf-8

# Monkey patch для того, чтобы focus_mask воспринимала callable.
# Без этого код пытается интерпретировать callable как displayable и падает.
# Вообще говоря надо патчить renpy.styledata.styleutil.expand_focus_mask,
# но renpy как-то хитро к нему обращается и при замене всё равно работает
# старая версия.
# TODO: Убрать костыль после патча в RenPy.

import renpy.exports as renpy
import pygame

def renpy_easy_monkey_patch():
    if not hasattr(renpy_easy_monkey_patch, 'patched'):
        displayable_origin = renpy.easy.displayable
        
        def displayable_patched(d):
            if callable(d):
                return d
            else:
                return displayable_origin(d)
                
        renpy.easy.displayable = displayable_patched
        
        renpy_easy_monkey_patch.patched = True
                
def screen_displayable_monkey_patch():
    if not hasattr(screen_displayable_monkey_patch, 'patched'):
        event_origin = renpy.display.screen.ScreenDisplayable.event
        
        def event_patched(self, ev, x, y, st):
            # Обработка фокуса.
            if ev.type == pygame.ACTIVEEVENT:
                # Клавиатура или сворачивание.
                if (ev.state & 2) or (ev.state & 4):
                    if ev.gain:
                        renpy.audio.audio.unpause_all()
                    else:
                        renpy.audio.audio.pause_all()
                                                
            return event_origin(self, ev, x, y, st)
                
        renpy.display.screen.ScreenDisplayable.event = event_patched
        
        screen_displayable_monkey_patch.patched = True    
                        