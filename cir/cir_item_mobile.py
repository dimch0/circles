# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                   MOBILE                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
from cir_item import Item
import cir_utils


class MobileItem(Item):
    """
    This is the base class for all CIR items
    """
    def __init__(self):
        super(MobileItem, self).__init__()
        self.speed = 1

    def change_speed(self, modifier):
        self.speed += modifier
        if self.speed < 0:
            self.speed = 0


    # --------------------------------------------------------------- #
    #                                                                 #
    #                             MOVEMENT                            #
    #                                                                 #
    # --------------------------------------------------------------- #
    def move_to_tile(self, grid, target_tile):
        """
        This method generates steps from the item pos to target_tile.
        :param target_tile: coordinates of destination point B (x, y)
        :return: a list of steps from point A to point B
        number of steps depends on the speed and the distance
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
        :param options: options
        :return: a list of all available tiles in direction_idx
        """
        if self.direction != None and not self.move_track:
            target_tile = grid.adj_tiles(self.pos)[self.direction]
            if self.speed > 0:
                if target_tile in grid.revealed_tiles and ((self.type != "signal" and target_tile not in grid.occupado_tiles.values()) or self.type == "signal"):
                        self.move_track = self.move_to_tile(grid, target_tile)
                else:
                    self.direction = None
            else:
                self.direction = None

    def gen_direction(self, pygame, grid, event):
        """ Generates item direction from 0-6 on pressed key """
        if self.direction == None and not self.birth_track:
            arrows = [
                pygame.K_w,
                pygame.K_e,
                pygame.K_d,
                pygame.K_s,
                pygame.K_a,
                pygame.K_q
            ]
            for idx, arrow in enumerate(arrows):
                if event.key == arrow:
                    if not (self.vibe_track or self.rot_revert or self.rot_track):
                        self.direction = idx
                        self.gen_rot_track(self.direction)

    def update_pos(self):
        """
        :return: move self.pos per point in move_track
        """
        if self.move_track and not self.birth_track:
            self.pos = self.move_track[0]
            self.move_track.pop(0)

    # --------------------------------------------------------------- #
    #                                                                 #
    #                           ROTATION                              #
    #                                                                 #
    # --------------------------------------------------------------- #
    def gen_rot_track(self, idx):
        """
        Generates rotating track and revert rotating track
        :param idx:  index of direction
        :param item: item to whom belongs the image
        """
        step = 15
        end_point = step * 4
        track = None
        if idx == 1:
            track = range(-step, -end_point, -step)
        elif idx == 2:
            track = range(-step, -end_point * 2, -step)
        elif idx == 3:
            track = range(-step, -end_point * 3, -step)
        elif idx == 4:
            track = range(step, end_point * 2, step)
        elif idx == 5:
            track = range(step, end_point, step)

        if track:
            self.rot_track = track
            if not self.rot_revert:
                if idx == 3:
                    self.rot_revert = range(-step, -end_point * 3, -step)
                else:
                    self.rot_revert = cir_utils.negative_list(self.rot_track)

    def rotate(self, pygame):
        """ Rotates the image """
        self.img = cir_utils.rot_center(pygame, self.default_img, self.rot_track[0])

        if len(self.rot_track) == 1:
            self.last_rotation = self.rot_track[-1]
        self.rot_track.pop(0)

    def rotate_reverse(self, pygame):
        """ Returns the image to start position """
        if self.last_rotation:
            self.img = cir_utils.rot_center(pygame, self.default_img, self.last_rotation)

        if self.rot_revert:
            self.img = cir_utils.rot_center(pygame, self.img, self.rot_revert[0])
            self.rot_revert.pop(0)

        elif not self.rot_revert:
            self.img = self.default_img
            self.last_rotation = False


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
                if tile in grid.revealed_tiles:
                    if tile not in grid.occupado_tiles.values():
                        empty_tile = tile
                        break

        return empty_tile


# --------------------------------------------------------------- #
#                                                                 #
#                            SIGNAL                               #
#                                                                 #
# --------------------------------------------------------------- #
    def get_aiming_direction(self, grid, current_tile):
        """  Currently gives the opposite mirror point of the mouse """
        # MIRROR POINT
        # aim_point = get_mirror_point(current_tile, self.pos)

        opposite_tile = None
        aim_dir_idx = None

        if current_tile:
            for dir_idx, adj_tile in enumerate(grid.adj_tiles(self.pos)):
                if not opposite_tile:
                    opposite_tile = adj_tile
                    aim_dir_idx = dir_idx
                elif cir_utils.dist_between(current_tile, adj_tile) > cir_utils.dist_between(current_tile, opposite_tile):
                    opposite_tile = adj_tile
                    aim_dir_idx = dir_idx

        return [opposite_tile, aim_dir_idx]