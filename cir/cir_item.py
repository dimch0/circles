#######################################################################################################################
#################                                                                                     #################
#################                           Item class, MobileItem class                              #################
#################                                                                                     #################
#######################################################################################################################
import pdb
import time
from math import sqrt
# TODO: pass grid object here

class Item(object):
    """
    This is the base class for all circle items
    It includes the open_menu method.
    """
    def __init__(self, name, pos=(), color=None, image=None, border=0):
        self.name = name
        self.pos = pos
        self.color = color
        self.img = image
        self.border = border
        self.options = []
        self.default_color = self.color
        self.default_img = self.img
        self.default_options = []
        self.items_to_restore = []
        self.in_menu = False
        self.available = True
        self.mode = self.name

        self.move_track = []
        self.radar_track = []


    def set_img_pos(self, grid):
        """
        Centers the image posotion
        :param grid:  grid object
        :return: coordinates of the centered image
        """
        img_x = self.pos[0] - grid.tile_radius / 2
        img_y = self.pos[1] - grid.tile_radius / 2
        return (img_x, img_y)


    def adj_tiles(self, grid):
        """
        :param grid: the grid instance
        :return: a list of the 6 adjacent to self.pos tiles
        """
        self_x = self.pos[0]
        self_y = self.pos[1]
        return [
                (self_x, self_y - 2 * grid.tile_radius),
                (self_x + grid.cathetus, self_y - grid.tile_radius),
                (self_x + grid.cathetus, self_y + grid.tile_radius),
                (self_x, self_y + 2 * grid.tile_radius),
                (self_x - grid.cathetus, self_y + grid.tile_radius),
                (self_x - grid.cathetus, self_y - grid.tile_radius)
               ]

    # TODO: Backup and restore existing items under menu items
    # TODO: Show backgourd menu
    # TODO: return option image and color
    # TODO: make function to blit option
    # TODO: execute adding and removing to grid.items here

    def set_option_pos(self, grid):
        # Returning the options only
        for idx, option in enumerate(self.options):
            if self.in_menu:
                option.pos = self.adj_tiles(grid)[idx]


    def set_mode(self, option, grid, mode_vs_option):
        """
        Changes the mode of an item to a given options
        :param option: an option item of a menu
        :param grid: grid instance
        """
        self.mode = option.name
        self.color = option.color
        self.img = option.img
        self.options = mode_vs_option[option.name]
        self.set_option_pos(grid)


    def reset_mode(self):
        """
        Resets the item to default mode
        """
        self.mode = self.name
        self.color = self.default_color
        self.img = self.default_img
        self.options = self.default_options


class MobileItem(Item):
    """
    This is the base class for all circle items
    """
    def __init__(self, speed, **kwargs):
        super(MobileItem, self).__init__(**kwargs)
        self.speed = speed


    def simple_move_track(self, Point_B, grid):
        """
        This method moves the item from the current position to Point_B.
        :param Point_B: coordinates of destination point B (x, y)
        :param SPEED: pixels moved for each step
        :return: a list of steps from point A to point B
        """
        self.move_track = []
        # Movement only allowed in revealed_tiles and not occupado_tiles
        if Point_B in grid.revealed_tiles and Point_B not in grid.occupado_tiles:
            ax = self.pos[0]
            ay = self.pos[1]
            bx = Point_B[0]
            by = Point_B[1]
            print "DEBUG coor", ax, bx, ay, by
            dx, dy = (bx - ax, by - ay)
            distance = sqrt(dx ** 2 + dy ** 2)
            steps_number = int(distance / self.speed)
            if steps_number > 0:
                stepx, stepy = int(dx / steps_number), int(dy / steps_number)
                for i in range(steps_number + 1):
                    step = (int(ax + stepx * i), int(ay + stepy * i))
                    self.move_track.append(step)
            self.move_track.append(Point_B)
        return self.move_track


    def move_south(self, grid):
        result = []
        for tile in grid.tiles:
            even_coef = range(2, 20, 2)
            for even_c in even_coef:
                if tile[0] == self.pos[0]:
                    if tile[1] == self.pos[1] + (even_c * grid.tile_radius):
                        if tile not in grid.occupado_tiles:
                            result.append(tile)
                        else:
                            return result
        return result

    def move(self):
        """
        :return: move self.pos per point in move_track
        """
        if self.move_track:
            self.pos = self.move_track[0]
            self.move_track.pop(0)
