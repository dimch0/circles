# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                   OBSERVER                                                          #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import random
from cir_item_body import BodyItem
import cir_utils as cu
from cir_item import Item


class Observer(BodyItem):

    def __init__(self):
        super(Observer, self).__init__()
        self.nearest_untile = None
        self.in_action = False

    def find_nearest(self, grid):
        nearest_untile = None
        for untile in grid.playing_tiles:
            if untile not in grid.revealed_tiles.keys() and untile not in grid.door_slots:
                if not nearest_untile:
                    nearest_untile = untile
                else:
                    if cu.dist_between(nearest_untile, self.pos) > cu.dist_between(untile, self.pos):
                        nearest_untile = untile
        return nearest_untile


    #     self.in_action = True
    #     # TEST
    #     self.speed = 10
    #     self.vspeed = 5
    #     self.vfreq.duration = 0.3
    #

    #         # Get new nearest unrevealed tile
    #         if not self.nearest_untile:
    #             self.nearest_untile = self.find_nearest(grid)
    #             foo = Item()
    #             foo.name = 'hui'
    #             foo.color = grid.white
    #             foo.available = True
    #             foo.pos = self.nearest_untile
    #             foo.radius = 5
    #             foo.type = 'triggerw'
    #             grid.items.append(foo)




    # CHASER
    def search_pos(self, grid, search_item):
        result = None
        for item in grid.items:
            if search_item in item.name:
                result = item.pos
        return result


    def action(self, grid):
        # TEST
        self.speed = 2

        # Check for legal tiles to move
        legal_moves = []
        for self_adj in grid.adj_tiles(self.pos):
            if self_adj in grid.playing_tiles and self_adj not in grid.occupado_tiles.values():
                legal_moves.append(self_adj)

        # Move
        if legal_moves:
            # Get new nearest unrevealed tile
            target = self.search_pos(grid, "my_body")

            # Choose nearest legal
            if target and target not in grid.adj_tiles(self.pos):
                best_legal = None
                for move_tile in legal_moves:
                    if not best_legal:
                        best_legal = move_tile
                    else:
                        if cu.dist_between(best_legal, target) > cu.dist_between(move_tile, target):
                            best_legal = move_tile

                self.move_track = self.move_to_tile(grid, best_legal)
