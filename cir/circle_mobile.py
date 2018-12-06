# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                   MOBILE                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
from circle import Circle
import grid_util


class Mobile(Circle):
    """
    This is the base class for all mobile cirlces
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
    #                          MOVEMENT NEW                           #
    #                                                                 #
    # --------------------------------------------------------------- #
    def choose_nearest_legal(self, target, grid):

        legal_moves = self.get_legal_moves(grid)

        # Choose nearest legal
        if legal_moves:
            # if target and target not in grid.adj_tiles(self.pos):
            best_legal = None
            for move_tile, move_idx in legal_moves.items():
                if not best_legal:
                    best_legal = move_tile
                elif grid_util.dist_between(best_legal, target) > grid_util.dist_between(move_tile, target):
                    best_legal = move_tile
            if grid_util.dist_between(self.pos, target) > grid_util.dist_between(best_legal, target):
                self.direction = legal_moves[best_legal]
                self.gen_move_track(grid)
                self.direction = None


    def move_to_tile_new(self, grid):
        if self.target_tile:
            self.choose_nearest_legal(self.target_tile, grid)
        if self.pos == self.target_tile:
            self.target_tile = None

    # --------------------------------------------------------------- #
    #                                                                 #
    #                             MOVEMENT                            #
    #                                                                 #
    # --------------------------------------------------------------- #
    def gen_steps(self, grid, to_tile):
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

    def gen_move_track(self, grid):
        """
        Generates a legal move track in the current direction
        """
        if self.direction != None and not self.move_track: # and not self.vibe_track['track']:
            to_tile = grid.adj_tiles(self.pos)[self.direction]
            if self.speed > 0:
                if to_tile in grid.revealed_tiles.keys() and to_tile not in grid.occupado_tiles.values():
                        self.move_track = self.gen_steps(grid, to_tile)
                else:
                    self.direction = None
            else:
                self.direction = None

    def gen_direction(self, grid, event):
        """ Generates item direction from 0-6 on pressed key """
        if self.direction == None and not self.birth_track:
            for idx, arrow in enumerate(grid.arrows):
                if event.key == arrow:
                    # if not self.vibe_track:
                    self.direction = idx


    # --------------------------------------------------------------- #
    #                    CHECK FOR EMPTY ADJ TILE                     #
    # --------------------------------------------------------------- #
    def check_for_empty_adj_tile(self, grid):
        """
        Checks for an empty adj tile
        :param grid: grid instance
        :return: the first available empty tile (1, 1) or None
        """
        empty_tile = None

        for idx, tile in enumerate(grid.adj_tiles(self.pos)):
            if not empty_tile:
                if tile in grid.revealed_tiles.keys():
                    if tile not in grid.occupado_tiles.values():
                        empty_tile = tile
                        break

        return empty_tile
