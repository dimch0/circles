#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                                 BodyItem class                                      #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################
from cir_item_mobile import MobileItem
from cir_utils import in_circle

class BodyItem(MobileItem):
    """
    This class holds all attributes and metrics of your body
    """
    def __init__(self, range=1, **kwargs):
        super(BodyItem, self).__init__(**kwargs)
        self.range = range
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

    # TODO: Link timer to body

    def gen_radar_track(self, grid):
        """
        :param grid: grid object
        :return: a list of tuples for each radar CIR iteration
        with the radius, thickness:
        (31, 10), (32, 10), (33, 10)
        """
        radar_thickness = range(1, (grid.tile_radius / 3) + 1)
        radar_thickness.reverse()
        radar_limit = (grid.tile_radius * 2 * self.range) + grid.tile_radius + 1
        radar_radius = range(grid.tile_radius , radar_limit)
        radar_delimiter = (radar_radius[-1] - radar_radius[0]) / radar_thickness[0]
        result = []

        for thick in radar_thickness:
            for rad_delim in range(radar_delimiter + 1):
                result.append(thick)

        self.radar_track = zip(radar_radius, result)
        return self.radar_track

    def radar(self, grid):
        """
        :param grid: grid object
        :return: the radius and thickness for each wave
        from the radar_track list and removes after returning it
        Also updates the revealed tiles
        """
        radar_radius, thick = None, None
        if self.radar_track:
            # for track in self.radar_track:
            radar_radius, thick = self.radar_track[0]
            self.radar_track.pop(0)

        # Mark tiles as revealed
        revealed = ((self.pos), radar_radius)
        if not revealed in grid.revealed_radius:
            #if revealed[0] in grid.playing_tiles:
              grid.revealed_radius.append(revealed)

        for tile in grid.tiles:
            if in_circle(self.pos, radar_radius, tile) and tile not in grid.revealed_tiles:
                if not tile in grid.revealed_tiles:
                    if tile in grid.playing_tiles:
                        grid.revealed_tiles.append(tile)

        return radar_radius, thick