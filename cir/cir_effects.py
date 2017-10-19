# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                                                                                     #
#                                                   EFFECTS                                                           #
#                                                                                                                     #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import os
import time
from cir_editor import Editor
import cir_utils

class GameEffects(object):

    def __init__(self, grid=None):
        self.grid = grid

        if self.grid.show_editor:
            self.editor = Editor(grid=self.grid)
        else:
            self.editor = None

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
                add_to_items=True):
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
        product_name = cir_utils.get_short_name(product_name)
        new_item = self.grid.loader.load_item(product_name)

        if pos:
            new_item.pos = pos
        if radius:
            new_item.radius = radius
            new_item.default_radius = radius
        if vfreq:
            new_item.vfreq.duration = vfreq
        if lifespan:
            new_item.lifespan = lifespan

        new_item.default_img = new_item.img
        new_item.available = True
        new_item.gen_birth_track()
        if add_to_items:
            if new_item.name in self.grid.occupado_tiles.keys():
                new_item.name = new_item.name + '-' + str(time.time())
            self.grid.items.append(new_item)

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

    def mitosis(self, item):
        """
        :param item: item to copy
        """
        for other_item in self.grid.items:
            if "new copy" in other_item.name:
                other_item.name = str(item.name + " - copy-" + str(time.time()))

            if item.name in other_item.name or other_item.name in str(item.name + " - copy"):
                empty_tile = other_item.check_for_empty_adj_tile(self.grid)
                if empty_tile:
                    if other_item.speed and not other_item.birth_track and not other_item.move_track:
                        self.cell_division(other_item)

    # --------------------------------------------------------------- #
    #                                                                 #
    #                              MAP                                #
    #                                                                 #
    # --------------------------------------------------------------- #
    def show_map(self, my_body):
        """ Shows the map room """

        self.grid.capture_room()

        if not self.grid.current_room == "999":
            self.grid.previous_room = self.grid.current_room
            self.grid.change_room("999")
            diff = 10
            try:
                for root, dirs, files in os.walk(self.grid.tmp_dir):

                    for file in files:

                        if file.endswith("png"):


                            img_file = os.path.join(root, file)
                            name = os.path.splitext(file)[0]
                            image = self.grid.pygame.image.load(img_file)

                            image_height = self.grid.tile_radius * 2
                            image = self.grid.pygame.transform.scale(
                                image, (
                                    image_height - diff,
                                    image_height))
                            pos = self.grid.tile_dict[name]
                            map_tile = self.produce(product_name="trigger", pos=pos)

                            map_tile.type = "map_tile"
                            map_tile.img = image
                            map_tile.available = True
                            self.grid.revealed_tiles.append(pos)

            except Exception as e:
                self.grid.msg("ERROR - Could not show map: {0}".format(e))

        else:
            self.grid.change_room(self.grid.previous_room)
            if my_body not in self.grid.items:
                self.grid.items.append(my_body)


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
            if my_body.in_menu:
                my_body.close_menu(self.grid)
            self.grid.needs_to_change_room = True
        else:
            self.grid.msg("SCREEN - door is far")
            item.in_menu = False

    # --------------------------------------------------------------- #
    #                                                                 #
    #                         MOUSE MODES                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    def echo_mode_click(self, current_tile, my_body):
        """ Signal effect """
        self.grid.msg("SCREEN - Echo!")
        if not cir_utils.in_circle(my_body.pos, my_body.radius, current_tile) and not my_body.move_track:
            signal = self.produce("signal",
                                  my_body.pos,
                                  radius=int(self.grid.tile_radius / 3)
                                  )
            signal.color = my_body.color
            signal.direction = signal.get_aiming_direction(self.grid, current_tile)[1]


    def terminate_mode_click(self, current_tile):
        """ Terminate this shit """
        non_terminates = [
            "my_body",
            "editor",
            "option",
            "trigger",
            "placeholder"
        ]
        if not any(non_terminate in current_tile.type for non_terminate in non_terminates):
            current_tile.destroy(self.grid)


    # --------------------------------------------------------------- #
    #                                                                 #
    #                         MOUSE MODES                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    def collect(self, my_body, clicked_item):
        """ Collect item: add it to inventory options """
        if not any([clicked_item.birth_track, clicked_item.move_track]):

            # CHECK FOR EMPTY SLOT IN BAG
            inventory_placeholder = None

            inventory = my_body.inventory
            reopen_inventory = False

            if inventory.in_menu:
                inventory.close_menu(self.grid)
                reopen_inventory = True
                backup_mouse_mode = self.grid.mouse_mode
                backup_mouse_img = self.grid.mouse_img

            for empty_item in inventory.options.values():
                if "inventory_placeholder" in empty_item.name:
                    inventory_placeholder = empty_item
                    break

            # PRODUCE MODABLE ITEM AS OPTION
            if inventory_placeholder:
                item_name = cir_utils.get_short_name(inventory_placeholder.name)

                item_as_option = self.produce(product_name=item_name,
                                              pos=inventory_placeholder.pos,
                                              add_to_items=False)

                item_as_option.name = clicked_item.name + '-' + str(time.time())
                item_as_option.type = "option"
                item_as_option.modable = True
                item_as_option.consumable = clicked_item.consumable
                item_as_option.effects = clicked_item.effects
                item_as_option.color = clicked_item.color
                item_as_option.img = clicked_item.img
                item_as_option.uses = clicked_item.uses
                if hasattr(clicked_item, "lifespan"):
                    item_as_option.lifespan = clicked_item.lifespan
                # ADD IN BAG AND REMOVE FROM FIELD
                if inventory_placeholder in my_body.inventory.options.values():
                    my_body.inventory.options = {k: v for k, v in my_body.inventory.options.items() if
                                                 not v == inventory_placeholder}
                inventory.options[item_as_option.name] = item_as_option
                clicked_item.destroy(self.grid)
            else:
                self.grid.msg("SCREEN - No space in bag")

            if reopen_inventory:
                inventory.open_menu(self.grid)
                self.grid.mouse_mode = backup_mouse_mode
                self.grid.mouse_img = backup_mouse_img

    def empty_inventory(self, inventory_item):

        print "Hmm", inventory_item.name, inventory_item.uses
        inventory_item.uses -= 1
        if inventory_item.uses < 1:
            if self.grid.mouse_mode:
                if cir_utils.get_short_name(self.grid.mouse_mode) in inventory_item.name:
                    self.grid.clean_mouse()
            inventory_item.name = "inventory_placeholder" + '-' + str(time.time())
            inventory_item.modable = False
            inventory_item.color = None
            inventory_item.img = None
            inventory_item.effects = ''
            inventory_item.uses = 0
            inventory_item.lifespan = None

    def drop(self, clicked_tile, my_body):
        """
        Drops item
        """

        # Drop item from inventory to body and consume
        if clicked_tile == my_body.pos and not my_body.effect_track:
            for bag_item in my_body.inventory.options.values():
                if self.grid.mouse_mode in bag_item.name and bag_item.uses >= 1:
                    if bag_item.consumable:
                        self.consume(my_body, bag_item)
                        self.empty_inventory(bag_item)
                        break

        # Drop item on an empty tile
        elif clicked_tile not in self.grid.occupado_tiles.values() and clicked_tile in self.grid.revealed_tiles:
            for bag_item in my_body.inventory.options.values():
                if self.grid.mouse_mode in bag_item.name and bag_item.uses >= 1:
                    item_name = cir_utils.get_short_name(self.grid.mouse_mode)
                    dropped_item = self.produce(item_name, clicked_tile)
                    if hasattr(bag_item, "lifespan"):
                        dropped_item.lifespan = bag_item.lifespan
                    self.empty_inventory(bag_item)
                    break
        else:
            self.grid.msg("SCREEN - No place here")


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

        effects = None
        protected_types = ['trigger']

        if isinstance(consumable, str):
            effects = consumable.split()
        elif hasattr(consumator, "effects"):
            effects = consumable.effects.split()

        if effects:
            try:
                if consumator.type == "my_body":
                    self.grid.msg("SCREEN - you eat {0}".format(cir_utils.get_short_name(consumable.name)))

                for effect in effects:
                    effect = effect.split("_")
                    eff_att = effect[0]
                    amount = float(effect[1])
                    if amount >= 0:
                        modifier_str = "+{0}".format(abs(int(amount)))
                    else:
                        modifier_str = "-{0}".format(abs(int(amount)))
                    attr_str = ''
                    if not consumator.type in protected_types:
                        if eff_att == 'LS' and consumator.lifespan:
                            consumator.lifespan.limit += amount
                            attr_str = 'max life'

                        elif eff_att == 'LP' and consumator.lifespan:
                            consumator.lifespan.update(amount)
                            attr_str = 'life'

                        elif eff_att == 'SP' and hasattr(consumator, "speed"):
                            consumator.change_speed(amount)
                            attr_str = 'speed'

                    if attr_str:
                        if consumable.color:
                            consumator.gen_effect_track(consumable.color)
                        else:
                            consumator.gen_effect_track(self.grid.white)

                    if consumator.type == "my_body":
                        self.grid.msg("SCREEN - {0} {1}".format(modifier_str, attr_str))

            except Exception as e:
                self.grid.msg("ERROR - invalid effects '{0}' \n {1}".format(effects, e))
