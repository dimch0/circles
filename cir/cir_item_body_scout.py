# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                    SCOUT                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
from cir_item_body import BodyItem
import cir_utils as cu


class Scout(BodyItem):

    def __init__(self):
        super(Scout, self).__init__()
        self.nearest_untile = None

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
        # FUN
        # self.speed = 5
        # self.vfreq.duration = 0.1
        # self.vspeed = 3
        # self.lifespan.duration = 5

        # Check for legal tiles to move
        legal_moves= {}
        for idx, adj_tile in enumerate(grid.adj_tiles(self.pos)):
            if adj_tile in grid.playing_tiles and adj_tile not in grid.occupado_tiles.values():
                legal_moves[adj_tile] = idx

        # Move
        if legal_moves:

            # Get target
            # target = self.nearest_unrevealed(grid)
            target = self.chase_pos(grid, "my_body")

            # Choose nearest legal
            if target and target not in grid.adj_tiles(self.pos):
                best_legal = None
                for move_tile, move_idx in legal_moves.items():
                    if not best_legal:
                        best_legal = move_tile
                    elif cu.dist_between(best_legal, target) > cu.dist_between(move_tile, target):
                        best_legal = move_tile

                self.direction = legal_moves[best_legal]
