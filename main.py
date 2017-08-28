# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                       MAIN                                                          #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------- #
#                            BUG FIXES                            #
# --------------------------------------------------------------- #

# TODO: Fix occupado
# TODO: Make trigger dissapear
# TODO: Fix signal
# TODO: Fix signal hit on intersecting
# TODO: Fix mitosis

# TODO: Move effect to items and allocate to other classes
# TODO: Remove bag and bodies from map
# TODO: Fix collect item

# TODO: Create drop mode
# TODO: Create trade mode
# TODO: Create craft mode

# TODO: Refactor default values allocation
# TODO: Refactor for iterations
# TODO: Create editor class
# --------------------------------------------------------------- #
#                            FEATURES                             #
# --------------------------------------------------------------- #
# TODO: Parametrize scenario files
# TODO: Item generation
# TODO: Create save button
# TODO: Create load button
# TODO: Create inside body view room 400
# TODO: Create spirit mode NEW SCENARIO
# TODO: Log statistics during a lifespan, calculate karma
# TODO: Create installation .exe file
# --------------------------------------------------------------- #
#                            COSMETICS                            #
# --------------------------------------------------------------- #
# TODO: Fix rotation on direction
# TODO: Indicate uses / metrics
# TODO: Animate item activation
# TODO: Animate demo
# TODO: Add sounds
# TODO: Log messages on screen
# TODO: Fixed constant hit bug - line 113 cir_item

import time
import pygame
from cir.cir_game_menu import game_menu
from cir.cir_cosmetic import Images, Fonts
from cir.cir_grid import Grid
from cir.cir_phase_0_load import DataLoader
from cir.cir_phase_1_events import GameEffects
from cir.cir_phase_2_draw import GameDrawer
from cir.cir_phase_3_update import VarChanger
pygame.init()


def game_loop(game_over, scenario="scenario_1"):
    # --------------------------------------------------------------- #
    #                        PHASE 0: LOADING                         #
    # --------------------------------------------------------------- #
    grid               = Grid(pygame, scenario)
    grid.images        = Images(grid)
    grid.fonts         = Fonts(grid)
    grid.loader        = DataLoader(grid)
    grid.event_effects = GameEffects(grid)
    grid.drawer        = GameDrawer(grid)
    grid.var_changer   = VarChanger(grid)
    grid.start_time    = time.time()
    my_body            = grid.loader.load_items()

    grid.clean_tmp_maps()

    if not my_body in grid.items:
        grid.items.append(my_body)

    if game_over:
        grid.rename_button("play", "replay")
    if scenario == "scenario_2":
        grid.game_menu = False
    elif scenario == "scenario_3":
        grid.fog_color = grid.dark_grey
        grid.room_color = grid.black

    # --------------------------------------------------------------- #
    #                            GAME LOOP                            #
    # --------------------------------------------------------------- #
    print("INFO: Game started")

    while not grid.game_over:
        # CURRENT TILE
        current_tile = grid.mouse_in_tile(pygame.mouse.get_pos())
        # SECONDS
        grid.seconds_in_game_tick()
        # GAME MENU
        game_menu(grid)
        # --------------------------------------------------------------- #
        #                          PHASE 1: EVENTS                        #
        # --------------------------------------------------------------- #
        for event in pygame.event.get():
            # QUIT
            if event.type == pygame.QUIT:
                grid.game_exit()
            # KEY EVENTS
            elif event.type == pygame.KEYDOWN:
                grid.event_effects.execute_key_events(event, my_body)
            # CLICK EVENTS
            elif event.type == pygame.MOUSEBUTTONDOWN:
                grid.event_effects.execute_click_events(event, my_body, current_tile)
        # --------------------------------------------------------------- #
        #                          PHASE 2: DRAWING                       #
        # --------------------------------------------------------------- #
        grid.drawer.draw(current_tile)
        # --------------------------------------------------------------- #
        #                          PHASE 3: CHANGE VARS                   #
        # --------------------------------------------------------------- #
        grid.var_changer.change_vars(my_body)

    # GAME OVER
    if grid.game_over:
        game_loop(grid.game_over, grid.scenario)

    # GAME EXIT
    grid.game_exit()
# --------------------------------------------------------------- #
#                              MAIN                               #
# --------------------------------------------------------------- #
if __name__ == '__main__':
    game_loop(game_over=False)
