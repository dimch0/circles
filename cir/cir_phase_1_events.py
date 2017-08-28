# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                                                                                     #
#                                                    Effects                                                          #
#                                                                                                                     #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import os
import time
import cir_utils


class GameEffects(object):

    def __init__(self, grid=None):
        self.grid = grid

    # --------------------------------------------------------------- #
    #                                                                 #
    #                             PRODUCE                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    def produce(self,
                product_name,
                pos=None,
                radius=None,
                birth=None,
                vibe_freq=None,
                lifespan=None,
                add_to_items=True):
        """
        Produces an item from the everything dict
        :param product_name: name of the item from the everything dict
        :param pos: set new position (optional)
        :param radius: set new radius (optional)
        :param birth: set new birth timer (optional)
        :param vibe_freq: set new vibe frequency (optional)
        :param lifespan: set new lifespan (optional)
        :return: the new item object
        """
        new_item = self.grid.loader.load_item(product_name)

        if radius:
            new_item.radius = radius
        if not birth == None:
            new_item.birth_time.duration = birth
        if vibe_freq:
            new_item.vibe_freq.duration = vibe_freq
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
            print("START MITO", item.name)

            if "new copy" in other_item.name:
                other_item.name = str(item.name + " - copy" + str(time.time()))

            if item.name in other_item.name or other_item.name in str(item.name + " - copy"):
                empty_tile = other_item.check_for_empty_adj_tile(self.grid)
                if empty_tile:
                    if other_item.speed and not other_item.birth_track and not other_item.move_track:
                        self.cell_division(other_item)

            print("FINISH MITO", item.name)

    # --------------------------------------------------------------- #
    #                                                                 #
    #                         MOUSE MODES                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    # DROP ITEM
    # def shit_mode_click(self, current_tile):
    #     """
    #     For mode 'shit', if clicked produces an item and exhausts mode uses
    #     :param current_tile: the clicked circle
    #     """
    #     for bag_item in self.grid.mode_vs_options["bag"]:
    #         if bag_item.name == mouse_mode:
    #             if bag_item.uses:
    #                 if current_tile not in self.grid.occupado_tiles.values():
    #                     self.produce("shit", current_tile)
    #                     bag_item.uses -= 1
    #                     return 1

    def laino_mode_click(self, current_tile):
        if current_tile not in self.grid.occupado_tiles.values() and current_tile in self.grid.revealed_tiles:
            self.produce("product_shit", current_tile)

    def see_mode_click(self, current_tile):
        if current_tile not in self.grid.occupado_tiles.values() and current_tile in self.grid.revealed_tiles:
            new_observer = self.produce("observer", current_tile)
            new_observer.lifespan.restart()

    def echo_mode_click(self, current_tile, my_body):
        """ Signal effect """
        print("Echo!")
        if not cir_utils.in_circle(my_body.pos, my_body.radius, current_tile) and not my_body.move_track:
            signal = self.produce("signal",
                                  my_body.pos,
                                  radius=int(self.grid.tile_radius / 3),
                                  birth=0)
            signal.direction = signal.get_aiming_direction(self.grid, current_tile)[1]

    def eat_mode_click(self, item):
        """ Eat that shit """
        print("Nom nom nom")
        item.destroy(self.grid)

    def terminate(self, item):
        """ Eat that shit """
        non_terminates = [
            "my_body",
            "editor",
            "option",
            "trigger",
            "placeholder"
            ]
        if not any(non_terminate in item.type for non_terminate in non_terminates):
            item.destroy(self.grid, fast=True)

    # --------------------------------------------------------------- #
    #                                                                 #
    #                           COLLECT                               #
    #                                                                 #
    # --------------------------------------------------------------- #
    def collect(self, my_body, clicked_item):
        """ Collect item: add it to bag options """
        # CHECK FOR EMPTY SLOT IN BAG
        bag_placeholder = None
        bag = [item for item in self.grid.rooms["ALL"]["items"] if item.name == "bag"][0]

        for empty_name, empty_item in bag.options.items():
            if "bag_placeholder" in empty_name:
                bag_placeholder = empty_item
                break

        # PRODUCE MODABLE ITEM AS OPTION
        if bag_placeholder:
            item_as_option = self.produce(product_name=bag_placeholder.name,
                                          pos=bag_placeholder.pos,
                                          birth=0,
                                          add_to_items=False)
            item_as_option.name = clicked_item.name + str(time.time())
            item_as_option.type = "option"
            item_as_option.modable = True
            item_as_option.color = self.grid.yellow
            item_as_option.img = clicked_item.img
            # ADD IN BAG AND REMOVE FROM FIELD
            del bag.options[bag_placeholder.name]
            bag.options[item_as_option.name] = item_as_option
            clicked_item.destroy(self.grid, fast=True)
        else:
            print("No space in bag")

    # --------------------------------------------------------------- #
    #                                                                 #
    #                          ENTER EFFECTS                          #
    #                                                                 #
    # --------------------------------------------------------------- #
    def enter_effect(self, my_body, item):
        """
        Changes the current room
        :param my_body: my_body instance
        :param item: enter / exit item
        """
        if my_body.pos in self.grid.adj_tiles(item.pos):
            my_body.move_track = my_body.move_to_tile(self.grid, item.pos)
            self.grid.needs_to_change_room = True
        else:
            print("it far")
            item.in_menu = False


    # --------------------------------------------------------------- #
    #                                                                 #
    #                           KEY EVENTS                            #
    #                                                                 #
    # --------------------------------------------------------------- #
    def execute_key_events(self, event, my_body):
        # --------------------------------------------------------------- #
        #                             ESCAPE                              #
        # --------------------------------------------------------------- #
        if event.key == self.grid.pygame.K_ESCAPE:
            if not self.grid.game_menu:
                self.grid.rename_button("replay", "play")
                self.grid.game_menu = True

        # --------------------------------------------------------------- #
        #                             SPACE                               #
        # --------------------------------------------------------------- #
        if event.key == self.grid.pygame.K_SPACE:

            # GEN RADAR
            my_body.gen_radar_track(self.grid)

            # DEBUG PRINT
            cir_utils.debug_print_space(self.grid, my_body)

        # --------------------------------------------------------------- #
        #                             NUMBERS                             #
        # --------------------------------------------------------------- #
        elif event.key == self.grid.pygame.K_1:
            print(">>>> key 1")
            self.grid.change_room("12_12")
        elif event.key == self.grid.pygame.K_2:
            print(">>>> key 2")
            self.grid.change_room("12_10")
        elif event.key == self.grid.pygame.K_3:
            print(">>>> key 3")
            self.grid.change_room("12_8")
        elif event.key == self.grid.pygame.K_4:
            print(">>>> key 4")
            self.grid.change_room("12_6")

        # --------------------------------------------------------------- #
        #                             OTHER                               #
        # --------------------------------------------------------------- #
        elif not my_body.in_menu:
            my_body.gen_direction(self.grid.pygame, self.grid, event)


    # --------------------------------------------------------------- #
    #                                                                 #
    #                             EDITOR                              #
    #                                                                 #
    # --------------------------------------------------------------- #
    def editor(self, item, my_body):
        """ EDITOR CLICKS """

        # MAPS
        if item.name == "EDITOR6":

            self.grid.capture_room()

            if not self.grid.current_room == "999":
                self.grid.previous_room = self.grid.current_room
                self.grid.change_room("999")
                diff = 10

                try:
                    for root, dirs, files in os.walk(self.grid.maps_dir):
                        for file in files:
                            img_file = os.path.join(root, file)
                            name = os.path.splitext(file)[0]
                            image = self.grid.pygame.image.load(img_file)
                            image_height = self.grid.tile_radius * 2
                            image = self.grid.pygame.transform.scale(
                                image, (
                                    image_height - diff,
                                    image_height))

                            pos = self.grid.tile_dict[name]

                            map_tile = self.produce(product_name="trigger",
                                                    pos=pos)
                            map_tile.type = "map_tile"
                            map_tile.img = image
                            map_tile.available = True

                            self.grid.revealed_tiles.append(pos)

                except Exception as e:
                    print("ERROR, could not show map - ", e)

            else:
                self.grid.change_room(self.grid.previous_room)
                if my_body not in self.grid.items:
                    self.grid.items.append(my_body)

        # CAMERA
        elif item.name == "EDITOR7":
            self.grid.capture_room()

        elif item.name == "EDITOR10":
            my_body.vibe_speed += 0.1

        if item.name == "EDITOR11":
            if my_body.lifespan:
                my_body.lifespan.update(10)

        elif item.name == "EDITOR12":
            if my_body.lifespan:
                my_body.lifespan.update(-10)

        elif item.name == "EDITOR13":
            my_body.img = self.grid.images.ape
            my_body.default_img = self.grid.images.ape
            my_body.speed = 10

        elif item.name == "EDITOR14":
            my_body.lifespan = None
            # my_body.lifespan.update(200)

        elif item.name == "EDITOR15" and not self.grid.current_room == "999":
            trigger = self.produce(product_name="trigger",
                                   pos=self.grid.center_tile,
                                   lifespan=1.5)
            trigger.range = 4
            trigger.vibe_speed = 3
            trigger.birth_time = 0

            self.grid.loader.set_timers(trigger)
            trigger.vibe_freq = None
            trigger.birth_track = []
            trigger.gen_radar_track(self.grid)

        elif item.name == "EDITOR16":
            if my_body.lifespan:
                my_body.lifespan.duration = 60
                my_body.lifespan.restart()

        elif item.name == "EDITOR17":
            self.grid.scenario = 'scenario_2'
            self.grid.game_over = True

        elif item.name == "EDITOR18":
            my_body.gen_fat()



    # --------------------------------------------------------------- #
    #                           CLICK ITEMS                           #
    # --------------------------------------------------------------- #
    def click_items(self, clicked_item, my_body):
        """
        Check if clicked on an event
        :param clicked_item: Item clicked on!
        :param my_body: my_body instance
        """
        mouse_mode = self.grid.mouse_mode

        # EDITOR CLICK
        self.editor(clicked_item, my_body)

        # EAT
        if mouse_mode in ["eat"]:
            if clicked_item.consumable:
                self.eat_mode_click(clicked_item)

        # TERMINATE
        elif mouse_mode in ["EDITOR9"]:
            self.terminate(clicked_item)

        # COLLECT
        elif mouse_mode in ["collect"]:
            if clicked_item.collectible:
                self.collect(my_body, clicked_item)

        # ENTER
        elif "Enter" in clicked_item.name:
            self.enter_effect(my_body, clicked_item)

        # OPTIONS
        elif clicked_item.type == "option":

            ober_item = clicked_item.get_ober_item(self.grid)
            if ober_item:

                # SUICIDE
                if clicked_item.name == "suicide":
                    ober_item.destroy(self.grid)

                # MITOSIS
                elif clicked_item.name == "mitosis":
                    self.mitosis(ober_item)
                # SMEL
                elif clicked_item.name == "smel":
                    print("Sniff hair")

                # MEDI
                elif clicked_item.name == "medi":
                    print("Ommmm")
                    ober_item.range += 3
                    ober_item.vibe_speed += 3
                    my_body.gen_radar_track(self.grid)
                    ober_item.vibe_speed -= 3
                    ober_item.range -= 3

                # ACCELERATE
                elif clicked_item.name == "move":
                    ober_item.change_speed(0.1)


    def execute_click_events(self, event, my_body, current_tile):

        # --------------------------------------------------------------- #
        #                        MOUSE MODE CLICK                         #
        # --------------------------------------------------------------- #
        if self.grid.mouse_mode in ["laino", "EDITOR2"]:
            self.laino_mode_click(current_tile)

        elif self.grid.mouse_mode in ["shit"]:
            self.laino_mode_click(current_tile)

        elif self.grid.mouse_mode in ["see", "EDITOR1"]:
            self.see_mode_click(current_tile)

        elif self.grid.mouse_mode in ["EDITOR3"]:
            if current_tile not in self.grid.occupado_tiles.values() and current_tile in self.grid.revealed_tiles:
                self.produce("block_of_steel", current_tile)

        elif self.grid.mouse_mode == "echo":
            self.echo_mode_click(current_tile, my_body)

        # --------------------------------------------------------------- #
        #                          CLICK ON ITEMS                         #
        # --------------------------------------------------------------- #
        for item in self.grid.items:
            if item.clickable and item.available:
                if current_tile == item.pos:
                    print("INFO: Clicked item: {0}".format(item.name))

                    if item.type == "option":
                        oitem = item.get_ober_item(self.grid)
                        if oitem.in_menu and not oitem.type in ["inventory"]:
                            oitem.close_menu(self.grid)

                    if item.in_menu:
                        if not item.mode and not (item.has_opts and item.type == "option"):
                            item.close_menu(self.grid)
                        else:
                            item.revert_menu(self.grid)

                    elif item.has_opts and not item.in_menu:
                        item.open_menu(self.grid)

                    # SET MOUSE MODE
                    if item.modable:
                        self.grid.set_mouse_mode(item)
                        my_body.mode = item.name

                    # CLICK ON ITEMS
                    self.grid.event_effects.click_items(item, my_body)

                    # CLEAN MOUSE
                    if item.in_menu:
                        self.grid.clean_mouse()
                # MENU OFF
                elif current_tile not in self.grid.adj_tiles(item.pos):
                    if item.in_menu:
                        if not item.type == "inventory":
                            item.close_menu(self.grid)

        # DEBUG PRINT
        cir_utils.debug_print_click(self.grid, current_tile, my_body)
