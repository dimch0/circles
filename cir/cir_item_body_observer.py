# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                   OBSERVER                                                          #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import random
from cir_item_body import BodyItem
import cir_utils as cu


class Observer(BodyItem):

    def __init__(self):
        super(Observer, self).__init__()

    def action(self, grid):
        # TEST
        self.speed = 10
        self.vspeed = 5
        self.vfreq.duration = 0.3

        # OBSERVER
        if len(self.vibe_track) == 1:

            # Check for legal tiles to move
            legal_moves = []
            for self_adj in grid.adj_tiles(self.pos):
                if self_adj in grid.playing_tiles and self_adj not in grid.occupado_tiles.values():
                    legal_moves.append(self_adj)

            print legal_moves
            # Move
            if legal_moves:

                # Check if nearest is revealed
                if self.nearest_untile in grid.revealed_tiles:
                    self.nearest_untile = None

                # Get new nearest unrevealed tile
                if not self.nearest_untile:
                    for untile in grid.playing_tiles:
                        if untile not in grid.revealed_tiles:
                            if untile not in grid.door_slots:

                                if not self.nearest_untile:
                                    self.nearest_untile = untile
                                    if grid.pos_to_name(untile) == '14_8':
                                        print "AIDE 1"
                                else:
                                    if cu.dist_between(self.nearest_untile, self.pos) > cu.dist_between(untile, self.pos):
                                        self.nearest_untile = untile
                                        if grid.pos_to_name(untile) == '14_8':
                                            print "AIDE 2", untile not in grid.revealed_tiles

                # Choose nearest legal
                if self.nearest_untile:
                    best_legal = None
                    for move_tile in legal_moves:
                        if not best_legal:
                            best_legal = move_tile
                        else:
                            if cu.dist_between(best_legal, self.nearest_untile) > cu.dist_between(move_tile, self.nearest_untile):
                                self.nearest_untile = move_tile
                    if best_legal:
                        move_to_tile = best_legal
                        print "best_legal", grid.pos_to_name(best_legal), grid.pos_to_name(self.nearest_untile)
                    else:
                        move_to_tile = random.choice(legal_moves)
                else:
                    move_to_tile = random.choice(legal_moves)

                self.move_track = self.move_to_tile(grid, move_to_tile)

            # If no legal moves - vibe like crazy
            if self.vfreq:
                self.vfreq.restart()