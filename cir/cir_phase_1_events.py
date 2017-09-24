# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                    EVENTS                                                           #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import time
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
    #                         MOUSE MODES                             #
    #                                                                 #
    # --------------------------------------------------------------- #

    def laino_mode_click(self, current_tile):
        if current_tile not in self.grid.occupado_tiles.values() and current_tile in self.grid.revealed_tiles:
            self.produce("product_shit", current_tile)

    def see_mode_click(self, current_tile):
        if current_tile not in self.grid.occupado_tiles.values() and current_tile in self.grid.revealed_tiles:
            new_observer = self.produce("observer", current_tile)
            new_observer.lifespan.restart()

    def echo_mode_click(self, current_tile, my_body):
        """ Signal effect """
        self.grid.msg("SCREEN - Echo!")
        if not cir_utils.in_circle(my_body.pos, my_body.radius, current_tile) and not my_body.move_track:
            signal = self.produce("signal",
                                  my_body.pos,
                                  radius=int(self.grid.tile_radius / 3),
                                  birth=0)
            signal.color = my_body.color
            signal.direction = signal.get_aiming_direction(self.grid, current_tile)[1]


    def terminate_mode_click(self, current_tile):
        """ Terminate this shit """
        non_terminates = [
            "my_body",
            "editor",
            "option",
            "trigger",
            "placeholder"
            ]
        if not any(non_terminate in current_tile.type for non_terminate in non_terminates):
            current_tile.destroy(self.grid, fast=True)

    def collect_mode_click(self, my_body, clicked_item):
        """ Collect item: add it to inventory options """
        # CHECK FOR EMPTY SLOT IN BAG
        inventory_placeholder = None
        inventory = my_body.inventory
        reopen_inventory = False

        if inventory.in_menu:
            inventory.close_menu(self.grid)
            reopen_inventory = True
            backup_mouse_mode = self.grid.mouse_mode
            backup_mouse_img = self.grid.mouse_img
            backup_body_mode = my_body.mode

        for empty_item in inventory.options.values():
            if "inventory_placeholder" in empty_item.name:
                inventory_placeholder = empty_item
                break

        # PRODUCE MODABLE ITEM AS OPTION
        if inventory_placeholder:
            item_name = cir_utils.get_short_name(inventory_placeholder.name)

            item_as_option = self.produce(product_name=item_name,
                                          pos=inventory_placeholder.pos,
                                          birth=0,
                                          add_to_items=False)
            item_as_option.name = clicked_item.name + str(time.time())
            item_as_option.type = "option"
            item_as_option.modable = True
            item_as_option.consumable = True
            item_as_option.color = clicked_item.color
            item_as_option.img = clicked_item.img
            item_as_option.uses = clicked_item.uses
            # ADD IN BAG AND REMOVE FROM FIELD
            if inventory_placeholder in my_body.inventory.options.values():
                my_body.inventory.options = {k:v for k, v in my_body.inventory.options.items() if not v == inventory_placeholder}
            inventory.options[item_as_option.name] = item_as_option
            clicked_item.destroy(self.grid, fast=True)
        else:
            self.grid.msg("SCREEN - No space in bag")

        if reopen_inventory:
            inventory.open_menu(self.grid)
            self.grid.mouse_mode = backup_mouse_mode
            self.grid.mouse_img = backup_mouse_img
            my_body.mode = backup_body_mode


    def empty_inventory(self, inventory_item):

        inventory_item.uses -= 1
        if inventory_item.uses < 1:
            if cir_utils.get_short_name(self.grid.mouse_mode) in inventory_item.name:
                self.grid.clean_mouse()
            inventory_item.name = "inventory_placeholder" + str(time.time())
            inventory_item.modable = False
            inventory_item.color = None
            inventory_item.img = None
            inventory_item.uses = 0



    def drop_mode_click(self, current_tile, my_body):
        """
        Drops item
        """

        # Drop item from inventory to body and consume
        if current_tile == my_body.pos:
            for bag_item in my_body.inventory.options.values():
                if self.grid.mouse_mode in bag_item.name and bag_item.uses >= 1:
                    if bag_item.consumable:
                        self.consume(my_body, bag_item)
                        self.empty_inventory(bag_item)
                        break

        # Drop item on an empty tile
        elif current_tile not in self.grid.occupado_tiles.values() and current_tile in self.grid.playing_tiles:
            for bag_item in my_body.inventory.options.values():
                if self.grid.mouse_mode in bag_item.name and bag_item.uses >= 1:

                    item_name = cir_utils.get_short_name(self.grid.mouse_mode)
                    self.produce(item_name, current_tile)

                    self.empty_inventory(bag_item)
                    break
        else:
            self.grid.msg("SCREEN - No place here")

    # --------------------------------------------------------------- #
    #                                                                 #
    #                           KEY EVENTS                            #
    #                                                                 #
    # --------------------------------------------------------------- #
    def execute_key_events(self, event, my_body):
        # --------------------------------------------------------------- #
        #                             ESCAPE                              #
        # --------------------------------------------------------------- #
        if event.key == self.grid.pygame.K_ESCAPE:
            if not self.grid.game_menu:
                self.grid.rename_button("replay", "play")
                self.grid.game_menu = True

                if self.grid.current_room in ["999"]:
                    self.grid.event_effects.show_map(my_body)
                    self.grid.game_menu = False
        # --------------------------------------------------------------- #
        #                             SPACE                               #
        # --------------------------------------------------------------- #
        elif event.key == self.grid.pygame.K_SPACE:

            # GEN RADAR
            my_body.gen_vibe_track(self.grid)

            # DEBUG
            cir_utils.show_debug_on_space(self.grid, my_body)
        # --------------------------------------------------------------- #
        #                             NUMBERS                             #
        # --------------------------------------------------------------- #
        elif event.key == self.grid.pygame.K_1:
            self.grid.msg("INFO - Key 1 pressed")
            self.grid.change_room("11_11")
        elif event.key == self.grid.pygame.K_2:
            self.grid.msg("INFO - Key 2 pressed")
            self.grid.change_room("11_9")
        elif event.key == self.grid.pygame.K_3:
            self.grid.msg("INFO - Key 3 pressed")
            self.grid.change_room("11_7")
        # --------------------------------------------------------------- #
        #                             OTHER                               #
        # --------------------------------------------------------------- #
        elif not my_body.in_menu:
            my_body.gen_direction(self.grid.pygame, self.grid, event)


    # --------------------------------------------------------------- #
    #                                                                 #
    #                         CLICK EVENTS                            #
    #                                                                 #
    # --------------------------------------------------------------- #
    def execute_click_events(self, my_body, current_tile):

        mouse_mode = self.grid.mouse_mode

        # --------------------------------------------------------------- #
        #                    MOUSE MODE CLICK NO ITEM                     #
        # --------------------------------------------------------------- #
        if mouse_mode in ["laino", "EDITOR2"]:
            self.laino_mode_click(current_tile)

        elif mouse_mode in ["shit"]:
            self.laino_mode_click(current_tile)

        elif mouse_mode in ["see", "EDITOR1"]:
            self.see_mode_click(current_tile)

        elif mouse_mode in ["EDITOR3"]:
            if current_tile not in self.grid.occupado_tiles.values() and current_tile in self.grid.revealed_tiles:
                self.produce("block_of_steel", current_tile)

        elif mouse_mode == "echo":
            self.echo_mode_click(current_tile, my_body)

        elif mouse_mode and any(mouse_mode in inventory_item.name for inventory_item in my_body.inventory.options.values()):
            self.drop_mode_click(current_tile, my_body)

        # --------------------------------------------------------------- #
        #                   CLICK ON ITEMS NO MOUSE MODE                  #
        # --------------------------------------------------------------- #
        for CLICKED_ITEM in self.grid.items:
            if CLICKED_ITEM.clickable and CLICKED_ITEM.available:
                if current_tile == CLICKED_ITEM.pos:

                    self.grid.msg("INFO - Clicked CLICKED_ITEM: {0}".format(CLICKED_ITEM.name))

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
                    elif CLICKED_ITEM.type == "door":
                        self.enter_room(my_body, CLICKED_ITEM)

                    # SET MOUSE MODE
                    if CLICKED_ITEM.modable and not (mouse_mode in ['eat'] and CLICKED_ITEM.consumable):
                        self.grid.set_mouse_mode(CLICKED_ITEM)
                        my_body.mode = CLICKED_ITEM.name

                    # SET MENU
                    if CLICKED_ITEM.in_menu and not mouse_mode:
                        if not CLICKED_ITEM.mode and not (CLICKED_ITEM.has_opts and CLICKED_ITEM.type == "option"):
                            CLICKED_ITEM.close_menu(self.grid)

                    elif CLICKED_ITEM.has_opts and not CLICKED_ITEM.in_menu:
                        if (mouse_mode in CLICKED_ITEM.options.keys() or not mouse_mode):
                            CLICKED_ITEM.open_menu(self.grid)

                    # --------------------------------------------------------------- #
                    #                   MOUSE MODE CLICK ON ITEM                      #
                    # --------------------------------------------------------------- #
                    # EAT
                    if mouse_mode in ["eat"]:
                        if CLICKED_ITEM.consumable:
                            if (CLICKED_ITEM.pos in self.grid.adj_tiles(my_body.pos)) or (CLICKED_ITEM in my_body.inventory.options.values()):
                                self.consume(my_body, CLICKED_ITEM)
                                if CLICKED_ITEM in my_body.inventory.options.values():
                                    self.empty_inventory(CLICKED_ITEM)
                                else:
                                    CLICKED_ITEM.destroy(self.grid)
                            else:
                                self.grid.msg("SCREEN - It far")
                        else:
                            self.grid.msg("SCREEN - No eat this")

                    # TERMINATE
                    elif mouse_mode in ["EDITOR9"]:
                        self.terminate_mode_click(CLICKED_ITEM)

                    # COLLECT
                    elif mouse_mode in ["collect"]:
                        if CLICKED_ITEM.collectible:
                            self.collect_mode_click(my_body, CLICKED_ITEM)

                # CLOSE MENU IF OUTSIDE ADJ ITEMS
                elif current_tile not in self.grid.adj_tiles(CLICKED_ITEM.pos):
                    if CLICKED_ITEM.in_menu:
                        if not CLICKED_ITEM.type == "inventory":
                            CLICKED_ITEM.close_menu(self.grid)

        # DEBUG
        cir_utils.show_debug_on_click(self.grid, current_tile, my_body)
