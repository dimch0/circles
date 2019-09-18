class Room(object):
    """ master class for the grid """

    def __init__(self):
        # -------------------------------------------------- #
        #                      HELPERS                       #
        # -------------------------------------------------- #
        self.room_name = None
        self.circles = []
        self.revealed_tiles = {}
