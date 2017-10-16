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
        new_item = self.grid.loader.load_item(product_name)

        if radius:
            new_item.radius = radius
            new_item.default_radius = radius
        if vfreq:
            new_item.vfreq.duration = vfreq
        if pos:
            new_item.pos = pos
        if lifespan:
            new_item.lifespan = lifespan

        new_item.default_img = new_item.img
        new_item.available = True
        new_item.gen_birth_track()
        if add_to_items:
            if new_item.name in self.grid.occupado_tiles.keys():
                new_item.name = new_item.name + str(time.time())
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
            placeholder.name = "placeholder" + str(time.time())
            searched_name = item.name.split()[0]
            new_copy = self.produce(searched_name, item.pos)
            new_copy.color = item.color
            new_copy.img = item.img
            new_copy.speed = item.speed
            new_copy.radius = item.radius
            new_copy.name = "new copy" + str(time.time())
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
                other_item.name = str(item.name + " - copy" + str(time.time()))

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
    #                          CONSUMABLES                            #
    #                                                                 #
    # --------------------------------------------------------------- #
    def consume(self, consumator, consumable):

        # self.grid.msg("SCREEN - nom nom nom")
        effects = None

        if isinstance(consumable, str):
            effects = consumable.split()
        elif hasattr(consumator, "effects"):
            effects = consumable.effects.split()
            if effects and consumator.type == "my_body":
                self.grid.msg("SCREEN - u eat {0}".format(cir_utils.get_short_name(consumable.name)))

        if effects:
            try:
                for effect in effects:
                    effect = effect.split("_")
                    eff_att = effect[0]
                    amount = float(effect[1])
                    abs_amount = abs(int(amount))

                    if eff_att == 'LS' and consumator.lifespan:
                        consumator.gen_effect_track(consumable.color)
                        consumator.lifespan.limit += amount
                        if amount >= 0:
                            self.grid.msg(u"SCREEN - {0}: max life ↑{1}".format(consumator.name, abs_amount))
                        else:
                            self.grid.msg(u"SCREEN - {0}: max life ↓€{1}".format(consumator.name, abs_amount))

                    elif eff_att == 'LP' and consumator.lifespan:
                        consumator.gen_effect_track(consumable.color)
                        consumator.lifespan.update(amount)
                        if amount >= 0:
                            self.grid.msg(u"SCREEN - {0}: life ↑{1}".format(consumator.name, abs_amount))
                        else:
                            self.grid.msg(u"SCREEN - {0}: life ↓{1}".format(consumator.name, abs_amount))

                    elif eff_att == 'SP':
                        if hasattr(consumator, "speed"):
                            consumator.gen_effect_track(consumable.color)
                            consumator.change_speed(amount)
                            if amount >= 0:
                                self.grid.msg(u"SCREEN - speed ↑{0}".format(abs_amount))
                            else:
                                self.grid.msg(u"SCREEN - speed ↓{0}".format(abs_amount))
            except Exception as e:
                self.grid.msg("ERROR - invalid effects '{0}' \n {1}".format(effects, e))
