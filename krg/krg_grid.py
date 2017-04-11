#######################################################################################################################
#################                                                                                     #################
#################                                 Grid class                                          #################
#################                                                                                     #################
#######################################################################################################################


from krg_utils import in_circle
from math import sqrt


class Grid(object):
    """
    master class for the grid
    """
    def __init__(self, circle_radius):
        self.tile_radius = circle_radius
        self.tiles = []
        self.occupado_tiles = []
        self.revealed_tiles = []
        self.revealed_radius = []
        self.items = []
        self.mouse_mode = None
        self.mouse_img = None
        self.mode = []


    # TODO: set as a property to self.tiles
    def grid_gen(self):
        """
        :return: generating the grid tiles
        """
        katet = int(sqrt(((2 * self.tile_radius) ** 2) - (self.tile_radius ** 2)))
        for x in range(0, 11):
            for y in range(1, 24):
                if x % 2 == y % 2:
                    centre_x = self.tile_radius + (x * katet)
                    centre_y = y * self.tile_radius
                    centre = (centre_x, centre_y)
                    if not centre in self.tiles:
                        self.tiles.append(centre)
        return self.tiles

    def mouse_in_tile(self, mouse_pos):
        """
        :param mouse_pos: position of the mouse
        :return: returns the current tile, the mouse is in
         or None if there is no such
        """
        current_tile = None
        for tile in self.tiles:
            if in_circle(tile, self.tile_radius, mouse_pos):
                current_tile = tile
        return current_tile

    def starting_pos(self, display_width, display_height):
        """
        :param display_width:
        :param display_height:
        :return: the tile (x, y) of the center tile
        """
        mid_x = int(display_width / 2)
        mid_y = int(display_height / 2)
        result = None
        for tile in self.tiles:
            if in_circle(tile, self.tile_radius, (mid_x, mid_y)):
                result = tile
                break
        return result