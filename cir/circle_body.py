# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                     BODY                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
from circle_mobile import Mobile
from grid_util import get_list_drange


class Body(Mobile):
    """
    This class holds all attributes and metrics of your body
    """
    def __init__(self):
        super(Body, self).__init__()
        self.hungry = False

        self.range = 1
        # VIBE SPEED CAN NOT BE < 1!
        self.vspeed = 1
        self.vfreq = None
        self.inventory = None
        self.muscle = 1
        self.ego = 0
        self.hyg = 100
        self.joy = 0

        self.loved = 0

        # TIME
        self.time = 0
        self.max_time = 0
        self.time_color = None
    # --------------------------------------------------------------- #
    #                                                                 #
    #                             VIBE                                #
    #                                                                 #
    # --------------------------------------------------------------- #
    def gen_vibe_track(self, grid):
        """
        :param grid: grid object
        :return: a list of tuples for each vibe CIR iteration
        with the radius, thickness:
        (31, 10), (32, 10), (33, 10)
        """

        if not self.move_track and not self.vibe_track['track'] and not self.birth_track:

            vibe_thickness = 1
            vibe_limit = (grid.tile_radius * 2 * self.range) + grid.tile_radius + 1
            vibe_radius = get_list_drange(grid.tile_radius, vibe_limit, self.vspeed)

            track = [(v_radius, vibe_thickness) for v_radius in vibe_radius]
            track.append((vibe_limit, vibe_thickness))

            self.vibe_track = {'center': self.pos,
                               'track': track}
        return self.vibe_track


    def muscle_test(self, hit_circle, grid):
        """
        Compare the muscle attribute
        :return: muscle diff
        """
        if hasattr(hit_circle, 'muscle'):
            amount = self.muscle - hit_circle.muscle
            if amount > 0:
                hit_effects = 't:-%s joy:-1' % amount
                self_effects = 'joy:+1'

            elif amount < 0:
                hit_effects = 'joy:+1'
                self_effects = 't:%s joy:-1' % amount

            else:
                hit_effects = 'joy:-1'
                self_effects = 'joy:-1'

            grid.event_effects.consume(hit_circle, hit_effects)
            grid.event_effects.consume(self, self_effects)


    def love(self, grid, amount):
        # self.color = grid.f35d73
        # self.default_color = grid.f35d73
        self.loved += amount

        if self.loved >= 15:
            self.color = grid.f35d73
            self.default_color = grid.f35d73
            self.effects = self.effects.replace("#fear", "#inlove")
