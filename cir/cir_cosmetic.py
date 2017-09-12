# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                                                                                     #
#                                                  COSMETIC                                                           #
#                                                                                                                     #
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
        colors = {
            "black": "000000",
            "grey01": "3b3b3b",
            "grey02": "565656",
            "grey03": "707070",
            "grey04": "a9a9a9",
            "grey05": "c5c5c5",
            "grey06": "e1e1e1",
            "grey07": "e5e3d7",
            "grey08": "d8d5cc",
            "grey09": "c9c6bd",
            "grey10": "aca89c",
            "grey11": "676760",
            "grey12": "9a9a93",
            "grey13": "8a8b7f",
            "grey14": "b9bab4",
            "grey15": "c9cbc0",
            "grey16": "dcd7dc",
            "grey17": "dce1db",
            "grey18": "d3d2d0",
            "grey19": "c9c5c2",
            "grey20": "b2aeab",
            "grey21": "8a857f",
            "grey22": "746f69",
            "grey23": "65666d",
            "grey24": "878892",
            "grey25": "98999f",
            "grey26": "9b919b",
            "grey27": "afa5af",
            "grey28": "c3c3c3",
            "grey29": "dcd7dc",
            "white": "ffffff",
            "gelb01": "ffffdd",
            "gelb02": "fcffbe",
            "gelb03": "ffff8c",
            "gelb04": "ffff00",
            "gelb05": "fcc21c",
            "gelb06": "feb371",
            "gelb07": "cba983",
            "gelb08": "ada397",
            "gelb09": "ccc0b2",
            "gelb10": "cebea5",
            "gelb11": "cbc8b7",
            "gelb12": "d2d2c8",
            "gelb13": "d8d5c4",
            "gelb14": "dad4be",
            "gelb15": "cdc7af",
            "gelb16": "d8ceb3",
            "gelb17": "e5dec4",
            "gelb18": "e2dac5",
            "gelb19": "e6e2d7",
            "gelb20": "ede8d5",
            "gelb21": "d4d1c2",
            "gelb22": "dedacf",
            "gelb23": "898375",
            "gelb24": "bab7a8",
            "gelb25": "cdd0bd",
            "mag01": "ed6d31",
            "mag02": "f35d73",
            "mag03": "ff6b9b",
            "mag04": "f4c3fd",
            "mag05": "fed7fc",
            "mag06": "ffd1dc",
            "mag07": "f0dedd",
            "cyan01": "17fbf4",
            "cyan02": "bcfffe",
            "cyan03": "3fff00",
            "cyan04": "d2ffbf",
                  }
        for color_name, color_value in colors.items():
            setattr(grid, color_name, hex2rgb(color_value))


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
        grid.msg("INFO - Loading images")
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
            grid.msg("ERROR - could not set image as attribute: {0}".format(e))
