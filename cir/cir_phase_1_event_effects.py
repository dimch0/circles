# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                                                                                     #
#                                                    Effects                                                          #
#                                                                                                                     #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import os
import copy
import cir_utils


class GameEffects(object):

    def __init__(self, grid=None):
        self.grid = grid

    # --------------------------------------------------------------- #
    #                                                                 #
    #                             PRODUCE                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    def produce(self, product_name, pos=None, radius=None, birth=None, vibe_freq=None, lifespan=None):
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

        # self.grid.loader.set_timers(new_item)
        # new_item.name = new_item.name + str(time.time())
        # new_item.marked_for_destruction = False

        new_item.default_img = new_item.img
        new_item.available = True
        new_item.gen_birth_track()
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
            self.produce("placeholder", empty_tile)
            search_for_name = item.name.replace(" - copy", "")
            new_copy = self.produce(search_for_name, item.pos)
            new_copy.color = item.color
            new_copy.img = item.img
            new_copy.speed = item.speed
            new_copy.radius = item.radius
            new_copy.name = "new copy"
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
            if other_item.name == "new copy":
                other_item.name = str(item.name + " - copy")

            if other_item.name in [item.name, str(item.name + " - copy")]:
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
    # BAG ITEM CLICK
    # def shit_mode_click(self, current_tile):
    #     """
    #     For mode 'shit', if clicked produces an item and exhausts mode uses
    #     :param current_tile: the clicked circle
    #     """
    #     for bag_item in self.grid.mode_vs_options["bag"]:
    #         if bag_item.name == mouse_mode:
    #             if bag_item.uses:
    #                 if current_tile not in self.grid.occupado_tiles:
    #                     self.produce("shit", current_tile)
    #                     bag_item.uses -= 1
    #                     return 1

    def laino_mode_click(self, current_tile):
        if current_tile not in self.grid.occupado_tiles and current_tile in self.grid.revealed_tiles:
            self.produce("product_shit", current_tile)

    def see_mode_click(self, current_tile):
        if current_tile not in self.grid.occupado_tiles and current_tile in self.grid.revealed_tiles:
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

    # --------------------------------------------------------------- #
    #                                                                 #
    #                           BAG MODES                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    def collect(self, item, my_body):
        """ Collect item: add it to bag options """
        pass
        # if item.collectible:
        #     for bag in my_body.options:
        #         if bag.name == "bag":
        #             for option in bag.options:
        #                 if "bag_placeholder" in option.name:
        #                     bag.options.remove(option)
        #                     new_item = copy.deepcopy(item)
        #                     new_item.modable = True
        #                     new_item.img = item.img
        #                     new_item.default_img = item.default_img
        #                     new_item.color = item.color
        #                     bag.options.append(new_item)
        #                     item.available = False
        #                     self.grid.items.remove(item)
        #                     return 1

    # --------------------------------------------------------------- #
    #                                                                 #
    #                       ENTER / EXIT EFFECTS                      #
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
    #                         TIMER EFFECTS                           #
    #                                                                 #
    # --------------------------------------------------------------- #
    def signal_lifespan_over_effect(self, item):
        item.destroy(self.grid)

    # --------------------------------------------------------------- #
    #                        MOUSE MODE CLICK                         #
    # --------------------------------------------------------------- #
    def mouse_mode_click(self, current_tile, my_body):
        """ CLICK WITH THE CURRENT MOUSE MODE ACTIVATES EFFECT ACCORDINGLY """

        # --------------------------------------------------------------- #
        #                          PRODUCTION                             #
        # --------------------------------------------------------------- #
        if self.grid.mouse_mode in ["laino", "EDITOR2"]:
            self.laino_mode_click(current_tile)

        elif self.grid.mouse_mode in ["shit"]:
            # TODO: BAG ITEM DROP
            self.laino_mode_click(current_tile)

        elif self.grid.mouse_mode in ["see", "EDITOR1"]:
            self.see_mode_click(current_tile)

        elif self.grid.mouse_mode in ["EDITOR3"]:
            if current_tile not in self.grid.occupado_tiles and current_tile in self.grid.revealed_tiles:
                self.produce("block_of_steel", current_tile)

        elif self.grid.mouse_mode == "echo":
            self.echo_mode_click(current_tile, my_body)



    # --------------------------------------------------------------- #
    #                             EDITOR                              #
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
                if my_body in self.grid.items:
                    self.grid.items.remove(my_body)

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
                                   lifespan=1)
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
            self.grid.scenario = 'Scenario_2'
            self.grid.game_over = True

        elif item.name == "EDITOR18":
            my_body.gen_fat()


    # --------------------------------------------------------------- #
    #                          CLICK ON ITEM                          #
    # --------------------------------------------------------------- #
    def eat(self, item):
        """ Eat that shit """
        if not any(forbidden_type in item.type for forbidden_type in [
            "my_body",
            "editor",
            "option",
            "trigger",
            "placeholder"
        ]):
            item.destroy(self.grid)

    def terminate(self, item):
        """ Eat that shit """
        if not any(forbidden_type in item.type for forbidden_type in [
            "my_body",
            "editor",
            "option",
            "trigger",
            "placeholder"
        ]):
            item.destroy(self.grid, fast=True)


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

        # EAT MODE
        # if clicked_item.edible:
        if mouse_mode in ["eat"]:
            self.eat(clicked_item)

        # TERMINATE
        elif mouse_mode in ["EDITOR9"]:
            self.terminate(clicked_item)

        elif mouse_mode in ["bag"]:
            if clicked_item.collectible:
                pass
                # TODO: produce modable option of the item
                # TODO: include opt in bag options
                # TODO: terminate item

        # BAG MOUSE MODE CLICK
        # if mouse_mode == "bag":
        #     self.collect(clicked_item, my_body)

        # ENTER
        if "Enter" in clicked_item.name:
            self.enter_effect(my_body, clicked_item)

        # OPTIONS
        if clicked_item.type == "option":
            ober_item = clicked_item.get_ober_item(self.grid)
            # SUICIDE
            if clicked_item.name == "suicide":
                if ober_item:
                    ober_item.destroy(self.grid)

            # mitosis
            elif clicked_item.name == "mitosis":
                if ober_item:
                    self.mitosis(ober_item)


    #         elif option.name == "move":
    #             item.change_speed(0.1)


        # --------------------------------------------------------------- #
        #                        CLICK SUB-OPTIONS                        #
        # --------------------------------------------------------------- #
        # elif option in self.grid.mode_vs_options[item.mode]:
        #     # see
        #     if option.name == "see":
        #         print "Seen"
        #
        #     # smel
        #     elif option.name == "smel":
        #         print "Sniff hair"
        #
        #     # medi
        #     elif option.name == "medi":
        #         print "Ommmm"
        #         item.range += 3
        #         my_body.gen_radar_track(self.grid)
        #         item.range -= 3
        #
        #     # audio
        #     elif option.name == "audio":
        #         print "Who"
        #         item.range += 1
        #
        #     # eat
        #     elif option.name == "eat":
        #         print "Nom Nom Nom"
        #
        #     # touch
        #     elif option.name == "touch":
        #         print "Can't touch this"
        #
        #     # Close menu when sub-option selected
        #     item.set_in_menu(self.grid, False)