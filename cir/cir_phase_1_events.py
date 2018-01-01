# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                    EVENTS                                                           #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import cir_utils
from cir_editor import Editor
from cir_effects import GameEffects

class GameEvents(GameEffects):

    def __init__(self, grid):
        super(GameEffects, self).__init__()
        self.grid = grid
        if self.grid.show_editor:
            self.editor = Editor(grid=self.grid)
        else:
            self.editor = None


    # --------------------------------------------------------------- #
    #                                                                 #
    #                           KEY EVENTS                            #
    #                                                                 #
    # --------------------------------------------------------------- #
    def execute_key_events(self, event, my_body):

        if event.type == self.grid.pygame.KEYDOWN:
            # --------------------------------------------------------------- #
            #                             ESCAPE                              #
            # --------------------------------------------------------------- #
            if event.key == self.grid.pygame.K_ESCAPE:
                if not self.grid.game_menu:
                    self.grid.rename_button("replay", "play")
                    self.grid.game_menu = True

                    if self.grid.current_room in ["map"]:
                        self.grid.event_effects.show_map(my_body)
                        self.grid.game_menu = False
            # --------------------------------------------------------------- #
            #                             SPACE                               #
            # --------------------------------------------------------------- #
            elif event.key == self.grid.pygame.K_SPACE:
                # GEN VIBE
                my_body.gen_vibe_track(self.grid)
            # --------------------------------------------------------------- #
            #                             NUMBERS                             #
            # --------------------------------------------------------------- #
            elif event.key == self.grid.pygame.K_1:

                self.grid.msg("INFO - Key 1 pressed")
                # EFFECT_GEN
                my_body.gen_effect_track(self.grid.white)

                # self.grid.change_room("11_11")
            elif event.key == self.grid.pygame.K_2:
                self.grid.msg("INFO - Key 2 pressed")
                self.grid.change_room("11_9")
            elif event.key == self.grid.pygame.K_3:
                self.grid.msg("INFO - Key 3 pressed")
                self.grid.change_room("11_7")
            # --------------------------------------------------------------- #
            #                            SHIFT                                #
            # --------------------------------------------------------------- #
            elif event.key in [self.grid.pygame.K_RSHIFT, self.grid.pygame.K_LSHIFT]:
                self.grid.shift = True

            # --------------------------------------------------------------- #
            #                            QWEADS                               #
            # --------------------------------------------------------------- #
            elif not my_body.in_menu:

                # GEN DIRECTION
                my_body.gen_direction(self.grid.pygame, self.grid, event)

                # CHECK FOR DOOR
                doors = {door.pos : door  for door in self.grid.items if "door" in door.type}

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

        # --------------------------------------------------------------- #
        #                    MOUSE MODE CLICK NO ITEM                     #
        # --------------------------------------------------------------- #
        if not event.button == 3:
            if current_tile not in self.grid.occupado_tiles.values() and current_tile in self.grid.revealed_tiles.keys():
                if mouse_mode in ["edit_scout"]:
                    self.produce("scout", current_tile)

                elif mouse_mode in ["edit_poop"]:
                    self.produce("shit", current_tile)

                elif mouse_mode in ["edit_cube"]:
                    self.produce("block_of_steel", current_tile)

            if mouse_mode == "echo":
                self.echo_mode_click(current_tile, my_body)

            elif mouse_mode and any(mouse_mode in inventory_item.name for inventory_item in my_body.inventory.options.values()):
                self.drop(current_tile, my_body)

        # --------------------------------------------------------------- #
        #                   CLICK ON ITEMS NO MOUSE MODE                  #
        # --------------------------------------------------------------- #
        for CLICKED_ITEM in self.grid.items:
            if CLICKED_ITEM.clickable and CLICKED_ITEM.available and CLICKED_ITEM.type not in ["trigger"]:
                if current_tile == CLICKED_ITEM.pos:
                    self.grid.msg("INFO - clicked item: {0} {1} {2}".format(
                                                    CLICKED_ITEM.name,
                                                    CLICKED_ITEM.pos,
                                                    CLICKED_ITEM.available))

                    # OPTION CLICKED
                    if CLICKED_ITEM.type == "option":
                        ober_item = CLICKED_ITEM.get_ober_item(self.grid)
                        if ober_item:
                            # CLOSE MENU
                            if ober_item.in_menu and not ober_item.type in ["inventory"]:
                                ober_item.close_menu(self.grid)

                            # SUICIDE
                            if CLICKED_ITEM.name == "suicide":
                                ober_item.destroy(self.grid)

                            # MITOSIS
                            elif CLICKED_ITEM.name == "mitosis":
                                self.mitosis(ober_item)

                            # SMEL
                            elif CLICKED_ITEM.name == "smel":
                                self.grid.msg("SCREEN - Sniff hair")

                            # MEDI
                            elif CLICKED_ITEM.name == "medi":
                                self.satellite()
                                self.grid.msg("SCREEN - Ommmm")
                                # ober_item.range += 3
                                # ober_item.vibe_speed += 3
                                # my_body.gen_radar_track(self.grid)
                                # ober_item.vibe_speed -= 3
                                # ober_item.range -= 3

                            # SPEED
                            elif CLICKED_ITEM.name == "move":
                                ober_item.change_speed(0.1)

                    # EDITOR
                    elif CLICKED_ITEM.type == "editor" and self.editor:
                        self.editor.execute_editor_clicks(CLICKED_ITEM, my_body)

                    # ENTER
                    # elif "door" in CLICKED_ITEM.type:
                    #     self.enter_room(my_body, CLICKED_ITEM)

                    # SET MOUSE MODE
                    if CLICKED_ITEM.modable and not (mouse_mode in ['eat'] and CLICKED_ITEM.consumable):
                        self.grid.set_mouse_mode(CLICKED_ITEM)

                    # SET MENU
                    if CLICKED_ITEM.in_menu and not mouse_mode:
                        if not (CLICKED_ITEM.has_opts and CLICKED_ITEM.type == "option"):
                            CLICKED_ITEM.close_menu(self.grid)

                    elif CLICKED_ITEM.has_opts and not CLICKED_ITEM.in_menu:
                        if (mouse_mode in CLICKED_ITEM.options.keys() or not mouse_mode):
                            CLICKED_ITEM.open_menu(self.grid)

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
                                    self.grid.msg("SCREEN - no eat %s" % CLICKED_ITEM.name)
                            else:
                                self.grid.msg("SCREEN - {0} is far".format(CLICKED_ITEM.name))
                        else:
                            self.grid.msg("SCREEN - no eat %s" % CLICKED_ITEM.name)

                    # DROP
                    elif mouse_mode and any(mouse_mode in inventory_item.name for inventory_item in my_body.inventory.options.values()):
                            self.drop(CLICKED_ITEM, my_body)

                    # TERMINATE
                    elif mouse_mode in ["edit_del"]:
                        self.terminate_mode_click(CLICKED_ITEM)

                    # COLLECT
                    elif mouse_mode in ["collect", None, ""]:
                        if CLICKED_ITEM.collectible:
                            if (CLICKED_ITEM.pos in self.grid.adj_tiles(my_body.pos)):
                                self.collect(my_body, CLICKED_ITEM)
                            else:
                                self.grid.msg("SCREEN - {0} is far".format(CLICKED_ITEM.name))

                # CLOSE MENU IF OUTSIDE ADJ ITEMS
                elif current_tile not in self.grid.adj_tiles(CLICKED_ITEM.pos):
                    if event.button == 3:
                        self.grid.clean_mouse()
                    if CLICKED_ITEM.in_menu:
                        if not CLICKED_ITEM.type == "inventory":
                            CLICKED_ITEM.close_menu(self.grid)

        # DEBUG
        cir_utils.show_debug_on_click(self.grid, current_tile, my_body)
