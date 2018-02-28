# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                   UPDATE                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
from grid_util import get_mirror_point, intersecting, get_short_name, in_circle
from grid_gen import ItemGenerator


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
                    if lname not in [it.name for it in self.grid.circles]:
                        LOSE_GAME = True

        for cond in self.grid.win_cond:
            if 'places' in cond.keys():
                wname = cond['item_name']
                places = [str(place) for place in cond['places']]
                witems = [self.grid.pos_to_name(wit.pos) for wit in self.grid.circles if wname in wit.name]
                if sorted(places) == sorted(witems):
                    win_count += 1
            elif 'cond' in cond.keys():
                wname = cond['item_name']
                wcond = cond['cond']
                if 'not in items' in wcond:
                    if wname not in [it.name for it in self.grid.circles]:
                        win_count += 1

            if win_count == len(self.grid.win_cond):
                WIN_GAME = True

        if LOSE_GAME:
            for lmsg in self.grid.lose_msg:
                self.grid.msg("SCREEN - %s" % lmsg)
            self.grid.game_over = True

        elif WIN_GAME:
            for wmsg in self.grid.win_msg:
                self.grid.msg("SCREEN - %s" % wmsg)
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
            my_body.move_track = {'center':'', 'track':[]}
            if not my_body in self.grid.circles:
                self.grid.circles.append(my_body)

            my_body.pos = get_mirror_point(item.pos, self.grid.center_tile)
            self.grid.revealed_tiles[my_body.pos] = []
            my_body.gen_birth_track()
            for circle in self.grid.circles:
                if circle.pos == my_body.pos and 'door' in circle.type:
                    circle.available = True

    # --------------------------------------------------------------- #
    #                                                                 #
    #                           DESTRUCTION                           #
    #                                                                 #
    # --------------------------------------------------------------- #
    def destruction(self, item):

        self.grid.messages = self.grid.messages
        # if item.name in ['my_body']:
        #     self.grid.msg("SCREEN - you dead")

        if not item.birth_track:

            item.available = False
            self.grid.msg("DEBUG - Destroying: {0}".format(item.name))
            if item in self.grid.circles:
                self.grid.circles.remove(item)
            # if item in self.grid.panel_circles.values():
            #     del self.grid.panel_circles[item.name]
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
                item.destroy(self.grid)

        # VIBE TIMER
        if hasattr(item, "vfreq"):
            if item.vfreq and not isinstance(item.vfreq, (float, int)):
                if item.vfreq.duration and not item.move_track:
                    item.vfreq.tick()
                    if item.vfreq.is_over:
                        do_action = False
                        if not hasattr(item, 'tok'):
                            do_action = True
                        elif item.tok > 0:
                            do_action = True

                        if do_action:

                            if hasattr(item, 'range'):
                                if item.range and not item.move_track and item.vfreq:
                                    item.gen_vibe_track(self.grid)
                                    item.vfreq.restart()
                            if hasattr(item, 'action'):
                                item.action(self.grid)

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
        if "signal" in signal.type:
            if not signal.marked_for_destruction:
                if (signal.pos in self.grid.occupado_tiles.values() and not signal.intersects(
                        sender)) or signal.direction == None:
                    signal.destroy(self.grid)
                    hit = True
        return hit

    def signal_hit_effect(self, signal, sender):
        for hit_circle in self.grid.circles:
            if hit_circle.available and not get_short_name(hit_circle.name) == get_short_name(signal.name):
                if not signal.intersects(sender):
                    cir1 = (hit_circle.pos, hit_circle.radius)
                    cir2 = (signal.pos, signal.radius)
                    if intersecting(cir1, cir2):
                        if self.grid.event_effects.consume(hit_circle, signal):
                            self.grid.msg("SCREEN - %s eat %s" % (get_short_name(hit_circle.name),
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
        all_circles = self.grid.circles + self.grid.panel_circles.values()
        if not self.grid.game_menu:

            # ITEMS
            for circle in all_circles:

                # OCCUPADO
                # self.update_occupado(item)

                # MY_BODY OVERLAP
                if not any (otype in circle.type for otype in ["my_body", "option"]):
                    if circle.pos == my_body.pos and not circle.birth_track:
                        circle.clickable = False
                        circle.radius = circle.default_radius

                    elif circle.pos != my_body.pos and circle not in self.grid.overlap:
                        circle.clickable = True

                # ENTER
                if self.grid.needs_to_change_room:
                    my_body.vibe_track = {'center': '', 'track': []}
                    self.enter_room(my_body, circle)

                # DESTRUCTION
                if circle.marked_for_destruction:
                    self.destruction(circle)

                if circle.available:

                    # TIMERS
                    self.timer_effect(circle)

                    # KISSING CIRCLES
                    # if circle.type == 'body':
                    #     for adj_circle in self.grid.circles:
                    #         if adj_circle.type == 'body' and adj_circle.pos in self.grid.adj_tiles(circle.pos):
                    #             circle.gen_fat()

                    # ANIMATE MOVEMENT
                    if circle.direction != None:
                        circle.gen_move_track(self.grid)
                    if circle.move_track and not circle.birth_track:
                        circle.pos = circle.move_track[0]
                        circle.move_track.pop(0)

                    # ANIMATE BIRTH
                    if circle.birth_track:
                        circle.radius = circle.birth_track[0]
                        circle.birth_track.pop(0)

                    # ANIMATE FAT
                    elif not circle.birth_track and circle.fat_track:
                        circle.radius = circle.fat_track[0]
                        circle.fat_track.pop(0)

                    # ANIMATE EFFECT
                    if circle.effect_track:
                        circle.effect_track.pop(0)
                        if not circle.effect_track:
                            circle.color = circle.default_color

                    # ANIMATE VIBE
                    if circle.vibe_track['track']:
                        vibe_area = ((circle.vibe_track['center']), circle.vibe_track['track'][0][0])
                        # REVEAL TILE
                        if circle in self.grid.circles:
                            for rtile in self.grid.playing_tiles:
                                if in_circle(circle.vibe_track['center'], circle.vibe_track['track'][0][0], rtile):
                                    if not rtile in circle.hit_tiles:
                                        circle.hit_tiles.append(rtile)
                                    if "#rev" in circle.effects:
                                        if not rtile in self.grid.revealed_tiles.keys():
                                            self.grid.revealed_tiles[rtile] = range(1, self.grid.tile_radius + 1)
                                            self.grid.total_revealed += 1
                                            self.igen.generate_item(rtile)
                                            # REVEAL ADJ DOORS
                                            for adj_rtile in self.grid.adj_tiles(rtile):
                                                for ditem in self.grid.circles:
                                                    if "door" in ditem.type and ditem.pos == adj_rtile:
                                                        if not ditem.available:
                                                            ditem.available = True
                                                            ditem.gen_birth_track()

                        for hit_item in self.grid.circles:
                            # REVEALED / AVAILABLE
                            if "#rev" in circle.effects:
                                if hit_item.pos in self.grid.revealed_tiles.keys():
                                    if not hit_item.available and not hit_item in self.grid.overlap:
                                        hit_item.available = True
                                        hit_item.gen_birth_track()

                            # CONSUME VIBE
                            if circle.effects:
                                if hit_item.available and not get_short_name(hit_item.name) == get_short_name(circle.name):
                                    cir1 = (hit_item.pos, hit_item.radius - (hit_item.radius / self.radius_buffer))
                                    if intersecting(cir1, vibe_area):
                                        if not hit_item in circle.hit_circles:
                                            self.grid.event_effects.consume(hit_item, circle)
                                            circle.hit_circles.append(hit_item)

                        circle.vibe_track['track'].pop(0)
                        if not circle.vibe_track['track']:
                            circle.hit_circles = []
                            circle.hit_tiles = []

                    # CONSUME SIGNAL
                    if 'signal' in circle.type:
                        if self.signal_hit(circle, my_body) and circle != my_body:
                            self.signal_hit_effect(circle, my_body)

                    # CLEAN PLACEHOLDERS
                    self.grid.clean_placeholders(circle)
            # for

            # FORCE BODY MOVE
            if my_body.pos in self.grid.door_slots:
                arrival_point = self.grid.adj_tiles(my_body.pos, playing=True)
                my_body.move_track = my_body.move_to_tile(self.grid, arrival_point)
                my_body.direction = None

        self.grid.sort_circles_by_layer()

        self.grid.set_occupado()

        self.grid.clock.tick(self.grid.fps)

        self.check_conditions()