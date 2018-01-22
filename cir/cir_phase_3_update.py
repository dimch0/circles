# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                   UPDATE                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
from cir_utils import get_mirror_point, intersecting, get_short_name, in_circle
from cir_gen import ItemGenerator


class VarUpdater(object):

    def __init__(self, grid=None, my_body=None):
        self.grid = grid
        self.my_body = my_body
        self.igen = ItemGenerator(grid, my_body)
        self.radius_buffer = 2.5

    def check_conditions(self):
        """ Check win / lose conditions """
        LOSE_GAME = False
        WIN_GAME = False

        win_count = 0

        for lcond in self.grid.lose_cond:
            lname = lcond['item_name']

            if 'places' in lcond.keys():
                lplaces = lcond['places']
            if 'cond' in lcond.keys():
                lcondition = lcond['cond']
                if lcondition == "not in items":
                    if lname not in [it.name for it in self.grid.items]:
                        LOSE_GAME = True


        for cond in self.grid.win_cond:
            if 'places' in cond.keys():
                wname = cond['item_name']
                places = [str(place) for place in cond['places']]
                witems = [self.grid.pos_to_name(wit.pos) for wit in self.grid.items if wname in wit.name]
                if sorted(places) == sorted(witems):
                    win_count += 1
            elif 'cond' in cond.keys():
                wname = cond['item_name']
                wcond = cond['cond']
                if 'not in items' in wcond:
                    if wname not in [it.name for it in self.grid.items]:
                        win_count += 1

            if win_count == len(self.grid.win_cond):
                WIN_GAME = True



        if LOSE_GAME:
            self.grid.msg("SCREEN - no meat")
            self.grid.msg("SCREEN - you lose")
            self.grid.game_over = True

        elif WIN_GAME:
            self.grid.msg("SCREEN - dog in fence")
            self.grid.msg("SCREEN - you win")
            for report in self.grid.report:
                if hasattr(self.grid, report):
                    self.grid.msg("SCREEN - score %s" % getattr(self.grid, report))
            self.grid.game_over = True






    # --------------------------------------------------------------- #
    #                                                                 #
    #                        ENTER ROOM EFFECTS                       #
    #                                                                 #
    # --------------------------------------------------------------- #
    def enter_room(self, my_body, item):
        if "Enter_" in item.name and my_body.pos == item.pos:
            room_number = item.name.replace("Enter_", "")
            self.grid.msg("INFO - Leaving room: {0}".format(self.grid.current_room))
            self.grid.change_room(room_number)
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

        self.grid.messages = self.grid.messages
        if item.name in ['my_body']:
            self.grid.msg("SCREEN - you dead")

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
    def timer_effect(self, item):
        """ Timer effects  """

        # LIFESPAN
        if item.lifespan and not isinstance(item.lifespan, (float, int)):
            item.lifespan.tick()
            if item.lifespan.is_over:
                if hasattr(item, 'home'):
                    item.home.vfreq = item.home_vfreq
                    item.home.vfreq.restart()
                item.destroy(self.grid)

        # VIBE TIMER
        if hasattr(item, "vfreq"):
            if item.vfreq and not isinstance(item.vfreq, (float, int)):
                if item.vfreq.duration:
                    item.vfreq.tick()
                    if item.vfreq.is_over:
                        if hasattr(item, 'action'):
                            item.action(self.grid)

                        if hasattr(item, 'range'):
                            if item.range and not item.move_track:
                                item.gen_vibe_track(self.grid)
                                item.vfreq.restart()

        # BOOST TIMER
        if hasattr(item, "boost"):
            for boost_timer in item.boost:
                if boost_timer and not isinstance(boost_timer, (float, int)):
                    if boost_timer.duration:
                        boost_timer.tick()
                        if boost_timer.is_over:
                            self.grid.event_effects.consume(item, boost_timer)
                            item.default_color = boost_timer.store_color
                            item.boost.remove(boost_timer)
                            boost_timer.destroy(self.grid)


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

        for hit_item in self.grid.items:
            if hit_item.available and not hit_item.name == signal.name:
                cir1 = (hit_item.pos, hit_item.radius)
                cir2 = (signal.pos, signal.radius)
                if intersecting(cir1, cir2):
                    if self.grid.event_effects.consume(hit_item, signal):
                        self.grid.msg("SCREEN - %s eat %s" % (get_short_name(hit_item.name),
                                                              get_short_name(signal.name)))
                    else:
                        self.grid.msg("SCREEN - %s no eat %s" % (get_short_name(hit_item.name),
                                                              get_short_name(signal.name)))

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
                        if item in self.grid.items:
                            for rtile in self.grid.playing_tiles:
                                if in_circle(item.pos, item.vibe_track[0][0], rtile):
                                    if not rtile in item.hit_tiles:
                                        item.hit_tiles.append(rtile)
                                    if "#rev" in item.effects:
                                        if not rtile in self.grid.revealed_tiles.keys():
                                            self.grid.revealed_tiles[rtile] = range(1, self.grid.tile_radius + 1)
                                            self.igen.generate_item(rtile)
                                            # REVEAL ADJ DOORS
                                            for adj_rtile in self.grid.adj_tiles(rtile):
                                                for ditem in self.grid.items:
                                                    if "door" in ditem.type and ditem.pos == adj_rtile:
                                                        if not ditem.available:
                                                            ditem.available = True
                                                            ditem.gen_birth_track()

                        for hit_item in self.grid.items:
                            # REVEALED / AVAILABLE
                            if "#rev" in item.effects:
                                if hit_item.pos in self.grid.revealed_tiles.keys():
                                    if not hit_item.available and not hit_item in self.grid.overlap:
                                        hit_item.available = True
                                        hit_item.gen_birth_track()

                            # CONSUME VIBE
                            if item.effects:
                                if hit_item.available and not get_short_name(hit_item.name) == get_short_name(item.name):
                                    cir1 = (hit_item.pos, hit_item.radius - (hit_item.radius / self.radius_buffer))
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

        self.check_conditions()