# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                                                                                     #
#                                                Item Generator                                                       #
#                                                                                                                     #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import random


class ItemGenerator(object):
    """ Generating items on each level """
    def __init__(self, grid, my_body):
        self.grid = grid
        self.generated = {}
        self.my_body = my_body
        self.gen_schema = grid.gen_schema

    def should_generate(self):
        """ Checks bases for generation
         returns boolean """
        result = 0
        # revealed_tiles = 0
        # for room in self.grid.rooms.values():
        #     revealed_tiles += len(room['revealed_tiles'])

        for level in sorted(self.gen_schema.keys()):
            base = int(self.gen_schema[level]['base'])
            count_level = len([n for n in range(base,
                                                self.grid.total_revealed,
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
            items = self.gen_schema[level]['items']
            if self.gen_schema[level]['items']:
                random_item = random.choice(items)
                if random_item:
                    self.grid.event_effects.produce(random_item, gen_pos)
                    self.generated[level] += 1
