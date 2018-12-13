# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                   MOBILE                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
from circle import Circle
import grid_util


class Mobile(Circle):
    """
    A class for all circles that move
    """
    def __init__(self):
        super(Mobile, self).__init__()
        self.speed = 1
        self.target_tile = None
        self.move_track = []

    def change_speed(self, modifier):
        self.speed += modifier
        if self.speed < 0:
            self.speed = 0

    # --------------------------------------------------------------- #
    #                                                                 #
    #                        GET STEP TILE                            #
    #                                                                 #
    # --------------------------------------------------------------- #
    # TODO: PATHFINDING

    def get_legal_moves(self, grid):
        # Check for legal tiles to move
        legal_moves = {}
        for idx, adj_tile in enumerate(grid.adj_tiles(self.pos)):
            if adj_tile in grid.playing_tiles and adj_tile not in grid.occupado_tiles.values():
                legal_moves[adj_tile] = idx
        return legal_moves

    def get_nearest_step_tile(self, target, grid):
        """
        :param target: target to go to
        :param grid: global grid
        :return: nearest tile to target
        """
        legal_moves = self.get_legal_moves(grid)
        result = None
        # Choose nearest legal
        if legal_moves:
            # if target and target not in grid.adj_tiles(self.pos):
            best_legal = None
            for move_tile in legal_moves.keys():
                if not best_legal:
                    best_legal = move_tile
                elif grid_util.dist_between(best_legal, target) > grid_util.dist_between(move_tile, target):
                    best_legal = move_tile
            if grid_util.dist_between(self.pos, target) > grid_util.dist_between(best_legal, target):
                result = best_legal

        return result


    def move(self, grid):
        """
        Generates move track for the next step
        """
        if self.target_tile:
            step_tile = self.get_nearest_step_tile(self.target_tile, grid)
            self.gen_move_track(grid, step_tile)
        if self.pos == self.target_tile:
            self.target_tile = None


    # --------------------------------------------------------------- #
    #                                                                 #
    #                           MOVE TRACK                            #
    #                                                                 #
    # --------------------------------------------------------------- #
    def get_steps(self, grid, to_tile):
        """
        This method generates steps from the item pos to to_tile.
        :param to_tile: coordinates of destination point B (x, y)
        :return: a list of steps from point A to point B
        """
        result = []
        if self.speed > 0:
            distance = 2 * grid.tile_radius
            steps = int(distance / self.speed)
            from_tile_x = self.pos[0]
            from_tile_y = self.pos[1]
            to_tile_x = to_tile[0]
            to_tile_y = to_tile[1]

            for step in range(1, steps):
                a = float(step) / steps
                step_x = int((1 - a) * from_tile_x + a * to_tile_x)
                step_y = int((1 - a) * from_tile_y + a * to_tile_y)
                new_step = (step_x, step_y)
                result.append(new_step)
            result.append(to_tile)

        return result

    def gen_move_track(self, grid, to_tile):
        """
        Generates a legal move track to_tile
        """
        if not self.move_track and self.speed: # and not self.vibe_track['track']:
            if to_tile in grid.revealed_tiles.keys() and to_tile not in grid.occupado_tiles.values():
                    self.move_track = self.get_steps(grid, to_tile)
