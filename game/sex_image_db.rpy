init -1 python hide:
    def label_callback(name, abnormal):
        store.last_label = name
    config.label_callback = label_callback

screen label_callback():
    zorder 10**10
    text "[last_label]" align (0.5, 0) size 25
    
init python:
    """
    Added chain random music function as per Hunters request on Skype:
    """
    def get_random_files(folder, shuffle=True):
        import os
        
        path = renpy.loader.transfn(folder)
        files = _list("/".join([folder, f]) for f in os.listdir(path))
        if shuffle:
            renpy.random.shuffle(files)
        return files
    
    """
    Added get random file function as per Hunters request on Skype:
    """
    def get_random_file(folder):
        return renpy.random.choice(get_random_files(folder))
    
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
                    if subfolder == "color":
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
                        for image in os.listdir('/'.join([path, folder, subfolder])):
                            if not getattr(self, folder).get("any", None):
                                getattr(self, folder)["any"] = _set()
                            img_path = "/".join([rp_path, folder, subfolder, image])
                            getattr(self, folder)["any"].add(img_path)
                            
            # These are not sex images, but Hunter asked me to get a random from them so I'll add it here as well:
            rp_path = 'img/scene/eat'
            path = renpy.loader.transfn(rp_path)
            eat_image_folder = os.listdir(path)
            self.eat = _set()
            for i in eat_image_folder:
                self.eat.add("/".join([rp_path, i]))
                
        def get_eat_image(self):
            return renpy.random.sample(self.eat, 1).pop()
                            
        def has_image_with_color(self, type):
            if getattr(self, type).get(store.game.dragon.color_eng, None):
                return True
                
        def get_any_image(self, type):
            """
            returns an image from "any" folder randomly.
            Picks color of hair if available.
            """
            images = getattr(self, type)["any"]
            correct_hair_images = _list()
            
            # Get a list of images with correct hair colors:
            if type != "dragon": # We do not do this for dragon images.
                if store.game.girl.hair_color:
                    for i in images:
                        img_name = i.split("/")[-1]
                        if store.game.girl.hair_color in img_name:
                            correct_hair_images.append(i)
                    
            if correct_hair_images:
                return renpy.random.choice(correct_hair_images)
            else:
                return renpy.random.sample(images, 1).pop()
                                
        def __call__(self, type):
            if type == "mistress": # @ Unique condition: Always get dragon images!
                return renpy.random.sample(getattr(self, type)[store.game.dragon.color_eng], 1).pop()
            elif not self.has_image_with_color(type):
                return self.get_any_image(type)
            elif renpy.random.randint(0, 2):
                return self.get_any_image(type)
            else:
                return renpy.random.sample(getattr(self, type)[store.game.dragon.color_eng], 1).pop()
