# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                   MOBILE                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
from circle import Circle
import grid_util


class Panel(Circle):
    """
    This is the base class for all mobile cirlces
    """
    def __init__(self):
        super(Panel, self).__init__()
        self.options = {}
    # --------------------------------------------------------------- #
    #                                                                 #
    #                           ITEM MENU                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    def open_menu(self, grid):

        option_positions = []
        for n in range(1,7):
            new_pos = (self.pos[0], self.pos[1] + (n * grid.tile_radius * 2))
            option_positions.append(new_pos)

        for idx, option in enumerate(self.options.values()):
            option.pos = option_positions[idx]
            if option not in grid.panel_circles.values():
                grid.panel_circles[option.name] = option



