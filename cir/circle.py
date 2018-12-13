# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                     ITEM                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import grid_util


class BasicCircle(object):
    """
    Basic geometry circle class
    """
    def __init__(self):
        self.pos = () # x, y coordinates tuple
        self.radius = None
        self.color = None
        self._rect = []
        self.border = 0
        self.border_color = None
        self.border_width = None

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


class Circle(BasicCircle):
    """
    In game circle class
    """
    def __init__(self):
        super(Circle, self).__init__()
        self.name = None
        self.img = None
        self.type = None
        self.layer = None
        self.available = False
        self.marked_for_destruction = False
        self.lvl = None
        # --------------------------------------------------------------- #
        #                            OPTIONS                              #
        # --------------------------------------------------------------- #
        self.effects = None # TODO: Create list for bot behaviour
        self.modable = False # TODO: Create new class but keep here default
        self.collectible = False # TODO: Create new class but keep here default
        self.consumable = False # TODO: Create new class but keep here default
        # --------------------------------------------------------------- #
        #                            ANIMATION                            #
        # --------------------------------------------------------------- #
        self.vibe_track = {'center': '', 'track':[]}
        self.birth_track = []
        self.effect_track = []
        self.hit_circles = []
        self.hit_tiles = []

    def gen_birth_track(self):
        self.birth_track = range(1, self.radius + 1)

    def gen_effect_track(self, effect_color):
        # TODO:
        pass

    def intersects(self, intersecting_item):
        """ Checks and returns a bool if this item is intersecting with intersecting_item """
        cir1 = (self.pos, self.radius)
        cir2 = (intersecting_item.pos, intersecting_item.radius)
        return grid_util.intersecting(cir1, cir2)

    def destroy(self, grid):
        if hasattr(self, 'home'):
            # TODO: move restart to home parent item
            pass
        if self.name in ['mybody']:
            grid.msg("SCREEN - you dead")
        self.marked_for_destruction = True
        all_circles = grid.circles + grid.panel_circles.values()
        if self in all_circles and not self.birth_track:
            if hasattr(self, "move_track"):
                self.move_track = []
            if self.color:
                self.gen_birth_track()
                self.birth_track.reverse()
