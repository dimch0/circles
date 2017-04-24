#######################################################################################################################
#################                                                                                     #################
#################                           Item class, MobileItem class                              #################
#################                                                                                     #################
#######################################################################################################################
import pdb
import time
import math
from math import sqrt, ceil, hypot


class Item(object):
    """
    This is the base class for all circle items
    It includes the open_menu method.
    """
    def __init__(self, grid, name, pos=(), color=None, uncolor=None, image=None, border=0):
        self.grid = grid
        self.name = name
        self.pos = pos
        self.color = color
        self.uncolor = uncolor
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

    def set_img_pos(self):
        """
        Centers the image posotion
        :param grid:  grid object
        :return: coordinates of the centered image
        """
        img_x = self.pos[0] - self.grid.tile_radius / 2
        img_y = self.pos[1] - self.grid.tile_radius / 2
        return (img_x, img_y)

    def set_option_pos(self):
        # Returning the options only
        for idx, option in enumerate(self.options):
            if self.in_menu:
                option.pos = self.grid.adj_tiles(self.pos)[idx]

    def set_mode(self, option, mode_vs_option):
        """
        Changes the mode of an item to a given options
        :param option: an option item of a menu
        :param grid: grid instance
        """
        self.mode = option.name
        self.color = option.color
        if option.uncolor:
            self.uncolor = option.uncolor
        self.img = option.img
        if option.name in mode_vs_option.keys():
            self.options = mode_vs_option[option.name]
        self.set_option_pos()

    def reset_mode(self):
        """
        Resets the item to default mode
        """
        self.mode = self.name
        self.color = self.default_color
        self.img = self.default_img
        self.options = self.default_options

    def overlap(self):
        """
        Checks for overlapping items
        if in menu: creates a backup in grid.overlapped_items
        if not in menu: restores from grid.overlapped_items
        :return:
        """
        if self.in_menu:
            for overlapping_item in self.grid.items:
                if overlapping_item.pos in self.grid.adj_tiles(self.pos):
                    self.grid.overlapped_items.append(overlapping_item)
                    self.grid.items.remove(overlapping_item)
        else:
            if self.grid.overlapped_items:
                for overlapping_item in self.grid.overlapped_items:
                    self.grid.items.append(overlapping_item)
                    self.grid.overlapped_items.remove(overlapping_item)

    def set_in_menu(self, clicked_circle, mode_vs_options):
        # Clicked on item
        if clicked_circle == self.pos and self.name in mode_vs_options.keys():
            # If default mode:
            if self.mode is self.name:
                if not self.in_menu:
                    self.in_menu = True
                    self.overlap()
                elif self.in_menu:
                    self.in_menu = False
                    self.overlap()
            # If not default - reset
            elif self.mode is not self.name:
                if self.in_menu:
                    self.reset_mode()
                elif not self.in_menu:
                    self.in_menu = True
                    self.overlap()
        # Clicked outside
        elif clicked_circle is not self.pos and clicked_circle not in self.grid.adj_tiles(self.pos):
            self.in_menu = False
            self.overlap()


class MobileItem(Item):
    """
    This is the base class for all circle items
    """
    def __init__(self, speed, **kwargs):
        super(MobileItem, self).__init__(**kwargs)
        self.speed = speed

    # TODO Debug one of the below methods
    def move_to_tile(self, Tile_A, Tile_B):
        """
        This method moves the item from the current position to Tile_B.
        :param Tile_B: coordinates of destination point B (x, y)
        :return: a list of steps from point A to point B
        number of steps depends on the speed and the distance
        """
        print "Inside move to tile"
        result = []
        # Movement only allowed in revealed_tiles and not occupado_tiles
        if Tile_B in self.grid.revealed_tiles and Tile_B not in self.grid.occupado_tiles:
            ax = Tile_A[0]
            ay = Tile_A[1]
            bx = Tile_B[0]
            by = Tile_B[1]
            # TODO: debug step generation
            dx, dy = (bx - ax, by - ay)
            # distance = int(sqrt(dx ** 2 + dy ** 2))
            distance = 2 * self.grid.tile_radius
            steps_number = int(ceil(2 * distance / (2 * self.speed)))
            step_size = int(distance / steps_number)
            if steps_number > 0:
                stepx, stepy = int(dx / steps_number), int(dy / steps_number)
                for i in range(steps_number + 1):
                    step = (int(ax + (stepx * i)), int(ay + (stepy * i)))
                    result.append(step)
            result.append(Tile_B)
        return result

    def gen_move_track(self, direction, direction_items):
        """
        :param self.grid: self.grid instance
        :return: a list of all available tiles in northeast direction
        """
        print "Inside gen move track"
        dir = None
        for idx, direction_item in enumerate(direction_items):
            if direction == direction_item.name:
                dir = idx
        result = []
        Point_A = self.pos
        Point_B = self.grid.adj_tiles(self.pos)[dir]

        for fields in range(1,len(self.grid.tiles)):
            if Point_B in self.grid.playing_tiles:
                if Point_B not in self.grid.occupado_tiles and Point_B in self.grid.revealed_tiles:
                    for new_steps in self.move_to_tile(Point_A, Point_B):
                        if not new_steps in result:
                            result.append(new_steps)
                else:
                    self.move_track = result
                    return result
            Point_A = Point_B
            Point_B = self.grid.adj_tiles(Point_A)[dir]
        self.move_track = result
        print "result:", result
        return result

    def move(self):
        """
        :return: move self.pos per point in move_track
        """
        if self.move_track:
            self.pos = self.move_track[0]
            self.move_track.pop(0)
