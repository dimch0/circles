# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                    SCOUT                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
from circle_body import Body
import grid_util as cu


class Scout(Body):

    def __init__(self):
        super(Scout, self).__init__()
        self.target = None

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

    def nearest_item(self, grid, itype):
        result = None
        for circle in grid.circles:
            if itype in circle.type:
                if not result:
                    result = circle
                else:
                    if cu.dist_between(result.pos, self.pos) > cu.dist_between(circle.pos, self.pos):
                        result = circle
        return result

    def most_far_exit(self, grid):
        result = None
        for tile in grid.door_slots:
            if not result:
                result = tile
            else:
                if cu.dist_between(result, self.pos) < cu.dist_between(tile, self.pos):
                    result = tile
        return result

    def most_far_circle(self, grid, fear_name):
        result = None
        try:
            fear_cir = [circle for circle in grid.circles if circle.name == fear_name][0]
        except:
            fear_cir = None
        if fear_cir:
            for tile in grid.revealed_tiles.keys():
                if tile in grid.playing_tiles:
                    if not result:
                        result = tile
                    else:
                        if cu.dist_between(result, fear_cir.pos) < cu.dist_between(tile, fear_cir.pos):
                            result = tile
        return result

    def chase_pos(self, grid, search_circle):
        result = None
        for circle in grid.circles:
            if search_circle in circle.name:
                result = circle.pos
        return result

    def action(self, grid):

        # Check for legal tiles to move
        legal_moves= {}
        for idx, adj_tile in enumerate(grid.adj_tiles(self.pos)):
            if adj_tile in grid.playing_tiles and adj_tile not in grid.occupado_tiles.values():
                legal_moves[adj_tile] = idx

        # Move
        if legal_moves:

            if "#fear" in self.effects:
                self.target = self.most_far_circle(grid, "my_body")
            # Get target
            # target = self.nearest_unrevealed(grid)
            # target = self.chase_pos(grid, "my_body")
            if self.target:
                target = self.target
                if "#traffic" in self.effects:
                    if self.target in grid.adj_tiles(self.pos):
                        self.destroy(grid)
            else:
                target = None

                if self.hungry:
                    target = self.nearest_item(grid, itype='food')
                    if target:
                        if target.pos in grid.adj_tiles(self.pos):
                            grid.event_effects.consume(consumable=target,
                                                       consumator=self)
                        target = target.pos
                    else:
                        target = self.chase_pos(grid, "my_body")
                elif "#traffic" in self.effects:
                    if self.target in grid.adj_tiles(self.pos):
                        self.destroy(grid)
                    if not self.target:
                        self.target = self.most_far_exit(grid)

            # Choose nearest legal
            if target and target not in grid.adj_tiles(self.pos):
                best_legal = None
                for move_tile, move_idx in legal_moves.items():
                    if not best_legal:
                        best_legal = move_tile
                    elif cu.dist_between(best_legal, target) > cu.dist_between(move_tile, target):
                        best_legal = move_tile
                if cu.dist_between(self.pos, target) > cu.dist_between(best_legal, target):
                    self.direction = legal_moves[best_legal]
                    self.gen_move_track(grid)
                    self.direction = None
