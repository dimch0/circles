#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                                    Main file                                        #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################
# --------------------------------------------------------------- #
#                            Features                             #
# --------------------------------------------------------------- #
# TODO: Create map (screenshot all rooms) room 401
# TODO: Create inside body view room 400
# TODO: Create spirit mode NEW SCENARIO
# TODO: Log statistics during a lifespan, calculate karma
# TODO: Create save button
# TODO: Create load button
# TODO: Create installation .exe file
# TODO: Create reverse get position
# TODO: Item generation
# --------------------------------------------------------------- #
#                            Animation                            #
# --------------------------------------------------------------- #
# TODO: Indicate uses / meters
# TODO: Animate item activation
# TODO: Animate demo
# TODO: Add sounds
# TODO: Log messages on screen
# --------------------------------------------------------------- #
#                            Bug fixes                            #
# --------------------------------------------------------------- #
# TODO: Fix mitosis (lag, overlap)
# TODO: Fix item collection
# TODO: Improve item options
# TODO: remove everything dict
# --------------------------------------------------------------- #
#                            Imports                              #
# --------------------------------------------------------------- #
import time
import pygame
pygame.init()
from cir import cir_utils
from cir import cir_grid
from cir import cir_cosmetic
from cir.cir_draw import GameDrawer
from cir.cir_loader import DataLoader
from cir.cir_effects import GameEffects


def game_loop(game_over, scenario="Scenario_1"):
    # --------------------------------------------------------------- #
    #                            LOADING                              #
    # --------------------------------------------------------------- #
    grid            = cir_grid.Grid(pygame, scenario)
    grid.images     = cir_cosmetic.Images(grid, pygame)
    grid.fonts      = cir_cosmetic.Fonts(grid, pygame)
    loader          = DataLoader(grid)
    drawer          = GameDrawer(grid, pygame)
    effects         = GameEffects(grid, loader)
    my_body         = loader.load_items()
    grid.start_time = time.time()

    if game_over:
        grid.rename_button("play", "replay")
    if scenario == "Scenario_2":
        grid.game_menu = False

    # --------------------------------------------------------------- #
    #                         TEST TESTING PLACE                      #
    # --------------------------------------------------------------- #
    # my_body.lifespan.duration = 60

    print "Game started"

    while not grid.game_over:

        current_tile = grid.mouse_in_tile(pygame.mouse.get_pos())

        grid.seconds_in_game_tick()

        # --------------------------------------------------------------- #
        #                            EVENTS                               #
        # --------------------------------------------------------------- #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                # TODO: Create a key sector class
                # --------------------------------------------------------------- #
                #                             'Escape'                               #
                # --------------------------------------------------------------- #
                if event.key == pygame.K_ESCAPE:
                    if not grid.game_menu:
                        grid.game_menu = True
                        grid.rename_button("replay", "play")
                    elif grid.game_menu and grid.seconds_in_game > 0:
                        grid.game_menu = False

                if not grid.game_menu:
                    # --------------------------------------------------------------- #
                    #                            'Space'                              #
                    # --------------------------------------------------------------- #
                    if event.key == pygame.K_SPACE:

                        # GEN RADAR
                        my_body.gen_radar_track(grid)

                        # DEBUG PRINT
                        cir_utils.debug_print_space(grid, my_body)

                    if event.key == pygame.K_KP_ENTER:
                        editor_buttons = loader.load_editor()
                        for editor_button in editor_buttons:
                            effects.produce(editor_button.name)

                    elif event.key == pygame.K_1:
                        print ">>>> key 1"
                        grid.change_room(1)

                    elif event.key == pygame.K_2:
                        print ">>>> key 2"
                        grid.change_room(2)

                    elif event.key == pygame.K_3:
                        print ">>>> key 3"
                        grid.change_room(3)


                    # GENERATE MOVEMENT
                    elif not my_body.in_menu:
                        my_body.gen_direction(pygame, grid, event)

            # --------------------------------------------------------------- #
            #                          CLICK EVENTS                           #
            # --------------------------------------------------------------- #
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_tile:

                    # GAME MENU
                    if grid.game_menu:
                        for button in grid.buttons:
                            if current_tile == button.pos and button.clickable:
                                if button.name in ["play", "replay"]:
                                    grid.game_menu = False
                                    if grid.game_over:
                                        grid.game_over = False
                                elif button.name == "quit":
                                    pygame.quit()
                                    quit()
                    else:
                        # --------------------------------------------------------------- #
                        #                         MOUSE MODE CLICK                        #
                        # --------------------------------------------------------------- #
                        effects.mouse_mode_click(current_tile, my_body)

                        # --------------------------------------------------------------- #
                        #                          CLICK ON ITEMS                         #
                        # --------------------------------------------------------------- #
                        for item in grid.items:
                            if item.clickable:
                                if current_tile == item.pos:

                                    # SET MOUSE MODE
                                    if item.modable:
                                        grid.set_mouse_mode(item)

                                    # EDITOR CLICK
                                    effects.editor(item, my_body)

                                    # --------------------------------------------------------------- #
                                    #                    MOUSE MODE CLICK ON ITEM                     #
                                    # --------------------------------------------------------------- #
                                    effects.mouse_mode_click_item(item)

                                    # --------------------------------------------------------------- #
                                    #                           MENU OPTIONS                          #
                                    # --------------------------------------------------------------- #
                                    # SET IN MENU
                                    item.check_in_menu(grid, current_tile)
                                    # SET OPTS POS
                                    item.set_option_pos(grid)
                                    # OPT CLICKED
                                    if item.in_menu:
                                        grid.clean_mouse()

                                # --------------------------------------------------------------- #
                                #                       CLICK ITEM OPTIONS                        #
                                # --------------------------------------------------------------- #
                                elif current_tile in grid.adj_tiles(item.pos) and item.in_menu:
                                    if item.options:
                                        for option in item.options:
                                            if current_tile == option.pos:

                                                # SET MOUSE MODE
                                                if option.modable:
                                                    grid.set_mouse_mode(option)
                                                # --------------------------------------------------------------- #
                                                #                      OPTIONS / SUB-OPTIONS                      #
                                                # --------------------------------------------------------------- #
                                                effects.click_options(item, option, my_body)

                                # CLICKED OUTSIDE
                                elif (current_tile != item.pos) and (current_tile not in grid.adj_tiles(item.pos)):
                                    item.set_in_menu(grid, False)

                # DEBUG PRINT
                cir_utils.debug_print_click(grid, current_tile, my_body)

        # --------------------------------------------------------------- #
        #                             DRAWING                             #
        # --------------------------------------------------------------- #
        # GAME MENU
        if grid.game_menu:
            if grid.buttons:
                drawer.draw_menu_buttons(current_tile)
        else:
            # BACKGROUND
            drawer.draw_background_stuff()
            # ANIMATIONS
            drawer.draw_animations(my_body, current_tile)

        pygame.display.update()

        # --------------------------------------------------------------- #
        #                           CHANGE VARS                           #
        # --------------------------------------------------------------- #
        effects.change_vars(my_body)

        # FINISH LOOP
        grid.clock.tick(grid.fps)

    if grid.game_over:
        game_loop(grid.game_over, grid.scenario)

    pygame.quit()
    quit()

# --------------------------------------------------------------- #
#                              MAIN                               #
# --------------------------------------------------------------- #
if __name__ == '__main__':
    game_loop(game_over=False)
