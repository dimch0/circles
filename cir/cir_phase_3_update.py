#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                                     Change vars                                     #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################
import random
from cir_utils import get_mirror_point

class VarChanger(object):

    def __init__(self, grid=None):
        self.grid = grid


    # --------------------------------------------------------------- #
    #                                                                 #
    #                          BAG EFFECTS                            #
    #                                                                 #
    # --------------------------------------------------------------- #
    # def empty_bag(self):
    #     """ Empties the bag if an item's uses are exhausted """
    #     for bag_item in self.grid.mode_vs_options["bag"]:
    #         if bag_item.uses == 0:
    #             self.grid.mode_vs_options["bag"].remove(bag_item)
    #             empty_placeholder = copy.deepcopy(self.grid.everything["bag_placeholder"])
    #             empty_placeholder.color = self.grid.everything["bag_placeholder"].color
    #             self.grid.mode_vs_options["bag"].append(empty_placeholder)
    #             if self.grid.mouse_mode == bag_item.name:
    #                 self.grid.clean_mouse()
    #             return 1

    # --------------------------------------------------------------- #
    #                                                                 #
    #                        ENTER ROOM EFFECTS                       #
    #                                                                 #
    # --------------------------------------------------------------- #
    def enter_room(self, my_body, item):

        if "Enter_" in item.name and my_body.pos == item.pos:

            room_number = item.name.replace("Enter_", "")
            print("Leaving room : '{0}' \nEntering room: '{1}'".format(
                self.grid.current_room,
                room_number))

            self.grid.change_room(room_number)
            if not my_body in self.grid.items:
                self.grid.items.append(my_body)
            # my_body.available = True
            my_body.pos = get_mirror_point(item.pos, self.grid.center_tile)
            self.grid.needs_to_change_room = False
            my_body.gen_birth_track()

    # --------------------------------------------------------------- #
    #                                                                 #
    #                           DESTRUCTION                           #
    #                                                                 #
    # --------------------------------------------------------------- #
    def destruction(self, item):
        if not item.birth_track:
            item.available = False
            self.grid.items.remove(item)
            if item.name == "my_body":
                self.grid.game_over = True

    # --------------------------------------------------------------- #
    #                                                                 #
    #                             TIMERS                              #
    #                                                                 #
    # --------------------------------------------------------------- #
    def update_birth_track(self, item):
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


    def timer_effect(self, item):
        """ Timer effects  """
        if item.lifespan:
            item.lifespan.tick()
            if item.lifespan.is_over:
                item.destroy(self.grid)

        if hasattr(item, "vibe_freq"):
            if item.vibe_freq and not isinstance(item.vibe_freq, float):
                if item.vibe_freq.duration:
                    item.vibe_freq.tick()
                    if item.vibe_freq.is_over:
                        self.vibe_freq_over_effect(item)

        if item.birth_track:
            if item.birth_time and not isinstance(item.birth_time, float):
                if item.birth_time.duration > 0:
                    item.birth_time.tick()
                    # performance - gen birth track without birth_time = faster birth
                    if item.birth_time.is_over:
                        self.update_birth_track(item)
                else:
                    item.birth_track.pop(0)

    # --------------------------------------------------------------- #
    #                                                                 #
    #                            SIGNALS                              #
    #                                                                 #
    # --------------------------------------------------------------- #
    def signal_hit(self, item, my_body):
        hit = False
        if item.type == "signal":
            if (item.pos in self.grid.occupado_tiles and not item.intersects(
                    my_body)) or item.direction == None:
                hit = True
                print("Hit!")
        return hit

    def signal_hit_effect(self, item):
        item.destroy(self.grid)

    # --------------------------------------------------------------- #
    #                                                                 #
    #                           CHANGE VARS                           #
    #                                                                 #
    # --------------------------------------------------------------- #
    def change_vars(self, my_body):
        """
        U[darting all variables before next iteration of the main loop
        :param my_body: my_body instance
        """
        if not self.grid.game_menu:

            # My_body to room
            # if not my_body in self.grid.items\
            #         and self.grid.current_room not in ["999"]:
            #     self.grid.items.append(my_body)

            # Check bag
            # if "bag" in self.grid.everything.keys():
            #     self.empty_bag()

            # Items
            for item in self.grid.items:

                # Enter
                if self.grid.needs_to_change_room:
                    self.enter_room(my_body, item)

                # Destruction
                if item.marked_for_destruction:
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
                    # Fat
                    if item.fat_track:
                        item.fat_track.pop(0)

                    # Signal hit
                    if self.signal_hit(item, my_body):
                        self.signal_hit_effect(item)

                    # Clean placeholders
                    self.grid.clean_placeholders(item)

                    # Overlap
                    # item.overlapping(self.grid)

        self.grid.clock.tick(self.grid.fps)