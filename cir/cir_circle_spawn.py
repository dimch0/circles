# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                    SCOUT                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import random
from cir_utils import get_short_name
from cir_circle_body import Body


class Spawn(Body):

    def __init__(self):
        super(Spawn, self).__init__()
        self.reversed_timer = True

    def spawn(self, product, grid):
        product = product.split('_')
        result = None
        product = random.choice(product)
        for adj_tile in grid.adj_tiles(self.pos):
            if not adj_tile in grid.occupado_tiles.values() \
                    and adj_tile in grid.playing_tiles \
                    and adj_tile in grid.revealed_tiles:
                pos = adj_tile
                result = grid.event_effects.produce(product_name=product,
                                                    pos=pos)
                break
        return result

    def action(self, grid):
        """
        Action of the spawning quelle
        :param grid: grid instance
        """
        effects = self.effects.split()
        for eff in effects:
            if "#home" in eff or "#spawn" in eff:
                product = eff.split(':')[1]
                spawn = self.spawn(product, grid)
                if spawn:
                    if "#home" in eff:
                        setattr(spawn, 'home_vfreq', self.vfreq)
                        setattr(spawn, 'home', self)
                        self.vfreq = None
                    # break
        if self.vfreq:
            self.vfreq.restart()

    def trade(self, take_item, grid):
        payment_lvl = take_item.lvl
        spawn = None
        if payment_lvl:
            # TODO: Pricing, profit
            # payment_type = take_item.type
            # take_item.destroy(grid)
            effects = self.effects.split()
            for eff in effects:
                if "#lvl" in eff and payment_lvl in eff:
                    product = eff.split(':')[1]
                    spawn = self.spawn(product, grid)
                    break
                    # product_lvl = eff.replace('#lvl', "")
            if spawn:
                grid.msg("SCREEN - you pay %s" % get_short_name(take_item.name).replace('_', ' '))

            else:
                grid.msg("SCREEN - no trade")

        return spawn