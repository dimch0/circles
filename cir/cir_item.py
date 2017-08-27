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
        self.available = True
        self.clickable = True
        self.collectible = False
        self.consumable = False
        self.mode = self.name
        self.options = {}
        self.default_options = {}
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


    def gen_birth_track(self):
        if self.type == "signal":
            self.birth_track = range(1, self.radius)
        else:
            self.birth_track = range(1, self.radius + 1)


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
            print("INFO: Option belongs to {0}".format(ober_item.name))
        else:
            print("INFO: No ober item found for {0}".format(self.name))
        return ober_item


    # --------------------------------------------------------------- #
    #                                                                 #
    #                           ITEM MENU                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    def open_menu(self, grid):

        self.in_menu = True
        print("INFO: Open menu {0}".format(self.name))
        olap_pos = []

        # SUB-OPTION
        ober_item = self.get_ober_item(grid)
        if ober_item:
            ober_item.close_menu(grid)
            ober_item.options = self.options
            ober_item.open_menu(grid)
            ober_item.mode = self.name

        # NORMAL OPTIONS
        else:
            for idx, option in enumerate(self.options.values()):
                option.pos = grid.adj_tiles(self.pos)[idx]
                olap_pos.append(option.pos)
                if option not in grid.items:
                    grid.items.append(option)

        # OVERLAP
        if olap_pos:
            for olap_item in grid.items:
                if not olap_item.type in ["option"]:
                    if olap_item.pos in olap_pos:
                        olap_item.clickable = False
                        if not olap_item in grid.overlap:
                            grid.overlap.append(olap_item)


    def close_menu(self, grid):

        print("INFO: Close menu {0}".format(self.name))
        self.in_menu = False

        # REMOVE OPTIONS
        for option in self.options.values():
            if option in grid.items:
                grid.items.remove(option)
        # OVERLAP
        while grid.overlap:
            for olap_item in grid.overlap:
                olap_item.clickable = True
                if olap_item in grid.overlap:
                    grid.overlap.remove(olap_item)

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
    def destroy(self, grid, fast=False):
        if self in grid.items and not self.birth_track:
            if self.in_menu:
                self.close_menu(grid)
            if hasattr(self, "lifespan"):
                self.lifespan = None
            if hasattr(self, "vibe_freq"):
                self.vibe_freq = None

            if hasattr(self, "move_track"):
                self.move_track = []

            if fast and self.birth_time:
                self.birth_time.duration = 0
            self.gen_birth_track()
            self.birth_track.reverse()
            self.marked_for_destruction = True
