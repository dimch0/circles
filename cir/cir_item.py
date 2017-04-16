#######################################################################################################################
#################                                                                                     #################
#################                     Item class / MobileItem class                                   #################
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
    def __init__(self, name, color):
        self.name = name
        self.pos = ()
        self.color = color
        self.current_img = None
        self.default_options = []
        self.options = []
        self.items_to_restore = []
        self.in_menu = False
        self.available = True
        self.mode = self.name


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



class MobileItem(Item):
    """
    This is the base class for all circle items
    """
    def __init__(self, speed, **kwargs):
        super(MobileItem, self).__init__(**kwargs)
        self.speed = speed
        self.pos = ()
        self.move_track = []

    def gen_move_track(self, Point_B, grid):
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

    def move(self):
        """
        :return: move self.pos per point in move_track
        """
        if self.move_track:
            self.pos = self.move_track[0]
            self.move_track.pop(0)
