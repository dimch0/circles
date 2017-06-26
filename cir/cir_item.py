#######################################################################################################################
#################                                                                                     #################
#################                           Item class, MobileItem class                              #################
#################                                                                                     #################
#######################################################################################################################
import pdb

class Item(object):
    """
    This is the base class for all CIR items
    It includes the open_menu method.
    """
    def __init__(self, name, pos=(), color=None, uncolor=None, image=None, border=0, modable=False):
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
        self.modable = modable
        self.mode = self.name

        self.overlap = []
        self.rot_track = []
        self.rot_revert = []


    def rotate_img(self, pygame, angle):
        # Rotating image
        orig_rect = self.default_img.get_rect()

        rot_image = pygame.transform.rotate(self.default_img, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        self.img = rot_image


    def rotate_revert_img(self, pygame, start_angle, angle):
        # Rotating image
        self.rotate_img(pygame, start_angle)
        orig_rect = self.img.get_rect()

        rot_image = pygame.transform.rotate(self.img, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        self.img = rot_image


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
        # if option.uncolor:
        #     self.uncolor = option.uncolor
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

    def set_in_menu(self, grid, FLAG):
        """ Setting the in_menu attribute
        :param FLAG: boolean -True or False
        """
        if FLAG:
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

