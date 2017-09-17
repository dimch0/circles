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
        self.grid.msg("DISPLAY - Echo!")
        if not cir_utils.in_circle(my_body.pos, my_body.radius, current_tile) and not my_body.move_track:
            signal = self.produce("signal",
                                  my_body.pos,
                                  radius=int(self.grid.tile_radius / 3),
                                  birth=0)
            signal.color = my_body.color
            signal.direction = signal.get_aiming_direction(self.grid, current_tile)[1]

    def eat_mode_click(self, item):
        """ Eat that shit """
        self.grid.msg("DISPLAY - Nom nom nom")
        item.destroy(self.grid)

    def terminate_mode_click(self, current_tile):
        """ Eat that shit """
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
        """ Collect item: add it to bag options """
        # CHECK FOR EMPTY SLOT IN BAG
        bag_placeholder = None
        bag = my_body.inventory
        reopen_bag = False

        if bag.in_menu:
            bag.close_menu(self.grid)
            reopen_bag = True
            backup_mouse_mode = self.grid.mouse_mode
            backup_mouse_img = self.grid.mouse_img
            backup_body_mode = my_body.mode

        for empty_item in bag.options.values():
            if "bag_placeholder" in empty_item.name:
                bag_placeholder = empty_item
                break

        # PRODUCE MODABLE ITEM AS OPTION
        if bag_placeholder:
            item_name = cir_utils.get_short_name(bag_placeholder.name)

            item_as_option = self.produce(product_name=item_name,
                                          pos=bag_placeholder.pos,
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
            if bag_placeholder in my_body.inventory.options.values():
                my_body.inventory.options = {k:v for k, v in my_body.inventory.options.items() if not v == bag_placeholder}
            bag.options[item_as_option.name] = item_as_option
            clicked_item.destroy(self.grid, fast=True)
        else:
            self.grid.msg("DISPLAY - No space in bag")

        if reopen_bag:
            bag.open_menu(self.grid)
            self.grid.mouse_mode = backup_mouse_mode
            self.grid.mouse_img = backup_mouse_img
            my_body.mode = backup_body_mode


    def empty_inventory(self, bag_item):

        bag_item.uses -= 1
        if bag_item.uses < 1:
            print cir_utils.get_short_name(self.grid.mouse_mode)
            print self.grid.mouse_mode
            print bag_item.name
            if cir_utils.get_short_name(self.grid.mouse_mode) in bag_item.name:
                self.grid.clean_mouse()
            bag_item.name = "bag_placeholder" + str(time.time())
            bag_item.modable = False
            bag_item.color = None
            bag_item.img = None
            bag_item.uses = 0



    def drop_mode_click(self, current_tile, my_body):
        """
        Drops item
        """
        if current_tile == my_body.pos:
            for bag_item in my_body.inventory.options.values():
                if self.grid.mouse_mode in bag_item.name and bag_item.uses >= 1:
                    if bag_item.consumable:

                        self.empty_inventory(bag_item)
                        break

        elif current_tile not in self.grid.occupado_tiles.values() and current_tile in self.grid.playing_tiles:
            for bag_item in my_body.inventory.options.values():
                if self.grid.mouse_mode in bag_item.name and bag_item.uses >= 1:

                    item_name = cir_utils.get_short_name(self.grid.mouse_mode)
                    self.produce(item_name, current_tile)

                    self.empty_inventory(bag_item)
                    break
        else:
            self.grid.msg("DISPLAY - No place here")

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
    def execute_click_events(self, event, my_body, current_tile):

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
        for item in self.grid.items:
            if item.clickable and item.available:
                if current_tile == item.pos:

                    self.grid.msg("INFO - Clicked item: {0}".format(item.name))

                    # OPTION CLICKED
                    if item.type == "option":
                        ober_item = item.get_ober_item(self.grid)
                        if ober_item:
                            # CLOSE MENU
                            if ober_item.in_menu and not ober_item.type in ["inventory"]:
                                ober_item.close_menu(self.grid)

                            # SUICIDE
                            if item.name == "suicide":
                                ober_item.destroy(self.grid)

                            # MITOSIS
                            elif item.name == "mitosis":
                                self.mitosis(ober_item)

                            # SMEL
                            elif item.name == "smel":
                                self.grid.msg("DISPLAY - Sniff hair")

                            # MEDI
                            elif item.name == "medi":
                                self.satellite()
                                self.grid.msg("DISPLAY - Ommmm")
                                # ober_item.range += 3
                                # ober_item.vibe_speed += 3
                                # my_body.gen_radar_track(self.grid)
                                # ober_item.vibe_speed -= 3
                                # ober_item.range -= 3

                            # SPEED
                            elif item.name == "move":
                                ober_item.change_speed(0.1)

                    # EDITOR
                    elif item.type == "editor" and self.editor:
                        self.editor.execute_editor_clicks(item, my_body)

                    # ENTER
                    elif item.type == "door":
                        self.enter_room(my_body, item)

                    # SET MOUSE MODE
                    if item.modable and not (mouse_mode in ['eat'] and item.consumable):
                        self.grid.set_mouse_mode(item)
                        my_body.mode = item.name

                    # SET MENU
                    if item.in_menu and not mouse_mode:
                        if not item.mode and not (item.has_opts and item.type == "option"):
                            item.close_menu(self.grid)

                    elif item.has_opts and not item.in_menu:
                        if (mouse_mode in item.options.keys() or not mouse_mode):
                            item.open_menu(self.grid)

                    # --------------------------------------------------------------- #
                    #                   MOUSE MODE CLICK ON ITEM                      #
                    # --------------------------------------------------------------- #
                    # EAT
                    if mouse_mode in ["eat"]:
                        if item.consumable:
                            if item in my_body.inventory.options.values():
                                self.empty_inventory(item)
                                # TODO: Consume item
                                pass
                            else:
                                self.eat_mode_click(item)

                    # TERMINATE
                    elif mouse_mode in ["EDITOR9"]:
                        self.terminate_mode_click(item)

                    # COLLECT
                    elif mouse_mode in ["collect"]:
                        if item.collectible:
                            self.collect_mode_click(my_body, item)

                # CLOSE MENU IF OUTSIDE ADJ ITEMS
                elif current_tile not in self.grid.adj_tiles(item.pos):
                    if item.in_menu:
                        if not item.type == "inventory":
                            item.close_menu(self.grid)

        # DEBUG
        cir_utils.show_debug_on_click(self.grid, current_tile, my_body)
