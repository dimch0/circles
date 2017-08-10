# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                                                                                     #
#                                                       MAIN                                                          #
#                                                                                                                     #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------- #
#                            FEATURES                             #
# --------------------------------------------------------------- #
# TODO: Create map tile positions / calculate seconds
# TODO: Create inside body view room 400
# TODO: Create spirit mode NEW SCENARIO
# TODO: Log statistics during a lifespan, calculate karma
# TODO: Create save button
# TODO: Create load button
# TODO: Create installation .exe file
# TODO: Item generation
# --------------------------------------------------------------- #
#                            ANIMATION                            #
# --------------------------------------------------------------- #
# TODO: Indicate uses / meters
# TODO: Animate item activation
# TODO: Animate demo
# TODO: Add sounds
# TODO: Log messages on screen
# --------------------------------------------------------------- #
#                            BUG FIXES                            #
# --------------------------------------------------------------- #
# TODO: Use IMG / SOUND lib
# TODO: Fix mitosis (lag, overlap)
# TODO: Improve item options
# TODO: Fix item collection / remove everything dict
# TODO: Fix room change
# TODO: Fix signal hit on intersecting
# TODO: Fix signal lag
# --------------------------------------------------------------- #
#                            IMPORTS                              #
# --------------------------------------------------------------- #
import time
import pygame
pygame.init()
from cir.cir_game_menu import game_menu
from cir import cir_utils
from cir .cir_cosmetic import Images, Fonts
from cir.cir_grid import Grid
from cir.cir_draw import GameDrawer
from cir.cir_loader import DataLoader
from cir.cir_event_effects import GameEffects
from cir.cir_change_vars import VarChanger


def game_loop(game_over, scenario="Scenario_1"):
    # --------------------------------------------------------------- #
    #                            LOADING                              #
    # --------------------------------------------------------------- #
    grid               = Grid(pygame, scenario)
    grid.images        = Images(grid)
    grid.fonts         = Fonts(grid)
    grid.drawer        = GameDrawer(grid)
    grid.loader        = DataLoader(grid)
    grid.var_changer   = VarChanger(grid)
    grid.event_effects = GameEffects(grid)
    grid.start_time    = time.time()
    my_body            = grid.loader.load_items()

    if game_over:
        grid.rename_button("play", "replay")
    if scenario == "Scenario_2":
        grid.game_menu = False

    # --------------------------------------------------------------- #
    #                        TEST TESTING PLACE                       #
    # --------------------------------------------------------------- #


    # --------------------------------------------------------------- #
    #                            GAME LOOP                            #
    # --------------------------------------------------------------- #
    print "Game started"
    while not grid.game_over:

        current_tile = grid.mouse_in_tile(pygame.mouse.get_pos())
        grid.seconds_in_game_tick()

        # --------------------------------------------------------------- #
        #                            GAME MENU                            #
        # --------------------------------------------------------------- #
        game_menu(grid, pygame)

        # --------------------------------------------------------------- #
        #                                                                 #
        #                            EVENTS                               #
        #                                                                 #
        # --------------------------------------------------------------- #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                # --------------------------------------------------------------- #
                #                             ESCAPE                              #
                # --------------------------------------------------------------- #
                if event.key == pygame.K_ESCAPE:
                    if not grid.game_menu:
                        grid.rename_button("replay", "play")
                        grid.game_menu = True

                # --------------------------------------------------------------- #
                #                             SPACE                               #
                # --------------------------------------------------------------- #
                if event.key == pygame.K_SPACE:

                    # GEN RADAR
                    my_body.gen_radar_track(grid)

                    # DEBUG PRINT
                    cir_utils.debug_print_space(grid, my_body)

                elif event.key == pygame.K_KP_ENTER:
                    editor_buttons = grid.loader.load_editor()
                    for editor_button in editor_buttons:
                        grid.event_effects.produce(editor_button.name)

                elif event.key == pygame.K_1:
                    print ">>>> key 1"
                    grid.change_room("12_12")
                elif event.key == pygame.K_2:
                    print ">>>> key 2"
                    grid.change_room("12_10")
                elif event.key == pygame.K_3:
                    print ">>>> key 3"
                    grid.change_room("12_14")

                # --------------------------------------------------------------- #
                #                             OTHER                               #
                # --------------------------------------------------------------- #
                elif not my_body.in_menu:
                    my_body.gen_direction(pygame, grid, event)

            # --------------------------------------------------------------- #
            #                          CLICK EVENTS                           #
            # --------------------------------------------------------------- #
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_tile:

                    # --------------------------------------------------------------- #
                    #                         MOUSE MODE CLICK                        #
                    # --------------------------------------------------------------- #
                    grid.event_effects.mouse_mode_click(current_tile, my_body)

                    # --------------------------------------------------------------- #
                    #                          CLICK ON ITEMS                         #
                    # --------------------------------------------------------------- #
                    for item in grid.items:
                        if item.clickable:

                            # --------------------------------------------------------------- #
                            #                          CLICK ON ITEM                          #
                            # --------------------------------------------------------------- #
                            if current_tile == item.pos:

                                # SET MOUSE MODE
                                if item.modable:
                                    grid.set_mouse_mode(item)

                                # CLICK ON ITEMS
                                grid.event_effects.click_items(item, my_body)

                                # SET IN MENU OPTIONS
                                item.check_in_menu(grid, current_tile)

                                # SET OPTS POS
                                item.set_option_pos(grid)

                                # OPT CLICKED
                                if item.in_menu:
                                    grid.clean_mouse()

                            # --------------------------------------------------------------- #
                            #                       CLICK ON ITEM OPTIONS                     #
                            # --------------------------------------------------------------- #
                            elif current_tile in grid.adj_tiles(item.pos) and item.in_menu:
                                if item.options:
                                    for option in item.options:
                                        if current_tile == option.pos:

                                            # SET MOUSE MODE
                                            if option.modable:
                                                grid.set_mouse_mode(option)

                                            # OPTIONS SUB-OPTIONS
                                            grid.event_effects.click_options(item, option, my_body)

                            # --------------------------------------------------------------- #
                            #                          CLICKED OUTSIDE                        #
                            # --------------------------------------------------------------- #
                            else:
                                item.set_in_menu(grid, False)

                # DEBUG PRINT
                cir_utils.debug_print_click(grid, current_tile, my_body)

        # --------------------------------------------------------------- #
        #                         PHASE: DRAWING                          #
        # --------------------------------------------------------------- #
        grid.drawer.draw(current_tile)

        # --------------------------------------------------------------- #
        #                         PHASE: CHANGE VARS                      #
        # --------------------------------------------------------------- #
        grid.var_changer.change_vars(my_body)

    if grid.game_over:
        game_loop(grid.game_over, grid.scenario)

    pygame.quit()
    quit()

# --------------------------------------------------------------- #
#                              MAIN                               #
# --------------------------------------------------------------- #
if __name__ == '__main__':
    game_loop(game_over=False)
