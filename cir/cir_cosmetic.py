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
            "grey08": "c9c6bd",
            "grey09": "b9bab4",
            "grey10": "dce1db",
            "grey11": "d3d2d0",
            "grey12": "c9c5c2",
            "grey13": "b2aeab",
            "grey14": "9a9a93",
            "grey15": "676760",
            "grey16": "65666d",
            "grey17": "878892",
            "grey18": "98999f",
            "grey19": "9b919b",
            "grey20": "afa5af",
            "grey21": "c3c3c3",
            "grey22": "dcd7dc",
            "white": "ffffff",
            "gelb01": "ffffdd",
            "gelb02": "fcffbe",
            "gelb03": "ffff8c",
            "gelb04": "ffff00",
            "gelb05": "fcc21c",
            "gelb06": "feb371",
            "gelb07": "8a857f",
            "gelb08": "ada397",
            "gelb09": "cba983",
            "gelb10": "bab7a8",
            "gelb11": "ccc0b2",
            "gelb12": "cebea5",
            "gelb13": "cdc7af",
            "gelb14": "cdd0bd",
            "gelb15": "d8d5c4",
            "gelb16": "d8ceb3",
            "gelb17": "e5dec4",
            "gelb18": "ede8d5",
            "gelb19": "e6e2d7",
            "red01": "ed6d31",
            "red02": "f35d73",
            "red03": "ff6b9b",
            "red04": "f4c3fd",
            "red05": "fed7fc",
            "red06": "ffd1dc",
            "red07": "f0dedd",
            "cyan01": "17fbf4",
            "cyan02": "bcfffe",
            "cyan03": "3fff00",
            "cyan04": "d2ffbf"
                  }
        for color_name, color_value in colors.items():
            setattr(grid, color_name, hex2rgb(color_value))


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

                    if 'emoji' in img_file:
                        img_side = grid.tile_radius
                    elif 'neon' in img_file:
                        img_side = int(grid.tile_radius * 2.5)
                    else:
                        img_side = grid.tile_radius * 2

                    image = grid.pygame.transform.scale(image, (img_side, img_side))

                    if not 'insta' in img_file:
                        setattr(self, name, image)

        except Exception as e:
            grid.msg("ERROR - could not set image as attribute: {0}".format(e))
