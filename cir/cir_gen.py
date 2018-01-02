# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                                                                                     #
#                                                Item Generator                                                       #
#                                                                                                                     #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import random


ITEMS_LVL_1 = [
    'bread',
    # 'carrot',
    # 'apple',
    # 'banana',
    # 'chili',
    # 'lemon',
    # 'pineapple',
    # 'can',
    # 'egg',
    # 'kibabchi',
    # 'icecream',
    # 'fresh',
    # 'spoget',
    # 'hotdog',
    # 'pizza'
]


ITEMS_LVL_2 = [
    # 'bread',
    # 'carrot',
    # 'apple',
    # 'banana',
    # 'chili',
    # 'lemon',
    # 'pineapple',
    # 'can',
    # 'egg',
    # 'kibabchi',
    # 'icecream',
    'fresh',
    # 'spoget',
    # 'hotdog',
    # 'pizza'
]


class ItemGenerator(object):
    """ Generating items on each level """
    def __init__(self, grid, my_body):
        self.grid = grid
        self.gen_lvl_1 = 0
        self.base_lvl_1 = 15
        self.gen_lvl_2 = 0
        self.base_lvl_2 = 26

        self.my_body = my_body

    def should_generate(self):
        """ Checks bases for generation
         returns boolean """
        result = 0
        revealed_tiles = 0
        for room in self.grid.rooms.values():
            revealed_tiles += len(room['revealed_tiles'])

        count_base_lvl_1 = len([n for n in range(self.base_lvl_1,
                                                 revealed_tiles,
                                                 self.base_lvl_1)])
        count_base_lvl_2 = len([n for n in range(self.base_lvl_2,
                                                 revealed_tiles,
                                                 self.base_lvl_2)])
        if self.gen_lvl_1 < count_base_lvl_1:
            result = 1
        if self.gen_lvl_2 < count_base_lvl_2:
            result = 2

        return result

    def get_gen_pos(self, last_revealed):
        """ Checks if last revealed tile is empty
        and returns the pos of that tile or None"""
        result = None
        if last_revealed not in self.grid.occupado_tiles.values():
            result = last_revealed
        return result

    def generate_item(self, last_revealed):
        gen_pos = self.get_gen_pos(last_revealed)

        if gen_pos:
            if self.should_generate() == 1:
                indx_lvl_1 = random.randint(1, len(ITEMS_LVL_1))
                item_lvl_1 = ITEMS_LVL_1[indx_lvl_1 - 1]
                self.grid.event_effects.produce(item_lvl_1, gen_pos)
                self.gen_lvl_1 += 1
            elif self.should_generate() == 2:
                print "2"
                indx_lvl_2 = random.randint(1, len(ITEMS_LVL_2))
                item_lvl_2 = ITEMS_LVL_2[indx_lvl_2 - 1]
                self.grid.event_effects.produce(item_lvl_2, gen_pos)
                self.gen_lvl_2 += 1
