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
                  "black"   :"000000",
                  "grey1"   :"3b3b3b",
                  "grey2"   :"565656",
                  "grey3"   :"707070",
                  "grey4"   :"a9a9a9",
                  "grey5"   :"c5c5c5",
                  "grey6"   :"e1e1e1",
                  "grey7"   :"e5e3d7",
                  "grey8"   :"d8d5cc",
                  "grey9"   :"c9c6bd",
                  "grey10"  :"aca89c",
                  "grey11"  :"898375",
                  "grey12"  :"676760",
                  "grey13"  :"9a9a93",
                  "grey14"  :"8a8b7f",
                  "grey15"  :"b9bab4",
                  "grey16"  :"c7c8c3",
                  "grey17"  :"c9cbc0",
                  "grey18"  :"bab7a8",
                  "grey19"  :"cdd0bd",
                  "grey20"  :"d5d9d8",
                  "grey21"  :"d4d1c2",
                  "grey22"  :"dce1db",
                  "grey23"  :"d3d2d0",
                  "grey24"  :"c9c5c2",
                  "grey25"  :"b2aeab",
                  "grey26"  :"8a857f",
                  "grey27"  :"746f69",
                  "grey28"  :"65666d",
                  "grey29"  :"878892",
                  "grey30"  :"98999f",
                  "white"   :"ffffff",
                  "brown1"  :"ada397",
                  "brown2"  :"ccc0b2",
                  "brown3"  :"cebea5",
                  "brown4"  :"cbc8b7",
                  "brown5"  :"d2d2c8",
                  "brown6"  :"d8d5c4",
                  "brown7"  :"dad4be",
                  "brown8"  :"cecbbc",
                  "brown9"  :"cdc7af",
                  "brown10" :"e1d9c4",
                  "brown11" :"dedacf",
                  "brown12" :"d8ceb3",
                  "brown13" :"e5dec4",
                  "brown14" :"e8dcc4",
                  "brown15" :"e7dac9",
                  "brown16" :"e2dac5",
                  "brown17" :"e6e2d7",
                  "brown18" :"ede8d5",
                  "dark_grey" :"9b919b",
                  "grey"    :"afa5af",
                  "ungrey"  :"c3c3c3",
                  "light_grey" :"dcd7dc",
                  "light_gelb" :"ffffdd",
                  "gelb"    :"fcffbe",
                  "neapo"   :"ffff8c",
                  "yellow"  :"ffff00",
                  "ggelb"   :"fcc21b",
                  "orange"  :"feb371",
                  "brown"   :"cba983",
                  "red"     :"f35d73",
                  "cyclama" :"ff6b9b",
                  "purp"    :"f4c3fd",
                  "pastel_pink" :"ffd1dc",
                  "unpink"  :"f0dedd",
                  "pink"    :"fed7fc",
                  "blue"    :"bcfffe",
                  "azure"   :"17fbf4",
                  "electric":"3fff00",
                  "green"   :"d2ffbf"
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
