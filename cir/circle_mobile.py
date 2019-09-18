# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                   MOBILE                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
from circle import Circle


class Mobile(Circle):
    """
    A class for all circles that move
    """
    def __init__(self):
        super(Mobile, self).__init__()
        self.speed = 1
        self.target_tile = None

    def change_speed(self, modifier):
        pass

    # TODO: PATHFINDING

    def move(self, grid):
        """
        Generates move track for the next step
        """
        if self.target_tile:
            self.pos = self.target_tile
        if self.pos == self.target_tile:
            self.target_tile = None