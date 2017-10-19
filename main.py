# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                       MAIN                                                          #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------- #
#                             BUG FIXES                           #
# --------------------------------------------------------------- #
# TODO: Fix movement to occupado / mitosis
# TODO: Avoid recursive calling of loop
# TODO: Fix unicode characters
# --------------------------------------------------------------- #
#                             FEATURES                            #
# --------------------------------------------------------------- #
# TODO: Create save button
# TODO: Create load button
# TODO: Create map
# TODO: Feed with shrimp
# TODO: Display last msg on game over
# --------------------------------------------------------------- #
#                             BACKLOG                             #
# --------------------------------------------------------------- #
# TODO: Create trade mode
# TODO: Create craft mode
# TODO: Create item generation
# TODO: Create inside body view room 400
# TODO: Create spirit mode NEW SCENARIO
# TODO: Log statistics during a lifespan, calculate karma
# TODO: Create installation .exe file
# --------------------------------------------------------------- #
#                             COSMETICS                           #
# --------------------------------------------------------------- #
# TODO: Indicate uses / metrics
# TODO: Animate demo
# TODO: Add sounds


import pygame
from cir.cir_game_menu import game_menu
from cir.cir_grid import Grid
from cir.cir_phase_0_load import DataLoader
pygame.init()


# unistr = u"♛   ↑"
# pygame.font.init()
# srf = pygame.display.set_mode((500,500))
# f = pygame.font.Font("/home/dimcho/PycharmProjects/dzhrt/CIR/cosmetics/fonts/HelveticaNeueMed.ttf",64)
# srf.blit(f.render(unistr,True,(255,0,0)),(0,0))
# pygame.display.flip()
# from time import sleep
# sleep(3)


def game_loop(game_over, scenario="scenario_1"):
    # --------------------------------------------------------------- #
    #                        PHASE 0: LOADING                         #
    # --------------------------------------------------------------- #
    grid               = Grid(pygame, scenario)
    grid.loader        = DataLoader(grid)
    my_body            = grid.loader.load_game()

    if game_over:
        grid.rename_button("play", "replay")

    # TESTING

    # --------------------------------------------------------------- #
    #                            GAME LOOP                            #
    # --------------------------------------------------------------- #
    grid.msg("SCREEN - game started")

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
            elif event.type == pygame.KEYDOWN:
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
        game_loop(grid.game_over, grid.scenario)

    # GAME EXIT
    grid.game_exit()
# --------------------------------------------------------------- #
#                              MAIN                               #
# --------------------------------------------------------------- #
if __name__ == '__main__':
    game_loop(game_over=False)
