# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                                                                                     #
#                                                Item Generator                                                       #
#                                                                                                                     #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import os
import csv
import random


class ItemGenerator(object):
    """ Generating items on each level """
    def __init__(self, grid, mybody):
        self.grid = grid
        self.mybody = mybody
        self.gen_file = '%s/../data/%s/gen.json' % (os.path.dirname(__file__), grid.scenario)
        self.gen_file2 = '%s/../data/%s/gen.csv' % (os.path.dirname(__file__), grid.scenario)
        self.decks = {}
        self.read_gen_schema()
        self.generated = {}

    def read_gen_schema(self):
        """
        Sets all decks from gen.json as attributes
        and a progress dict for each deck
        """
        with open(self.gen_file2, 'rb') as csvfile:
            data = csv.reader(csvfile, delimiter=',')
            header = next(data)
            for row in data:
                if not row == header:
                    deck_name = row[0]
                    deck_lvl = int(row[1])
                    deck_base = int(row[2])
                    deck_items = row[3].split()
                    progress = {}
                    for cir_to_gen in range(len(deck_items)):
                        progress[str(cir_to_gen)] = 0
                    self.decks[deck_name] = {'base':deck_base,
                                             'items':deck_items,
                                             'lvl':deck_lvl,
                                             'progress':progress}

    def decks_togen(self):
        """ Checks bases for generation
         returns str """
        result = []
        for deck, deck_data in self.decks.items():
            base = deck_data['base']
            count = len([n for n in range(base,
                                          self.grid.total_revealed,
                                          base)])
            if not deck in self.generated:
                self.generated[deck] = 0
            if self.generated[deck] < count:
                result.append(deck)
        return result

    def get_gen_pos(self, last_revealed):
        """ Checks if last revealed tile is empty
        and returns the pos of that tile or None"""
        result = None

        illegal = self.grid.occupado_tiles.values()
        if last_revealed not in illegal:
            result = last_revealed
        return result

    def min_progress(self, deck_name):
        """ Returns a random element (str) from the indeces of the items in
        the given deck_name (str) """
        progress = self.decks[deck_name]['progress']
        min_val = min(progress.values())
        min_indeces = [item for item in progress.keys() if progress[item] == min_val]
        result = random.choice(min_indeces)
        progress[result] += 1
        return result

    def add2deck(self, deck_name, item_name):
        """ Add an item to a deck with progress min - 1 """
        deck = self.decks[deck_name]
        progress = deck['progress']
        items = deck['items']
        items.append(item_name)
        new_idx = len(items)
        progress[str(new_idx)] = min(progress.values() - 1)


    def generate_item(self, last_revealed):
        """ Produce a random item from a deck """
        gen_pos = self.get_gen_pos(last_revealed)
        decks2gen = self.decks_togen()

        for deck in decks2gen:
            if gen_pos and deck:
                items = self.decks[deck]['items']
                if items:
                    idx = int(self.min_progress(deck))
                    self.grid.event_effects.produce(items[idx], gen_pos)
                    self.generated[deck] += 1
