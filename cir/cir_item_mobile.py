#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                              MobileItem class                                       #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################
from cir_item import Item
from cir_item_timer import TimerItem
import cir_utils
from cir_effects import produce

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
        if not self.type == "signal":
            if self.direction != None and not self.move_track:
                target_tile = grid.adj_tiles(self.pos)[self.direction]
                if self.speed > 0:
                    if target_tile in grid.revealed_tiles and target_tile not in grid.occupado_tiles:
                        self.move_track = self.move_to_tile(grid, target_tile)
                    else:
                        self.direction = None
                else:
                    self.direction = None

        # TODO: Identify signal
        else:
            if self.direction != None and not self.move_track:
                target_tile = grid.adj_tiles(self.pos)[self.direction]
                if self.speed > 0:
                    if target_tile in grid.revealed_tiles:
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
                    if not (self.radar_track or self.rot_revert or self.rot_track):
                        self.direction = idx
                        self.gen_rot_track(self.direction)

    def move(self):
        """
        :return: move self.pos per point in move_track
        """
        if self.move_track and not self.birth_track:
            self.pos = self.move_track[0]
            self.move_track.pop(0)

    # --------------------------------------------------------------- #
    #                                                                 #
    #                             MITOSIS                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    def check_for_empty_adj_tile(self, grid):
        """
        Checks for an empty adj tile
        :param grid: grid instance
        :return: the first available empty tile (1, 1) or None
        """
        empty_tile = None

        for idx, tile in enumerate(grid.adj_tiles(self.pos)):
            if tile in grid.revealed_tiles:
                if tile not in grid.occupado_tiles:
                    empty_tile = tile
                    break
        return empty_tile


    def cell_division(self, grid, empty_tile):
        """
        Creates a placeholder in the empty tile.
        Than creates a copy of the item and moves it into the placehoder.
        They're being cleaned with the clean_placehoder function.
        :param grid: grid instance
        :return:
        """
        if empty_tile:
            occupado_placeholder = Item()
            occupado_placeholder.name = "placeholder"
            occupado_placeholder.pos = empty_tile
            occupado_placeholder.birth_time = TimerItem()
            occupado_placeholder.birth_time.duration = 0
            grid.items.append(occupado_placeholder)

            new_copy = produce(grid, self.name, self.pos)
            print new_copy
            # new_copy.name = "new copy"
            # new_copy = MobileItem()
            # new_copy.img = self.img
            # new_copy.speed = self.speed
            # new_copy.name = "new copy"
            # new_copy.pos = self.pos
            # new_copy.color = self.color
            # new_copy.birth_time = None
            # new_copy.radius = self.radius
            # new_copy.birth_time = TimerItem()
            # new_copy.birth_time.duration = 0.03
            # new_copy.gen_birth_track()
            new_copy.move_track = self.move_to_tile(grid, empty_tile)
            # grid.items.append(new_copy)


    def mitosis(self, grid):
        """
        :param grid: grid instance
        :return:
        """
        copies = [item for item in grid.items if self.name in item.name]
        # Ready copies
        for item in grid.items:
            print "START MITO", item.name
            if item.name == "new copy":
                item.name = str(self.name + " - copy")

            if item.name in [self.name, str(self.name + " - copy")]:
                empty_tile = item.check_for_empty_adj_tile(grid)
                if empty_tile:
                    if item.speed and not item.birth_track and not item.move_track:
                        item.cell_division(grid, empty_tile)
            print "FINISH MITO", item.name


# --------------------------------------------------------------- #
#                                                                 #
#                            SIGNAL                               #
#                                                                 #
# --------------------------------------------------------------- #
    def get_aiming_direction(self, grid, MOUSE_POS, current_tile):
        """  Currently gives the opposite mirror point of the mouse """
        # MIRROR POINT
        # aim_point = get_mirror_point(current_tile, self.pos)

        opposite_tile = None
        aim_dir_idx = None
        if current_tile:
            start_point = current_tile
        else:
            start_point = MOUSE_POS
        if start_point:
            for dir_idx, adj_tile in enumerate(grid.adj_tiles(self.pos)):
                if not opposite_tile:
                    opposite_tile = adj_tile
                    aim_dir_idx = dir_idx
                elif cir_utils.dist_between(start_point, adj_tile) > cir_utils.dist_between(start_point, opposite_tile):
                    opposite_tile = adj_tile
                    aim_dir_idx = dir_idx

        return [opposite_tile, aim_dir_idx]