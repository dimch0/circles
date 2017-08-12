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
# TODO: Fix mitosis lag
# TODO: Fix signal lag
# TODO: Fix item options
# TODO: Fix item collection / remove everything dict
# TODO: Fix room change
# TODO: Fix signal hit on intersecting
# TODO: Set rotation on direction

# TODO: Fix constant hit bug - line 113 cir_item

import time
import pygame
from cir.cir_game_menu import game_menu
from cir .cir_cosmetic import Images, Fonts
from cir.cir_grid import Grid
from cir.cir_phase_0_load import DataLoader
from cir.cir_phase_1_event_effects import GameEffects
from cir.cir_phase_1a_key_events import execute_key_events
from cir.cir_phase_1b_click_events import execute_click_events
from cir.cir_phase_2_draw import GameDrawer
from cir.cir_phase_3_change_vars import VarChanger
pygame.init()

def game_loop(game_over, scenario="Scenario_1"):
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

    if game_over:
        grid.rename_button("play", "replay")
    if scenario == "Scenario_2":
        grid.game_menu = False

    # --------------------------------------------------------------- #
    #                            GAME LOOP                            #
    # --------------------------------------------------------------- #
    print("Game started")

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
                execute_key_events(grid, event, my_body)
            # CLICK EVENTS
            elif event.type == pygame.MOUSEBUTTONDOWN:
                execute_click_events(grid, event, my_body, current_tile)
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
