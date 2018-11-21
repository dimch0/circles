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
        self.go_to_tile = None
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
        if self.go_to_tile:
            self.choose_nearest_legal(self.go_to_tile, grid)
        if self.pos == self.go_to_tile:
            self.go_to_tile = None

    # --------------------------------------------------------------- #
    #                                                                 #
    #                             MOVEMENT                            #
    #                                                                 #
    # --------------------------------------------------------------- #
    def gen_steps(self, grid, target_tile):
        """
        This method generates steps from the item pos to target_tile.
        :param target_tile: coordinates of destination point B (x, y)
        :return: a list of steps from point A to point B
        """
        result = []
        if self.speed > 0:
            distance = 2 * grid.tile_radius
            steps = int(distance / self.speed)
            from_tile_x = self.pos[0]
            from_tile_y = self.pos[1]
            target_tile_x = target_tile[0]
            target_tile_y = target_tile[1]

            for step in range(1, steps):
                a = float(step) / steps
                step_x = int((1 - a) * from_tile_x + a * target_tile_x)
                step_y = int((1 - a) * from_tile_y + a * target_tile_y)
                new_step = (step_x, step_y)
                result.append(new_step)
            result.append(target_tile)

        return result

    def gen_move_track(self, grid):
        """
        Generates a legal move track in the current direction
        """
        if self.direction != None and not self.move_track: # and not self.vibe_track['track']:
            target_tile = grid.adj_tiles(self.pos)[self.direction]
            if self.speed > 0:
                if target_tile in grid.revealed_tiles.keys() and target_tile not in grid.occupado_tiles.values():
                        self.move_track = self.gen_steps(grid, target_tile)
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
