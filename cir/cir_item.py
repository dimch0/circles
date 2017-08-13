#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                           Item class, MobileItem class                              #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################
import cir_utils


class Item(object):

    def __init__(self):
        # --------------------------------------------------------------- #
        #                            BASICS                               #
        # --------------------------------------------------------------- #
        self.name = None
        self.type = None
        self.category = None
        self.pos = ()
        self.color = None
        self.default_color = self.color
        self.img = None
        self.default_img = self.img
        self.radius = None
        self.default_radius = self.radius
        self._rect = []
        self.border = 0
        self.border_color = None
        self.border_width = None
        # --------------------------------------------------------------- #
        #                            OPTIONS                              #
        # --------------------------------------------------------------- #
        self.has_opts = False
        self.in_menu = False
        self.modable = False
        self.mode = self.name
        self.options = []
        self.default_options = []
        self.overlap = []

        self.available = True
        self.clickable = True
        self.collectible = False
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

    # --------------------------------------------------------------- #
    #                                                                 #
    #                          MODE OPTIONS                           #
    #                                                                 #
    # --------------------------------------------------------------- #
    def get_ober_item(self, grid):
        ober_item = None
        if self.type == "option":
            for item in grid.items:
                if not ober_item:
                    if self.category in item.name:
                        ober_item = item

                    elif item.mode and (self.category in item.mode):
                        ober_item = item
        if ober_item:
            print("Option belongs to {0}".format(ober_item.name))
        else:
            print("No ober item found for {0}".format(self.name))
        return ober_item




    def open_menu(self, grid):

        # SUB-OPTION
        ober_item = self.get_ober_item(grid)
        if ober_item:
            ober_item.close_menu(grid)
            ober_item.options = self.options
            ober_item.open_menu(grid)
            ober_item.mode = self.name
        else:
            for idx, option in enumerate(self.options):
                option.pos = grid.adj_tiles(self.pos)[idx]
                if option not in grid.items:
                    grid.items.append(option)
        self.in_menu = True

            # for overlap_item in grid.items:
            #     if option.pos == overlap_item.pos:
            #         overlap_item.clickable = False
            #         if not overlap_item in grid.overlapped:
            #             grid.overlapped.append(overlap_item)


    def close_menu(self, grid):
        print("Closing menu {0}".format(self.name))
        for option in self.options:
            if option in grid.items:
                grid.items.remove(option)
        # for overlap_item in grid.overlapped:
        #     overlap_item.clickable = True
        #     if overlap_item in grid.overlapped:
        #         grid.overlapped.remove(overlap_item)
        self.in_menu = False


    def revert_menu(self, grid):
        self.close_menu(grid)
        self.options = self.default_options
        self.open_menu(grid)
        self.mode = None


    def set_mode(self, grid, option):
        """
        Changes the mode of an item to a given options
        :param option: an option item of a menu
        :param grid: grid instance
        """
        self.mode = option.name
        # if option.options:
        #     self.options = option.options

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
    # def check_in_menu(self, grid, clicked_circle):
    #     """
    #     On a clicked circle - check if this item is in menu and set it
    #     :param grid: grid instance
    #     :param clicked_circle: the current clicekd circle
    #     """
    #
    #     # Clicked on item
    #     if self.clickable and self.available and self.options\
    #             and not (self.name != "my_body" and grid.mouse_mode):
    #
    #         # If default mode:
    #         if self.mode is self.name:
    #             if not self.in_menu:
    #                 self.in_menu = True
    #             elif self.in_menu:
    #                 self.in_menu = False
    #
    #         # If not default mode
    #         elif self.mode is not self.name:
    #             if self.in_menu:
    #                 self.reset_mode()
    #             elif not self.in_menu:
    #                 self.in_menu = True
    #
    #     # Clicked outside
    #     elif (clicked_circle != self.pos) and (clicked_circle not in grid.adj_tiles(self.pos)) and self.clickable:
    #         self.in_menu = False


    # --------------------------------------------------------------- #
    #                                                                 #
    #                            OVERLAP                              #
    #                                                                 #
    # --------------------------------------------------------------- #
    # def overlapping(self, grid):
    #     """
    #     Checks for overlapping items
    #     if in menu: creates a archive in self.overlap
    #     if not in menu: restores from self.overlap
    #     """
    #     if self.in_menu:
    #         for olapped_item in grid.items:
    #             for option in self.options:
    #                 if olapped_item.pos == option.pos and olapped_item.available:
    #                     if not olapped_item in self.overlap:
    #                         self.overlap.append(olapped_item)
    #                         grid.overlapped.append(olapped_item)
    #                         olapped_item.clickable = False
    #     else:
    #         for opt in self.options:
    #             if opt in grid.items:
    #                 grid.items.remove(opt)
    #         if self.overlap:
    #             for item in self.overlap:
    #                 item.clickable = True
    #                 self.overlap.remove(item)
    #                 if item in grid.overlapped:
    #                     grid.overlapped.remove(item)

    # --------------------------------------------------------------- #
    #                                                                 #
    #                           INTERSECTS                            #
    #                                                                 #
    # --------------------------------------------------------------- #
    def intersects(self, item2):
        """ Checks and returns a bool if this item is intersecting with item2 """
        cir1 = (self.pos, self.radius)
        cir2 = (item2.pos, item2.radius)
        return cir_utils.intersecting(cir1, cir2)


    # --------------------------------------------------------------- #
    #                                                                 #
    #                             DESTROY                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    def destroy(self, grid):
        if self in grid.items and not self.birth_track:
            if hasattr(self, "lifespan"):
                self.lifespan = None
            if hasattr(self, "vibe_freq"):
                self.vibe_freq = None
            self.in_menu = False
            if hasattr(self, "move_track"):
                self.move_track = []
            self.gen_birth_track()
            self.birth_track.reverse()
            self.marked_for_destruction = True
