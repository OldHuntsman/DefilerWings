# coding=utf-8

# Monkey patch for focus_mask to allow it receive callable.
# Without it code tryes to interpret callable as displayable and crashes.
# renpy.styledata.styleutil.expand_focus_mask should be patched,
# but renpy access it not in common way and when it changed
# old version still works.
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
        
# Monkey patch to infiltrate in pygame event loop. In this way
# we can gain access to all arising events and react to needed ones, 
# specifically on keyboard focus changing and window minimization.
def screen_displayable_monkey_patch():
    if not hasattr(screen_displayable_monkey_patch, 'patched'):
        event_origin = renpy.display.screen.ScreenDisplayable.event
        
        def event_patched(self, ev, x, y, st):
            # Focus processing.
            if ev.type == pygame.ACTIVEEVENT:
                # keyboard or minimize.
                if (ev.state & 2) or (ev.state & 4):
                    if ev.gain:
                        renpy.audio.audio.unpause_all()
                    else:
                        renpy.audio.audio.pause_all()
                                                
            return event_origin(self, ev, x, y, st)
                
        renpy.display.screen.ScreenDisplayable.event = event_patched
        
        screen_displayable_monkey_patch.patched = True    
                        