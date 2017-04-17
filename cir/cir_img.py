#######################################################################################################################
#################                                                                                     #################
#################                                 Images class                                        #################
#################                                                                                     #################
#######################################################################################################################

import os
import pygame


class Images(object):
    """
    a class containing all the images
    """
    def __init__(self, grid):
        self.set_images(grid)

    def set_images(self, grid):
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
