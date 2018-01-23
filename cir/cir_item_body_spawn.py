# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                    SCOUT                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
from cir_item_body import BodyItem


class Spawn(BodyItem):

    def __init__(self):
        super(Spawn, self).__init__()

    def action(self, grid):
        """
        Action of the spawning quelle
        :param grid: grid instance
        """
        effects = self.effects.split()
        for eff in effects:
            if "home" in eff or "spawn" in eff:
                product = eff.split(':')[1]
                for adj_tile in grid.adj_tiles(self.pos):
                    if not adj_tile in grid.occupado_tiles.values() \
                            and adj_tile in grid.playing_tiles \
                            and adj_tile in grid.revealed_tiles:
                        pos = adj_tile
                        summon = grid.event_effects.produce(product_name=product,
                                                            pos=pos)
                        if "home" in eff:
                            setattr(summon, 'home_vfreq', self.vfreq)
                            setattr(summon, 'home', self)
                            self.vfreq = None
                        break
        if self.vfreq:
            self.vfreq.restart()