#######################################################################################################################
#################                                                                                     #################
#################                           Item class, MobileItem class                              #################
#################                                                                                     #################
#######################################################################################################################


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
        # self.uncolor = uncolor
        self.img = image
        self.border = border
        self.options = []
        self.default_color = self.color
        self.default_img = self.img
        self.default_options = []
        self.in_menu = False
        self.available = True
        self.mode = self.name

        self.move_track = []
        self.radar_track = []

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
        # if option.uncolor:
        #     self.uncolor = option.uncolor
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

    def set_in_menu(self, FLAG):
        """ Setting the in_menu attribute
        :param FLAG: boolean -True or False
        """
        if FLAG:
            self.in_menu = True
        else:
            self.in_menu = False
        self.overlap()
        return self.in_menu

    def check_in_menu(self, clicked_circle, mode_vs_options):
        # Clicked on item
        if clicked_circle == self.pos and self.name in mode_vs_options.keys():
            # If default mode:
            if self.mode is self.name:
                if not self.in_menu:
                    self.set_in_menu(True)
                elif self.in_menu:
                    self.set_in_menu(False)
            # If not default mode
            elif self.mode is not self.name:
                if self.in_menu:
                    self.reset_mode()
                elif not self.in_menu:
                    self.set_in_menu(True)
        # Clicked outside
        elif clicked_circle is not self.pos and clicked_circle not in self.grid.adj_tiles(self.pos):
            self.set_in_menu(False)

