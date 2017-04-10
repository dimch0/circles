"""
================================== Item class ==================================
"""

import pdb
from math import sqrt
from krg_grid import Grid


class Item(object):
    """
    This is the base class for all circle items
    """
    def __init__(self, name):
        self.name = name
        self.pos = ()
        self.move_track = []
        self.radar_track = []
        self.color = None
        self.current_img = None
        self.options = []
        self.in_menu = False


    def menu(self, clicked_circle, grid):
        """
        This method shows all options for the item and
        temporary disables the other items on the same positions.
        :param grid:
        :return:
        """
        # TODO: Backup and restore items under options
        # TODO: Set all options position correctly
        # TODO: Show backgourd menu
        if clicked_circle == self.pos:
            if self.in_menu == False:
                self.in_menu = True
            else:
                self.in_menu = False
        else:
            self.in_menu = False

        for option in self.options:
            if self.in_menu:
                # TODO: set all options position correctly
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

    def gen_move_track(self, Point_B):
        """
        This method moves the item from the current position to Point_B.
        :param Point_B: coordinates of destination point B (x, y)
        :param SPEED: pixels moved for each step
        :return: a list of steps from point A to point B
        """
        self.move_track = []
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
        if self.move_track:
            self.pos = self.move_track[0]
            self.move_track.pop(0)


