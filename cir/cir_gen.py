# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                                                                                     #
#                                                Item Generator                                                       #
#                                                                                                                     #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import random


FOOD_ITEMS = [
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
        self.base_1_gen = 0
        self.base_1 = 12
        self.my_body = my_body

    def should_generate(self):
        """ Checks bases for generation
         returns boolean """
        result = False
        revealed_tiles = 0
        for room in self.grid.rooms.values():
            revealed_tiles += len(room['revealed_tiles'])

        count_base_1 = len([n for n in range(self.base_1,
                                             revealed_tiles,
                                             self.base_1)])
        if self.base_1_gen < count_base_1:
            result = True

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

        if self.should_generate() and gen_pos:
            food_idx = random.randint(1, len(FOOD_ITEMS))
            food_name = FOOD_ITEMS[food_idx - 1]

            self.grid.event_effects.produce(food_name, gen_pos)
            self.base_1_gen += 1
