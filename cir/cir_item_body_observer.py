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


    def action(self, grid):
        self.in_action = True
        # TEST
        self.speed = 10
        self.vspeed = 5
        self.vfreq.duration = 0.3

        # import pdb; pdb.set_trace()



        # Check for legal tiles to move
        legal_moves = []
        for self_adj in grid.adj_tiles(self.pos):
            if self_adj in grid.playing_tiles and self_adj not in grid.occupado_tiles.values():
                legal_moves.append(self_adj)

        # Move
        if legal_moves:

            # Get new nearest unrevealed tile
            if not self.nearest_untile:
                self.nearest_untile = self.find_nearest(grid)
                foo = Item()
                foo.name = 'hui'
                foo.color = grid.white
                foo.available = True
                foo.pos = self.nearest_untile
                foo.radius = 5
                foo.type = 'triggerw'
                grid.items.append(foo)


            print "new newarest", self.nearest_untile

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
                    # print "best_legal", grid.pos_to_name(best_legal), grid.pos_to_name(self.nearest_untile)
                else:
                    move_to_tile = random.choice(legal_moves)
            else:
                move_to_tile = random.choice(legal_moves)

            self.move_track = self.move_to_tile(grid, move_to_tile)

        self.in_action = False        # Check if nearest is revealed
        if self.nearest_untile in grid.revealed_tiles.keys():
            print "Clear untile"
            self.nearest_untile = None

        # print grid.names_to_pos('14_8')
        # print grid.names_to_pos('14_8') not in grid.revealed_tiles.keys()
        # print grid.revealed_tiles.keys()

            # If no legal moves - vibe like crazy
            # if self.vfreq:
            #
            #     self.vfreq.restart()