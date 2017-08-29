#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                           Images and Fonts classes                                  #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################
import os

class Colors(object):
    """
    A class containing all the colors
    """
    @staticmethod
    def set_colors(grid):
        print("INFO: Loading colors")
        colors = {
                  "black"      : [0, 0, 0],
                  "dark_grey"  : [155, 145, 155],
                  "grey"       : [175, 165, 175],
                  "ungrey"     : [195, 195, 195],
                  "light_grey" : [220, 215, 220],
                  "white"      : [255, 255, 255],
                  "unpink"     : [240, 222, 221],
                  "pastel_pink": [255, 209, 220],
                  "pink"       : [254, 215, 252],
                  "purp"       : [244, 195, 253],
                  "cyclama"    : [255, 107, 155],
                  "red"        : [243, 93, 115],
                  "blue"       : [188, 255, 254],
                  "azure"      : [23, 251, 244],
                  "green"      : [210, 255, 191],
                  "electric"   : [63, 255, 0],
                  "light_gelb" : [255, 255, 221],
                  "gelb"       : [252, 255, 190],
                  "neapo"      : [255, 255, 140],
                  "yellow"     : [255, 255, 0],
                  "yellowgrey" : [238, 224, 112],
                  "orange"     : [254, 179, 113],
                  "brown"      : [203, 169, 131],
                  "ggelb"      : [252, 194, 27]
                  }
        for color_name, color_value in colors.items():
            setattr(grid, color_name, color_value)


class Fonts(object):
    """
    A class containing all the fonts
    """
    def __init__(self, grid):
        self.tiny = grid.pygame.font.Font(grid.font_file, int(grid.tile_radius * 0.45))
        self.small = grid.pygame.font.Font(grid.font_file, int(grid.tile_radius * 0.60))
        self.medium = grid.pygame.font.Font(grid.font_file, int(grid.tile_radius))
        self.large = grid.pygame.font.Font(grid.font_file, grid.tile_radius * 2)


class Images(object):
    """
    A class containing all images
    """
    def __init__(self, grid):
        self.set_images(grid)

    def set_images(self, grid):
        """
        Setting attributes from the img directory
        and calculating the display metrics
        """
        print("INFO: Loading images")
        try:
            for root, dirs, files in os.walk(grid.img_dir, topdown=False):
                for file in files:
                    img_file = os.path.join(root, file)
                    name = os.path.splitext(file)[0]
                    image = grid.pygame.image.load(img_file)

                    if 'emoji' in img_file:
                        image = grid.pygame.transform.scale(image, (grid.tile_radius, grid.tile_radius))
                    else:
                        image = grid.pygame.transform.scale(image, (grid.tile_radius * 2, grid.tile_radius * 2))

                    if not 'insta' in img_file:
                        setattr(self, name, image)

        except Exception as e:
            print "ERROR, could not set image as attribute:", e
