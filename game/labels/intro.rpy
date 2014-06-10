# DONE: РќСѓР¶РЅРѕ С‡С‚РѕР±С‹ С‚РµРєСЃС‚ РѕРґРЅРёРј РєСѓСЃРєРѕРј РїСЂРѕРєСЂСѓС‡РёРІР°Р»СЃСЏ СЃРЅРёР·Сѓ РІРІРµСЂС… РЅР° С„РѕРЅРµ РјРµРЅСЏСЋС‰РёС…СЃСЏ РєР°СЂС‚РёРЅРѕРє. Р С‡С‚РѕР±С‹ С‚РµРєСЃС‚ РЅРѕСЂРјР°Р»СЊРЅРѕ С‡РёС‚Р°Р»СЃСЏ РЅСѓР¶РЅРѕ Р»РёР±Рѕ РѕР±РІРµСЃС‚Рё Р±СѓРєРІС‹, Р»РёР±Рѕ СЃРґРµР»Р°С‚СЊ РїРѕРґР»РѕР¶РєСѓ.
# РўODO: РќСѓР¶РЅРѕ С‡С‚РѕР±С‹ РїСЂРё РЅР°Р¶Р°С‚РёРё esc Рё РїСЂРѕС‡РёС… РІС‹Р·РѕРІРѕРІ РјРµРЅСЋ РїСЂРѕРєСЂСѓС‚РєР° РѕСЃС‚Р°РЅР°РІР»РёРІР°Р»Р°СЃСЊ.
    
transform bottom_to_top:
        ypos 720 
        linear 90.0 ypos 0 yanchor 1.0

transform intro_bg:
    "intro 1"
    pause 10
    "intro 2" with dissolve
    pause 10
    "intro 3" with dissolve
    pause 10
    "intro 4" with dissolve
    pause 10
    "intro 5" with dissolve
    pause 10
    "intro 6" with dissolve
    pause 10
    "intro 7" with dissolve
    pause 10
    "intro 8" with dissolve
    repeat
    
screen sc_intro:
    add "intro 1" at intro_bg
    #text intro_text at bottom_to_top:
    text intro_text:
        first_indent 30
        newline_indent True
        layout "tex-subtitle"
        #rest_indent 0
        justify True
        outlines [(1, "#0008", 1, 1)]
        #xmaximum 1280
    key "K_SPACE" action Return()
    key 'K_RETURN' action Return()
    key 'K_KP_ENTER' action Return()
    key "mousedown_1" action Return()