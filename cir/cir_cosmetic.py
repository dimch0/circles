#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                           Images and Fonts classes                                  #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################
import os


class Fonts(object):
    """
    A class containing all the fonts
    """
    def __init__(self, grid):
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
        print "Loading images..."
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
