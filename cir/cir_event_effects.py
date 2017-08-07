#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                                        Effects                                      #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################
import copy
import random
import cir_utils
import time


class GameEffects(object):

    def __init__(self, grid=None, loader=None):
        self.grid = grid
        self.loader = loader


    # --------------------------------------------------------------- #
    #                                                                 #
    #                             PRODUCE                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    def produce(self, product_name, pos=None, radius=None, birth=None, vf=None, lifespan=None):
        """
        Produces an item from the everything dict
        :param grid: grid instance
        :param product: name of the item from the everything dict
        :param pos: new position
        :return: the new item
        """
        new_item = self.loader.load_item(product_name)

        if radius:
            new_item.radius = radius
        if birth:
            new_item.birth_time.duration = birth
        if vf:
            new_item.vibe_freq.duration = vf
        if pos:
            new_item.pos = pos
        if lifespan:
            new_item.lifespan = lifespan
        # self.loader.set_timer(new_item)
        new_item.default_img = new_item.img
        # new_item.name        = new_item.name + str(time.time())
        # new_item.marked_for_destruction = False
        new_item.available = True
        new_item.gen_birth_track()

        self.grid.items.append(new_item)
        return new_item

    # --------------------------------------------------------------- #
    #                                                                 #
    #                             DESTROY                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    def destroy(self, item):
        if item in self.grid.items and not item.birth_track:
            if item.lifespan:
                item.lifespan = None
            if hasattr(item, "vibe_freq"):
                item.vibe_freq = None
            item.in_menu = False
            item.move_track = []
            item.gen_birth_track()
            item.birth_track.reverse()

            item.marked_for_destruction = True

    def destruction(self, item):
        if item.marked_for_destruction and not item.birth_track:
            item.available = False
            self.grid.items.remove(item)
            if item.name == "my_body":
                self.grid.game_over = True



    # --------------------------------------------------------------- #
    #                                                                 #
    #                             MITOSIS                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    def cell_division(self, item):
        """
        Creates a placeholder in the empty tile.
        Than creates a copy of the item and moves it into the placehoder.
        They're being cleaned with the clean_placehoder function.
        :param grid: grid instance
        :return:
        """
        empty_tile = item.check_for_empty_adj_tile(self.grid)
        if empty_tile:
            placeholder = self.produce("placeholder", empty_tile)
            search_for_name = item.name.replace(" - copy", "")
            new_copy = self.produce(search_for_name, item.pos)
            new_copy.img = item.img
            new_copy.speed = item.speed
            new_copy.name = "new copy"
            new_copy.birth_track = []
            # new_copy.pos = item.pos
            # new_copy.color = self.color
            # new_copy.birth_time = None
            # new_copy.radius = self.radius
            # new_copy.birth_time = TimerItem()
            # new_copy.birth_time.duration = 0
            # new_copy.gen_birth_track()
            new_copy.move_track = new_copy.move_to_tile(self.grid, empty_tile)
            if new_copy.lifespan:
                new_copy.lifespan.duration = 10
                new_copy.lifespan.restart()

    def mitosis(self, item):
        """
        :param grid: grid instance
        :return:
        """
        for other_item in self.grid.items:
            print "START MITO", item.name
            if other_item.name == "new copy":
                other_item.name = str(item.name + " - copy")

            if other_item.name in [item.name, str(item.name + " - copy")]:
                empty_tile = other_item.check_for_empty_adj_tile(self.grid)
                if empty_tile:
                    if other_item.speed and not other_item.birth_track and not other_item.move_track:
                        self.cell_division(other_item)
            print "FINISH MITO", item.name



    # --------------------------------------------------------------- #
    #                                                                 #
    #                         MOUSE MODES                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    def laino_mode_click(self, current_tile):
        """
        For mode 'laino', if clicked produces an item
        :param self.grid: self.grid instance
        :param current_tile: the clicked circle
        """
        if current_tile not in self.grid.occupado_tiles and current_tile in self.grid.revealed_tiles:
            self.produce("product_shit", current_tile)


    def shit_mode_click(self, current_circle):
        """
        For mode 'shit', if clicked produces an item and exhausts mode uses
        :param self.grid: self.grid instance
        :param current_circle: the clicked circle
        """
        for bag_item in self.grid.mode_vs_options["bag"]:
            if bag_item.name == self.grid.mouse_mode:
                if bag_item.uses:
                    if current_circle not in self.grid.occupado_tiles: #and current_circle in self.grid.revealed_tiles:
                        self.produce("shit", current_circle)
                        bag_item.uses -= 1
                        return 1


    def eat_mode_click(self, current_tile):
        """ Eat that shit """
        for item in self.grid.items:
            if current_tile == item.pos and not item.name == "my_body" and not "EDITOR" in item.name:
                self.destroy(item)


    def echo_mode_click(self, current_tile, my_body):
        """ Signal effect """
        if not cir_utils.in_circle(my_body.pos, my_body.radius, current_tile) and not my_body.move_track:
            # trace = self.produce("signal",
            #                       my_body.pos,
            #                       radius = int((self.grid.tile_radius / 3) + 1),
            #                       birth = 0.05,
            #                      )
            # trace.color = self.grid.pink
            # trace.direction = trace.get_aiming_direction(self.grid, current_tile)[1]
            signal = self.produce("signal",
                                  my_body.pos,
                                  radius = int(self.grid.tile_radius / 3),
                                  birth = 0.05)
            signal.direction = signal.get_aiming_direction(self.grid, current_tile)[1]


    def signal_hit(self, item, my_body):
        hit = False
        if item.type == "signal":
            if (item.pos in self.grid.occupado_tiles and not item.intersects(my_body)) or item.direction == None:
                hit = True
                print "Hit!"
        return hit


    def signal_hit_effect(self, item):
        item.in_menu = False
        item.move_track = []
        item.gen_birth_track()
        item.birth_track.reverse()
        item.marked_for_destruction = True

    # --------------------------------------------------------------- #
    #                                                                 #
    #                           BAG MODES                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    def collect(self, item):
        """ Collect item: add it to bag options """
        if item.collectible:
            for option in self.grid.mode_vs_options["bag"]:
                if "bag_placeholder" in option.name:
                    self.grid.mode_vs_options["bag"].remove(option)
                    new_item = copy.deepcopy(item)
                    new_item.modable = True
                    new_item.img = item.img
                    new_item.default_img = item.default_img
                    new_item.color = item.color
                    self.grid.mode_vs_options["bag"].append(new_item)
                    item.available = False
                    self.grid.items.remove(item)
                    return 1


    def empty_bag(self):
        """ Empties the bag if an item's uses are exhausted """
        for bag_item in self.grid.mode_vs_options["bag"]:
            if bag_item.uses == 0:
                self.grid.mode_vs_options["bag"].remove(bag_item)
                empty_placeholder = copy.deepcopy(self.grid.everything["bag_placeholder"])
                empty_placeholder.color = self.grid.everything["bag_placeholder"].color
                self.grid.mode_vs_options["bag"].append(empty_placeholder)
                if self.grid.mouse_mode == bag_item.name:
                    self.grid.clean_mouse()
                return 1


    # --------------------------------------------------------------- #
    #                                                                 #
    #                       ENTER / EXIT EFFECTS                      #
    #                                                                 #
    # --------------------------------------------------------------- #
    def enter_room(self, my_body, item):
        if "Exit_" in item.name or "Enter_" in item.name:
            room_number = None
            for option in item.options:
                if "Enter_" in option.name:
                    room_number = option.name.replace("Enter_", "")
                    room_number = int(room_number)

            if my_body.pos == item.pos and self.grid.needs_to_change_room:
                self.grid.change_room(room_number)
                my_body.available = True
                my_body.gen_birth_track()
                self.grid.rooms[self.grid.current_room]["revealed_radius"].append(((item.pos), self.grid.tile_radius))


    def exit_room(self, my_body, item):
        """
        Changes the current room
        :param self.grid: self.grid instance
        :param my_body: my_body instance
        :param item: enter / exit item
        :param option: option of the above item -> holds the room number
        """
        if my_body.pos in self.grid.adj_tiles(item.pos):
            my_body.move_track = my_body.move_to_tile(self.grid, item.pos)
            self.grid.needs_to_change_room = True
        else:
            print "it far"



    # --------------------------------------------------------------- #
    #                                                                 #
    #                         TIMER EFFECTS                           #
    #                                                                 #
    # --------------------------------------------------------------- #
    def birth_time_over_effect(self, item):
        """ Birth timer effect """
        if item.birth_track:
            item.birth_track.pop(0)
            item.birth_time.restart()

    def vibe_freq_over_effect(self, item):
        """ Vibe frequency timer over effect """
        if not item.move_track:
            item.gen_radar_track(self.grid)

        if len(item.radar_track) == 1:
            legal_moves = []
            for item_adj in self.grid.adj_tiles(item.pos):
                if item_adj in self.grid.playing_tiles and item_adj not in self.grid.occupado_tiles:
                    legal_moves.append(item_adj)

            if legal_moves:
                item.move_track = item.move_to_tile(self.grid, random.choice(legal_moves))
                if item.vibe_freq:
                    item.vibe_freq.restart()


    def signal_lifespan_over_effect(self, item):
        self.destroy(item)


    def timer_effect(self, item):
        """ Timer effects  """
        if item.lifespan:
            item.lifespan.tick()
            if item.lifespan.is_over:
                self.destroy(item)

        if hasattr(item, "vibe_freq"):
            if item.vibe_freq and not isinstance(item.vibe_freq, float):
                if item.vibe_freq.duration:
                    item.vibe_freq.tick()
                    if item.vibe_freq.is_over:
                        self.vibe_freq_over_effect(item)

        if item.birth_track:
            if item.birth_time and not isinstance(item.birth_time, float):
                item.birth_time.tick()
                if item.birth_time.is_over:
                    self.birth_time_over_effect(item)



    # --------------------------------------------------------------- #
    #                        MOUSE MODE CLICK                         #
    # --------------------------------------------------------------- #
    def mouse_mode_click(self, current_tile, my_body):
        if self.grid.mouse_mode in ["laino", "EDITOR2"]:
            self.laino_mode_click(current_tile)
        elif self.grid.mouse_mode in ["shit"]:
            self.shit_mode_click(current_tile)
        elif self.grid.mouse_mode in ["see", "EDITOR1"]:
            if current_tile not in self.grid.occupado_tiles and current_tile in self.grid.revealed_tiles:
                new_observer = self.produce("observer", current_tile)
                new_observer.lifespan.restart()
        elif self.grid.mouse_mode in ["EDITOR3"]:
            if current_tile not in self.grid.occupado_tiles and current_tile in self.grid.revealed_tiles:
                self.produce("block_of_steel", current_tile)
        elif self.grid.mouse_mode in ["eat", "EDITOR9"]:
            self.eat_mode_click(current_tile)
        elif self.grid.mouse_mode == "echo":
            self.echo_mode_click(current_tile, my_body)




    # --------------------------------------------------------------- #
    #                             EDITOR                              #
    # --------------------------------------------------------------- #
    def editor(self, item, my_body):
        # EDITOR CLICK
        if item.name == "EDITOR10":
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
            if my_body.lifespan:
                my_body.lifespan.update(60)

        elif item.name == "EDITOR15":
            trigger = self.produce(product_name="trigger",
                                   pos=self.grid.center_tile,
                                   lifespan=1)
            trigger.range = 4
            trigger.vibe_speed = 3
            trigger.birth_time = 0

            self.loader.set_timer(trigger)
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
    def click_items(self, item, my_body):

        # EDITOR CLICK
        self.editor(item, my_body)

        # BAG MOUSE MODE CLICK
        if self.grid.mouse_mode == "bag":
            self.collect(item)


    # --------------------------------------------------------------- #
    #                                                                 #
    #                            BODY MODES                           #
    #                                                                 #
    # --------------------------------------------------------------- #
    def click_options(self, item, option, my_body):
        # --------------------------------------------------------------- #
        #                       CLICK DEFAULT OPTIONS                     #
        # --------------------------------------------------------------- #
        if option in item.default_options:

            # bag
            if option.name == "bag":
                print "Gimme the loot!"

            # mitosis
            elif option.name == "mitosis":
                self.mitosis(item)

            elif option.name == "move":
                item.change_speed(0.1)

            elif option.name == "suicide":
                self.destroy(item)

            elif option.name == "echo":
                print "Echo!"

            # enter / exit
            elif "Enter_" in option.name:
                self.exit_room(my_body, item)

            # Setting the mode
            item.set_mode(self.grid, option)

        # --------------------------------------------------------------- #
        #                        CLICK SUB-OPTIONS                        #
        # --------------------------------------------------------------- #
        elif option in self.grid.mode_vs_options[item.mode]:
            # see
            if option.name == "see":
                print "Seen"

            # smel
            elif option.name == "smel":
                print "Sniff hair"

            # medi
            elif option.name == "medi":
                print "Ommmm"
                item.range += 3
                my_body.gen_radar_track(self.grid)
                item.range -= 3

            # audio
            elif option.name == "audio":
                print "Who"
                item.range += 1

            # eat
            elif option.name == "eat":
                print "Nom Nom Nom"

            # touch
            elif option.name == "touch":
                print "Can't touch this"

            # Close menu when sub-option selected
            item.set_in_menu(self.grid, False)

        # Close menu if option has no sub-options
        if option.name not in self.grid.mode_vs_options.keys():
            item.set_in_menu(self.grid, False)





    # --------------------------------------------------------------- #
    #                                                                 #
    #                           CHANGE VARS                           #
    #                                                                 #
    # --------------------------------------------------------------- #
    def change_vars(self, my_body):
        if not self.grid.game_menu:

            # My_body to room
            if not my_body in self.grid.items:
                self.grid.items.append(my_body)

            # Check bag
            if "bag" in self.grid.everything.keys():
                self.empty_bag()

            # Items
            for item in self.grid.items:

                # Enter
                self.enter_room(my_body, item)

                # Destruction
                self.destruction(item)

                if item.available:

                    # Timers
                    self.timer_effect(item)

                    # Kissing circles
                    if item.type == 'body':
                        for adj_item in self.grid.items:
                            if adj_item.type == 'body' and adj_item.pos in self.grid.adj_tiles(item.pos):
                                item.gen_fat()

                    # Movement
                    if item.direction != None:
                        item.gen_move_track(self.grid)
                    if item.move_track:
                        item.move()

                    # Signal hit
                    if self.signal_hit(item, my_body):
                        self.signal_hit_effect(item)

                    # Clean placeholders
                    self.grid.clean_placeholders(item)
                    # Overlap
                    item.overlapping(self.grid)
