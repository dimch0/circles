#######################################################################################################################
#################                                                                                     #################
#################                     Item class / MobileItem class                                   #################
#################                                                                                     #################
#######################################################################################################################

import pdb
from math import sqrt

class Item(object):
    """
    This is the base class for all circle items
    It includes the open_menu method.
    """
    def __init__(self, name):
        self.name = name
        self.pos = ()
        self.color = None
        self.current_img = None
        self.options = []
        self.in_menu = False


    def open_menu(self, clicked_circle, grid):
        """
        This method opens the menu with
        all options for the item and
        temporary disables the other items on the same positions.
        :param grid: the given grid instance
        """
        # TODO: Backup and restore existing items under menu items
        # TODO: Set all options position correctly
        # TODO: Show backgourd menu
        # TODO: return option image and color
        # TODO: make function to blit option

        if clicked_circle == self.pos:
            if self.in_menu == False:
                self.in_menu = True
            else:
                self.in_menu = False
        else:
            self.in_menu = False

        for option in self.options:
            if self.in_menu:
                if option.name == "move":
                    option.pos = (self.pos[0], self.pos[1] + grid.tile_radius * 2)
                    if not option in grid.items:
                        grid.items.append(option)
                if option.name == "radar":
                    option.pos = (self.pos[0], self.pos[1] - grid.tile_radius * 2)
                    if not option in grid.items:
                        grid.items.append(option)

            elif not self.in_menu and option in grid.items:
                grid.items.remove(option)


class MobileItem(Item):
    """
    This is the base class for all circle items
    """
    # TODO: change naming
    def __init__(self):
        super(MobileItem, self).__init__(name="Mobile Item")
        self.speed = 2
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
        # Movement forbidden outside revealed_tiles of the grid
        if Point_B in grid.revealed_tiles:
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
