###################################bodies####################################################################################
#################                                                                                     #################
#################                           Item class, MobileItem class                              #################
#################                                                                                     #################
#######################################################################################################################
import cir_utils

class Item(object):
    """
    This is the base class for all CIR items
    It includes the open_menu method.
    """

    def __init__(self, name, pos=(), color=None, uncolor=None, image=None, border=0, modable=False):
        # --------------------------------------------------------------- #
        #                            BASICS                               #
        # --------------------------------------------------------------- #
        self.name = name
        self.pos = pos
        self.color = color
        self.img = image
        self.border = border
        self.default_color = self.color
        self.default_img = self.img
        self.available = True
        # --------------------------------------------------------------- #
        #                            OPTIONS                              #
        # --------------------------------------------------------------- #
        self.in_menu = False
        self.modable = modable
        self.mode = self.name
        self.options = []
        self.default_options = []
        self.overlap = []
        # --------------------------------------------------------------- #
        #                            ANIMATION                            #
        # --------------------------------------------------------------- #
        self.direction = None
        self.last_direction = None
        self.move_track = []
        self.radar_track = []
        self.rot_track = []
        self.rot_revert = []


    # --------------------------------------------------------------- #
    #                           ROTATION                              #
    # --------------------------------------------------------------- #
    def gen_rot_track(self, idx):
        """
        Generates rotating track and revert rotating track
        :param idx:  index of direction
        :param item: item to whom belongs the image
        """
        step = 15
        end_point = step * 4
        track = None
        if idx == 1:
            track = range(-step, -end_point, -step)
        elif idx == 2:
            track = range(-step, -end_point * 2, -step)
        elif idx == 3:
            track = range(-step, -end_point * 3, -step)
        elif idx == 4:
            track = range(step, end_point * 2, step)
        elif idx == 5:
            track = range(step, end_point, step)

        if track:
            self.rot_track = track
            if not self.rot_revert:
                if idx == 3:
                    self.rot_revert = range(-step, -end_point * 2, -step)
                else:
                    self.rot_revert = cir_utils.negative_list(self.rot_track)

    def rotate(self, pygame):
        """ Rotates the image """
        self.img = cir_utils.rot_center(pygame, self.default_img, self.rot_track[0])

        if len(self.rot_track) == 1:
            self.last_direction = self.rot_track[-1]
        self.rot_track.pop(0)

    def rotate_reverse(self, pygame):
        """ Returns the image to start position """
        if self.last_direction:
            self.img = cir_utils.rot_center(pygame, self.default_img, self.last_direction)

        if self.rot_revert:
            self.img = cir_utils.rot_center(pygame, self.img, self.rot_revert[0])
            self.rot_revert.pop(0)

        else:
            self.img = self.default_img
            self.last_direction = False

    # --------------------------------------------------------------- #
    #                          MODE OPTIONS                           #
    # --------------------------------------------------------------- #
    def set_option_pos(self, grid):
        # Returning the options only
        for idx, option in enumerate(self.options):
            if self.in_menu:
                option.pos = grid.adj_tiles(self.pos)[idx]

    def set_mode(self, grid, option, mode_vs_option):
        """
        Changes the mode of an item to a given options
        :param option: an option item of a menu
        :param grid: grid instance
        """
        self.mode = option.name
        self.color = option.color
        # self.img = option.img
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


    # --------------------------------------------------------------- #
    #                           ITEM MENU                             #
    # --------------------------------------------------------------- #
    def set_in_menu(self, grid, value):
        """ Setting the in_menu attribute to value
        :param value: boolean -True or False
        """
        if value:
            self.in_menu = True
        else:
            self.in_menu = False
        return self.in_menu

    def check_in_menu(self, grid, clicked_circle, mode_vs_options):
        """
        On a clicked circle - check if this item is in menu and set it
        :param grid: grid instance
        :param clicked_circle: the current clicekd circle
        :param mode_vs_options: dict of the mode and options for it
        """
        # Clicked on item
        if clicked_circle == self.pos and self.name in mode_vs_options.keys():
            # If default mode:
            if self.mode is self.name:
                if not self.in_menu:
                    self.set_in_menu(grid, True)
                elif self.in_menu:
                    self.set_in_menu(grid, False)
            # If not default mode
            elif self.mode is not self.name:
                if self.in_menu:
                    self.reset_mode()
                elif not self.in_menu:
                    self.set_in_menu(grid, True)
        # Clicked outside
        elif clicked_circle is not self.pos and clicked_circle not in grid.adj_tiles(self.pos):
            self.set_in_menu(grid, False)


    # --------------------------------------------------------------- #
    #                            OVERLAP                              #
    # --------------------------------------------------------------- #
    def overlapping(self, grid):
        """
        Checks for overlapping items
        if in menu: creates a archive in self.overlap
        if not in menu: restores from self.overlap
        """
        if self.in_menu:
            for overlapping_item in grid.items:
                for ajd_tile in grid.adj_tiles(self.pos):
                    if overlapping_item.pos == ajd_tile:
                        if not overlapping_item in self.overlap:
                            self.overlap.append(overlapping_item)
                            overlapping_item.available = False
        else:
            if self.overlap:
                for item in self.overlap:
                    item.available = True
                    self.overlap.remove(item)
