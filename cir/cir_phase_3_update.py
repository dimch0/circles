# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                   UPDATE                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
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
            self.grid.msg("INFO - Leaving room: {0}".format(self.grid.current_room))
            inventory_in_menu = my_body.inventory.in_menu
            self.grid.change_room(room_number)
            if inventory_in_menu:
                my_body.inventory.open_menu(self.grid)
            else:
                my_body.inventory.close_menu(self.grid)

            self.grid.needs_to_change_room = False
            if not my_body in self.grid.items:
                self.grid.items.append(my_body)
            my_body.pos = get_mirror_point(item.pos, self.grid.center_tile)
            my_body.gen_birth_track()

    # --------------------------------------------------------------- #
    #                                                                 #
    #                           DESTRUCTION                           #
    #                                                                 #
    # --------------------------------------------------------------- #
    def destruction(self, item):
        you_dead_msg = "SCREEN - you dead"
        if item.name in ['my_body']:
            if not you_dead_msg in self.grid.messages:
                self.grid.msg(you_dead_msg)

        if not item.birth_track:

            item.available = False
            self.grid.msg("INFO - Destroying: {0}".format(item.name))
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
        self.grid.msg("INFO - Hit!")


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

                # REVEALED / AVAILABLE
                if item.pos in self.grid.revealed_tiles:
                    if not item.available and not item in self.grid.overlap:
                        item.available = True
                        item.gen_birth_track()

                if item.available:

                    # TIMERS
                    self.timer_effect(item)

                    # KISSING CIRCLES
                    # if item.type == 'body':
                    #     for adj_item in self.grid.items:
                    #         if adj_item.type == 'body' and adj_item.pos in self.grid.adj_tiles(item.pos):
                    #             item.gen_fat()

                    # ANIMATE MOVEMENT
                    if item.direction != None:
                        item.gen_move_track(self.grid)
                    if item.move_track and not item.birth_track:
                        item.pos = item.move_track[0]
                        item.move_track.pop(0)

                    # ANIMATE BIRTH
                    if item.birth_track:
                        item.radius = item.birth_track[0]
                        item.birth_track.pop(0)

                    # ANIMATE FAT
                    elif not item.birth_track and item.fat_track:
                        item.radius = item.fat_track[0]
                        item.fat_track.pop(0)

                    # ANIMATE EFFECT
                    if item.effect_track:
                        item.effect_track.pop(0)
                        if not item.effect_track:
                            item.color = item.default_color

                    # ANIMATE VIBE
                    if item.vibe_track:

                        vibe_area = ((item.pos), item.vibe_track[0][0])

                        # Reveal vibe effect
                        if not vibe_area in self.grid.revealed_radius:
                            self.grid.revealed_radius.append(vibe_area)
                        # Set revealed tiles
                        self.grid.set_rev_tiles()


                        for hit_item in self.grid.items:
                            if hit_item.available and not hit_item.name == item.name:
                                cir1 = (hit_item.pos, hit_item.radius - (hit_item.radius / 2.5))
                                if intersecting(cir1, vibe_area):
                                    if not hit_item in item.hit_items:
                                        # CONSUME VIBE
                                        self.grid.event_effects.consume(hit_item, item)

                                        item.hit_items.append(hit_item)

                        item.vibe_track.pop(0)
                        if not item.vibe_track:
                            item.hit_items = []

                    # SIGNAL HIT
                    if self.signal_hit(item, my_body):
                        self.signal_hit_effect(item)

                    # CLEAN PLACEHOLDERS
                    self.grid.clean_placeholders(item)

        self.grid.sort_items_by_layer()

        self.update_occupado()

        self.grid.clock.tick(self.grid.fps)