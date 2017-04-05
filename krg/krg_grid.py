"""
================================== Grid class ==================================
"""


from krg_utils import in_circle as in_circle
from math import sqrt


class Grid(object):
    """
    master class for the grid
    """
    def __init__(self, circle_radius):
        self.tile_radius = circle_radius
        self.tiles = []
        self.occupado = []
        self.revealed = []

    @staticmethod
    def grid_gen(circle_radius):
        """
        :param circle_radius:
        :return:
        """
        result = {}
        katet = int(sqrt(((2 * circle_radius) ** 2) - (circle_radius ** 2)))
        for x in range(0, 12):
            for y in range(1, 20):
                if x % 2 == y % 2:
                    centre_x = circle_radius + (x * katet)
                    centre_y = y * circle_radius
                    centre = (centre_x, centre_y)
                    name = "{0}, {1}".format(x, y)
                    result[name] = centre
                    # pygame.draw.circle(gameDisplay, white, centre, circle_radius, 1)
        return result

    @staticmethod
    def mouse_in_tile(circle_radius, mouse_pos):
        current_circle = None
        grid = Grid.grid_gen(circle_radius)
        for tile, circle in grid.items():
            if in_circle(circle, circle_radius, mouse_pos):
                current_circle = circle
                print tile
        return current_circle