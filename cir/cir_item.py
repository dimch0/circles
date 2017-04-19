#######################################################################################################################
#################                                                                                     #################
#################                           Item class, MobileItem class                              #################
#################                                                                                     #################
#######################################################################################################################
import pdb
import time
from math import sqrt, ceil
# TODO: pass grid object here

class Item(object):
    """
    This is the base class for all circle items
    It includes the open_menu method.
    """
    def __init__(self, name, pos=(), color=None, uncolor=None, image=None, border=0):
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


    def set_img_pos(self, grid):
        """
        Centers the image posotion
        :param grid:  grid object
        :return: coordinates of the centered image
        """
        img_x = self.pos[0] - grid.tile_radius / 2
        img_y = self.pos[1] - grid.tile_radius / 2
        return (img_x, img_y)


    # TODO: Backup and restore existing items under menu items
    # TODO: Show backgourd menu
    # TODO: return option image and color
    # TODO: make function to blit option
    # TODO: execute adding and removing to grid.items here

    def set_option_pos(self, grid):
        # Returning the options only
        for idx, option in enumerate(self.options):
            if self.in_menu:
                option.pos = grid.adj_tiles(self.pos)[idx]


    def set_mode(self, option, grid, mode_vs_option):
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


    def free_move_track(self, Point_B, grid):
        """
        This method moves the item from the current position to Point_B.
        :param Point_B: coordinates of destination point B (x, y)
        :return: a list of steps from point A to point B
        number of steps depends on the speed and the distance
        """
        # TODO: fix the steps generation
        result = []
        # Movement only allowed in revealed_tiles and not occupado_tiles
        if Point_B in grid.revealed_tiles and Point_B not in grid.occupado_tiles:
            ax = self.pos[0]
            ay = self.pos[1]
            bx = Point_B[0]
            by = Point_B[1]
            dx, dy = (bx - ax, by - ay)
            distance = int(sqrt(dx ** 2 + dy ** 2))
            steps_number = int(ceil(distance / (2 * self.speed)))
            print "STEPS NUMBER", steps_number
            print "RADIUS DISTANCE", distance, grid.tile_radius
            if steps_number > 0:
                stepx, stepy = int(dx / steps_number), int(dy / steps_number)
                for i in range(steps_number + 1):
                    step = (int(ax + stepx * i), int(ay + stepy * i))
                    result.append(step)
            result.append(Point_B)
        return result


    def direct_move_track(self, grid, direction):
        """
        :param grid: grid instance
        :return: a list of all available tiles in northeast direction
        """

        # TODO: parametrize
        dir = None
        if direction is "north":
            dir = 0
        elif direction is "northeast":
            dir = 1
        elif direction is "southeast":
            dir = 2
        elif direction is "south":
            dir = 3
        elif direction is "southwest":
            dir = 4
        elif direction is "northwest":
            dir = 5

        result = []
        new_track = grid.adj_tiles(self.pos)[dir]
        for fields in range(1,11):
            if new_track in grid.revealed_tiles:
                if new_track not in grid.occupado_tiles:
                    for new_steps in self.free_move_track(new_track, grid):
                        if not new_steps in result:
                            result.append(new_steps)
                else:
                    self.move_track = result
                    return result
            new_track = grid.adj_tiles(new_track)[dir]

        self.move_track = result
        return result


    def move_northeast(self, grid):
        """
        :param grid: grid instance
        :return: a list of all available tiles in northeast direction
        """
        result = []
        new_track = grid.adj_tiles(self.pos)[1]
        for fields in range(1,11):
            if new_track in grid.revealed_tiles:
                if new_track not in grid.occupado_tiles:
                    for new_steps in self.free_move_track(new_track, grid):
                        if not new_steps in result:
                            result.append(new_steps)
                else:
                    self.move_track = result
                    return result
            new_track = grid.adj_tiles(new_track)[1]

        self.move_track = result
        return result



    def move(self):
        """
        :return: move self.pos per point in move_track
        """
        if self.move_track:
            self.pos = self.move_track[0]
            self.move_track.pop(0)
