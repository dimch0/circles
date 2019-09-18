# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                     BODY                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
from circle_mobile import Mobile
from grid_util import get_list_drange


class Body(Mobile):
    """
    This class holds all attributes and metrics of a body
    """
    def __init__(self):
        super(Body, self).__init__()
        # TIME
        self.time = 0
        self.max_time = 0
        self.set_max_time()
        self.time_color = None
        self.fat = 0

        self.range = 1
        self.vspeed = 4 # VIBE SPEED CAN NOT BE < 1 !!!
        # self.muscle = 1
        # self.ego = 0
        # self.keff = 0
        self.loved = 0

    # --------------------------------------------------------------- #
    #                                                                 #
    #                             TIME                                #
    #                                                                 #
    # --------------------------------------------------------------- #
    def set_max_time(self):
        self.max_time = self.time

    def add_time(self, amount):
        self.time += amount
        if self.time > self.max_time:
            self.fat = self.max_time - self.time
            self.time = self.max_time
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

        if not self.vibe_track['track'] and not self.birth_track:

            vibe_thickness = 1
            vibe_limit = (grid.tile_radius * 2 * self.range) + grid.tile_radius + 1
            vibe_radius = get_list_drange(grid.tile_radius, vibe_limit, self.vspeed)

            track = [(v_radius, vibe_thickness) for v_radius in vibe_radius]
            track.append((vibe_limit, vibe_thickness))

            self.vibe_track = {'center': self.pos,
                               'track': track}
        return self.vibe_track

    # --------------------------------------------------------------- #
    #                                                                 #
    #                             TURN                                #
    #                                                                 #
    # --------------------------------------------------------------- #
    def turn(self, grid):
        """ Timer effects  """

        # TIME
        self.time -= 1

        # DEATH TIME
        if self.time <= 0:
            self.destroy(grid)

        grid.new_turn()
        # grid.drawer.time_vs_max = [self.time, self.max_time]

    # --------------------------------------------------------------- #
    #                                                                 #
    #                             MOVE                                #
    #                                                                 #
    # --------------------------------------------------------------- #
    # TODO: PATHFINDING

    def move(self, grid):
        """
        Generates move track for the next step
        """
        if self.target_tile:
            self.pos = self.target_tile
        if self.pos == self.target_tile:
            self.target_tile = None
        self.turn(grid)

    # --------------------------------------------------------------- #
    #                                                                 #
    #                             OTHER                               #
    #                                                                 #
    # --------------------------------------------------------------- #
    def love(self, grid, amount):
        self.loved += amount

        if self.loved >= 15:
            self.color = grid.f35d73
            self.effects = self.effects.replace("#fear", "#inlove")

    def muscle_test(self, hit_circle, grid):
        """
        Compare the muscle attribute
        :return: muscle diff
        """
        pass