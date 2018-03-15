# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                  COSMETIC                                                           #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import os


def hex2rgb(hex_str):
    """ Converts color from hex string to rgb tuple """
    return tuple(int(hex_str[i:i + 2], 16) for i in (0, 2, 4))


class Colors(object):
    """
    A class containing all the colors
    """
    @staticmethod
    def set_colors(grid):
        grid.msg("INFO - Loading colors")
        setattr(grid, 'black', hex2rgb('000000'))
        setattr(grid, 'white', hex2rgb('ffffff'))
        with open(grid.colors_file, 'r') as f:
            colors = f.read().splitlines()
            for color in colors:
                setattr(grid, color, hex2rgb(color))


class Fonts(object):
    """
    A class containing all the fonts
    """
    def __init__(self, grid):
        self.tiny = grid.pygame.font.Font(grid.font_file, int(grid.tile_radius * 0.45))
        self.small = grid.pygame.font.Font(grid.font_file, int(grid.tile_radius * 0.55))
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
        grid.msg("INFO - Loading images")
        try:
            for root, dirs, files in os.walk(grid.img_dir, topdown=False):
                for file in files:
                    img_file = os.path.join(root, file)
                    name = os.path.splitext(file)[0]
                    image = grid.pygame.image.load(img_file)

                    if 'neon' in img_file:
                        scale = 2.5
                    else:
                        scale = 1.2

                    img_side = int(grid.tile_radius * scale)
                    image = grid.pygame.transform.scale(image, (img_side, img_side))
                    setattr(self, name, image)

        except Exception as e:
            grid.msg("ERROR - could not set image as attribute: {0}".format(e))
