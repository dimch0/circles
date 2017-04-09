"""
================================== Item / Body class ==================================
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




class Body(Item):
    """
    This class holds all attributes and metrics of your body
    """
    def __init__(self):
        super(Body, self).__init__(name="my body")
        self.range = 4
        self.speed = 4
        self.muscle = 1
        self.mind = 0
        self.ego = 0
        self.charm = 1
        self.lux = 1
        self.vision = 1
        self.audio = 0
        self.smell = 0
        self.touch = 0
        self.eat = 0
        self.spirit_pool = 100
        self.lifespan = 100
        self.hygiene = 100
        self.stress = 0
        self.status = []
        # TODO Separate menu items generation
        move_option = Item(name="move")
        radar_option = Item(name="radar")
        self.options.append(move_option)
        self.options.append(radar_option)


    def gen_radar_track(self, grid, SCALE):
        """
        :param grid: grid object
        :param SCALE: SCALE size parameter
        :return: a list of tuples for each radar circle iteration
        with the radius, thickness:
        (31, 10), (32, 10), (33, 10)
        """

        radar_thickness = range(1, (10 / SCALE) + 1)
        radar_thickness.reverse()
        radar_limit = (grid.tile_radius * 2 * self.range) + 1 + grid.tile_radius
        radar_radius = range(grid.tile_radius + 1, radar_limit)
        radar_delimiter = (radar_radius[-1] - radar_radius[0]) / radar_thickness[0]
        result = []

        for thick in radar_thickness:
            for rad_delim in range(radar_delimiter + 1):
                result.append(thick)

        self.radar_track = zip(radar_radius, result)
        return self.radar_track

    def radar(self, grid):
        """
        :param grid: grid object
        :return: the radius and thickness for each wave
        from the radar_track list and removes after returning it
        """
        radar_radius, thick = None, None
        if self.radar_track:
            radar_radius, thick = self.radar_track[0]
            self.radar_track.pop(0)

        grid.revealed_radius.append(((self.pos), radar_radius))
        return radar_radius, thick