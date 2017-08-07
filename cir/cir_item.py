#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                           Item class, MobileItem class                              #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################
import cir_utils


class Item(object):
    """
    This is the base class for all CIR items
    It includes the open_menu method.
    """
    def __init__(self):
        # --------------------------------------------------------------- #
        #                            BASICS                               #
        # --------------------------------------------------------------- #
        self.name = None
        self.type = None
        self.pos = ()
        self.color = None
        self.img = None
        self.radius = None
        self.default_radius = self.radius
        self._rect = []
        self.border = 0
        self.border_color = None
        self.border_width = None
        self.default_color = self.color
        self.default_img = self.img
        # --------------------------------------------------------------- #
        #                            OPTIONS                              #
        # --------------------------------------------------------------- #
        self.in_menu = False
        self.modable = False
        self.available = True
        self.clickable = True
        self.collectible = False
        self.mode = self.name
        self.options = []
        self.default_options = []
        self.overlap = []
        # --------------------------------------------------------------- #
        #                              STATS                              #
        # --------------------------------------------------------------- #
        self.lifespan = None
        self.time_color = None
        self.room = None
        self.uses = 1
        # --------------------------------------------------------------- #
        #                            ANIMATION                            #
        # --------------------------------------------------------------- #
        self.direction = None
        self.last_rotation = None
        self.birth_time = 0.033
        self.move_track = []
        self.radar_track = []
        self.rot_track = []
        self.rot_revert = []
        self.birth_track = []
        self.fat_track = []
        self.marked_for_destruction = False


    @property
    def rect(self):
        """ This defines the rect argument for the arch drawing """
        if self.radius and self.pos:
            self._rect = [self.pos[0] - self.radius,
                          self.pos[1] - self.radius,
                          2 * self.radius,
                          2 * self.radius]
        else:
            self._rect = []
        return self._rect

    # --------------------------------------------------------------- #
    #                                                                 #
    #                           ROTATION                              #
    #                                                                 #
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
                    self.rot_revert = range(-step, -end_point * 3, -step)
                else:
                    self.rot_revert = cir_utils.negative_list(self.rot_track)

    def gen_birth_track(self):
        self.birth_track = range(1, self.radius)


    def gen_fat(self):
        if not self.fat_track:
            result = []
            reverse_result = []
            for fat in range(self.radius / 4):
                result.append(self.radius + fat)
                reverse_result.append(self.radius + fat)

            reverse_result.reverse()
            final_result = result + reverse_result
            final_result.append(self.default_radius)
            self.fat_track = final_result

    def rotate(self, pygame):
        """ Rotates the image """
        self.img = cir_utils.rot_center(pygame, self.default_img, self.rot_track[0])

        if len(self.rot_track) == 1:
            self.last_rotation = self.rot_track[-1]
        self.rot_track.pop(0)

    def rotate_reverse(self, pygame):
        """ Returns the image to start position """
        if self.last_rotation:
            self.img = cir_utils.rot_center(pygame, self.default_img, self.last_rotation)

        if self.rot_revert:
            self.img = cir_utils.rot_center(pygame, self.img, self.rot_revert[0])
            self.rot_revert.pop(0)

        elif not self.rot_revert:
            self.img = self.default_img
            self.last_rotation = False

    # --------------------------------------------------------------- #
    #                                                                 #
    #                          MODE OPTIONS                           #
    #                                                                 #
    # --------------------------------------------------------------- #
    def set_option_pos(self, grid):
        # Returning the options only
        for idx, option in enumerate(self.options):
            if self.in_menu:
                option.pos = grid.adj_tiles(self.pos)[idx]

    def set_mode(self, grid, option):
        """
        Changes the mode of an item to a given options
        :param option: an option item of a menu
        :param grid: grid instance
        """
        self.mode = option.name
        self.color = option.color
        # self.img = option.img
        if option.name in grid.mode_vs_options.keys():
            self.options = grid.mode_vs_options[option.name]
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
    #                                                                 #
    #                           ITEM MENU                             #
    #                                                                 #
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

    def check_in_menu(self, grid, clicked_circle):
        """
        On a clicked circle - check if this item is in menu and set it
        :param grid: grid instance
        :param clicked_circle: the current clicekd circle
        """

        # Clicked on item
        if clicked_circle == self.pos and self.name in grid.mode_vs_options.keys() and self.clickable and not (self.name != "my_body" and grid.mouse_mode):
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
        elif (clicked_circle != self.pos) and (clicked_circle not in grid.adj_tiles(self.pos)) and self.clickable:
            self.set_in_menu(grid, False)


    # --------------------------------------------------------------- #
    #                                                                 #
    #                            OVERLAP                              #
    #                                                                 #
    # --------------------------------------------------------------- #
    def overlapping(self, grid):
        """
        Checks for overlapping items
        if in menu: creates a archive in self.overlap
        if not in menu: restores from self.overlap
        """
        if self.in_menu:
            for olapped_item in grid.items:
                for option in self.options:
                    if olapped_item.pos == option.pos and olapped_item.available:
                        if not olapped_item in self.overlap:
                            self.overlap.append(olapped_item)
                            grid.overlapped.append(olapped_item)
                            olapped_item.clickable = False
        else:
            if self.overlap:
                for item in self.overlap:
                    item.clickable = True
                    self.overlap.remove(item)
                    if item in grid.overlapped:
                        grid.overlapped.remove(item)


    def intersects(self, item2):
        """ Checks and returns a bool if this item is intersecting with item2 """
        cir1 = (self.pos, self.radius)
        cir2 = (item2.pos, item2.radius)
        return cir_utils.intersecting(cir1, cir2)
