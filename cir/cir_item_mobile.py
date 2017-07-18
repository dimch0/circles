#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                              MobileItem class                                       #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################
from cir_item import Item


class MobileItem(Item):
    """
    This is the base class for all CIR items
    """
    def __init__(self, speed=2, **kwargs):
        super(MobileItem, self).__init__(**kwargs)
        self.speed = speed

    def change_speed(self, modifier):
        self.speed += modifier
        if self.speed < 0:
            self.speed = 0


    # --------------------------------------------------------------- #
    #                                                                 #
    #                             MOVEMENT                            #
    #                                                                 #
    # --------------------------------------------------------------- #
    def move_to_tile(self, grid, Tile_A, Tile_B):
        """
        This method moves the item from Tile_A to Tile_B.
        :param Tile_B: coordinates of destination point B (x, y)
        :return: a list of steps from point A to point B
        number of steps depends on the speed and the distance
        """
        result = []
        if self.speed > 0:
            distance = 2 * grid.tile_radius
            steps = distance / self.speed
            x1 = Tile_A[0]
            y1 = Tile_A[1]
            x2 = Tile_B[0]
            y2 = Tile_B[1]
            for step in range(1, steps):
                a = float(step) / steps
                x = int((1 - a) * x1 + a * x2)
                y = int((1 - a) * y1 + a * y2)
                result.append((x, y))
            result.append(Tile_B)
        return result

    def gen_move_track(self, grid, direction_idx):
        """
        Generates a legal move track
        :param direction_idx: index of the 6 directions (0-5)
        :param options: options
        :return: a list of all available tiles in direction_idx
        """
        result = []
        Point_A = self.pos
        # pdb.set_trace()
        Point_B = grid.adj_tiles(self.pos)[direction_idx]
        if self.speed > 0:
            for fields in range(1, 26):
                if Point_B in grid.playing_tiles:
                    if Point_B not in grid.occupado_tiles and Point_B in grid.revealed_tiles:
                        for new_steps in self.move_to_tile(grid, Point_A, Point_B):
                            if not new_steps in result:
                                result.append(new_steps)
                    else:
                        self.move_track = result
                        return result
                Point_A = Point_B
                Point_B = grid.adj_tiles(Point_A)[direction_idx]
            self.move_track = result
        return result


    def gen_movement_arrows(self, pygame, grid, event):
        """ Generates steps to move my body - gen_move_track() """
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
                if not self.move_track and not self.radar_track and not self.rot_revert and not self.rot_track:
                    if not self.rot_track:
                        self.gen_rot_track(idx)
                        self.gen_move_track(grid, idx)

    def move(self):
        """
        :return: move self.pos per point in move_track
        """
        if self.move_track:
            self.pos = self.move_track[0]
            self.move_track.pop(0)

    # --------------------------------------------------------------- #
    #                                                                 #
    #                             MITOSIS                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    def check_for_empty_tile(self, grid):
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

    def cell_division(self, grid):
        """
        Creates a placeholder in the empty tile.
        Than creates a copy of the item and moves it into the placehoder.
        They're being cleaned with the clean_placehoder function.
        :param grid: grid instance
        :return:
        """
        empty_tile = self.check_for_empty_tile(grid)
        if empty_tile:
            occupado_placeholder = Item(
                name="placeholder",
                pos=empty_tile,
            )
            grid.items.append(occupado_placeholder)

            new_copy = MobileItem(
                speed=self.speed,
                name="new copy",
                pos=self.pos,
                color=self.color,
                image=self.img,

            )
            new_copy.move_track = self.move_to_tile(grid, new_copy.pos, empty_tile)
            grid.items.append(new_copy)

    def mitosis(self, grid):
        """
        :param grid: grid instance
        :return:
        """
        # Ready copies
        for item in grid.items:
            if item.name == "new copy":
                item.name = str(self.name + " - copy")

        for item_a in grid.items:
            if item_a.name in [self.name, str(self.name + " - copy")]:
                if item_a.speed:
                    item_a.cell_division(grid)

