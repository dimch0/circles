# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                    SCOUT                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import random
from cir_item_body import BodyItem
import cir_utils as cu


class Scout(BodyItem):

    def __init__(self):
        super(Scout, self).__init__()
        self.nearest_untile = None
        self.in_action = False


    def nearest_unrevealed(self, grid):
        result = None
        for playing_tile in grid.playing_tiles:
            if playing_tile not in grid.revealed_tiles.keys() and playing_tile not in grid.door_slots:
                if not result:
                    result = playing_tile
                else:
                    if cu.dist_between(result, self.pos) > cu.dist_between(playing_tile, self.pos):
                        result = playing_tile
        return result


    def chase_pos(self, grid, search_item):
        result = None
        for item in grid.items:
            if search_item in item.name:
                result = item.pos
        return result


    def action(self, grid):

        # Check for legal tiles to move
        legal_moves = []
        for self_adj in grid.adj_tiles(self.pos):
            if self_adj in grid.playing_tiles and self_adj not in grid.occupado_tiles.values():
                legal_moves.append(self_adj)

        # Move
        if legal_moves:

            # Get new nearest unrevealed tile
            target = self.nearest_unrevealed(grid)

            # Get position of my body
            # target = self.chase_pos(grid, "my_body")

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
