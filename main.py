"""
================================== Main file ==================================
"""


import pygame
import time
import random
from pygame.locals import *

from krg import krg_body, krg_grid, krg_utils
pygame.init()


# COLORS
white = (255, 255, 255)
black = (0, 0, 0)
grey = (195, 195, 195)
pink = (252, 217, 229)
green = (210, 255, 191)

# DEFAULT SCALE IS 1, INCREASE THE NUMBER FOR A SMALLER SIZE
SCALE = 1
FPS = 30
SPEED = 5
SHOW_GRID = False

print "INFO Loading..."
circle_radius = 30 / SCALE
display_width = 600 / SCALE
display_height = 600 / SCALE
mid_x = int(display_width/2)
mid_y = int(display_height/2)
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('krg')
clock = pygame.time.Clock()

player = krg_body.Body()
grid = krg_grid.Grid(circle_radius)
grid.tiles = grid.grid_gen(circle_radius)
print "Player born."
print "Grid created."
print "Grid tiles:", grid.tiles.keys()
print "Number of tiles:", len(grid.tiles.keys())

def game_loop():
    """
    main game loop
    """
    print "INFO Game started"
    pygame.mouse.set_visible(1)
    game_exit = False
    player.pos = (mid_x, mid_y)
    menu = False
    radar = 0

    while not game_exit:
        # MOUSE POSITION X AND Y
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            # print event
            if event.type == pygame.QUIT:
                game_exit = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                print "-" * 30
                print "click:", mouse_pos
                print "circle:", krg_grid.Grid.mouse_in_tile(circle_radius, mouse_pos)
                clicked_circle = krg_grid.Grid.mouse_in_tile(circle_radius, mouse_pos)
                if clicked_circle:
                    # MOVEMENT populating tracks
                    track = player.tracks(clicked_circle)
                    print "track:", track
                if krg_utils.in_circle(player.pos, circle_radius, mouse_pos) and not menu:
                    menu = True
                else:
                    menu = False

        # MOVEMENT only moves if tracks are populated
        player.move()

        # BACKGROUND
        gameDisplay.fill(grey)

        # TODO blit stuff here

        if SHOW_GRID:
            for tile in grid.tiles.values():
                pygame.draw.circle(gameDisplay, white, tile, circle_radius, 1)

        # MENU
        if menu:
            # pygame.draw.circle(gameDisplay, green, player.pos, circle_radius * 3, 0)
            limit = circle_radius * 2
            thikness = range(1,11)
            thikness.reverse()
            if radar < limit:
                for thik in thikness:
                    if radar < limit / thik:
                        pygame.draw.circle(gameDisplay, green, player.pos, circle_radius + radar, thik)
                radar += 1
            else:
                radar = 0

        # BODY
        pygame.draw.circle(gameDisplay, pink, player.pos, circle_radius, 0)

        # MOUSE IMG
        for tile in grid.tiles.values():
            if krg_utils.in_circle(tile, circle_radius, mouse_pos):
                pygame.draw.circle(gameDisplay, white, tile, circle_radius, 1)

        # UPDATE DISPLAY
        pygame.display.update()

        # TODO: if change vars to blit

        clock.tick(FPS)
    pygame.quit()
    quit()


if __name__ == '__main__':
    game_loop()
