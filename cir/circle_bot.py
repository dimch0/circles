# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                    SCOUT                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
from circle_body import Body
import grid_util as cu


class Bot(Body):

    def __init__(self):
        super(Bot, self).__init__()
        self.target = None
        self.muscle = 2

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

    def farthest_exit(self, grid):
        result = None
        for tile in grid.door_slots:
            if not result:
                result = tile
            else:
                if cu.dist_between(result, self.pos) < cu.dist_between(tile, self.pos):
                    result = tile
        return result

    def farthest_circle(self, grid, fear_name):
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
        print "in action"
        legal_moves= self.get_legal_moves(grid)

        # Move
        if legal_moves:

            if "#fear" in self.effects:
                self.target = self.farthest_circle(grid, "mybody")
            elif "#inlove" in self.effects:
                self.target = self.chase_pos(grid, "mybody")
            # Get target
            # target = self.nearest_unrevealed(grid)
            # target = self.chase_pos(grid, "mybody")
            if self.target:
                target = self.target
                if "#traffic" in self.effects:
                    if self.target in grid.adj_tiles(self.pos):
                        self.destroy(grid)
            else:
                target = None

                if self.hungry or "#inlove" in self.effects:
                    target = self.nearest_item(grid, itype='food')
                    if target:
                        if target.pos in grid.adj_tiles(self.pos):
                            grid.event_effects.consume(consumable=target,
                                                       consumer=self)
                        target = target.pos
                    else:
                        target = self.chase_pos(grid, "mybody")
                elif "#traffic" in self.effects:
                    if self.target in grid.adj_tiles(self.pos):
                        self.destroy(grid)
                    if not self.target:
                        self.target = self.farthest_exit(grid)

            if target and target not in grid.adj_tiles(self.pos):
                self.target_tile = target
