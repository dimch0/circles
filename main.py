#######################################################################################################################
#################                                                                                     #################
#################                                 Main file                                           #################
#################                                                                                     #################
#######################################################################################################################

import pdb
from math import sqrt
import pygame
import time
import random
from pygame.locals import *
# TODO: Check all files for obsolete imports

from cir import cir_grid, cir_utils, cir_body
pygame.init()


# CREATING GRID, PLAYER, ITEMS
grid = cir_grid.Grid()
my_body = cir_body.BodyItem()
my_body.pos = grid.middle_tile
grid.items.append(my_body)

# GAME SETTINGS
gameDisplay = pygame.display.set_mode((grid.display_width, grid.display_height))
pygame.display.set_caption(grid.caption)
clock = pygame.time.Clock()
pygame.mouse.set_visible(1)


def game_loop():
    """
    The main game loop.
    """
    game_exit = False


    while not game_exit:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

            # TODO: K_ESCAPE screen
            # -------------------------------------- SPACEBAR EVENTS -------------------------------------- #
            # Radar track populating
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print ">>>> space"
                    if "radar" in grid.mode:
                        my_body.gen_radar_track(grid)
            # -------------------------------------- SPACEBAR EVENTS -------------------------------------- #


            # -------------------------------------- CLICK EVENTS ----------------------------------------- #
            if event.type == pygame.MOUSEBUTTONDOWN:

                clicked_circle = grid.mouse_in_tile(mouse_pos)
                if clicked_circle:

                    # Movement track populating
                    if "move" in grid.mode and not my_body.in_menu:
                        my_body.gen_move_track(clicked_circle, grid)

                    # Radar track populating
                    if "radar" in grid.mode:
                        pass

                    # Setting the mode
                    for item in grid.items:
                        if clicked_circle == item.pos:
                            if not item.name in grid.mode:
                                grid.mode.append(item.name)

                    # Check for item menu
                    for item in grid.items:
                        item.open_menu(clicked_circle, grid)

                print("grid items: {0}".format([item.name for item in grid.items]))
                # print("revealed tiles: {0}".format(grid.revealed_tiles))
                print(">>>> click: {0}, circle: {1}, mode: {2}".format(mouse_pos, clicked_circle, grid.mode))
            # ------------------------------------- CLICK EVENTS ----------------------------------------- #

        # -------------------------------------- BACKGROUND -------------------------------------- #
        # Background
        gameDisplay.fill(grid.grey)
        # Revealed radius
        for revealed in grid.revealed_radius:
            pygame.draw.circle(gameDisplay, grid.ungrey, revealed[0], revealed[1], 0)
        # Grid
        if grid.show_grid:
            for tile in grid.tiles:
                pygame.draw.circle(gameDisplay, grid.white, tile, grid.tile_radius, 1)
        # -------------------------------------- BACKGROUND -------------------------------------- #


        # -------------------------------------- ANIMATIONS -------------------------------------- #
        # Radar
        if my_body.radar_track:
            radar_radius, thick = my_body.radar(grid)
            if radar_radius and thick:
                pygame.draw.circle(gameDisplay, grid.green, my_body.pos, radar_radius, thick)

        # Movement
        if my_body.move_track:
            my_body.move()

        # Items and Body
        # TODO: blit for item.color and image
        for item in grid.items:
            pygame.draw.circle(gameDisplay, grid.pink, item.pos, grid.tile_radius, 0)

        # Mouse image
        for tile in grid.tiles:
            if cir_utils.in_circle(tile, grid.tile_radius, mouse_pos):
                pygame.draw.circle(gameDisplay, grid.white, tile, grid.tile_radius, 1)
        # -------------------------------------- ANIMATIONS -------------------------------------- #


        pygame.display.update()
        # TODO: check changes for placement
        clock.tick(grid.fps)
    pygame.quit()
    quit()

if __name__ == '__main__':
    game_loop()
