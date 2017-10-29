# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                   UPDATE                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
from cir_utils import get_mirror_point, intersecting, get_short_name, in_circle, dist_between

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
            self.grid.revealed_tiles[my_body.pos] = []
            my_body.gen_birth_track()
            for item in self.grid.items:
                if item.pos == my_body.pos and 'door' in  item.type:
                    item.available = True


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
            if item in self.grid.items:
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
    def vfreq_over_effect(self, item):
        """ Vibe frequency timer over effect """
        if not item.move_track:
            item.gen_vibe_track(self.grid)

            if item.type in ['observer'] and not item.in_action:
                item.action(self.grid)

            item.vfreq.restart()


    def timer_effect(self, item):
        """ Timer effects  """

        # LIFESPAN
        if item.lifespan:
            item.lifespan.tick()
            if item.lifespan.is_over:
                item.destroy(self.grid)

        # VIBE TIMER
        if hasattr(item, "vfreq"):
            if item.vfreq and not isinstance(item.vfreq, float):
                if item.vfreq.duration:
                    item.vfreq.tick()
                    if item.vfreq.is_over:
                        self.vfreq_over_effect(item)
                        # item.vfreq.restart()


        # MOVE TIMER



    # --------------------------------------------------------------- #
    #                                                                 #
    #                            SIGNALS                              #
    #                                                                 #
    # --------------------------------------------------------------- #
    def signal_hit(self, signal, sender):
        hit = False
        if signal.type == "signal":
            if not signal.marked_for_destruction:
                if (signal.pos in self.grid.occupado_tiles.values() and not signal.intersects(
                        sender)) or signal.direction == None:
                    signal.destroy(self.grid)
                    hit = True
        return hit


    def signal_hit_effect(self, signal):
        self.grid.msg("INFO - Hit!")
        for hit_item in self.grid.items:
            if hit_item.available and not hit_item.name == signal.name:
                cir1 = (hit_item.pos, hit_item.radius)
                cir2 = (signal.pos, signal.radius)
                if intersecting(cir1, cir2):
                    self.grid.event_effects.consume(hit_item, signal)

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

                        # REVEAL TILE
                        for rtile in self.grid.playing_tiles:
                            if in_circle(item.pos, item.vibe_track[0][0], rtile):
                                if not rtile in item.hit_tiles:
                                    item.hit_tiles.append(rtile)
                                if not rtile in self.grid.revealed_tiles.keys():
                                    self.grid.revealed_tiles[rtile] = range(1, self.grid.tile_radius + 1)
                                    # REVEAL ADJ DOORS
                                    for adj_rtile in self.grid.adj_tiles(rtile):
                                        for ditem in self.grid.items:
                                            if "door" in ditem.type and ditem.pos == adj_rtile:
                                                if not ditem.available:
                                                    ditem.available = True
                                                    ditem.gen_birth_track()

                        for hit_item in self.grid.items:
                            # REVEALED / AVAILABLE
                            if hit_item.pos in self.grid.revealed_tiles.keys():
                                if not hit_item.available and not hit_item in self.grid.overlap:
                                    hit_item.available = True
                                    hit_item.gen_birth_track()

                            # CONSUME VIBE
                            if item.effects:
                                if hit_item.available and not get_short_name(hit_item.name) == get_short_name(item.name):
                                    cir1 = (hit_item.pos, hit_item.radius - (hit_item.radius / 2.5))
                                    if intersecting(cir1, vibe_area):
                                        if not hit_item in item.hit_items:
                                            self.grid.event_effects.consume(hit_item, item)
                                            item.hit_items.append(hit_item)

                        item.vibe_track.pop(0)
                        if not item.vibe_track:
                            item.hit_items = []
                            item.hit_tiles = []

                    # CONSUME SIGNAL
                    if self.signal_hit(item, my_body):
                        self.signal_hit_effect(item)

                    # CLEAN PLACEHOLDERS
                    self.grid.clean_placeholders(item)

            # for

            # FORCE BODY MOVE
            if my_body.pos in self.grid.door_slots:
                arrival_point = self.grid.adj_tiles(my_body.pos, playing=True)
                my_body.move_track = my_body.move_to_tile(self.grid, arrival_point)
                my_body.direction = None

        self.grid.sort_items_by_layer()

        self.grid.set_occupado()

        self.grid.clock.tick(self.grid.fps)