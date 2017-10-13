# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                     BODY                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
from cir_item_mobile import MobileItem
from cir_utils import get_list_drange


class BodyItem(MobileItem):
    """
    This class holds all attributes and metrics of your body
    """
    def __init__(self):
        super(BodyItem, self).__init__()
        self.range = 1
        # VIBE SPEED CAN NOT BE LESS THAN 1 !!!
        self.vibe_speed = 1
        self.vibe_freq = None
        self.inventory = None
        # self.muscle = 1
        # self.mind = 0
        # self.ego = 0
        # self.charm = 1
        # self.lux = 1
        # self.vision = 1
        # self.audio = 0
        # self.smell = 0
        # self.touch = 0
        # self.eat = 0
        # self.spirit_pool = 100
        # self.lifespan = 100
        # self.hygiene = 100
        # self.stress = 0
        # self.status = []

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

        if not self.move_track and not self.vibe_track and not self.birth_track and not self.in_menu:
            vibe_thickness = range(1, (grid.tile_radius / 3) + 1)
            vibe_thickness.reverse()
            vibe_limit = (grid.tile_radius * 2 * self.range) + grid.tile_radius + 1
            vibe_radius = get_list_drange(grid.tile_radius , vibe_limit, self.vibe_speed)
            vibe_delimiter = (vibe_radius[-1] - vibe_radius[0]) / vibe_thickness[0]
            result = []

            rad_delimiter_list = get_list_drange(1, (vibe_delimiter + 1), 1)
            for thick in vibe_thickness:
                for rad_delim in rad_delimiter_list:
                    result.append(thick)

            self.vibe_track = zip(vibe_radius, result)
            self.gen_fat()
        return self.vibe_track
