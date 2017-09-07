#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                                     Change vars                                     #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################
import random
from cir_utils import get_mirror_point, intersecting

class VarUpdater(object):

    def __init__(self, grid=None):
        self.grid = grid


    # --------------------------------------------------------------- #
    #                                                                 #
    #                        ENTER ROOM EFFECTS                       #
    #                                                                 #
    # --------------------------------------------------------------- #
    def enter_room(self, my_body, item):

        if "Enter_" in item.name and my_body.pos == item.pos:

            room_number = item.name.replace("Enter_", "")
            self.grid.logger.log(
                self.grid.logger.INFO, "Leaving room: {0}".format(
                    self.grid.current_room))

            self.grid.change_room(room_number)

            if not my_body in self.grid.items:
                self.grid.items.append(my_body)

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
            self.grid.logger.log(self.grid.logger.INFO, "Destroying: {0}".format(item.name))
            self.grid.items.remove(item)
            if item.name in self.grid.occupado_tiles:
                del self.grid.occupado_tiles[item.name]
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
            item.gen_vibe_track(self.grid)

        if len(item.vibe_track) == 1:
            legal_moves = []
            for item_adj in self.grid.adj_tiles(item.pos):
                if item_adj in self.grid.playing_tiles and item_adj not in self.grid.occupado_tiles.values():
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
                    if item.birth_time.is_over:
                        self.update_birth_track(item)
                else:
                    item.birth_track.pop(0)
            # else:
            #     item.birth_track = []

    # --------------------------------------------------------------- #
    #                                                                 #
    #                            SIGNALS                              #
    #                                                                 #
    # --------------------------------------------------------------- #
    def signal_hit(self, signal, my_body):
        hit = False
        if signal.type == "signal":
            if not signal.marked_for_destruction:
                if (signal.pos in self.grid.occupado_tiles.values() and not signal.intersects(
                        my_body)) or signal.direction == None:
                    signal.destroy(self.grid)
                    hit = True
        return hit


    def signal_hit_effect(self, item):
        self.grid.logger.log(self.grid.logger.INFO, "Hit!")


    def update_occupado(self):
        for item in self.grid.items:
            if not item.type in ["signal", "trigger", "option"]:
                for tile in self.grid.playing_tiles:
                    circle_1 = (tile, self.grid.tile_radius)
                    circle_2 = (item.pos, self.grid.tile_radius)
                    if intersecting(circle_1, circle_2):
                        self.grid.occupado_tiles[item.name] = tile

    # --------------------------------------------------------------- #
    #                                                                 #
    #                           CHANGE VARS                           #
    #                                                                 #
    # --------------------------------------------------------------- #
    def update_vars(self, my_body):
        """
        U[darting all variables before next iteration of the main loop
        :param my_body: my_body instance
        """

        if not self.grid.game_menu:
            # ITEMS
            for item in self.grid.items:

                # OCCUPADO
                # self.update_occupado(item)

                # MY_BODY OVERLAP
                if item.type not in ["my_body", "option", "map_tile"]:
                    if item.pos == my_body.pos and not item.birth_track:
                        item.clickable = False
                        item.radius = item.default_radius

                    elif item.pos != my_body.pos and item not in self.grid.overlap:
                        item.clickable = True

                # ENTER
                if self.grid.needs_to_change_room:
                    self.enter_room(my_body, item)

                # DESTRUCTION
                if item.marked_for_destruction:
                    self.destruction(item)

                if item.available:

                    # TIMERS
                    self.timer_effect(item)

                    # KISSING CIRCLES
                    # if item.type == 'body':
                    #     for adj_item in self.grid.items:
                    #         if adj_item.type == 'body' and adj_item.pos in self.grid.adj_tiles(item.pos):
                    #             item.gen_fat()

                    # MOVEMENT
                    if item.direction != None:
                        item.gen_move_track(self.grid)
                    if item.move_track:
                        item.update_pos()

                    # FAT
                    if item.fat_track:
                        item.fat_track.pop(0)

                    # SIGNAL HIT
                    if self.signal_hit(item, my_body):
                        self.signal_hit_effect(item)

                    # CLEAN PLACEHOLDERS
                    self.grid.clean_placeholders(item)

        self.grid.sort_items_by_layer()

        self.update_occupado()

        self.grid.clock.tick(self.grid.fps)