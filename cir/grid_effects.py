# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                                                                                     #
#                                                   EFFECTS                                                           #
#                                                                                                                     #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import grid_util


class GameEffects(object):

    def __init__(self, grid=None):
        self.grid = grid
        self.food_unit = 10


    # --------------------------------------------------------------- #
    #                                                                 #
    #                             PRODUCE                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    def produce(self,
                product_name,
                pos=None,
                radius=None,
                time=None,
                add_circle=True,
                effects=None,
                panel=False):
        """
        Produces an item from the everything dict
        :param product_name: name of the item from the everything dict
        :param pos: set new position (optional)
        :param radius: set new radius (optional)
        :param birth: set new birth timer (optional)
        :param time: set new time (optional)
        :return: the new item object
        """
        new_item = None
        try:
            product_name = grid_util.get_short_name(product_name)
            new_item = self.grid.loader.load_item(product_name)
            new_item.name = new_item.name + '-' + str(time.time())
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


                if add_circle:
                    self.grid.circles.append(new_item)
                if panel:
                    self.grid.panel_circles[new_item.name] = new_item

            else:
                self.grid.msg('ERROR - Could not produce item {0}'.format(
                    grid_util.get_short_name(product_name)))
        except Exception as e:
            self.grid.msg('ERROR - Failed to produce item %s' % product_name)
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
    #                            SATELLITE                            #
    #                                                                 #
    # --------------------------------------------------------------- #
    def satellite(self, speed=3):
        trigger = self.produce(product_name="trigger",
                               pos=self.grid.center_tile,
                               time=2)
        trigger.range = 4.5
        trigger.vspeed = speed
        trigger.effects = "#scout"

        self.grid.loader.set_timers(trigger)
        trigger.birth_track = []
        trigger.gen_vibe_track(self.grid)

    # --------------------------------------------------------------- #
    #                                                                 #
    #                           ENTER ROOM                            #
    #                                                                 #
    # --------------------------------------------------------------- #
    def enter_room(self, mybody, item):
        """
        Changes the current room
        :param mybody: mybody instance
        :param item: enter / exit item
        """
        if mybody.pos in self.grid.adj_tiles(item.pos):
            mybody.move_track = mybody.move(self.grid, item.pos)
            self.grid.needs_to_change_room = True
        else:
            self.grid.msg("SCREEN - no enter")

    # --------------------------------------------------------------- #
    #                                                                 #
    #                         MOUSE MODES                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    def terminate_mode_click(self, item):
        """ Terminate """
        non_terminates = [
            "mybody",
            "option",
            "trigger",
            "placeholder",
        ]

        if not any(non_terminate in item.type for non_terminate in non_terminates):
            item.destroy(self.grid)


    # --------------------------------------------------------------- #
    #                                                                 #
    #                         MOUSE MODES                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    def collect(self, mybody, clicked_item):
        """ Collect item: add it to inventory options """
        if not any([clicked_item.birth_track, clicked_item.move_track]):
            inventory = mybody.inventory
            if len(inventory.options) < 6:

                # PRODUCE MODABLE ITEM AS OPTION
                item_as_option = self.produce(product_name='placeholder',
                                              pos=(),
                                              add_circle=False)
                item_as_option.name = clicked_item.name # + '-' + str(time.time())
                item_as_option.type = clicked_item.type + ' option'
                item_as_option.lvl = clicked_item.lvl
                item_as_option.modable = True
                item_as_option.consumable = clicked_item.consumable
                item_as_option.effects = clicked_item.effects
                item_as_option.color = mybody.inventory.color
                item_as_option.img = clicked_item.img
                setattr(item_as_option, "ober_item", mybody.inventory)
                if hasattr(clicked_item, "time"):
                    item_as_option.time = clicked_item.time

                # ADD IN BAG AND REMOVE FROM FIELD
                inventory.options[item_as_option.name] = item_as_option
                clicked_item.destroy(self.grid)
            else:
                self.grid.msg("SCREEN - no space")

            inventory.open_menu(self.grid)


    def empty_inventory(self, inventory_item, mybody):

        if self.grid.mouse_mode:
            if grid_util.get_short_name(self.grid.mouse_mode) in inventory_item.name:
                self.grid.clean_mouse()

        if inventory_item.name in self.grid.panel_circles.keys():
            del self.grid.panel_circles[inventory_item.name]
        del inventory_item.ober_item.options[inventory_item.name]

        # mybody.inventory.open_menu(self.grid)
    # --------------------------------------------------------------- #
    #                                                                 #
    #                          CONSUMABLES                            #
    #                                                                 #
    # --------------------------------------------------------------- #
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
                    amount = float(effect[1])
                    if amount >= 0:
                        modifier_str = '+{0}'.format(abs(amount))
                    else:
                        modifier_str = '-{0}'.format(abs(amount))

                    if consumer.type not in protected_types:
                        if eff_att == 'max' and consumer.time:
                            # consumer.time.limit += amount * self.food_unit
                            attr_str = 'max'

                        elif eff_att == 't' and consumer.time:
                            # consumer.time.update(amount * self.food_unit)
                            attr_str = 'life'

                        elif eff_att == 'sp' and hasattr(consumer, 'speed'):
                            consumer.change_speed(amount)
                            attr_str = 'speed'

                        elif eff_att == 'r' and hasattr(consumer, 'range'):
                            consumer.range += amount
                            attr_str = 'range'

                        elif eff_att == 'vsp' and hasattr(consumer, 'vspeed'):
                            consumer.vspeed += amount
                            attr_str = 'vibe speed'

                        elif eff_att == 'mus' and hasattr(consumer, 'muscle'):
                            consumer.muscle += amount
                            attr_str = 'muscle'

                        elif eff_att == 'ego' and hasattr(consumer, 'ego'):
                            consumer.ego += amount
                            attr_str = 'ego'

                        elif eff_att == 'keff' and hasattr(consumer, 'keff'):
                            consumer.keff += amount
                            attr_str = 'keff'

                        elif eff_att == 'vfreq' and hasattr(consumer, 'vfreq'):
                            consumer.vfreq.duration += amount
                            attr_str = 'frequency'

                        elif eff_att == 'tok' and hasattr(consumer, 'tok'):
                            consumer.tok += amount
                            attr_str = 'electricity'

                    if attr_str:
                        # BOOST
                        if len(effect) > 2:
                            negative_effect = "%s:-%s" % (eff_att, str(amount))
                            boost_duration = float(effect[2]) * self.food_unit
                            self.grid.loader.set_boost_timer(
                                duration = boost_duration,
                                effect = negative_effect,
                                boosted_item = consumer,
                                boost_item = consumable)
                            modifier_str += ' boost '

                        # add msg
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
                        if 'boost' in consumable.type:
                            self.grid.msg('SCREEN - %s boost over' %
                                          grid_util.get_short_name(consumable.boost_item).replace('_', ' '))
                            effect_color = self.grid.white
                        else:
                            self.grid.msg('SCREEN - you eat %s' %
                                          grid_util.get_short_name(consumable.name).replace('_', ' '))
                    for effm in eff_msg:
                        self.grid.msg('SCREEN - {0}'.format(effm))

                consumer.gen_effect_track(effect_color)

            # except Exception as e:
            #     self.grid.msg("ERROR - invalid effects '{0}' \n {1}".format(effects, e))

        if exhaust and consumed:
            consumable.destroy(self.grid)
        return consumed

    def drop(self, clicked, mybody, force=False):
        """
        Drops item
        """
        will_drop = force
        # Drop item on an empty tile
        if isinstance(clicked, tuple):
            if clicked not in self.grid.occupado_tiles.values() and clicked in self.grid.revealed_tiles.keys():
                if clicked in self.grid.adj_tiles(mybody.pos):
                    will_drop = True
                else:

                    self.grid.msg("SCREEN - no reach1")
            else:
                self.grid.msg("SCREEN - no place here1")

            if will_drop:
                for bag_item in mybody.inventory.options.values():
                    if self.grid.mouse_mode in bag_item.name:
                        item_name = grid_util.get_short_name(self.grid.mouse_mode)
                        dropped_item = self.produce(item_name, clicked)
                        if dropped_item:
                            if hasattr(bag_item, "time"):
                                dropped_item.time = bag_item.time
                            self.empty_inventory(bag_item, mybody)
                            break
        # Drop item from inventory to body and consume
        else:
            if clicked:
                # Drop to adj only or to self (telekinesis)
                if clicked.pos in self.grid.adj_tiles(mybody.pos) or 'mybody' in clicked.type:
                    will_drop = True
                else:
                    self.grid.msg("SCREEN - no reach")
            else:
                self.grid.msg("SCREEN - No place here")

            if will_drop:
                for bag_item in mybody.inventory.options.values():
                    if self.grid.mouse_mode and self.grid.mouse_mode in bag_item.name:
                        if 'vendor' in clicked.type:
                            if clicked.trade(bag_item, self.grid):
                                self.empty_inventory(bag_item, mybody)
                        elif bag_item.consumable and not clicked in mybody.inventory.options.values():
                            if self.consume(clicked, bag_item):
                                self.empty_inventory(bag_item, mybody)
                                break
