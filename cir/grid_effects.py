# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                                                                                     #
#                                                   EFFECTS                                                           #
#                                                                                                                     #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import grid_util
import time as time_stamp


class GameEffects(object):

    def __init__(self, grid=None):
        self.grid = grid


    # --------------------------------------------------------------- #
    #                                                                 #
    #                             PRODUCE                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    def produce(self,
                name,
                pos=None,
                radius=None,
                time=None,
                add_circle=True,
                effects=None):
        """
        Produces an item from the everything dict
        :param name: name of the item from the everything dict
        :param pos: set new position (optional)
        :param radius: set new radius (optional)
        :param birth: set new birth timer (optional)
        :param time: set new time (optional)
        :return: the new item object
        """
        new_item = None
        try:
            name = grid_util.get_short_name(name)
            new_item = self.grid.loader.load_item(name)
            new_item.name = new_item.name + '-' + str(time_stamp.time())
            if new_item:

                if pos:
                    new_item.pos = pos
                if radius:
                    new_item.radius = radius
                if effects:
                    new_item.effects = effects
                if time:
                    new_item.time = time

                new_item.available = True
                new_item.gen_birth_track()

                if "door" in new_item.type and not all([new_item.side_1, new_item.side_2]):
                    new_item.connect(self.grid)
                if add_circle:
                    self.grid.circles.append(new_item)

            else:
                self.grid.msg('ERROR - Could not produce item {0}'.format(
                    grid_util.get_short_name(name)))
        except Exception as e:
            self.grid.msg('ERROR - Failed to produce item %s' % name)
            self.grid.msg('ERROR - %s' % e)

        return new_item

    # --------------------------------------------------------------- #
    #                                                                 #
    #                              MAP                                #
    #                                                                 #
    # --------------------------------------------------------------- #
    def show_map(self, mybody):
        """ Shows the map room 999 """
        if not self.grid.current_room == "map":
            self.grid.previous_room = self.grid.current_room
            self.grid.change_room("map")
            self.grid.gen_map_dots()
            self.grid.draw_map = True

        else:
            self.grid.change_room(self.grid.previous_room)
            self.grid.draw_map = False
            # if mybody not in self.grid.circles:
            #     self.grid.circles.append(mybody)


    # --------------------------------------------------------------- #
    #                                                                 #
    #                           MOUSE MODES                           #
    #                                                                 #
    # --------------------------------------------------------------- #
    def enter_room(self, mybody, item):
        pass

    def collect(self, mybody, clicked_item):
        pass

    def drop(self, clicked, mybody, force=False):
        pass

    def consume(self, consumer, consumable):
        """
        Consume effects
        :param consumer: item obj, that will consume the consumable effects
        :param consumable: item obj, that has consumable effects or the effects as a string
        """
        consumed = False
        exhaust = False
        effects = None
        protected_types = ['trigger']

        if isinstance(consumable, str):
            effects = consumable.split()
        elif hasattr(consumer, "effects"):
            effects = consumable.effects.split()
            if consumable.consumable:
                exhaust = True

        if effects:
            # try:
            eff_msg = []
            effect_color = self.grid.white
            for effect in effects:

                # Exclude # (non-consumable) effects
                if not '#' in effect:
                    attr_str = ''
                    effect = effect.split(':')
                    eff_att = effect[0]
                    amount = int(effect[1])
                    if amount >= 0:
                        modifier_str = '+{0}'.format(abs(amount))
                    else:
                        modifier_str = '-{0}'.format(abs(amount))

                    if consumer.type not in protected_types:
                        if eff_att == 'max' and consumer.time:
                            consumer.max_time += amount
                            attr_str = 'max'

                        elif eff_att == 't' and consumer.time:
                            consumer.add_time(amount)
                            attr_str = 'time'

                    if attr_str:
                        eff_msg.append(modifier_str + ' ' + attr_str)

                # hash
                elif not consumer.birth_track:
                    if "#fight" in effect and hasattr(consumer, 'muscle') and not consumer.muscle in [None, '']:
                        if 'mybody' in consumable.type:
                            self.grid.msg('SCREEN - you fight %s' %
                                          grid_util.get_short_name(consumer.name).replace('_', ' '))
                        if 'mybody' in consumer.type:
                            self.grid.msg('SCREEN - you fight %s' %
                                          grid_util.get_short_name(consumable.name).replace('_', ' '))
                        consumable.muscle_test(consumer, self.grid)

                    if "#flirt" in effect and "lover" in consumer.type and hasattr(consumable, 'ego'):
                        if 'mybody' in consumable.type:
                           self.grid.msg('SCREEN - flirt %s' %
                                         grid_util.get_short_name(consumer.name).replace('_', ' '))
                        if 'mybody' in consumer.type:
                            self.grid.msg('SCREEN - flirt %s' %
                                          grid_util.get_short_name(consumable.name).replace('_', ' '))

                        # consumable.muscle_test(consumer, self.grid)
                        consumer.love(self.grid, amount = consumable.ego)


            if eff_msg:
                consumed = True
                if 'mybody' in consumer.type:
                    if not isinstance(consumable, str):
                        self.grid.msg('SCREEN - you eat %s' %
                                       grid_util.get_short_name(consumable.name).replace('_', ' '))
                    for effm in eff_msg:
                        self.grid.msg('SCREEN - {0}'.format(effm))

                consumer.gen_effect_track(effect_color)

        if exhaust and consumed:
            consumable.destroy(self.grid)
        return consumed