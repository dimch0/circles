#######################################################################################################################
#################                                                                                     #################
#################                                 Button class                                        #################
#################                                                                                     #################
#######################################################################################################################
import math
from cir_item import Item
from math import sqrt, ceil, hypot


class ButtonItem(Item):
    """
    This is the base class for all circle items
    """
    def __init__(self, font, text_color, text=None, **kwargs):
        super(ButtonItem, self).__init__(**kwargs)

        self.font = font
        self.text_color = text_color

        if text:
            self.text = self.font.render(text, True, self.text_color)
        else:
            self.text = self.font.render(self.name, True, self.text_color)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.pos


    # @property
    # def text_rect(self):
    #     self._text_rect = self.text.get_rect()
    #     return self._text_rect
    #
    # @property
    # def text_rect(self):
    #     self._text_rect.center = self.pos
    #     return self._text_rect.center

    # def change_speed(self, increment):
    #     self.speed += increment
    #     if self.speed < 0:
    #         self.speed = 0
    #     if self.speed is 1:
    #         self.speed = 2
    #     if self.speed is 2 and increment < 0:
    #         self.speed = 0
    #     if self.speed > 8:
    #         self.speed = 8
    #
    # def move_to_tile(self, Tile_A, Tile_B):
    #     """
    #     This method moves the item from the current position to Tile_B.
    #     :param Tile_B: coordinates of destination point B (x, y)
    #     :return: a list of steps from point A to point B
    #     number of steps depends on the speed and the distance
    #     """
    #     # print "Inside move to tile"
    #     result = []
    #     # Movement only allowed in revealed_tiles and not occupado_tiles
    #     if Tile_B in self.grid.revealed_tiles and Tile_B not in self.grid.occupado_tiles and self.speed > 0:
    #         ax = Tile_A[0]
    #         ay = Tile_A[1]
    #         bx = Tile_B[0]
    #         by = Tile_B[1]
    #         # TODO: debug step generation
    #         dx, dy = (bx - ax, by - ay)
    #         # distance = int(sqrt(dx ** 2 + dy ** 2))
    #         distance = 2 * self.grid.tile_radius
    #         # steps_number = int(ceil(2 * distance / (2 * self.speed)))
    #         steps_number = 2 * distance / (2 * self.speed)
    #         step_size = int(distance / steps_number)
    #         if steps_number > 0:
    #             stepx, stepy = int(dx / steps_number), int(dy / steps_number)
    #             for i in range(steps_number + 1):
    #                 step = (int(ax + (stepx * i)), int(ay + (stepy * i)))
    #                 result.append(step)
    #         result.append(Tile_B)
    #     return result
    #
    # def gen_move_track(self, direction, options):
    #     """
    #     :param self.grid: self.grid instance
    #     :return: a list of all available tiles in northeast direction
    #     """
    #     # print "Inside gen move track"
    #     dir = None
    #     for idx, option in enumerate(options):
    #         if direction == option.name:
    #             dir = idx
    #     result = []
    #     Point_A = self.pos
    #     Point_B = self.grid.adj_tiles(self.pos)[dir]
    #     if self.speed > 0:
    #         for fields in range(1,13):
    #             if Point_B in self.grid.playing_tiles:
    #                 if Point_B not in self.grid.occupado_tiles and Point_B in self.grid.revealed_tiles:
    #                     for new_steps in self.move_to_tile(Point_A, Point_B):
    #                         if not new_steps in result:
    #                             result.append(new_steps)
    #                 else:
    #                     self.move_track = result
    #                     return result
    #             Point_A = Point_B
    #             Point_B = self.grid.adj_tiles(Point_A)[dir]
    #         self.move_track = result
    #     print "steps:", len(result)
    #     return result
    #
    # def move(self):
    #     """
    #     :return: move self.pos per point in move_track
    #     """
    #     if self.move_track:
    #         self.pos = self.move_track[0]
    #         self.move_track.pop(0)