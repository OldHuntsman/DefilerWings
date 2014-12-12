# coding=utf-8
screen sc_treasury_gems:
    python:
        class del_gem(object):
            def __init__(self, gem_store, gem_index):
                self.gem_store = gem_store
                self.gem_index = gem_index

            def __call__(self):
                self.gem_store.pop(self.gem_index)
                renpy.restart_interaction()
    vbox:
        
        for i in range(0, len(game.lair.treasury.gems)):
            hbox:
                text "Тип:%s Цена:%d" % (game.lair.treasury.gems[i].g_type,
                                         game.lair.treasury.gems[i].cost)
                textbutton "Удалить" action del_gem(game.lair.treasury.gems, i)
    
    use sc_gem_creator

screen sc_gem_creator:
    python:
        class add_gem(object):
            def __init__(self, gemstore, gem):
                self.gemstore = gemstore
                self.gem = gem

            def __call__(self):
                self.gemstore.receive_treasures([self.gem])
                renpy.restart_interaction()
    
    default type = treasures.gem_types.keys()[0]
    default cut = treasures.Gem.cut_dict.keys()[0]
    default size = treasures.Gem.size_dict.keys()[0]
    
    vbox:
        #xalign 1.0
        xpos 640
        textbutton "Добавить" action add_gem(game.lair.treasury,
                                             treasures.Gem(g_type=type, size=size, cut=cut))
        text "Type: %s"%type
        text "Cut: %s" %cut
        text "Size %s" %size
        
        
        hbox:
            vbox:
                for i in treasures.gem_types:
                    textbutton i action [ SetScreenVariable("type", i), renpy.restart_interaction ]
            vbox:
                for i in treasures.Gem.cut_dict:
                    textbutton i action SetScreenVariable("cut", i)
            
            vbox:
                for i in treasures.Gem.size_dict:
                    textbutton i action SetScreenVariable("size", i)
