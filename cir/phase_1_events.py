# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                    EVENTS                                                           #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import grid_util
from grid_effects import GameEffects


class GameEvents(GameEffects):

    def __init__(self, grid):
        super(GameEffects, self).__init__()
        self.grid = grid
        self.food_unit = 10

    # --------------------------------------------------------------- #
    #                                                                 #
    #                           KEY EVENTS                            #
    #                                                                 #
    # --------------------------------------------------------------- #
    def execute_key_events(self, event, my_body):

        if event.type == self.grid.pygame.KEYDOWN:

            numbers = [self.grid.pygame.K_1,
                       self.grid.pygame.K_2,
                       self.grid.pygame.K_3,
                       self.grid.pygame.K_4,
                       self.grid.pygame.K_5,
                       self.grid.pygame.K_6]
            # --------------------------------------------------------------- #
            #                             ESCAPE                              #
            # --------------------------------------------------------------- #
            if event.key == self.grid.pygame.K_ESCAPE:
                if not self.grid.game_menu:
                    self.grid.game_menu = True

                    if self.grid.current_room in ["map"]:
                        self.grid.event_effects.show_map(my_body)
                        self.grid.game_menu = False
            # --------------------------------------------------------------- #
            #                             SPACE                               #
            # --------------------------------------------------------------- #
            # elif event.key == self.grid.pygame.K_SPACE:
            #     # GEN VIBE
            #     my_body.gen_vibe_track(self.grid)
            # --------------------------------------------------------------- #
            #                             NUMBERS                             #
            # --------------------------------------------------------------- #
            elif event.key in numbers:
                number_pressed = numbers.index(event.key) + 1
                self.grid.msg("INFO - Key %s pressed" % number_pressed)
                if len(my_body.inventory.options.values()) >= number_pressed:
                    self.grid.set_mouse_mode(my_body.inventory.options.values()[number_pressed-1])
                else:
                    self.grid.clean_mouse()
            # --------------------------------------------------------------- #
            #                            SHIFT                                #
            # --------------------------------------------------------------- #
            elif event.key in [self.grid.pygame.K_RSHIFT, self.grid.pygame.K_LSHIFT]:
                self.grid.shift = True

            # --------------------------------------------------------------- #
            #                            QWEADS                               #
            # --------------------------------------------------------------- #
            else:

                # GEN DIRECTION
                my_body.gen_direction(self.grid, event)

                # CHECK FOR DOOR
                doors = {door.pos : door  for door in self.grid.circles if "door" in door.type}

                for doorpos, door in doors.items():
                    for adj_idx, adj_to_mybod  in enumerate(self.grid.adj_tiles(my_body.pos)):

                        if adj_to_mybod == doorpos:
                            if my_body.direction == adj_idx:
                                self.enter_room(my_body, door)

        # --------------------------------------------------------------- #
        #                            SHIFT                                #
        # --------------------------------------------------------------- #
        elif event.type == self.grid.pygame.KEYUP:
            if event.key in [self.grid.pygame.K_RSHIFT, self.grid.pygame.K_LSHIFT]:
                self.grid.shift = False
    # --------------------------------------------------------------- #
    #                                                                 #
    #                         CLICK EVENTS                            #
    #                                                                 #
    # --------------------------------------------------------------- #
    def execute_click_events(self, event, my_body, current_tile):

        mouse_mode = self.grid.mouse_mode
        all_circles = self.grid.circles + self.grid.panel_circles.values()
        # --------------------------------------------------------------- #
        #                    MOUSE MODE CLICK NO ITEM                     #
        # --------------------------------------------------------------- #
        if not event.button == 3:
            if current_tile not in self.grid.occupado_tiles.values() and current_tile in self.grid.revealed_tiles.keys():
                if mouse_mode and any(mouse_mode in inventory_item.name for inventory_item in my_body.inventory.options.values()):
                    self.drop(current_tile, my_body)

            if mouse_mode == "echo":
                self.echo_mode_click(current_tile, my_body)

        # --------------------------------------------------------------- #
        #                   CLICK ON ITEMS NO MOUSE MODE                  #
        # --------------------------------------------------------------- #
        for CLICKED_ITEM in all_circles:
            clicked_screen_name = grid_util.get_short_name(CLICKED_ITEM.name).replace('_', ' ')
            if CLICKED_ITEM.clickable and CLICKED_ITEM.available and CLICKED_ITEM.type not in ["trigger"]:
                if current_tile == CLICKED_ITEM.pos:
                    self.grid.msg("INFO - clicked item: {0} {1} {2}".format(
                                                    CLICKED_ITEM.name,
                                                    CLICKED_ITEM.pos,
                                                    CLICKED_ITEM.available))

                    # OPTION CLICKED
                    if "option" in CLICKED_ITEM.type:
                        ober_item = CLICKED_ITEM.get_ober_item(self.grid)
                        if ober_item:

                            # SLAB
                            if CLICKED_ITEM.name in ["map_app"]:
                                self.grid.event_effects.show_map(my_body)
                            elif CLICKED_ITEM.name in ["sat_app"] and not self.grid.current_room in ["map"]:
                                if mouse_mode and 'battery' in mouse_mode:
                                    self.grid.event_effects.satellite()
                                    self.grid.event_effects.drop(CLICKED_ITEM, my_body, force=True)
                                    CLICKED_ITEM.boost = []
                                    CLICKED_ITEM.tok = 0
                                else:
                                    self.grid.msg("SCREEN - No bat")
                            elif CLICKED_ITEM.name in ["phone"]:
                                self.grid.show_debug = not self.grid.show_debug
                                self.grid.show_grid = not self.grid.show_grid

                            # SUICIDE
                            if CLICKED_ITEM.name == "suicide":
                                my_body.destroy(self.grid)

                            # MITOSIS
                            elif CLICKED_ITEM.name == "mitosis":
                                self.mitosis(ober_item)

                            # SMEL
                            elif CLICKED_ITEM.name == "smel":
                                self.grid.msg("SCREEN - Sniff hair")


                    # SET MOUSE MODE
                    if CLICKED_ITEM.modable:
                        self.grid.set_mouse_mode(CLICKED_ITEM)

                    # --------------------------------------------------------------- #
                    #                   MOUSE MODE CLICK ON ITEM                      #
                    # --------------------------------------------------------------- #
                    # EAT
                    if mouse_mode in ["eat"] or event.button == 3:
                        if CLICKED_ITEM.consumable and not CLICKED_ITEM.birth_track:
                            if (CLICKED_ITEM.pos in self.grid.adj_tiles(my_body.pos)) or (CLICKED_ITEM in my_body.inventory.options.values()):
                                if self.consume(my_body, CLICKED_ITEM):
                                    if CLICKED_ITEM in my_body.inventory.options.values():
                                        self.empty_inventory(CLICKED_ITEM)
                                    else:
                                        CLICKED_ITEM.destroy(self.grid)
                                else:
                                    self.grid.msg("SCREEN - no eat %s" % clicked_screen_name)
                            else:
                                self.grid.msg("SCREEN - %s is far" % clicked_screen_name)
                        else:
                            self.grid.msg("SCREEN - no eat %s" % clicked_screen_name)

                    # DROP
                    elif mouse_mode and any(mouse_mode in inventory_item.name for inventory_item in my_body.inventory.options.values()):
                        self.drop(CLICKED_ITEM, my_body)

                    # COLLECT
                    elif mouse_mode in ["collect", None, ""]:
                        if CLICKED_ITEM.collectible:
                            if (CLICKED_ITEM.pos in self.grid.adj_tiles(my_body.pos)):
                                self.collect(my_body, CLICKED_ITEM)
                            else:
                                self.grid.msg("SCREEN - {0} is far".format(clicked_screen_name))

                # CLEAN MOUSE IF OUTSIDE ADJ ITEMS
                elif CLICKED_ITEM.pos and current_tile not in self.grid.adj_tiles(CLICKED_ITEM.pos):
                    if event.button == 3:
                        self.grid.clean_mouse()

        # DEBUG
        grid_util.show_debug_on_click(self.grid, current_tile, my_body)
