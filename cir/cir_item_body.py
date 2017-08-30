#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                                 BodyItem class                                      #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################
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
    #                             RADAR                               #
    #                                                                 #
    # --------------------------------------------------------------- #
    def gen_vibe_track(self, grid):
        """
        :param grid: grid object
        :return: a list of tuples for each radar CIR iteration
        with the radius, thickness:
        (31, 10), (32, 10), (33, 10)
        """

        if not self.move_track and not self.vibe_track and not self.birth_track:
            radar_thickness = range(1, (grid.tile_radius / 3) + 1)
            radar_thickness.reverse()
            radar_limit = (grid.tile_radius * 2 * self.range) + grid.tile_radius + 1
            radar_radius = get_list_drange(grid.tile_radius , radar_limit, self.vibe_speed)
            radar_delimiter = (radar_radius[-1] - radar_radius[0]) / radar_thickness[0]
            result = []

            rad_delimiter_list = get_list_drange(1, (radar_delimiter + 1), 1)
            for thick in radar_thickness:
                for rad_delim in rad_delimiter_list:
                    result.append(thick)

            self.vibe_track = zip(radar_radius, result)
            self.gen_fat()
        return self.vibe_track

    def radar(self, grid):
        """
        :param grid: grid object
        :return: the radius and thickness for each wave
        from the vibe_track list and removes after returning it
        Also updates the revealed tiles
        """
        radar_radius, thick = None, None
        if self.vibe_track:
            radar_radius, thick = self.vibe_track[0]
            self.vibe_track.pop(0)

        # Mark tiles as revealed
        revealed = ((self.pos), radar_radius)
        if not revealed in grid.revealed_radius:
            grid.revealed_radius.append(revealed)

        # Set revealed tiles and items
        grid.set_rev_tiles()
        for item in grid.items:
            if item.pos in grid.revealed_tiles:
                if not item.available and not item in grid.overlap:
                    item.available = True
                    item.gen_birth_track()

        return radar_radius, thick
