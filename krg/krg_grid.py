"""
================================== Grid class ==================================
"""


from krg_utils import in_circle
from math import sqrt


class Grid(object):
    """
    master class for the grid
    """
    def __init__(self, circle_radius):
        self.tile_radius = circle_radius
        self.tiles = {}
        self.occupado = []
        self.revealed = []
        self.revealed_radius = []
        self.items = []
        self.mouse_mode = None
        self.mouse_img = None
        self.mode = []

    @staticmethod
    def grid_gen(circle_radius):
        """
        :param circle_radius:
        :return:
        """
        result = {}
        katet = int(sqrt(((2 * circle_radius) ** 2) - (circle_radius ** 2)))
        for x in range(0, 11):
            for y in range(1, 24):
                if x % 2 == y % 2:
                    centre_x = circle_radius + (x * katet)
                    centre_y = y * circle_radius
                    centre = (centre_x, centre_y)
                    name = "{0}, {1}".format(x, y)
                    result[name] = centre
        return result

    @staticmethod
    def mouse_in_tile(circle_radius, mouse_pos):
        current_circle = None
        grid = Grid.grid_gen(circle_radius)
        for tile, circle in grid.items():
            if in_circle(circle, circle_radius, mouse_pos):
                current_circle = circle
        return current_circle

    def starting_pos(self, display_width, display_height):
        """
        :param display_width:
        :param display_height:
        :return: the tile (x, y) of the center tile
        """
        mid_x = int(display_width / 2)
        mid_y = int(display_height / 2)
        result = None
        for tile in self.tiles.values():
            if in_circle(tile, self.tile_radius, (mid_x, mid_y)):
                result = tile
                break
        return result