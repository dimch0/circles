#######################################################################################################################
#################                                                                                     #################
#################                           Images and Fonts classes                                  #################
#################                                                                                     #################
#######################################################################################################################
import os


class Fonts(object):
    """
    a class containing all the fonts
    """
    def __init__(self, grid, pygame):
        self.small = pygame.font.Font(grid.font_file, int(grid.tile_radius * 0.60))
        self.medium = pygame.font.Font(grid.font_file, int(grid.tile_radius * 1))
        self.large = pygame.font.Font(grid.font_file, grid.tile_radius * 2)


class Images(object):
    """
    a class containing all images
    """
    def __init__(self, grid, pygame):
        self.set_images(grid, pygame)

    def set_images(self, grid, pygame):
        """
        Setting attributes from the img directory
        and calculating the display metrics
        """
        try:
            for root, dirs, files in os.walk(grid.img_dir, topdown=False):
                for file in files:
                    img_file = os.path.join(root, file)
                    name = os.path.splitext(file)[0]
                    image = pygame.image.load(img_file)
                    image = pygame.transform.scale(image, (grid.tile_radius, grid.tile_radius))
                    setattr(self, name, image)
        except Exception as e:
            print "ERROR, could not set image as attribute:", e


