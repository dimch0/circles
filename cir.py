#!/usr/bin/python

# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                       MAIN                                                          #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import pygame

# Internal imports
from circles.cir.cir_grid import Grid
from circles.cir.grid_game_menu import game_menu
from circles.cir.phase_0_load import DataLoader
pygame.init()


def game_loop(game_over, scenario="scenario_01", msg=list()):
    # --------------------------------------------------------------- #
    #                        PHASE 0: LOADING                         #
    # --------------------------------------------------------------- #
    grid = Grid(pygame, scenario)
    grid.loader = DataLoader(grid)
    my_body = grid.loader.load_game()
    grid.updater.my_body = my_body

    if game_over:
        grid.messages = msg
    else:
        grid.messages = ["SCREEN - start"]


    # --------------------------------------------------------------- #
    #                            GAME LOOP                            #
    # --------------------------------------------------------------- #
    while not grid.game_over:

        CURRENT_TILE = grid.mouse_in_tile(pygame.mouse.get_pos())
        grid.seconds_in_game_tick()
        game_menu(grid, my_body)

        # --------------------------------------------------------------- #
        #                          PHASE 1: EVENTS                        #
        # --------------------------------------------------------------- #
        for event in pygame.event.get():
            # QUIT
            if event.type == pygame.QUIT:
                grid.game_exit()
            # KEY EVENTS
            elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                grid.event_effects.execute_key_events(event, my_body)
            # CLICK EVENTS
            elif event.type == pygame.MOUSEBUTTONDOWN:
                grid.event_effects.execute_click_events(event, my_body, CURRENT_TILE)
        # --------------------------------------------------------------- #
        #                          PHASE 2: DRAWING                       #
        # --------------------------------------------------------------- #
        grid.drawer.draw(CURRENT_TILE)
        # --------------------------------------------------------------- #
        #                          PHASE 3: CHANGE VARS                   #
        # --------------------------------------------------------------- #
        grid.updater.update_vars(my_body)

    # GAME OVER
    if grid.game_over:
        for report in grid.reporting:
            if hasattr(grid, report):
                grid.msg("SCREEN - %s: %s" %
                         (report.replace('_', ' '), getattr(grid, report)))
        game_loop(grid.game_over, grid.scenario, grid.messages)

    # GAME EXIT
    grid.game_exit()
# --------------------------------------------------------------- #
#                              MAIN                               #
# --------------------------------------------------------------- #
if __name__ == '__main__':
    game_loop(game_over=False)
