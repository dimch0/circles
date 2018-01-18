# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                                                                                     #
#                                                Item Generator                                                       #
#                                                                                                                     #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import random

gen_schema = {
    "1": {
       "items": [
           'toilet_paper',
           'carrot',
           'fresh'
           # 'peanut',
           # 'pretzel',
           # 'apple',
           # "cheshma",
           # "dog house",
           # "casino",
           # "cage",
           # "gas_col",
           # "battery",
           # "lipstick",
           # "gascan"
       ],
       "base": 15
    },
    "2": {
        "items": [
            'banana',
            'pinapple',
            'can',
            'egg',
            'tomato',
            'carrot'
        ],
        "base": 40
    },
    "3": {
        "items": [
            'chili',
            'lemon',
            'kibabchi',
            'icecream',
            'cheese',
            'donut',
            'fresh',
        ],
        "base": 70
    },
    "4": {
        "items": [
            'spoget',
            'hotdog',
            'pizza',
            'miso',
            'miso_02',
        ],
        "base": 110
    }
}


class ItemGenerator(object):
    """ Generating items on each level """
    def __init__(self, grid, my_body):
        self.grid = grid
        self.generated = {}
        self.my_body = my_body

    def should_generate(self):
        """ Checks bases for generation
         returns boolean """
        result = 0
        revealed_tiles = 0
        for room in self.grid.rooms.values():
            revealed_tiles += len(room['revealed_tiles'])

        for level in sorted(gen_schema.keys()):
            base = int(gen_schema[level]['base'])
            count_level = len([n for n in range(base,
                                                revealed_tiles,
                                                base)])
            if not level in self.generated:
                self.generated[level] = 0
            if self.generated[level] < count_level:
                result = level

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

        if gen_pos and self.should_generate():
            level = self.should_generate()
            items = gen_schema[level]['items']
            random_item = random.choice(items)
            self.grid.event_effects.produce(random_item, gen_pos)
            self.generated[level] += 1
