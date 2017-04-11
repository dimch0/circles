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

from krg import krg_grid, krg_utils, krg_body
pygame.init()

# COLORS
# TODO: move colors in a config file
white = (255, 255, 255)
black = (0, 0, 0)
ungrey = (195, 195, 195)
grey = (175, 165, 175)
pink = (252, 217, 229)
green = (210, 255, 191)

# DEFAULT SCALE IS 1, INCREASE THE NUMBER FOR A SMALLER SIZE
# TODO: move flags in a config file
SCALE = 4
FPS = 30
SHOW_GRID = 0

# SETTINGS
# TODO: move settings in a config file
circle_radius = 30 / SCALE
katet = int(sqrt(((2 * circle_radius) ** 2) - (circle_radius ** 2)))
display_width = (katet * 10) + (circle_radius * 2)
display_height = 24 * circle_radius

# GAME SETTINGS
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('krg')
clock = pygame.time.Clock()

# INITIALIZING GRID AND PLAYER
grid = krg_grid.Grid(circle_radius)
grid.grid_gen()
my_body = krg_body.BodyItem()
grid.items.append(my_body)


def game_loop():
    """
    The main game loop.
    """
    pygame.mouse.set_visible(1)
    game_exit = False

    # Starting position of body
    my_body.pos = grid.starting_pos(display_width, display_height)


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
                        my_body.gen_radar_track(grid, SCALE)
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
        gameDisplay.fill(grey)
        # Revealed radius
        for revealed in grid.revealed_radius:
            pygame.draw.circle(gameDisplay, ungrey, revealed[0], revealed[1], 0)
        # Grid
        if SHOW_GRID:
            for tile in grid.tiles:
                pygame.draw.circle(gameDisplay, white, tile, grid.tile_radius, 1)
        # -------------------------------------- BACKGROUND -------------------------------------- #


        # -------------------------------------- ANIMATIONS -------------------------------------- #
        # Radar
        if my_body.radar_track:
            radar_radius, thick = my_body.radar(grid)
            if radar_radius and thick:
                pygame.draw.circle(gameDisplay, green, my_body.pos, radar_radius, thick)

        # Movement
        if my_body.move_track:
            my_body.move()

        # Items and Body
        # TODO: blit for item.color
        for item in grid.items:
            pygame.draw.circle(gameDisplay, pink, item.pos, grid.tile_radius, 0)

        # Mouse image
        for tile in grid.tiles:
            if krg_utils.in_circle(tile, grid.tile_radius, mouse_pos):
                pygame.draw.circle(gameDisplay, white, tile, grid.tile_radius, 1)
        # -------------------------------------- ANIMATIONS -------------------------------------- #


        pygame.display.update()
        # TODO: check changes for placement
        clock.tick(FPS)
    pygame.quit()
    quit()

if __name__ == '__main__':
    game_loop()
