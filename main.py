"""
================================== Main file ==================================
"""

import pdb
import pygame
import time
import random
from pygame.locals import *

from krg import krg_body, krg_grid, krg_utils
pygame.init()


# COLORS
white = (255, 255, 255)
black = (0, 0, 0)
ungrey = (195, 195, 195)
grey = (175, 165, 175)
pink = (252, 217, 229)
green = (210, 255, 191)

# DEFAULT SCALE IS 1, INCREASE THE NUMBER FOR A SMALLER SIZE
SCALE = 4
FPS = 30
SHOW_GRID = 0

# SETTINGS
circle_radius = 30 / SCALE
display_width = 600 / SCALE
display_height = 600 / SCALE
mid_x = int(display_width/2) - int (10 / SCALE)
mid_y = int(display_height/2) - int (10 / SCALE)
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('krg')
clock = pygame.time.Clock()


grid = krg_grid.Grid(circle_radius)
grid.tiles = grid.grid_gen(grid.tile_radius)
player = krg_body.Body()
grid.items.append(player)



print "INFO Player born."
print "INFO Grid created."
print "INFO Grid tiles:", grid.tiles.keys()
print "INFO Number of tiles:", len(grid.tiles.keys())


def game_loop():
    """
    main game loop
    """
    print "INFO Game started"
    pygame.mouse.set_visible(1)
    game_exit = False
    for tile in grid.tiles.values():
        if krg_utils.in_circle(tile, grid.tile_radius, (mid_y, mid_y)):
            player.pos = tile

    # TODO: make action on SPACEBAR
    action = False
    # radar = 0

    while not game_exit:
        # MOUSE POSITION X AND Y
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            # print event
            if event.type == pygame.QUIT:
                game_exit = True

            # CLICK EVENTS
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_circle = krg_grid.Grid.mouse_in_tile(grid.tile_radius, mouse_pos)
                print ">>>> click:", mouse_pos, "circle:", clicked_circle

                player.radar_limit = 0

                if clicked_circle:

                    # TODO: CHECK MODE
                    # TODO: CHECK TILE
                    # TODO: CHECK ITEM

                    # ITEM MENU OPTIONS
                    # for item in grid.items:
                    #     item.menu(clicked_circle, grid)

                    # TODO: CHECK WHICH OPTION IS SELECTED
                    # TODO: EXECUTED OPTION

                    # MOVEMENT TRACKS POPULATING
                    player.tracks(clicked_circle)
                    # print "track:", track

                if krg_utils.in_circle(player.pos, grid.tile_radius, mouse_pos) and not action:
                    action = True
                else:
                    action = False



        # PLACE BACKGROUND
        gameDisplay.fill(grey)
        # PLACE REVEALED CIRCLES
        for rgrid in grid.revealed_radius:
            pygame.draw.circle(gameDisplay, ungrey, rgrid[0], rgrid[1], 0)
        # PLACE GRID
        if SHOW_GRID:
            for tile in grid.tiles.values():
                pygame.draw.circle(gameDisplay, white, tile, grid.tile_radius, 1)
        # PLACE ANIMATION
        # PLACE RADAR
        # if action:
        if 0:
            radar_radius, thik = player.radar(grid)
            if radar_radius and thik:
                pygame.draw.circle(gameDisplay, green, player.pos, grid.tile_radius + player.radar_waves, thik)
        # MOVEMENT
        if player.move_track:
            player.move()
        # PLACE ITEMS (AND BODY)
        for item in grid.items:
            pygame.draw.circle(gameDisplay, pink, item.pos, grid.tile_radius, 0)
        # PLACE MOUSE IMG
        for tile in grid.tiles.values():
            if krg_utils.in_circle(tile, grid.tile_radius, mouse_pos):
                pygame.draw.circle(gameDisplay, white, tile, grid.tile_radius, 1)

        # UPDATE DISPLAY
        pygame.display.update()
        # TODO: check changed vars to blit stuff
        clock.tick(FPS)
    pygame.quit()
    quit()

if __name__ == '__main__':
    game_loop()
