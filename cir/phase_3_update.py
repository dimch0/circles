# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                   UPDATE                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
from grid_util import get_mirror_point, intersecting, get_short_name, in_circle
from grid_gen import ItemGenerator


class VarUpdater(object):

    def __init__(self, grid=None, mybody=None):
        self.grid = grid
        self.mybody = mybody
        self.igen = ItemGenerator(grid, mybody)
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
    def enter_room(self, mybody, item):
        if "Enter_" in item.name and mybody.pos == item.pos:
            room_number = item.name.replace("Enter_", "")
            self.grid.msg("INFO - Leaving room: {0}".format(self.grid.current_room))
            self.grid.change_room(room_number)
            self.grid.needs_to_change_room = False
            mybody.move_track = {'center':'', 'track':[]}
            if not mybody in self.grid.circles:
                self.grid.circles.append(mybody)

            mybody.pos = get_mirror_point(item.pos, self.grid.center_tile)
            self.grid.revealed_tiles[mybody.pos] = []
            mybody.gen_birth_track()
            for circle in self.grid.circles:
                if circle.pos == mybody.pos and 'door' in circle.type:
                    circle.available = True

    # --------------------------------------------------------------- #
    #                                                                 #
    #                           DESTRUCTION                           #
    #                                                                 #
    # --------------------------------------------------------------- #
    def destruction(self, item):

        self.grid.messages = self.grid.messages
        # if item.name in ['mybody']:
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
            if item.name == "mybody":
                self.grid.game_over = True

    # --------------------------------------------------------------- #
    #                                                                 #
    #                             TIMERS                              #
    #                                                                 #
    # --------------------------------------------------------------- #
    def circle_turn(self, circle):
        """ Timer effects  """

        # TIME
        if hasattr(circle, "time"):
            circle.time -= 1
            if circle.time <= 0:
                circle.destroy(self.grid)

        # VIBE
        if hasattr(circle, "vfreq") and hasattr(circle, 'range'):
            if circle.vfreq and circle.range and not circle.move_track:
                circle.gen_vibe_track(self.grid)

        # ACTION
        if hasattr(circle, 'action'):
            circle.action(self.grid)

        # BOOST TIME



    # --------------------------------------------------------------- #
    #                                                                 #
    #                           CHANGE VARS                           #
    #                                                                 #
    # --------------------------------------------------------------- #
    def update_vars(self, mybody):
        """
        Updarting all variables before next iteration of the main loop
        :param mybody: mybody instance
        """
        all_circles = self.grid.circles + self.grid.panel_circles.values()
        if not self.grid.game_menu:

            # TODO: SPENT TIME METHOD
            if not mybody.move_track and mybody.go_to_tile:
                self.grid.new_turn()
                print mybody.time, "/", mybody.max_time

            # ITEMS
            for circle in all_circles:

                # ENTER
                if self.grid.needs_to_change_room:
                    mybody.vibe_track = {'center': '', 'track': []}
                    self.enter_room(mybody, circle)

                # DESTRUCTION
                if circle.marked_for_destruction:
                    self.destruction(circle)

                if circle.available:

                    # ANIMATE MOVEMENT
                    if hasattr(circle, "go_to_tile") and circle.go_to_tile != None:
                        circle.move_to_tile_new(self.grid)

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
                                    if "#scout" in circle.effects:
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

                        for hit_circle in self.grid.circles:
                            # REVEALED / AVAILABLE
                            if "#scout" in circle.effects:
                                if hit_circle.pos in self.grid.revealed_tiles.keys():
                                    if not hit_circle.available and not hit_circle in self.grid.overlap:
                                        hit_circle.available = True
                                        hit_circle.gen_birth_track()

                            # CONSUME VIBE
                            if circle.effects:
                                if hit_circle.available and not get_short_name(hit_circle.name) == get_short_name(circle.name):
                                    cir1 = (hit_circle.pos, hit_circle.radius - (hit_circle.radius / self.radius_buffer))
                                    if intersecting(cir1, vibe_area):
                                        if not hit_circle in circle.hit_circles:
                                            self.grid.event_effects.consume(hit_circle, circle)
                                            circle.hit_circles.append(hit_circle)

                        circle.vibe_track['track'].pop(0)
                        if not circle.vibe_track['track']:
                            circle.hit_circles = []
                            circle.hit_tiles = []

                    # TIMER
                    if self.grid.new_turns:
                        self.circle_turn(circle)

                    # CLEAN PLACEHOLDERS
                    self.grid.clean_placeholders(circle)
            # for


            # FORCE BODY MOVE
            if mybody.pos in self.grid.door_slots:
                arrival_point = self.grid.adj_tiles(mybody.pos, playing=True)
                mybody.move_track = mybody.move_to_tile(self.grid, arrival_point)
                mybody.direction = None

            # END OF TURN
            if self.grid.new_turns:
                self.grid.new_turns -= 1

        self.grid.sort_circles_by_layer()

        self.grid.set_occupado()

        self.grid.clock.tick(self.grid.fps)

        self.check_conditions()