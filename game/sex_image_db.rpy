init -1 python hide:
    def label_callback(name, abnormal):
        store.last_label = name
    config.label_callback = label_callback

screen label_callback():
    zorder 10**10
    text "[last_label]" align (0.5, 0) size 25
    
init python:
    """
    Added by Alex on 07.05.2015
    Instructions to convert into code: https://github.com/OldHuntsman/DefilerWings/issues/51
    """
    class DragonSexImagesDatabase(object):
        def __init__(self):
            """
            Reads specified folder structure creating entries in the dict.
            """
            import os
            colors = ["black", "blue", "brown", "gold", "green", "red", "shadow", "white"]
            rp_path = 'img/scene/sex'
            path = renpy.loader.transfn(rp_path)
            sex_image_folders = os.listdir(path)
            for folder in sex_image_folders:
                if not hasattr(self, folder):
                    setattr(self, folder, _dict())
                subfolders = os.listdir('/'.join([path, folder]))
                for subfolder in subfolders:
                    for image in os.listdir('/'.join([path, folder, subfolder])):
                        l = list(c for c in colors if image.startswith(c))
                        if l:
                            color = l.pop()
                            if not getattr(self, folder).get(color, None):
                                getattr(self, folder)[color] = _set()
                            img_path = "/".join([rp_path, folder, subfolder, image])
                            getattr(self, folder)[color].add(img_path)
                        else:
                            # We assume this is an image from ""any"":
                            if not getattr(self, folder).get("any", None):
                                getattr(self, folder)["any"] = _set()
                            img_path = "/".join([rp_path, folder, subfolder, image])
                            getattr(self, folder)["any"].add(img_path)
                            
        def has_image_with_color(self, type):
            if getattr(self, type).get(store.game.dragon.color_eng, None):
                return True
                                
        def __call__(self, type):
            if not self.has_image_with_color(type):
                return renpy.random.sample(getattr(self, type)["any"], 1).pop()
            elif renpy.random.randint(0, 2):
                return renpy.random.sample(getattr(self, type)["any"], 1).pop()
            else:
                return renpy.random.sample(getattr(self, type)[store.game.dragon.color_eng], 1).pop()
