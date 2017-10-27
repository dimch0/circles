# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                     ITEM                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import cir_utils


class Item(object):

    def __init__(self):
        # --------------------------------------------------------------- #
        #                            BASIC                                #
        # --------------------------------------------------------------- #
        self.name = None
        self.type = None
        self.category = None
        self.color = None
        self.img = None
        self.radius = None
        self.pos = ()
        self.default_color = self.color
        self.default_img = self.img
        self.default_radius = self.radius
        self._rect = []
        self.border = 0
        self.border_color = None
        self.border_width = None
        self.layer = None
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
        self.options = {}
        self.effects = None
        # --------------------------------------------------------------- #
        #                              STATS                              #
        # --------------------------------------------------------------- #
        self.lifespan = None
        self.time_color = None
        self.room = None
        self.uses = 1
        self.marked_for_destruction = False
        # --------------------------------------------------------------- #
        #                            ANIMATION                            #
        # --------------------------------------------------------------- #
        self.direction = None
        self.move_track = []
        self.vibe_track = []
        self.birth_track = []
        self.fat_track = []
        self.effect_track = []
        self.hit_items = []
        self.hit_tiles = []
        # OBSERVER
        self.nearest_untile = None

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

    def gen_effect_track(self, effect_color):
        if not self.effect_track:
            for n in range(1, self.radius + 1):
                eff_cir = {
                    "color": effect_color,
                    "radius": n}
                self.effect_track.append(eff_cir)

        result = []
        for n in range(1, self.radius + 1):
            eff_cir = {
                "color": effect_color,
                "radius": n}
            result.append(eff_cir)
        self.effect_track = result

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
                    # elif item.mode and (self.category in item.mode):
                    #     ober_item = item
        if ober_item:
            grid.msg("INFO - Option belongs to {0}".format(ober_item.name))
        else:
            grid.msg("INFO - No ober item found for {0}".format(self.name))
        return ober_item


    # --------------------------------------------------------------- #
    #                                                                 #
    #                           ITEM MENU                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    def open_menu(self, grid):
        if not self.vibe_track:
            grid.msg("INFO - Open menu {0}".format(self.name))
            grid.clean_mouse()
            # self.mode = None
            self.in_menu = True
            olap_pos = []

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

        grid.msg("INFO - Close menu {0}".format(self.name))
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

    # --------------------------------------------------------------- #
    #                                                                 #
    #                           INTERSECTS                            #
    #                                                                 #
    # --------------------------------------------------------------- #
    def intersects(self, intersecting_item):
        """ Checks and returns a bool if this item is intersecting with intersecting_item """
        cir1 = (self.pos, self.radius)
        cir2 = (intersecting_item.pos, intersecting_item.radius)
        return cir_utils.intersecting(cir1, cir2)

    # --------------------------------------------------------------- #
    #                                                                 #
    #                             DESTROY                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    def destroy(self, grid):

        self.marked_for_destruction = True

        if self in grid.items and not self.birth_track:
            if self.in_menu:
                self.close_menu(grid)
            if hasattr(self, "lifespan"):
                self.lifespan = None
            if hasattr(self, "vfreq"):
                self.vfreq = None
            if hasattr(self, "move_track"):
                self.move_track = []
            if self.type not in ["trigger"]:
                self.gen_birth_track()
                self.birth_track.reverse()
