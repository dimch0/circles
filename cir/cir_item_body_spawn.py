# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                    SCOUT                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
from cir_item_body import BodyItem
from cir_item_body_scout import Scout
import cir_utils as cu


class Spawn(Scout):

    def __init__(self):
        super(Spawn, self).__init__()
        self.summon = None

    def action(self, grid):
        """
        Action of the spawning quelle
        :param grid: grid instance
        """
        if self.summon:
            if not self.summon in grid.items:
                self.summon = None

        if not self.summon:
            effects = self.effects.split()
            for eff in effects:
                if "spawn" in eff:
                    product = eff.split(':')[1]
                    for adj_tile in grid.adj_tiles(self.pos):
                        if not adj_tile in grid.occupado_tiles.values() \
                                and adj_tile in grid.playing_tiles \
                                and adj_tile in grid.revealed_tiles:
                            pos = adj_tile
                            self.summon = grid.event_effects.produce(product_name=product,
                                                                     pos=pos)
                            self.summon.hungry = True
                            break
        self.vfreq.restart()