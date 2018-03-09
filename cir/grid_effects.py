# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                                                                                     #
#                                                   EFFECTS                                                           #
#                                                                                                                     #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import time
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
                vfreq=None,
                lifespan=None,
                add_circle=True,
                effects=None,
                panel=False):
        """
        Produces an item from the everything dict
        :param product_name: name of the item from the everything dict
        :param pos: set new position (optional)
        :param radius: set new radius (optional)
        :param birth: set new birth timer (optional)
        :param vfreq: set new vibe frequency (optional)
        :param lifespan: set new lifespan (optional)
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
                    new_item.default_radius = radius
                if vfreq:
                    new_item.vfreq.duration = vfreq
                if effects:
                    new_item.effects = effects
                if lifespan:
                    new_item.lifespan = lifespan
                else:
                    if hasattr(new_item, 'lifespan'):
                        if new_item.lifespan:
                            new_item.lifespan.restart()

                new_item.default_img = new_item.img
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
    #                             MITOSIS                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    def cell_division(self, item):
        """
        Creates a placeholder in the empty tile.
        Than creates a copy of the item and moves it into the placeholder
        They're being cleaned with the clean_placeholder function
        """
        empty_tile = item.check_for_empty_adj_tile(self.grid)
        if empty_tile:
            placeholder = self.produce("placeholder", empty_tile)
            placeholder.name = "placeholder-" + str(time.time())
            searched_name = item.name.split()[0]
            new_copy = self.produce(searched_name, item.pos)
            new_copy.color = item.color
            new_copy.img = item.img
            new_copy.speed = item.speed
            new_copy.radius = item.radius
            new_copy.name = "new copy-" + str(time.time())
            new_copy.birth_track = []
            new_copy.move_track = new_copy.move_to_tile(self.grid, empty_tile)
            if new_copy.lifespan:
                new_copy.lifespan.duration = 10
                new_copy.lifespan.restart()

    def mitosis(self, cir):
        """
        :param cir: cir to copy
        """
        for other_cir in self.grid.circles:
            if "new copy" in other_cir.name:
                other_cir.name = str(cir.name + " - copy-" + str(time.time()))

            if cir.name in other_cir.name or other_cir.name in str(cir.name + " - copy"):
                empty_tile = other_cir.check_for_empty_adj_tile(self.grid)
                if empty_tile:
                    if other_cir.speed and not other_cir.birth_track and not other_cir.move_track:
                        self.cell_division(other_cir)

    # --------------------------------------------------------------- #
    #                                                                 #
    #                              MAP                                #
    #                                                                 #
    # --------------------------------------------------------------- #
    def show_map(self, my_body):
        """ Shows the map room 999 """
        if not self.grid.current_room == "map":
            self.grid.previous_room = self.grid.current_room
            self.grid.change_room("map")
            self.grid.gen_map_dots()
            self.grid.draw_map = True

        else:
            self.grid.change_room(self.grid.previous_room)
            self.grid.draw_map = False
            # if my_body not in self.grid.circles:
            #     self.grid.circles.append(my_body)


    # --------------------------------------------------------------- #
    #                                                                 #
    #                            SATELLITE                            #
    #                                                                 #
    # --------------------------------------------------------------- #
    def satellite(self, speed=3):
        trigger = self.produce(product_name="trigger",
                               pos=self.grid.center_tile,
                               lifespan=2)
        trigger.range = 4.5
        trigger.vspeed = speed
        trigger.effects = "#scout"

        self.grid.loader.set_timers(trigger)
        trigger.vfreq = None
        trigger.birth_track = []
        trigger.gen_vibe_track(self.grid)

    # --------------------------------------------------------------- #
    #                                                                 #
    #                           ENTER ROOM                            #
    #                                                                 #
    # --------------------------------------------------------------- #
    def enter_room(self, my_body, item):
        """
        Changes the current room
        :param my_body: my_body instance
        :param item: enter / exit item
        """
        if my_body.pos in self.grid.adj_tiles(item.pos):
            my_body.move_track = my_body.move_to_tile(self.grid, item.pos)
            self.grid.needs_to_change_room = True
        else:
            self.grid.msg("SCREEN - no enter")

    # --------------------------------------------------------------- #
    #                                                                 #
    #                         MOUSE MODES                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    def signal_mode_click(self, current_tile, my_body):
        """ Signal effect """
        if not grid_util.in_circle(my_body.pos, my_body.radius, current_tile) and not my_body.move_track:
            signal = self.produce("signal",
                                  my_body.pos,
                                  radius=int(self.grid.tile_radius / 3)
                                  )
            if signal:
                signal.color = my_body.color
                signal.direction = signal.get_aiming_direction(self.grid, current_tile)[1]


    def terminate_mode_click(self, item):
        """ Terminate this shit """
        non_terminates = [
            "my_body",
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
    def collect(self, my_body, clicked_item):
        """ Collect item: add it to inventory options """
        if not any([clicked_item.birth_track, clicked_item.move_track]):
            inventory = my_body.inventory
            # reopen_inventory = False
            if len(inventory.options) < 6:

                # backup_mouse_mode = self.grid.mouse_mode
                # backup_mouse_img = self.grid.mouse_img


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
                item_as_option.color = my_body.inventory.color
                item_as_option.img = clicked_item.img
                setattr(item_as_option, "ober_item", my_body.inventory)
                if hasattr(clicked_item, "lifespan"):
                    item_as_option.lifespan = clicked_item.lifespan

                # ADD IN BAG AND REMOVE FROM FIELD
                inventory.options[item_as_option.name] = item_as_option
                clicked_item.destroy(self.grid)
            else:
                self.grid.msg("SCREEN - no space")

            inventory.open_menu(self.grid)
            # self.grid.mouse_mode = backup_mouse_mode
            # self.grid.mouse_img = backup_mouse_img

    def empty_inventory(self, inventory_item, my_body):

        if self.grid.mouse_mode:
            if grid_util.get_short_name(self.grid.mouse_mode) in inventory_item.name:
                self.grid.clean_mouse()

        if inventory_item.name in self.grid.panel_circles.keys():
            del self.grid.panel_circles[inventory_item.name]
        del inventory_item.ober_item.options[inventory_item.name]

        # for iitem in my_body.inventory.options.values():
        #

        my_body.inventory.open_menu(self.grid)
    # --------------------------------------------------------------- #
    #                                                                 #
    #                          CONSUMABLES                            #
    #                                                                 #
    # --------------------------------------------------------------- #
    def consume(self, consumator, consumable):
        """
        Consume effects
        :param consumator: item obj, that will consume the consumable effects
        :param consumable: item obj, that has consumable effects or the effects as a string
        """
        consumed = False
        exhaust = False
        effects = None
        protected_types = ['trigger']

        if isinstance(consumable, str):
            effects = consumable.split()
        elif hasattr(consumator, "effects"):
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
                        modifier_str = '+{0}'.format(abs(int(amount)))
                    else:
                        modifier_str = '-{0}'.format(abs(int(amount)))

                    if consumator.type not in protected_types:
                        if eff_att == 'max' and consumator.lifespan:
                            consumator.lifespan.limit += amount * self.food_unit
                            attr_str = 'max'

                        elif eff_att == 't' and consumator.lifespan:
                            consumator.lifespan.update(amount * self.food_unit)
                            attr_str = 'life'

                        elif eff_att == 'sp' and hasattr(consumator, 'speed'):
                            consumator.change_speed(amount)
                            attr_str = 'speed'

                        elif eff_att == 'r' and hasattr(consumator, 'range'):
                            consumator.range += amount
                            attr_str = 'range'

                        elif eff_att == 'vsp' and hasattr(consumator, 'vspeed'):
                            consumator.vspeed += amount
                            attr_str = 'vibe speed'

                        elif eff_att == 'hyg' and hasattr(consumator, 'hyg'):
                            consumator.hyg += amount
                            attr_str = 'hygiene'

                        elif eff_att == 'mus' and hasattr(consumator, 'muscle'):
                            consumator.muscle += amount
                            attr_str = 'muscle'

                        elif eff_att == 'ego' and hasattr(consumator, 'ego'):
                            consumator.ego += amount
                            attr_str = 'ego'

                        elif eff_att == 'stress' and hasattr(consumator, 'stress'):
                            consumator.stress += amount
                            attr_str = 'stress'

                        elif eff_att == 'joy' and hasattr(consumator, 'joy'):
                            consumator.joy += amount
                            attr_str = 'joy'

                        elif eff_att == 'vfreq' and hasattr(consumator, 'vfreq'):
                            consumator.vfreq.duration += amount
                            attr_str = 'frequency'

                        elif eff_att == 'tok' and hasattr(consumator, 'tok'):
                            consumator.tok += amount
                            attr_str = 'electricity'

                    if attr_str:
                        eff_msg.append(modifier_str + ' ' + attr_str)
                        # BOOST
                        if len(effect) > 2:
                            negative_effect = "%s:-%s" % (eff_att, str(amount))
                            boost_duration = float(effect[2]) * self.food_unit
                            self.grid.loader.set_boost_timer(
                                duration = boost_duration,
                                effect = negative_effect,
                                boosted_item = consumator,
                                boost_item = consumable)

                elif "#fight" in effect and hasattr(consumator, 'muscle') and not consumator.muscle in [None, '']:
                    if 'my_body' in consumable.type:
                        self.grid.msg('SCREEN - you fight %s' %
                                      grid_util.get_short_name(consumator.name).replace('_', ' '))
                    if 'my_body' in consumator.type:
                        self.grid.msg('SCREEN - you fight %s' %
                                      grid_util.get_short_name(consumable.name).replace('_', ' '))
                    consumable.muscle_test(consumator, self.grid)


            if eff_msg:
                consumed = True
                if 'my_body' in consumator.type:
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

                consumator.gen_effect_track(effect_color)

            # except Exception as e:
            #     self.grid.msg("ERROR - invalid effects '{0}' \n {1}".format(effects, e))

        if exhaust and consumed:
            consumable.destroy(self.grid)
        return consumed

    def drop(self, clicked, my_body, force=False):
        """
        Drops item
        """
        will_drop = force
        # Drop item on an empty tile
        if isinstance(clicked, tuple):
            if clicked not in self.grid.occupado_tiles.values() and clicked in self.grid.revealed_tiles.keys():
                if clicked in self.grid.adj_tiles(my_body.pos):
                    will_drop = True
                else:

                    self.grid.msg("SCREEN - no reach1")
            else:
                self.grid.msg("SCREEN - no place here1")

            if will_drop:
                for bag_item in my_body.inventory.options.values():
                    if self.grid.mouse_mode in bag_item.name:
                        item_name = grid_util.get_short_name(self.grid.mouse_mode)
                        dropped_item = self.produce(item_name, clicked)
                        if dropped_item:
                            if hasattr(bag_item, "lifespan"):
                                dropped_item.lifespan = bag_item.lifespan
                            self.empty_inventory(bag_item, my_body)
                            break
        # Drop item from inventory to body and consume
        else:
            if clicked:
                # Drop to adj only or to self (telekinesis)
                if clicked.pos in self.grid.adj_tiles(my_body.pos) or 'my_body' in clicked.type:
                    will_drop = True
                else:
                    self.grid.msg("SCREEN - no reach")
            else:
                self.grid.msg("SCREEN - No place here")

            if will_drop:
                for bag_item in my_body.inventory.options.values():
                    if self.grid.mouse_mode and self.grid.mouse_mode in bag_item.name:
                        if 'vendor' in clicked.type:
                            if clicked.trade(bag_item, self.grid):
                                self.empty_inventory(bag_item, my_body)
                        elif bag_item.consumable and not clicked in my_body.inventory.options.values():
                            if self.consume(clicked, bag_item):
                                self.empty_inventory(bag_item, my_body)
                                break
