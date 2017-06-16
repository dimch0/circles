#######################################################################################################################
#################                                                                                     #################
#################                              MobileItem class                                       #################
#################                                                                                     #################
#######################################################################################################################
import math
import copy
import pdb
from cir_item import Item
from math import sqrt, ceil, hypot


class MobileItem(Item):
    """
    This is the base class for all CIR items
    """
    def __init__(self, speed, **kwargs):
        super(MobileItem, self).__init__(**kwargs)
        self.speed = speed
        self.direction = None

    def change_speed(self, modifier):
        self.speed += modifier
        if self.speed < 0:
            self.speed = 0
        if self.speed is 1:
            self.speed = 2
        if self.speed is 2 and modifier < 0:
            self.speed = 0
        if self.speed > 8:
            self.speed = 8

    def move_to_tile(self, grid, Tile_A, Tile_B):
        """
        This method moves the item from the current position to Tile_B.
        :param Tile_B: coordinates of destination point B (x, y)
        :return: a list of steps from point A to point B
        number of steps depends on the speed and the distance
        """
        # print "Inside move to tile"
        result = []
        # Movement only allowed in revealed_tiles and not occupado_tiles
        # if Tile_B in grid.revealed_tiles and Tile_B not in grid.occupado_tiles and self.speed > 0:
        if self.speed > 0:
            ax = Tile_A[0]
            ay = Tile_A[1]
            bx = Tile_B[0]
            by = Tile_B[1]
            # TODO: debug step generation
            dx, dy = (bx - ax, by - ay)
            # distance = int(sqrt(dx ** 2 + dy ** 2))
            distance = 2 * grid.tile_radius
            # steps_number = int(ceil(2 * distance / (2 * self.speed)))
            steps_number = 2 * distance / (2 * self.speed)
            step_size = int(distance / steps_number)
            if steps_number > 0:
                stepx, stepy = int(dx / steps_number), int(dy / steps_number)
                for i in range(steps_number + 1):
                    step = (int(ax + (stepx * i)), int(ay + (stepy * i)))
                    result.append(step)
            result.append(Tile_B)
        return result

    def gen_move_track(self, grid, direction_idx):
        """
        :param direction_idx: index of the 6 directions (0-5)
        :param options: options
        :return: a list of all available tiles in northeast direction_idx
        """
        # print "Inside gen move track"
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

    def move(self):
        """
        :return: move self.pos per point in move_track
        """
        if self.move_track:
            self.pos = self.move_track[0]
            self.move_track.pop(0)

    def check_for_empty_tile(self, grid):
        """
        Checks for an empty adj tile and creates a placeholder thare.
        :param grid: grid instance
        :return: the first available empty tile (1, 1) or None
        """
        EMPTY_TILE = None
        for idx, tile in enumerate(grid.adj_tiles(self.pos)):
            if tile in grid.revealed_tiles:
                if not tile in grid.occupado_tiles:
                    EMPTY_TILE = tile
                    break

        return EMPTY_TILE

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

            new_cell = MobileItem(
                speed=2,
                name="new copy",
                pos=self.pos,
                color=self.color,
                image=self.img,

            )
            new_cell.move_track = self.move_to_tile(grid, new_cell.pos, empty_tile)

            grid.items.append(new_cell)
            grid.bodies.append(new_cell)
            # new_cell.gen_move_track(grid, idx)


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


